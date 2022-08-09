from django.urls import path
from .views import PostList, PostDetail, CreateApi


urlpatterns = [
    path('<int:pk>/', PostDetail.as_view(), name='detail'),
    path('', PostList.as_view(), name='view'),
    path('create',  CreateApi.as_view(), name='create')
]


