from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

urlpatterns = [
    path('leaderboard/', views.LeaderBoardView.as_view()),
    path('leaderboard/<str:country_code>', views.LeaderBoardView.as_view()),
    path('score/submit', views.ScoreSubmitView.as_view()),
]