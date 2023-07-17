from django.urls import path
from .views import ViewList, DetailList, CreateApi, ViewTop3List, \
    GetUserEmailsList, GetUserGenreList, GetUsersGenres, GetSearchClient, \
    GetSearchOwnClient


urlpatterns = [
    path('<int:pk>/', DetailList.as_view(), name='detail'),
    path('', ViewList.as_view(), name='view'),
    path('create',  CreateApi.as_view(), name='create'),
    path('top3',  ViewTop3List.as_view(), name='top3'),
    path('user_emails', GetUserEmailsList.as_view(), name='emails'),
    path('genres', GetUserGenreList.as_view(), name='genres'),
    path('users_genres', GetUsersGenres.as_view(), name='users_genres'),
    path('get_client', GetSearchClient.as_view(), name='get_client'),
    path('get_owner_search', GetSearchOwnClient.as_view(), name='get_owner_search')
]


