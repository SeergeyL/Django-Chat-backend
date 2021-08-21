import pytest

from chat.models import Dialog
from friend.models import Friend


@pytest.mark.django_db
def test_dialog_creation(user1, user2):
    status = Dialog.objects.filter(user1=user1, user2=user2).exists()

    assert not status, "Пользователи никогда не были друзьями, диалога не должно быть в базе данных"

    qs = Friend.friend_objects.add_friend(user1, user2)
    qs.accept()

    status = Dialog.objects.filter(user1=user1, user2=user2).exists()

    assert status, "После добавления в друзья должен быть создан диалог у пользователя"

    status = Dialog.objects.filter(user1=user2, user2=user1).exists()

    assert status, "После добавления в друзья должен быть создан диалог у второго пользователя"


@pytest.mark.django_db
def test_dialog_deletion(user1, user2):
    qs = Friend.friend_objects.add_friend(user1, user2)
    qs.accept()
    Friend.friend_objects.delete_friend(user1, user2)

    dialog = Dialog.objects.get(user1=user1, user2=user2)

    assert not dialog.active, "После удаления из друзей атрибут active должен быть False"

    dialog = Dialog.objects.get(user1=user2, user2=user1)

    assert not dialog.active, "После удаления из друзей атрибут active должен быть False"



