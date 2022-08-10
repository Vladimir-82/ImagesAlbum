from rest_framework import serializers
from .models import Post, Category


class ViewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'category', 'photo_mod', 'created_at', 'views')
        model = Post


class DetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'category', 'photo', 'body', 'created_at', 'views')
        model = Post



class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'category', 'photo', 'body', 'created_at',)
        model = Post