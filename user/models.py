from django.db import models


from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.UUIDField()
    display_name = models.CharField(max_length=255)
    points = models.PositiveIntegerField()
    rank = models.PositiveIntegerField()
    country = models.CharField(max_length=8)
