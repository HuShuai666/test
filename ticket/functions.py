# coding: utf-8
import datetime
from secrets import token_hex
from redis_tool.redis_server import redis_client
from ticket.sql import ticket_sql
import logging

logger = logging.getLogger('django')


class TicketAuthorize:
    @staticmethod
    def validate_ticket(ticket):
        cached_user_id = redis_client.get_instance(ticket)
        if cached_user_id:
            valid_ticket = True
            user_id = cached_user_id
            err_msg = None
        else:
            res_ticket = ticket_sql.get_ticket(ticket)
            if not res_ticket:
                valid_ticket = False
                user_id = None
                err_msg = 'ticket不存在'
            else:
                ticket = res_ticket
                expire_time = ticket['expired_time'][: ticket['expired_time'].find('.')]
                expire_time = expire_time.replace('T', ' ')
                if datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S') > datetime.datetime.now():
                    valid_ticket = True
                    user_id = ticket['user']['id']
                    err_msg = None
                    redis_client.set_instance(key=ticket['ticket'], value=user_id)
                else:
                    valid_ticket = False
                    user_id = None
                    err_msg = 'ticket已过期'
        return {'valid_ticket': valid_ticket, 'user_id': user_id, 'err_msg': err_msg}

    @staticmethod
    def create_ticket(user_id):
        now = datetime.datetime.now()
        expired_time = datetime.datetime.now() + datetime.timedelta(days=1)
        ticket = token_hex(32)
        ticket_sql.create_ticket(user_id=user_id, ticket=ticket, create_time=str(now), expired_time=str(expired_time))
        redis_client.set_instance(ticket, user_id)
        return ticket

    @staticmethod
    def delete_ticket(ticket):
        redis_client.delete(ticket)
        ticket_sql.delete_ticket(ticket)
        return
