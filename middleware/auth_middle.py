# coding: utf-8
import json
from django.utils.deprecation import MiddlewareMixin
from django.http.response import HttpResponse
from authentication.models import User
from authentication.serializers import UserSerializer
from redis_tool.redis_server import redis_client
from CpBackend.settings import ignore_auth_urls
from ticket.functions import TicketAuthorize
import logging

logger = logging.getLogger("django")


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        url_path = request.path
        if url_path in ignore_auth_urls:
            return
        logger.info('Auth Url: %s' % url_path)
        # ticket = request.COOKIES.get('ticket')
        # if not ticket:
        #     data = request.GET.dict()
        #     ticket = data.get('ticket')
        data = request.GET.dict()
        ticket = data.get('ticket')
        if not ticket:
            return HttpResponse(content=json.dumps(dict(code=401, msg='未登录')),
                                content_type='application/json')
        auth_res = TicketAuthorize.validate_ticket(ticket)
        valid_ticket = auth_res['valid_ticket']
        if not valid_ticket:
            return HttpResponse(content=json.dumps(dict(code=401, msg='验证失败: %s' % auth_res['err_msg'])),
                                content_type='application/json')
        if not redis_client.get_instance(key=auth_res['user_id']):
            logger.info('Get User Info From DataBase')
            user = User.objects.filter(open_id=auth_res['user_id']).first()
            serializer = UserSerializer(user)
            user_info = serializer.data
            redis_client.set_instance(auth_res['user_id'], serializer.data)
        else:
            user_info = redis_client.get_instance(auth_res['user_id'])
            logger.info('Get User Info From Redis')
        user_info['ticket'] = ticket
        request.user_info = user_info
