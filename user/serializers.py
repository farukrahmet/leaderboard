import redis, pickle

from rest_framework import serializers

from django.contrib.auth import get_user_model

from django.conf import settings

redis_client = redis.Redis(settings.REDIS_HOST)


class UserSerializer(serializers.ModelSerializer):
    rank = serializers.SerializerMethodField(read_only=True)
    points = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ("user_id", "display_name", "points", "rank", "country")

    def create(self, validated_data):
        validated_data.update({"username": validated_data['user_id']})
        user_id = str(validated_data["user_id"])
        user_country = validated_data['country']
        new_score = redis_client.zadd(
            settings.LEADERBOARD_NAME,
            {str(user_id): float(self.initial_data['points'])}, incr=True)
        redis_client.zadd(
            "%s_%s" % (settings.LEADERBOARD_NAME, user_country),
            {str(user_id): float(self.initial_data['points'])}, incr=True)
        validated_data.update({"points": new_score})
        validated_data.update({"rank": self.initial_data['rank']})
        redis_client.set(
            str(user_id),
            pickle.dumps({"country": user_country, "display_name": validated_data['display_name']})
        )
        return super(UserSerializer, self).create(validated_data)

    def get_rank(self, user):
        return redis_client.zrevrank(settings.LEADERBOARD_NAME, str(user.user_id))
    
    def get_points(self, user):
        return redis_client.zscore(settings.LEADERBOARD_NAME, str(user.user_id))
