from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


User = get_user_model()


class FriendManager(models.Manager):

    def add_friend(self, user, friend):
        """ Add friend """

        if user == friend:
            raise ValidationError('You cant be friend with yourself.')

        if self.are_friends(user, friend):
            raise ValidationError('This user is already in your friend list')

        if FriendRequest.objects.filter(user=user, friend=friend).exists():
            raise ValidationError('Friend request has already been sent.')

        if FriendRequest.objects.filter(user=friend, friend=user).exists():
            raise ValidationError(
                'This user has already sent friend request.'
            )

        request = FriendRequest.objects.create(user=user, friend=friend)

        return request

    def delete_friend(self, user, friend):
        """ Delete friend """

        if self.are_friends(user, friend):
            Friend.objects.get(user=user).friends.remove(friend)
        else:
            raise ValidationError('This user is not in your friend list')

    def are_friends(self, user, friend):
        """ Check if two users are friends """

        return friend in Friend.objects.get_or_create(user=user)[0].friends.all()


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    objects = models.Manager()
    friend_objects = FriendManager()

    def __str__(self):
        return f'{self.user}'


class FriendRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')

    def accept(self):
        """
        Accept friend request
        """
        Friend.objects.get_or_create(user=self.user)[0].friends.add(self.friend)
        Friend.objects.get_or_create(user=self.friend)[0].friends.add(self.user)

        self.delete()

    def reject(self):
        """
        Reject the friend request
        """
        self.delete()

    def __str__(self):
        return f'{self.user}:{self.friend}'
