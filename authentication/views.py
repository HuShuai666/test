# Create your views here.
from django.db import transaction
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from common.ComputeNewCorn import NewCornCompute
from authentication.models import User
from authentication.serializers import UserSerializer
from register.models import RegisterInfo, NewCornRecord
from utils.weixin_functions import WxInterfaceUtil
import logging
from common.NewCornType import NewCornType
from redis_tool.redis_server import redis_client

logger = logging.getLogger('django')


class UserView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route(['GET'])
    def authorize(self, request):
        """客户端登录获取授权"""
        code = request.query_params.get('code')
        if not code:
            raise serializers.ValidationError('Param code is none')
        res = WxInterfaceUtil.code_authorize(code)
        response = Response(res)
        response.set_cookie('ticket', res['ticket'])
        return response

    @list_route(['POST'])
    @transaction.atomic
    def check_account(self, request):
        """
        检查用户信息
        :param request: 
        :return: 
        """
        params = request.data
        encryptedData = params.get('encryptedData')
        iv = params.get('iv')
        if not (iv, encryptedData):
            raise serializers.ValidationError('encryptedData、iv参数不能为空')
        user_info = User.objects.filter(open_id=params.get('user_id')).first()
        data = UserSerializer(user_info)
        if not data.data:
            logger.info('无法通过用户open_id获取用户记录: user_id=%s' % params.get('user_id'))
            raise serializers.ValidationError('无法通过用户open_id获取用户记录: user_id=%s' % params.get('user_id'))
        # 用户每日登陆获取new币
        NewCornCompute.compute_new_corn(user_info.open_id, NewCornType.DAILY_LOGIN.value)
        # 录入用户信息到数据库，同时也要注意微信用户可能会更换信息
        if user_info.nick_name != params.get('nick_name') or user_info.avatar_url != params.get('avatar_url'):
            logger.info('check_account更新用户信息: user_id=%s' % params.get('user_id'))
            user_info.nick_name = params.get('nick_name')
            user_info.gender = params.get('gender')
            user_info.province = params.get('province')
            user_info.country = params.get('country')
            user_info.city = params.get('city')
            user_info.avatar_url = params.get('avatar_url')
            user_info.language = params.get('language')
            user_info.save()
            temp = UserSerializer(user_info).data
            logger.info('Update User from Redis')
            logger.info(temp)
            redis_client.set_instance(user_info.open_id, temp)
        return Response()

    @list_route(['get'])
    def information(self, request):
        user = request.user_info
        result = dict()
        register_info = RegisterInfo.objects.filter(user_id=user.get('open_id'))
        if register_info:
            result['nickname'] = register_info[0].nickname
        record = NewCornRecord.objects.filter(user_id=user.get('open_id'))[0:1]
        if record:
            result['balance'] = record[0].balance
        result['avatar_url'] = user.get('avatar_url')
        result['sex'] = register_info[0].sex if register_info else user.get('gender')
        result['activity_code'] = user.get('code')
        return Response(result)

    @list_route(['get'])
    def cp(self, request):
        params = request.query_params
        nickname = params.get('nickname')
        if not nickname:
            raise serializers.ValidationError('参数nickname不能为空')
        user = User.objects.filter(nick_name=nickname).first()
        if not user:
            raise serializers.ValidationError('您还未参加CP活动哦')
        if not user.cp_user_id:
            raise serializers.ValidationError('您还未匹配到CP哦')
        register_info_cp = RegisterInfo.objects.filter(user_id=user.cp_user_id).first()
        return Response(register_info_cp.wechat)
