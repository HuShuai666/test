import json
import random

import datetime

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import mixins, viewsets, exceptions, serializers
from rest_framework.decorators import list_route, detail_route

from CpBackend import settings
from authentication.models import User
from register.models import RegisterInfo, Register, NewCornRecord
from register.serializer import RegisterInfoSerializer, RegisterSerializer, NewCornRecordSerializer
from django.db import transaction
from invitation.models import Invitation, UserRecord
import uuid
import logging
from common.ComputeNewCorn import NewCornCompute
from common.NewCornType import NewCornType

logger = logging.getLogger('django')


class RegisterInfoView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = RegisterInfo.objects.all()
    serializer_class = RegisterInfoSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user_info
        # 查看当前用户是否已经注册过信息
        record = RegisterInfo.objects.filter(user_id=request.data.get('user'))
        if record:
            raise exceptions.ValidationError('当前用户已经注册过信息')
        # 将注册信息录入数据库
        request.data['id'] = str(uuid.uuid4())
        request.data['user'] = user.get('open_id')
        request.data['constellation'] = self._get_constellations(request.data['birthday'])
        request.data['avatar_url'] = user.get('avatar_url')
        super().create(request, *args, **kwargs)
        # 报名指定的活动
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))
        # 给新用户添加New币
        NewCornCompute.compute_new_corn(user.get('open_id'), NewCornType.ATTEND_ACTIVITY.value)
        if request.data.get('invite_code'):
            inviter = User.objects.filter(code=request.data.get('invite_code'))
            if inviter:
                NewCornCompute.compute_new_corn(inviter[0].open_id, NewCornType.INVITE_USERS_ATTEND.value)
        # 判断用户是否是预报名
        if datetime.datetime.now().day < 15 and datetime.datetime.now().month == 4:
            NewCornCompute.compute_new_corn(user.get('open_id'), NewCornType.PRE_ACTIVITY.value)
        return Response()

    def _get_constellations(self, birthday):
        """
        根据出生日期计算星座
        :param birthday: 
        :return: 
        """
        if not birthday:
            raise exceptions.ValidationError('生日信息不能为空')
        temp = datetime.datetime.strptime(birthday, "%Y-%m-%d %H:%M:%S")
        day = temp.day
        month = temp.month
        dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
        constellations = ("摩羯座", "水瓶座", "双鱼座", "白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座")
        if day < dates[month - 1]:
            return constellations[month - 1]
        else:
            return constellations[month]

    def get_queryset(self):
        queryset = super().get_queryset()
        nickname = self.request.query_params.get('nickname')
        wechat = self.request.query_params.get('wechat')
        user_id = self.request.query_params.get('user_id')
        if nickname:
            queryset = queryset.filter(nickname=nickname)
        if wechat:
            queryset = queryset.filter(wechat=wechat)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @transaction.atomic
    @list_route(methods=['get'])
    def random(self, request):
        user_info = request.user_info
        if request.query_params.get('auto') == 'True':
            NewCornCompute.compute_new_corn(user_info.get('open_id'), NewCornType.SWITCH_USER.value)
        # 首先查询已看过用户记录表
        id_list = UserRecord.objects.filter(user_id=user_info['open_id']).values_list('view_user_id').order_by(
            '-create_at')
        # 定义目标用户ID
        target_user = None
        # 如果不扣new币，则从已看过的列表中选取最新的一个
        if id_list and request.query_params.get('auto') == 'False':
            target_user = RegisterInfo.objects.filter(user_id=id_list[0][0])[0]
        elif request.query_params.get('auto') == 'True' or len(id_list) == 0:
            id_result_list = list()
            for _id in id_list:
                id_result_list.append(_id[0])
            # 在查询的时候不能随机获取到当前用户，故需要将当前用户编号放入排他条件中
            id_result_list.append(user_info.get('open_id'))
            user_demand = RegisterInfo.objects.filter(user_id=user_info.get('open_id'))
            # 对CP性别的过滤
            user_demand_sex = [0, 1]
            if user_demand[0].sexual_orientation == 0:
                user_demand_sex = [1] if user_demand[0].sex == 0 else [0]
            elif user_demand[0].sexual_orientation == 1:
                user_demand_sex = [0] if user_demand[0].sex == 0 else [1]
            # 从注册信息表中随机获取不在已邀请的用户列表中的用户
            register_list = RegisterInfo.objects.filter(sex__in=user_demand_sex, tag=1).exclude(
                user_id__in=id_result_list)
            # 如果是同性，则需要精准匹配
            if user_demand[0].sexual_orientation == 1:
                register_list = register_list.filter(sexual_orientation=1)
            total = register_list.count()
            if total != 0:
                logger.info('*' * 70)
                logger.info('Get User From Real User')
                seed = random.randint(0, total - 1)
                result = register_list[seed:seed + 1]
                target_user = result[0]
                logger.info('target_user_id=%s' % target_user.user_id)
            else:
                # 从僵尸用户中查找
                logger.info('*' * 70)
                logger.info('Get User From Corpse')
                register_list = RegisterInfo.objects.filter(sex__in=user_demand_sex, tag=0).exclude(
                    user_id__in=id_result_list)
                if user_demand[0].sexual_orientation == 1:
                    register_list = register_list.filter(sexual_orientation=1)
                total = register_list.count()
                if total == 0:
                    raise exceptions.ValidationError('暂无匹配用户信息')
                seed = random.randint(0, total - 1)
                result = register_list[seed:seed + 1]
                if len(result) == 0:
                    raise exceptions.ValidationError('暂无匹配用户信息')
                target_user = result[0]
        user = User.objects.filter(open_id=target_user.user_id).first()
        data = RegisterInfoSerializer(target_user).data
        # 获取到随机用户之后，应将当前用户放入查看记录表user_record中
        if not (id_list and request.query_params.get('auto') == 'False'):
            UserRecord.objects.create(user_id=user_info['open_id'], view_user_id=data.get('user'))
        data['avatar_url'] = user.avatar_url
        data['age'] = datetime.datetime.now().year - int(data['birthday'][:4])
        data['sex'] = '男' if data['sex'] == 1 else '女'
        if data['picture_url'] and str(data['picture_url']).find('https') == -1:
            data['picture_url'] = 'https://cp1.lxhelper.com/media' + data['picture_url']
        if data['sexual_orientation'] == 0:
            data['sexual_orientation'] = '异性'
        elif data['sexual_orientation'] == 1:
            data['sexual_orientation'] = '同性'
        elif data['sexual_orientation'] == 2:
            data['sexual_orientation'] = '双性'
        if data['overseas_study_status'] == 0:
            data['overseas_study_status'] = '准留学生'
        elif data['overseas_study_status'] == 1:
            data['overseas_study_status'] = '留学生'
        elif data['overseas_study_status'] == 2:
            data['overseas_study_status'] = '毕业生'
        return Response(data)

    def update(self, request, *args, **kwargs):
        result = RegisterInfo.objects.get(id=kwargs.get('pk'))
        params = request.data
        if params.get('nickname'):
            result.nickname = params.get('nickname')
        if params.get('sexual_orientation'):
            result.sexual_orientation = params.get('sexual_orientation')
        if params.get('overseas_study_status'):
            result.overseas_study_status = params.get('overseas_study_status')
        if params.get('wechat'):
            result.wechat = params.get('wechat')
        if params.get('phone_number'):
            result.phone_number = params.get('phone_number')
        if params.get('hometown'):
            result.hometown = params.get('hometown')
        if params.get('future_city'):
            result.future_city = params.get('future_city')
        if params.get('future_school'):
            result.future_school = params.get('future_school')
        result.save()
        return Response()

    @list_route(methods=['post'])
    def upload(self, request):
        """
         用户上传图片
         """
        user = request.user_info
        user_register = RegisterInfo.objects.filter(user_id=user.get('open_id'))
        if not user_register:
            raise serializers.ValidationError('当前用户未填写注册信息，不能上传图片')
        try:
            f1 = request.FILES['image']
            rand_name = str(uuid.uuid4()) + f1.name[f1.name.rfind('.'):]
            fname = '%s/upload/picture/%s' % (settings.MEDIA_ROOT, rand_name)
            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)
            user_register[0].picture_url = '/upload/picture/' + rand_name
            user_register[0].save()
            return HttpResponse(json.dumps({'code': 0, 'data': 'success'}))
        except exceptions as e:
            logger.info(e + "")
            return HttpResponse(json.dumps({'code': -1, 'data': '图片上传失败'}))

    @list_route(methods=['get'])
    def by_user(self, request):
        params = request.query_params
        if not params.get('user_id'):
            raise exceptions.ValidationError('参数user_id不能为空')
        target_user = RegisterInfo.objects.filter(user_id=params.get('user_id')).first()
        if not target_user:
            raise exceptions.ValidationError('当前用户不存在')
        result = RegisterInfoSerializer(target_user).data
        if result['picture_url'] and str(result['picture_url']).find('https') == -1:
            result['picture_url'] = 'https://cp1.lxhelper.com/media' + result['picture_url']
        result['age'] = datetime.datetime.now().year - int(result['birthday'][:4])
        return Response(result)


class RegisterView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @list_route(methods=['get'])
    def check_register(self, request):
        """
        检查用户是否已参加活动
        :param request: 
        :return: 
        """
        user_info = request.user_info
        activity_id = request.query_params.get('activity_id')
        if not activity_id:
            raise exceptions.ValidationError('Param activity_id is none')
        result = Register.objects.filter(user_id=user_info.get('open_id'), activity_id=activity_id)
        return Response(True if len(result) != 0 else False)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user_info = request.user_info
        # 报名指定的活动
        Register.objects.create(id=str(uuid.uuid4()), user_id=request.data.get('user'),
                                activity_id=request.data.get('activity'))
        # 给新用户添加New币
        NewCornCompute.compute_new_corn(user_info.get('open_id'), NewCornType.ATTEND_ACTIVITY.value)

    @list_route(methods=['get'])
    def activity_number(self, request):
        count = Register.objects.all().count()
        return Response(count)


class NewCornRecordView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = NewCornRecord.objects.all()
    serializer_class = NewCornRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    @detail_route(methods=['get'])
    def balance(self, request, pk):
        user_id = pk
        new_corn_record = NewCornRecord.objects.filter(user_id=user_id)
        if not new_corn_record:
            balance = 0
        else:
            new_corn_record = new_corn_record.latest('create_at')
            balance = new_corn_record.balance
        return Response({'user_id': user_id, 'balance': balance})

    @list_route(methods=['get'])
    def check_public_number(self, request):
        user = request.user_info
        results = NewCornRecord.objects.filter(nickname=user.get('nick_name'), operation__in=(0, 2))
        data = {'NorthAmerican': False, 'OverseasYouth': False}
        for result in results:
            if result.operation == 0:
                data['OverseasYouth'] = True
            if result.operation == 2:
                data['NorthAmerican'] = True
        return Response(data)
