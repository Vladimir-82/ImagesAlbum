from django.urls import path
from .views import ViewList, DetailList, CreateApi, ViewTop3List, \
    GetUserEmailsList, GetUserGenreList


urlpatterns = [
    path('<int:pk>/', DetailList.as_view(), name='detail'),
    path('', ViewList.as_view(), name='view'),
    path('create',  CreateApi.as_view(), name='create'),
    path('top3',  ViewTop3List.as_view(), name='top3'),
    path('user_emails', GetUserEmailsList.as_view(), name='emails'),
    path('genres', GetUserGenreList.as_view(), name='genres')
]


