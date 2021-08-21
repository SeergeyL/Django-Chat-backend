import pytest

from friend.models import Friend, FriendRequest


@pytest.mark.django_db
def test_add_friend_accept(user1, user2):
    Friend.friend_objects.add_friend(user1, user2)
    qs = FriendRequest.objects.get(user=user1, friend=user2)

    assert qs, "При добавлении в друзья не создаётся FriendRequest"

    qs.accept()
    qs = FriendRequest.objects.filter(user=user1, friend=user2)

    assert not qs.exists(), "При принятия запроса в друзья FriendRequest не был удалён"

    count = user1.friends.count()

    assert count == 1, "Добавленный пользователь отсутствует в списке друзей у user1"

    count = user2.friends.count()

    assert count == 1, "Пользователь не отображается в списке друзей у user2"


@pytest.mark.django_db
def test_add_friend_reject(user1, user2):
    qs = Friend.friend_objects.add_friend(user1, user2)
    qs.reject()
    qs = FriendRequest.objects.filter(user=user1, friend=user2)

    assert not qs.exists(), "После отклонения запроса объект FriendRequest не был удалён"

    count = user1.friends.count()

    assert count == 0, "После отклонения запроса пользователь был добавлен в друзья"

    count = user2.friends.count()

    assert count == 0, "После отклонения запроса пользователь был добавлен в друзья"


@pytest.mark.django_db
def test_delete_friend(user1, user2):
    qs = Friend.friend_objects.add_friend(user1, user2)

    qs.accept()

    Friend.friend_objects.delete_friend(user1, user2)

    count = user1.friends.count()

    assert count == 0, "Пользователь не был удалён из списка друзей"

    count = user2.friends.count()

    assert count == 0, "Пользователь не был удалён из списка друзей"


@pytest.mark.django_db
def test_are_friends(user1, user2):
    qs = Friend.friend_objects.add_friend(user1, user2)
    qs.accept()

    status = Friend.friend_objects.are_friends(user1, user2)

    assert status, "Пользователь в списке друзей, но отображается неверный статус"

    status = Friend.friend_objects.are_friends(user2, user1)

    assert status, "Пользователь в списке друзей, но отображается неверный статус"




