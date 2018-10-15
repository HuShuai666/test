# coding: utf-8
from django.db import models


class User(models.Model):
    open_id = models.CharField('open_id', max_length=64, primary_key=True)
    nick_name = models.CharField('微信昵称', max_length=64, null=True)
    GENDER = (
        (0, '未知'),
        (1, '男'),
        (2, '女')
    )
    gender = models.IntegerField('性别', choices=GENDER, default=0)
    avatar_url = models.CharField('用户头像', max_length=255, null=True)
    city = models.CharField('城市', max_length=64, null=True)
    country = models.CharField('国家', max_length=64, null=True)
    province = models.CharField('省份', max_length=64, null=True)
    language = models.CharField('语言', max_length=64, null=True)
    session_key = models.CharField('微信用户标示', max_length=64)
    union_id = models.CharField('union_id', max_length=64, null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True, null=True)
    code = models.CharField('用户活动码', max_length=16, null=True)
    last_login = models.DateTimeField('最后登录时间', null=True)
    cp_user_id = models.CharField('用户CP编号', max_length=64, null=True)
    cp_time = models.DateTimeField('CP匹配成功时间', null=True)

    class Meta:
        db_table = "user"



