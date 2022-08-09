from PIL import Image
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework import generics
from .models import Post
from .serializers import PostSerializer, CreateSerializer

from io import BytesIO


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



class CreateApi(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = CreateSerializer


    def post(self, request, *args, **kwargs):
        serializer = CreateSerializer(data=request.data)
        if serializer.is_valid():
            author_id = request.user.id
            data = serializer.data
            print(data)
            # im = Image.open(data['photo'])


            Post.objects.create(author_id=author_id, category_id=data['category'],
                                       title=data['title'], photo=data['photo'],
                                       body=data['body'])
            return redirect('create')