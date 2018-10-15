from django.db import models

# Create your models here.
from activity.models import Activity
from authentication.models import User


class RegisterInfo(models.Model):
    SEX_CHOICE = (
        (0, '异性'),
        (1, '同性'),
        (2, '双性')
    )
    OVERSEAS_STUDY_STATUS = (
        (0, '准留学生'),
        (1, '留学生'),
        (2, '毕业生')
    )
    CP_AGE = (
        (0, '比TA大'),
        (1, '跟TA一样'),
        (2, '比TA小'),
        (3, '无要求')
    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    nickname = models.CharField('活动昵称', max_length=64)
    sex = models.IntegerField('性别')
    birthday = models.DateTimeField('生日')
    constellation = models.CharField('星座', null=True, max_length=32)
    sexual_orientation = models.IntegerField('性取向', choices=SEX_CHOICE)
    overseas_study_status = models.IntegerField('留学状态', choices=OVERSEAS_STUDY_STATUS)
    wechat = models.CharField('微信号或手机号', max_length=32)
    phone_number = models.CharField('手机号码', max_length=11, null=True)
    hometown = models.CharField('家乡', max_length=64)
    future_city = models.CharField('想就读的城市', max_length=64)
    future_school = models.CharField('想就读的学校', max_length=64)
    demand_area = models.CharField('区域选择', max_length=32)
    demand_cp_age = models.IntegerField('对CP的年龄要求', choices=CP_AGE, default=3)
    degree = models.CharField('学位', max_length=32)
    user = models.ForeignKey(User)
    avatar_url = models.CharField('用户微信头像地址', max_length=255, null=True)
    create_at = models.DateTimeField('注册时间', auto_now_add=True, null=True)
    update_at = models.DateTimeField('修改时间', auto_now=True, null=True)
    invite_code = models.CharField('邀请码', max_length=16, null=True)
    tag = models.IntegerField('用户标记', default=1, null=True)
    picture_url = models.CharField('用户图片', null=True, max_length=255)

    class Meta:
        db_table = "register_info"


class Register(models.Model):
    id = models.CharField('序列号', max_length=64, primary_key=True)
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    create_at = models.DateTimeField('报名时间', null=True, auto_now_add=True)

    class Meta:
        db_table = "register"


class NewCornRecord(models.Model):
    OPTION_CHOICE = (
        (0, '关注留学新青年'),
        (1, '邀请用户'),
        (2, '关注北美留学生'),
        (3, '每日登陆'),
        (4, '活动报名'),
        (5, '接受用户邀请'),
        (6, '切换用户'),
        (7, '邀请用户报名'),
        (8, '预报名活动'),
        (9, '系统赠送'),
        (10, '活动赠送')

    )
    id = models.CharField('序列号', max_length=64, primary_key=True)
    user = models.ForeignKey(User, db_index=True)
    operation = models.IntegerField('操作类型', choices=OPTION_CHOICE)
    corn = models.IntegerField('New币值')
    balance = models.IntegerField('账户余额')
    create_at = models.DateTimeField('记录时间', auto_now_add=True, null=True)
    extra = models.CharField('备注说明', max_length=64, null=True)
    other_open_id = models.CharField('其他公众号的ID', max_length=64, null=True)
    nickname = models.CharField('用户昵称', max_length=64, null=True)
    coupon = models.CharField('优惠券码', max_length=32, null=True)

    class Meta:
        db_table = "new_corn_record"
        ordering = ['-create_at']
