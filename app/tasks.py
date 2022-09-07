from django.core.mail import send_mail

from ImagesAlbum.celery import app
from .models import Post
from .utils import Curent_User


@app.task
def send_view_count_report():
    '''
    Sends a message to the top 3 users with the most views
    '''
    top = Post.objects.order_by('-views', 'created_at')[:3]
    users = [user.author.email for user in top]
    send_mail(
        'You are in the top 3 of our album!',
        'Congratulations! You entered the top 3 at the end of the month! '
        'Keep it up!',
        'from@sever_album.com',
        users,
        fail_silently=False,
    )
@app.task
def send_join_lieve_top():
    '''Sends a message lieve or (and) join top 3'''
    top = Post.objects.order_by('-views', 'created_at')[:3]
    top_users = [user.author.email for user in top]
    left_list_users = list(set(Curent_User.curent_users_list) - set(top_users))
    join_list_users = list(set(top_users) - set(Curent_User.curent_users_list))
    if join_list_users:
        send_mail(
            'You have been joining top 3 of our album!',
            'You have been joining top 3 of our album now! Grate!',
            'from@sever_album.com',
            join_list_users,
            fail_silently=False,
        )
    if left_list_users:
        send_mail(
            'You left top 3 of our album!',
            'You left top 3 of our album now! Good luck!',
            'from@sever_album.com',
            left_list_users,
            fail_silently=False,
        )
    Curent_User.curent_users_list = join_list_users + \
                                    list(set(top_users) &
                                         set(Curent_User.curent_users_list))
