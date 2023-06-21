from rest_framework import serializers
from .models import Post


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



class ViewTop3Serializer(serializers.ModelSerializer):

    email = serializers.EmailField(source="author.email", read_only=True)
    category_name = serializers.CharField(source="category.title", read_only=True)

    class Meta:
        fields = '__all__'
        model = Post