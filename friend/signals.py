from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from chat.models import Dialog
from friend.models import Friend, User


@receiver(m2m_changed, sender=Friend.friends.through)
def create_user_dialog(sender, instance, action, pk_set, **kwargs):
    """
    Create user-friend dialog
    """
    if action == 'post_add':
        friend_pk = pk_set.pop()
        friend = User.objects.get(pk=friend_pk)
        Dialog.objects.get_or_create(user1=instance.user, user2=friend)


@receiver(m2m_changed, sender=Friend.friends.through)
def delete_user_dialog(sender, instance, action, pk_set, **kwargs):
    """
    Set dialog attribute active to false
    """
    if action == 'post_remove':
        friend_pk = pk_set.pop()
        friend = User.objects.get(pk=friend_pk)
        dialog = Dialog.objects.get(user1=instance.user, user2=friend)
        dialog.active = False
        dialog.save()
