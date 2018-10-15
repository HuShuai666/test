# coding: utf-8
from rest_framework import serializers
from task.models import *


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'name', 'content', 'extra', 'create_at', 'update_at']


class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ['id', 'task', 'user_id', 'cp_user_id', 'status', 'extra', 'create_at', 'update_at']


class UserTaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskResult
        fields = ['id', 'task', 'user_id', 'cp_user_id', 'content', 'create_at']


class UserTaskImageMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTaskImageMapping
        fields = ['id', 'task', 'image_url', 'extra', 'create_at']
