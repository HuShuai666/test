from django.db import models


class Activity(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    name = models.CharField('活动名称', max_length=64)
    image_url = models.CharField('首页背景图片地址', max_length=128, null=True)
    image_text = models.CharField('背景图片文字', max_length=256, null=True)
    context = models.TextField('活动内容描述')
    register_time = models.CharField('报名时间', max_length=64, null=True)
    activity_time = models.CharField('活动时间', max_length=64, null=True)
    start_at = models.DateTimeField('活动开始时间', null=True)
    user_plan_count = models.IntegerField('计划报名人数', null=True)

    class Meta:
        db_table = "activity"


class Coupon(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    code = models.CharField('活动优惠码', max_length=64)
    corn = models.IntegerField('New币数量')
    extra = models.CharField('描述', null=True, max_length=255)
    create_at = models.DateTimeField('创建时间', auto_now_add=True, null=True)

    class Meta:
        db_table = "coupon"


class Notice(models.Model):
    id = models.AutoField('序列号', primary_key=True)
    title = models.CharField('公告标题', max_length=64)
    instruction = models.CharField('公告说明', max_length=255, null=True)
    content_one = models.CharField('公告内容', max_length=255, null=True)
    content_two = models.CharField('公告内容', max_length=255, null=True)
    content_three = models.CharField('公告内容', max_length=255, null=True)
    content_four = models.CharField('公告内容', max_length=255, null=True)
    extra = models.CharField('扩展信息', max_length=255, null=True)
    create_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "notice"
