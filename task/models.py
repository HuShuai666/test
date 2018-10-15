from django.db import models


class Task(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    name = models.CharField('任务名称', max_length=64)
    content = models.CharField('任务详情', max_length=255)
    extra = models.CharField('备注', max_length=255, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "task"
        ordering = ['-create_at']


class UserTask(models.Model):
    STATUS = (
        (0, '已领取'),
        (1, '已完成')
    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    task = models.ForeignKey(Task)
    user_id = models.CharField('率先领取任务的用户编号', max_length=64)
    cp_user_id = models.CharField('CP好友用户编号', max_length=64)
    status = models.IntegerField('任务状态', default=0, choices=STATUS)
    extra = models.CharField('备注', max_length=255, null=True)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)

    class Meta:
        db_table = "user_task"
        ordering = ['-create_at']


class UserTaskResult(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    task = models.ForeignKey(Task)
    user_id = models.CharField("用户编号", max_length=64)
    cp_user_id = models.CharField('CP编号', max_length=64)
    content = models.CharField('任务结果描述', max_length=255)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)

    class Meta:
        db_table = "user_task_result"
        ordering = ['-create_at']


class UserTaskImageMapping(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    task = models.ForeignKey(Task)
    user_id = models.CharField("用户编号", max_length=64)
    image_url = models.CharField('对应上传图片路径', max_length=255)
    extra = models.CharField('备注说明', null=True, max_length=64)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)

    class Meta:
        db_table = "user_task_image_mapping"
        ordering = ['-create_at']
