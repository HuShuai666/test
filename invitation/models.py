from django.db import models


# Create your models here.
class Invitation(models.Model):
    STATUS = (
        (0, '有效'),
        (1, '成功'),
        (2, '无效')
    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    inviter = models.CharField('邀请人', max_length=64)
    invitee = models.CharField('被邀请人', max_length=64)
    status = models.IntegerField('状态', choices=STATUS)
    expire_at = models.DateTimeField('过期时间', null=True)
    create_time = models.DateTimeField('邀请时间', null=True)
    update_at = models.DateTimeField('更新时间', auto_now=True, null=True)

    class Meta:
        db_table = "invitation"


class UserRecord(models.Model):
    STATUS = (
        (0, '未邀请'),
        (0, '有效'),
        (1, '成功'),
        (2, '无效')
    )
    id = models.AutoField('序列号', primary_key=True)
    user_id = models.CharField('用户编号', max_length=64)
    view_user_id = models.CharField('已查看的用户编号', max_length=64)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    invite_at = models.DateTimeField('邀请时间', null=True)
    invite_status = models.IntegerField('邀请状态', choices=STATUS, null=True, default=-1)
    invite_expire_at = models.DateTimeField('过期时间', null=True)

    class Meta:
        db_table = "user_record"


class Cp(models.Model):
    id = models.AutoField('序列号', primary_key=True)
    invitee = models.CharField('受邀请人编号', max_length=64)
    count = models.IntegerField('受邀次数')

    class Meta:
        db_table = "cp"
