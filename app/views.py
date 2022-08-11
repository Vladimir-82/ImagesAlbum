from PIL import Image
from io import BytesIO

from django.shortcuts import redirect
from django.core.files.base import ContentFile
from rest_framework import generics, permissions
from .models import Post
from .serializers import ViewSerializer, CreateSerializer, DetailViewSerializer
from .permissions import IsAuthorOrReadOnly


class ViewList(generics.ListAPIView):
    '''Returns a list of posts for all users'''
    permission_classes = (permissions.AllowAny,)
    queryset = Post.objects.all()
    serializer_class = ViewSerializer


class DetailList(generics.RetrieveUpdateDestroyAPIView):
    '''Returns a detailed list of publications for author or read only'''
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = DetailViewSerializer

    def get_object(self):
        '''Increases the number of views'''
        object = super().get_object()
        object.views += 1
        object.save()
        return object


class CreateApi(generics.ListCreateAPIView):
    '''Creates a post for registered users'''
    queryset = Post.objects.all()
    serializer_class = CreateSerializer

    def post(self, request, *args, **kwargs):
        '''resizes a photo'''
        serializer = CreateSerializer(data=request.data)
        if serializer.is_valid():
            author_id = request.user.id
            data = request.data
            image = Image.open(data['photo'])
            width, height = image.size
            if width > height:
                new_width = 150
                new_height = new_width * height // width
            else:
                new_height = 150
                new_width = new_height * width // height
            image = image.resize((new_width, new_height))
            buffer = BytesIO()
            image.save(fp=buffer, format='webp')
            post = Post.objects.create(author_id=author_id, category_id=data['category'],
                                       title=data['title'], photo=data['photo'],
                                       body=data['body'])
            name = ''.join(('photo_', str(post.id), '.webp'))
            post.photo_mod.save(name=name, content=ContentFile(buffer.getvalue()), save=False)
            post.save()
            return redirect('create')


class ViewTop3List(generics.ListAPIView):
    '''Returns a list of top 3 posts'''
    queryset = Post.objects.order_by('-views', 'created_at')[:3]
    serializer_class = ViewSerializer
