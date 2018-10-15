import datetime
import time
from django.db import transaction
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from authentication.models import User
from authentication.serializers import UserSerializer
from common.ComputeNewCorn import NewCornCompute
from invitation.models import Invitation, UserRecord, Cp
from invitation.serializer import InvitationSerializer, UserRecordSerializer
import logging
from common.execute_sql import execute_custom_sql
from redis_tool.redis_server import redis_client
from register.models import RegisterInfo
from register.serializer import RegisterInfoSerializer
from common.NewCornType import NewCornType
from utils.weixin_functions import WxInterfaceUtil

logger = logging.getLogger('django')


class InvitationView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer

    def list(self, request, *args, **kwargs):
        inviter = self.request.query_params.get('inviter')
        invitee = self.request.query_params.get('invitee')
        if inviter:
            sql = """SELECT invitation.*, register_info.nickname,register_info.avatar_url,register_info.sex FROM 
invitation LEFT JOIN register_info  ON invitation.invitee = register_info.user_id WHERE invitation.inviter = '%s'""" % inviter
        if invitee:
            sql = """SELECT invitation.*, register_info.nickname,register_info.avatar_url,register_info.sex FROM 
            invitation LEFT JOIN register_info ON invitation.inviter = register_info.user_id WHERE invitation.invitee = '%s'""" % invitee
        datas = execute_custom_sql(sql)
        logger.info(datas)
        result = self._wrapper_data(datas)
        return Response(result)

    def _wrapper_data(self, datas):
        data_list = []
        for data in datas:
            temp = dict()
            temp['id'] = data[0]
            temp['inviter'] = data[1]
            temp['invitee'] = data[2]
            temp['status'] = data[3]
            temp['create_time'] = data[4]
            temp['update_at'] = data[5]
            temp['expire_at'] = data[6]
            temp['nickname'] = data[7]
            temp['avatar_url'] = data[8]
            temp['sex'] = data[9]
            data_list.append(temp)
        return data_list

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        params = request.data
        user = request.user_info
        if not params.get('invitee'):
            raise serializers.ValidationError('参数 invitee 不能为空')
        if user.get('cp_user_id'):
            raise serializers.ValidationError('您已成功匹配CP，无法继续邀请')
        request.data['create_time'] = datetime.datetime.now()
        request.data['expire_at'] = request.data['create_time'] + datetime.timedelta(days=1)
        super().create(request, *args, **kwargs)
        # 发送邀请之后要修改用户记录表中数据
        UserRecord.objects.filter(user_id=user.get('open_id'), view_user_id=params.get('invitee')).update(
            invite_status=0, invite_expire_at=request.data['expire_at'], invite_at=request.data['create_time'])
        NewCornCompute.compute_new_corn(user.get('open_id'), NewCornType.INVITE_USERS.value)
        access_token = WxInterfaceUtil.get_access_token()
        WxInterfaceUtil.send_customer_message(params.get('invitee'), 'helloworld', access_token)
        return Response()

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        inviter = request.data.get('inviter')
        user = request.user_info
        status = request.data.get('status')
        if not status or status not in (0, 1, 2):
            logger.info('InvitationView update (status=%s)' % status)
            raise serializers.ValidationError('参数 status 有误')
        # 查看邀请人是否已经匹配成功
        inviter_info = User.objects.filter(open_id=inviter)
        if inviter_info and inviter_info[0].cp_user_id:
            raise serializers.ValidationError('很遗憾，邀请您的用户已成功匹配到CP')
        invitation = Invitation.objects.get(id=pk)
        invitation.status = status
        invitation.save()
        if status == 1:
            # 接收邀请，CP匹配成功
            NewCornCompute.compute_new_corn(user.get('open_id'), NewCornType.ACCEPT_INVITATION.value)
            # 同时更新User，将当前用户与inviter的cp_user_id进行更新
            now = datetime.datetime.now()
            current_user = User.objects.get(open_id=user.get('open_id'))
            current_user.cp_user_id = inviter
            current_user.cp_time = now
            current_user.save()
            current_user_cp = User.objects.get(open_id=inviter)
            current_user_cp.cp_user_id = user.get('open_id')
            current_user_cp.cp_time = now
            current_user_cp.save()
            # 同时更新缓存中用户信息
            redis_client.set_instance(current_user.open_id, UserSerializer(current_user).data)
            redis_client.set_instance(current_user_cp.open_id, UserSerializer(current_user_cp).data)
            # 更新用户记录表信息
            UserRecord.objects.filter(user_id=inviter, view_user_id=user.get('open_id')).update(invite_status=1)
            UserRecord.objects.filter(user_id=user.get('open_id'), view_user_id=inviter).update(invite_status=1)
        return Response()

    @list_route(methods=['get'])
    def cp(self, request):
        user = request.user_info
        if not user.get('cp_user_id'):
            raise serializers.ValidationError('当前用户暂无CP信息')
        data = RegisterInfo.objects.filter(user_id=user.get('cp_user_id'))
        if not data:
            raise serializers.ValidationError('该用户CP无注册信息，请检查数据库')
        data = data.first()
        temp = RegisterInfoSerializer(data).data
        temp['update_at'] = user.get('cp_time')
        temp['age'] = datetime.datetime.now().year - data.birthday.year
        if temp['picture_url'] and str(temp['picture_url']).find('https') == -1:
            temp['picture_url'] = 'https://cp1.lxhelper.com/media' + temp['picture_url']
        return Response(temp)

    @list_route(methods=['get'])
    def check_inviter(self, request):
        user = request.user_info
        data = Invitation.objects.filter(inviter=user.get('open_id'), status=1)
        return Response(True if data else False)

    @list_route(methods=['get'])
    def check_invitee(self, request):
        user = request.user_info
        data = Invitation.objects.filter(invitee=user.get('open_id'), status=0, expire_at__gt=datetime.datetime.now())
        return Response(True if data else False)

    @list_route(methods=['get'])
    def cp_god(self, request):
        user = request.user_info
        result = list()
        pageNum = request.query_params.get('pageNum', 1)
        pageSize = request.query_params.get('pageSize', 10)
        start = pageSize * (pageNum - 1)
        end = pageSize * pageNum
        sql1 = """SELECT invitee,COUNT(*) as number from invitation where invitee != '%s' GROUP BY invitee ORDER BY number desc
                limit %s, %s""" % (user.get('open_id'), 0, 10)
        datas_one = execute_custom_sql(sql1)
        id_list = list()
        temp_dict = dict()
        for data in datas_one:
            id_list.append(data[0])
            temp_dict[data[0]] = data[1]
        datas_two = Cp.objects.exclude(invitee=user.get('open_id'))
        for data in datas_two:
            id_list.append(data.invitee)
            temp_dict[data.invitee] = data.count
        register_info = RegisterInfo.objects.filter(user_id__in=id_list)
        for temp in register_info:
            data_temp = dict()
            data_temp['avatar_url'] = temp.avatar_url
            data_temp['nickname'] = temp.nickname
            data_temp['sex'] = temp.sex
            data_temp['total'] = temp_dict.get(temp.user_id)
            data_temp['user_id'] = temp.user_id
            result.append(data_temp)
        # 当前用户可能向CP发送过邀请（过期），故需要判断处理
        temp = Invitation.objects.filter(inviter=user.get('open_id'), invitee__in=id_list).values_list(
            'invitee', 'status', 'expire_at')
        temp_dict = dict()
        for basic in temp:
            basic_list = list(basic)
            if basic_list[2] < datetime.datetime.now():
                temp_dict[basic_list[0]] = 2
            else:
                temp_dict[basic_list[0]] = basic_list[1]
        for data in result:
            data['status'] = temp_dict.get(data['user_id'], -1)
        for i in range(len(result) - 1):
            index = i
            for j in range(i + 1, len(result)):
                if result[index].get('total') < result[j].get('total'):
                    index = j
            result[i], result[index] = result[index], result[i]
        return Response(result)

    @list_route(methods=['get'])
    def code(self, request):
        logger.info('*' * 70)
        params = request.query_params
        logger.info(params)
        logger.info('*' * 70)
        # 获取邀请码
        code = params.get('code')
        # 获取邀请类型
        type = int(params.get('type', 0))
        other_open_id = params.get('other_open_id')
        nickname = params.get('nickname')
        if not code:
            raise serializers.ValidationError('参数 code 不能为空')
        if not other_open_id:
            raise serializers.ValidationError('参数 other_open_id 不能为空')
        if not nickname:
            raise serializers.ValidationError('参数 nickname 不能为空')
        inviter = User.objects.filter(code=code)
        if not inviter:
            raise serializers.ValidationError('邀请码无结果哦，快检查是不是输错啦。小哥哥小姐姐还在等待这枚New币解锁呢！回复「CP」，一起参与该活动，解锁你的小哥哥和小姐姐吧。')
        NewCornCompute.compute_new_corn(inviter[0].open_id, type, other_open_id, nickname)
        return Response()


class UserRecordView(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = UserRecord.objects.all()
    serializer_class = UserRecordSerializer

    # filter_fields = ['user_id']

    @list_route(methods=['get'])
    def view_record(self, request):
        user = request.user_info
        pageNum = request.query_params.get('pageNum', 1)
        pageSize = request.query_params.get('pageSize', 100)
        start = pageSize * (pageNum - 1)
        end = pageSize * pageNum
        sql = """select A.view_user_id, A.create_at,A.invite_at, A.invite_status,A.invite_expire_at,B.nickname,B.sex, B.avatar_url 
from user_record A, register_info B where A.view_user_id=B.user_id AND A.user_id='%s' ORDER BY A.create_at DESC limit %s, %s""" % (
            user.get('open_id'), start, end)
        datas = execute_custom_sql(sql)
        return Response(self.wrapper(datas))

    def wrapper(self, datas):
        result = list()
        for data in datas:
            info = dict()
            info['view_user_id'] = data[0]
            info['create_at'] = time.mktime(
                time.strptime(str(data[1])[:str(data[1]).find('.')], "%Y-%m-%d %H:%M:%S")) if data[1] else data[1]
            info['invite_at'] = time.mktime(time.strptime(str(data[2]), "%Y-%m-%d %H:%M:%S")) if data[2] else data[2]
            info['invite_status'] = data[3]
            info['invite_expire_at'] = data[4]
            info['nickname'] = data[5]
            info['sex'] = data[6]
            info['avatar_url'] = data[7]
            result.append(info)
        return result
