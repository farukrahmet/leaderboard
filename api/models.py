from django.db import models
from django.contrib.auth import get_user_model


class LeaderBoard(models.Model):
    user = get_user_model()
    points = models.DecimalField(max_digits=32, decimal_places=4)