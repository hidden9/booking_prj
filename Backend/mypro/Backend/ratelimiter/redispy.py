from django.conf import settings
from Backend.Backend.ratelimiter.backend.base import base
from redis.exceptions import NoScriptError

class RedisBackend(base):
    def __init__(self):

        THROTTLE_REDIS_HOST = getattr(settings, 'THROTTLE_REDIS_HOST', 'localhost')
        THROTTLE_REDIS_PORT = getattr(settings, 'THROTTLE_REDIS_PORT', 6379)
        THROTTLE_REDIS_DB = getattr(settings, 'THROTTLE_REDIS_DB', 0)
        THROTTLE_REDIS_AUTH = getattr(settings, 'THROTTLE_REDIS_AUTH', None)

        self.pool = redis.ConnectionPool(host=THROTTLE_REDIS_HOST, port=THROTTLE_REDIS_PORT, db=THROTTLE_REDIS_DB, password=THROTTLE_REDIS_AUTH)  # TODO: Parameterize connecti