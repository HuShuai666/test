# coding: utf-8
from CpBackend.settings import REDIS_CONFIG
import redis

redis_valid_time = 2*60*60


class RedisClient:

    @property
    def redis_client(self):
        client = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])
        return client

    def get_instance(self, key, delete_cache=False):
        redis_instance = self.redis_client.get(key)
        if not redis_instance:
            return None
        try:
            res = eval(redis_instance)
        except:
            res = str(redis_instance, encoding='utf-8')
        if delete_cache:
            self.redis_client.delete(key)
        return res

    def set_instance(self, key, value, default_valid_time=redis_valid_time):
        self.redis_client.set(key, value, default_valid_time)
        return

    def delete(self, key):
        self.redis_client.delete(key)
        return

redis_client = RedisClient()