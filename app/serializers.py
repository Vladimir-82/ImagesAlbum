from rest_framework import serializers
from .models import Post, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'author', 'title', 'category', 'photo', 'photo_mod', 'body', 'created_at',)
        model = Post



class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'category', 'photo', 'body', 'created_at',)
        model = Post