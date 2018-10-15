import json

from django.db import transaction
from django.db.models import Q
import uuid

from django.http import HttpResponse
from rest_framework import mixins, viewsets, serializers
from rest_framework.decorators import list_route
from rest_framework.response import Response
from CpBackend import settings
from task.models import Task, UserTask, UserTaskResult, UserTaskImageMapping
from task.serializer import TaskSerializer, UserTaskSerializer, UserTaskResultSerializer, UserTaskImageMappingSerializer


class TaskView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
               mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        """
        获取当前用户任务列表
        :param request: 
        :return: 
        """
        user = request.user_info
        query_set = Task.objects.all()
        all_task = TaskSerializer(query_set, many=True).data
        task_ids = list()
        for task in all_task:
            task_ids.append(task['id'])
        user_task_infos = UserTask.objects.filter(Q(user_id=user.get('open_id'), task_id__in=task_ids)).values(
            'task_id', 'status')
        for task in all_task:
            task['attend'] = False
            for info in user_task_infos:
                if task['id'] == info['task_id']:
                    task['attend'] = True
                    task['status'] = info['status']
                    break
        return Response(all_task)

    def retrieve(self, request, *args, **kwargs):
        """
        获取任务详情
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        task_id = kwargs.get('pk')
        task_result = Task.objects.filter(id=task_id)
        if not task_result:
            raise serializers.ValidationError('未查询到当前活动信息')
        data = TaskSerializer(task_result[0]).data
        return Response(data)

    def create(self, request, *args, **kwargs):
        """
        创建活动
        :param request: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        request.data['id'] = str(uuid.uuid4())
        super().create(request, *args, **kwargs)
        return Response()


class UserTaskView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        param = request.data
        if not param.get('task_id'):
            raise serializers.ValidationError('参数task_id不能为空')
        user = request.user_info
        if not user.get('cp_user_id'):
            raise serializers.ValidationError('当前用户暂无CP信息')
        is_accept_task = UserTask.objects.filter(user_id=user.get('open_id'), task_id=param.get('task_id'))
        if is_accept_task:
            raise serializers.ValidationError('当前用户或CP好友已领取任务')
        # 当前用户领取任务后，CP也自动领取任务，故向数据了录入2条记录数据
        UserTask.objects.create(id=str(uuid.uuid4()), task_id=param.get('task_id'), user_id=user.get('open_id'),
                                cp_user_id=user.get('cp_user_id'))
        UserTask.objects.create(id=str(uuid.uuid4()), task_id=param.get('task_id'), user_id=user.get('cp_user_id'),
                                cp_user_id=user.get('open_id'))
        return Response("任务领取成功")


class UserTaskResultView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = UserTaskResult.objects.all()
    serializer_class = UserTaskResultSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user_info
        request.data['user_id'] = user.get('open_id')
        if not user.get('cp_user_id'):
            raise serializers.ValidationError('当前用户暂无CP信息')
        request.data['cp_user_id'] = user.get('cp_user_id')
        request.data['id'] = str(uuid.uuid4())
        check_task = UserTaskResult.objects.filter(task=request.data['task'], user_id=user.get('open_id'),
                                                   cp_user_id=user.get('cp_user_id'))
        if check_task:
            raise serializers.ValidationError('当前用户已提交任务')
        super().create(request, *args, **kwargs)
        # 用户提交任务之后要更新user_task中的任务状态
        UserTask.objects.filter(task_id=request.data['task'], user_id=user.get('open_id'),
                                cp_user_id=user.get('cp_user_id')).update(status=1)
        return Response()

    @list_route(methods=['get'])
    def check_task(self, request):
        user = request.user_info
        task_id = request.query_params.get('task_id')
        if not task_id:
            raise serializers.ValidationError('参数task_id不能为空')
        result = UserTaskResult.objects.filter(user_id=user.get('open_id'), task_id=task_id)
        return Response(True if result else False)

    @list_route(methods=['get'])
    def check_cp_task(self, request):
        user = request.user_info
        task_id = request.query_params.get('task_id')
        if not task_id:
            raise serializers.ValidationError('参数task_id不能为空')
        if not user.get('cp_user_id'):
            raise serializers.ValidationError('当前用户暂无CP信息')
        result = UserTaskResult.objects.filter(user_id=user.get('cp_user_id'), task_id=task_id)
        return Response(True if result else False)


class UserTaskImageMappingView(mixins.CreateModelMixin, viewsets.GenericViewSet, mixins.ListModelMixin,
                               mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = UserTaskImageMapping.objects.all()
    serializer_class = UserTaskImageMappingSerializer

    def create(self, request, *args, **kwargs):
        """
        用户提交任务上传图片
        """
        f1 = request.FILES['image']
        task_id = request.data.get('task_id')
        user = request.user_info
        if not task_id:
            raise serializers.ValidationError('参数task_id不能为空')
        rand_name = str(uuid.uuid4()) + f1.name[f1.name.rfind('.'):]
        fname = '%s/upload/task/%s' % (settings.MEDIA_ROOT, rand_name)
        with open(fname, 'wb') as pic:
            for c in f1.chunks():
                pic.write(c)
        UserTaskImageMapping.objects.create(id=str(uuid.uuid4()), task_id=task_id, user_id=user.get('open_id'),
                                            image_url='/upload/task/' + rand_name)
        return HttpResponse(json.dumps({'code': 0, 'data': 'success'}))
