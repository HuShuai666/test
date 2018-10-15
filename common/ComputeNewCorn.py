# coding: utf-8
import datetime

from rest_framework import exceptions

from register.models import NewCornRecord
import logging
import uuid

logger = logging.getLogger('django')
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


class NewCornCompute:
    @staticmethod
    def compute_new_corn(user_id, operation, other_open_id=None, nickname=None):
        logger.info('compute_new_corn user_id=%s, operation=%s' % (user_id, operation))
        # 新关注公众号与注册成功的new币计算规则一致，都是要判断用户是否是首次，且不允许重复
        if operation == 0 or operation == 2:
            # 查询数据库是否已有new币记录
            record = NewCornRecord.objects.filter(user_id=user_id)
            corn = 2
            extra = '关注留学新青年' if operation == 0 else '关注北美留学生'
            extra = '邀请用户' + nickname + extra
            # 数据库中没有当前用户new币记录则创建
            if not record:
                NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user_id, operation=operation, balance=corn,
                                             corn=corn, extra=extra, other_open_id=other_open_id, nickname=nickname)
            else:
                temp = NewCornRecord.objects.filter(user_id=user_id, operation=operation, other_open_id=other_open_id)
                # 判断是否是首次关注
                if not temp:
                    balance = record[0].balance
                    NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user_id, operation=operation,
                                                 balance=corn + balance, corn=corn, extra=extra,
                                                 other_open_id=other_open_id, nickname=nickname)
                else:
                    raise exceptions.ValidationError('你已经帮邀请码领取New币咯，不能重复领取。回复「CP」，一起参与该活动，解锁你的小哥哥和小姐姐吧。')
        # 每日登陆的逻辑处理
        elif operation == 3:
            start_date = datetime.datetime.now()
            record = NewCornRecord.objects.filter(user_id=user_id, operation=operation,
                                                  create_at__day=start_date.day, create_at__month=start_date.month)
            if not record:
                record = NewCornRecord.objects.filter(user_id=user_id)
                if not record:
                    NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user_id, operation=operation, balance=1,
                                                 corn=1,
                                                 extra='每日登陆')
                else:
                    balance = record[0].balance
                    # 查询最新记录添加记录
                    NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user_id, operation=operation,
                                                 balance=1 + balance, corn=1,
                                                 extra='每日登陆')
        else:
            record = NewCornRecord.objects.filter(user_id=user_id)
            if not record:
                balance = 0
            else:
                record = record.first()
                balance = record.balance
            corn = 0
            extra = None
            if operation == 1:
                corn = 3
                if balance < corn:
                    logger.info('compute_new_corn operation=%s,balance=%s' % (str(operation), str(balance)))
                    raise exceptions.ValidationError('您的new币不足，请去完成任务获取')
                balance -= corn
                extra = '邀请用户'
            elif operation == 4:
                corn = 5
                balance += corn
                extra = '活动报名'
            elif operation == 5:
                corn = 2
                if balance < corn:
                    logger.info('compute_new_corn operation=%s,balance=%s' % (str(operation), str(balance)))
                    raise exceptions.ValidationError('您的new币不足，请去完成任务获取')
                balance -= corn
                extra = '接受用户邀请'
            elif operation == 6:
                corn = 1
                if balance < corn:
                    logger.info('compute_new_corn operation=%s,balance=%s' % (str(operation), str(balance)))
                    raise exceptions.ValidationError('您的new币不足，请去完成任务获取')
                balance -= corn
                extra = '切换用户'
            elif operation == 7:
                extra = '邀请用户报名'
                corn = 2
                balance += corn
            elif operation == 8:
                extra = '预报名活动'
                corn = 20
                balance += corn
            NewCornRecord.objects.create(id=str(uuid.uuid4()), user_id=user_id, operation=operation, balance=balance,
                                         corn=corn, extra=extra)
        return "success"
