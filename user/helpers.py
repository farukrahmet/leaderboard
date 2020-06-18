import redis
import pickle

from django.conf import settings

redis_client = redis.Redis(settings.REDIS_HOST)


def fill_cache():
    from user.models import User
    for user in User.objects.all().iterator():
        redis_client.set(
            str(user.user_id),
            pickle.dumps({"country": user.country, "display_name": user.display_name})
        )