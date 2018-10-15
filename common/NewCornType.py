# coding: utf-8
from enum import Enum, unique


@unique
class NewCornType(Enum):
    # 关注留学新青年
    ATTENTION_OVERSEAS_YOUTH = 0
    # 邀请用户
    INVITE_USERS = 1
    # 关注北美留学生公众号
    ATTENTION_NORTH_AMERICA = 2
    # 每日登陆
    DAILY_LOGIN = 3
    # 活动报名
    ATTEND_ACTIVITY = 4
    # 接受用户邀请
    ACCEPT_INVITATION = 5
    # 切换用户
    SWITCH_USER = 6
    # 邀请用户报名
    INVITE_USERS_ATTEND = 7
    # 预报名
    PRE_ACTIVITY = 8
    # 系统赠送
    SYS_DONATE = 9
    # 活动赠送
    ACTIVITY_DONATE = 10

