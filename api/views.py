from rest_framework import response, status, views
from rest_framework.parsers import JSONParser, MultiPartParser

from api.models import LeaderBoard
from api.serializers import ScoreSubmitSerializer, LeaderBoardSerializer


class LeaderBoardView(views.APIView):
    serializer_class = LeaderBoardSerializer

    def get(self, request, country_code=None, *args, **kwargs):
        data = request.GET.copy()
        if country_code:
            data.update({"country_code": country_code})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        resp = serializer.save()
        return response.Response(resp, status=status.HTTP_200_OK)


class ScoreSubmitView(views.APIView):
    serializer_class = ScoreSubmitSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_score = serializer.save()
        return response.Response(
            {"new_score": new_score}, status=status.HTTP_201_CREATED)