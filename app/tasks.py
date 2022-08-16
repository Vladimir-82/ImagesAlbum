from django.core.mail import send_mail

from ImagesAlbum.celery import app
from .models import Post


@app.task
def send_view_count_report():
    '''Sends a message to the top 3 users with the most views'''
    queryset = Post.objects.order_by('-views', 'created_at')[:3]
    users = [user.author.email for user in queryset]
    send_mail(
        'You are in the top 3 of our album!',
        'Congratulations! You are in the top 3 of our album Keep it up!',
        'from@sever_album.com',
        users,
        fail_silently=False,
    )
