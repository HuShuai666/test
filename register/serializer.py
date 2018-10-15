# coding: utf-8
from rest_framework import serializers
from register.models import RegisterInfo, Register, NewCornRecord
import uuid


class RegisterInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterInfo
        fields = ['id', 'nickname', 'sexual_orientation', 'overseas_study_status', 'wechat', 'phone_number', 'hometown',
                  'future_city', 'future_school', 'user', 'create_at', 'update_at', 'constellation', 'sex', 'birthday',
                  'demand_area', 'demand_cp_age', 'degree', 'avatar_url', 'tag', 'picture_url']
        read_only_fields = ['phone_number']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = ['id', 'user', 'create_at', 'activity']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)


class NewCornRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewCornRecord
        fields = ['id', 'user', 'operation', 'corn', 'create_at', 'extra', 'balance', 'other_open_id', 'nickname', 'coupon']
        read_only_fields = ['id', 'coupon']

    def create(self, validated_data):
        validated_data['id'] = str(uuid.uuid4())
        return super().create(validated_data)
