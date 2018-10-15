# coding: utf-8
from activity.models import Activity, Coupon, Notice
from rest_framework import serializers


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name', 'image_url', 'image_text', 'context', 'register_time', 'activity_time', 'start_at',
                  'user_plan_count']


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ['id', 'code', 'corn', 'extra', 'create_at']


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'title', 'instruction', 'content_one', 'content_two', 'content_three', 'content_four', 'extra',
                  'create_at']
