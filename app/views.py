from PIL import Image
from io import BytesIO

from django.shortcuts import redirect
from django.core.files.base import ContentFile
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Genre
from .serializers import *
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
        '''
        Increases the number of views
        '''
        object = super().get_object()
        object.views += 1
        object.save()
        return object


class CreateApi(generics.ListCreateAPIView):
    '''
    Creates a post for registered users
    '''
    queryset = Post.objects.all()
    serializer_class = CreateSerializer

    def post(self, request, *args, **kwargs):
        '''
        Resizes a photo
        '''
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
            post = Post.objects.create(author_id=author_id,
                                       category_id=data['category'],
                                       title=data['title'],
                                       photo=data['photo'],
                                       body=data['body']
                                       )
            name = ''.join(('photo_', str(post.id), '.webp'))
            post.photo_mod.save(name=name,
                                content=ContentFile(buffer.getvalue()),
                                save=False
                                )
            post.save()
            return redirect('create')


class ViewTop3List(generics.ListAPIView):
    '''
    Returns a list of top 3 posts
    '''
    queryset = Post.objects.order_by('-views', 'created_at')[:3]
    serializer_class = ViewTop3Serializer


class GetUserEmailsList(APIView):
    def get(self, request):
        """юзер - mail"""
        queryset = Post.objects.all().select_related('author')
        emails = {user.author.username: user.author.email for user in queryset}
        return Response(emails)



# class GetUserGenreList(APIView):
#     def get(self, request):
#         queryset = Genre.objects.prefetch_related("publications")
#         dc = {}
#         for query in queryset:
#             for el in query.publications.values():
#                 dc.setdefault(query.title, []).append(el["title"])
#
#         return Response(dc)



class GetUserGenreList(APIView):
    def get(self, request):
        """жанры - соостветстветствующие посты!!!"""
        dc = {}
        queryset = Genre.objects.prefetch_related("publications")
        for ganre in queryset:
            posts = [post.title for post in ganre.publications.all()]
            dc.setdefault(ganre.title, posts)

        return Response(dc)


class GetUsersGenres(APIView):
    def get(self, request):
        """жанры - соостветстветствующие посты - текущего юзера"""
        user = request.user
        dc = {}
        queryset = Genre.objects.prefetch_related("publications")
        for ganre in queryset:
            posts = [post.title for post in ganre.publications.filter(
                author=user)
                     ]
            dc.setdefault(ganre.title, posts)

        return Response(dc)


