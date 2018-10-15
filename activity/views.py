import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from activity.models import Activity, Coupon, Notice
from activity.serializers import ActivitySerializer, NoticeSerializer
from rest_framework import exceptions, serializers

from authentication.models import User
from common.NewCornType import NewCornType
from register.models import Register, NewCornRecord
from common.execute_sql import dict_fetchall
import logging

logger = logging.getLogger('django')


class ActivityView(APIView):
    def get(self, request):
        params = request.query_params
        if not params.get('name'):
            raise exceptions.ValidationError('参数name(活动名称)不能为空')
        activity = Activity.objects.filter(name=params.get('name'))
        if not activity:
            raise exceptions.ValidationError('未查询到当前活动信息')
        serializer = ActivitySerializer(activity[0])
        result = serializer.data
        # 查询报名表中报名人数
        user_count = Register.objects.filter(activity=1).count()
        result['user_count'] = user_count
        return Response(result)


class ActivityStartAtView(APIView):
    def get(self, request):
        params = request.query_params
        if not params.get('name'):
            raise exceptions.ValidationError('参数name(活动名称)不能为空')
        activity = Activity.objects.filter(name=params.get('name'))
        if not activity:
            raise exceptions.ValidationError('未查询到当前活动信息')
        serializer = ActivitySerializer(activity[0])
        result = serializer.data
        return Response(result['start_at'])


class CornView(APIView):
    def get(self, request):
        params = request.query_params
        other_open_id = params.get('other_open_id')
        nickname = params.get('nickname')
        logger.info('*' * 70)
        logger.info(params)
        logger.info('*' * 70)
        # 获取邀请码
        coupon = params.get('coupon')
        if not all((coupon, other_open_id, nickname)):
            raise serializers.ValidationError('参数(coupon, other_open_id, nickname)均不能为空')
        coupon = Coupon.objects.filter(code=coupon).first()
        if not coupon:
            raise serializers.ValidationError('您的优惠券码无效哦')
        user = User.objects.filter(nick_name=nickname).first()
        if not user:
            raise serializers.ValidationError('您还未报名参加CP活动馆哦')
        new_corn_record = NewCornRecord.objects.filter(operation=NewCornType.ACTIVITY_DONATE.value,
                                                       other_open_id=other_open_id, nickname=nickname,
                                                       coupon=coupon.code).first()
        if new_corn_record:
            raise serializers.ValidationError('您已使用过优惠券哦')
        balance_record = NewCornRecord.objects.filter(user_id=user.open_id).latest('create_at')
        NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user.open_id,
                                     operation=NewCornType.ACTIVITY_DONATE.value,
                                     corn=coupon.corn, balance=balance_record.balance + coupon.corn,
                                     extra='优惠券' + coupon.code + '赠送',
                                     other_open_id=other_open_id, nickname=nickname, coupon=coupon.code)
        return Response('优惠券使用成功，您已成功获得' + str(coupon.corn) + 'New币')


class NoticeView(APIView):
    def get(self, request):
        params = request.query_params
        notice_id = params.get('notice_id')
        if not notice_id:
            raise serializers.ValidationError('参数notice_id不能为空')
        notice = Notice.objects.filter(id=notice_id).first()
        return Response(NoticeSerializer(notice).data)


class TestView(APIView):
    def get(self, request):
        sql = 'SELECT invitee,COUNT(*) as number from invitation GROUP BY invitee'
        result = dict_fetchall(sql)
        print(result)
        return Response(result)
