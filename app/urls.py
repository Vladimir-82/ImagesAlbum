from django.urls import path
from .views import ViewList, DetailList, CreateApi


urlpatterns = [
    path('<int:pk>/', DetailList.as_view(), name='detail'),
    path('', ViewList.as_view(), name='view'),
    path('create',  CreateApi.as_view(), name='create')
]


