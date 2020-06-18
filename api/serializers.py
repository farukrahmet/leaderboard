import redis
import pickle

from rest_framework import serializers
from django.conf import settings

from user.models import User

redis_client = redis.Redis(settings.REDIS_HOST)


class LeaderBoardSerializer(serializers.Serializer):
    country_code = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    limit = serializers.IntegerField(required=False)
    offset = serializers.IntegerField(required=False)

    def save(self):
        country_code = self.validated_data.get('country_code')
        limit = self.validated_data.get('limit', 20)
        offset = self.validated_data.get('offset', 0)
        if country_code:
            leaderboard = redis_client.zrevrange(
                "%s_%s" % (settings.LEADERBOARD_NAME, country_code),
                offset, offset+limit, withscores=True)
        else:
            leaderboard = redis_client.zrevrange(
                settings.LEADERBOARD_NAME, offset, offset+limit,
                withscores=True)
        response = []
        if not leaderboard:
            return response
        for id, (user_id, score) in enumerate(leaderboard):
            user_detail = pickle.loads(redis_client.get(user_id.decode()))
            response.append({
                "rank": id + 1,
                "points": score,
                "display_name": user_detail['display_name'],
                "country": user_detail['country']
            })
        return response

        
class ScoreSubmitSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    score_worth = serializers.DecimalField(max_digits=32, decimal_places=4)

    def validate_user_id(self, user_id):
        user_detail = redis_client.get(str(user_id))
        if not user_detail:
            raise serializers.ValidationError("User does not exist")
        user_detail = pickle.loads(user_detail)
        self.user_country = user_detail['country']
        return user_id

    def save(self):
        user_id = self.validated_data.get('user_id')
        score_worth = self.validated_data.get('score_worth')
        new_score = redis_client.zadd(
            settings.LEADERBOARD_NAME,
            {str(user_id): float(score_worth)}, incr=True)
        redis_client.zadd(
            "%s_%s" % (settings.LEADERBOARD_NAME, self.user_country),
            {str(user_id): float(score_worth)}, incr=True)
        # TODO: Kafka implementation for data sync redis and db
        return new_score
