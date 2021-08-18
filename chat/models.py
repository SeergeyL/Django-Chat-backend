from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Dialog(models.Model):
    """
    Stores information about the participants in the dialog.
    """
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dialogs')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user1} with {self.user2}'


class Message(models.Model):
    """
    The same message can refer to several dialogs.
    This allow user to store own message history or delete the dialog without affecting
    other user message history.
    """
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    dialogs = models.ManyToManyField(Dialog, related_name='messages')
    message = models.CharField(max_length=600)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author}: {self.message:.15s}'



