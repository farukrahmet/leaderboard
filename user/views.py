from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, JSONParser

from django.contrib.auth import get_user_model

from user.serializers import UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    lookup_field = 'user_id'
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, JSONParser]
