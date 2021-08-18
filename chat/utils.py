from channels.db import database_sync_to_async
from django.shortcuts import get_object_or_404

from chat.models import Dialog, Message, User
from friend.models import Friend


@database_sync_to_async
def get_user_by_username(username):
    user = get_object_or_404(User, username=username)
    return user


@database_sync_to_async
def get_friend_status(user, friend):
    """ Return friend status whether :friend: in :user: friend list """
    return Friend.friend_objects.are_friends(user, friend)


@database_sync_to_async
def save_dialog_message(user, friend, message):
    """ Create message object and add it to user-friend and friend-user dialogs """
    user_friend_dialog = Dialog.objects.get(user1=user, user2=friend)
    friend_user_dialog = Dialog.objects.get(user2=user, user1=friend)

    message = Message.objects.create(author=user, message=message)
    message.dialogs.add(user_friend_dialog, friend_user_dialog)
    message.save()


def get_group_name(user, friend):
    if user.pk < friend.pk:
        group = f'{user.pk}-{friend.pk}'
    else:
        group = f'{friend.pk}-{user.pk}'
    return f'chat_{group}'
