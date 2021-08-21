import pytest
from django.contrib.auth.models import User


@pytest.fixture
def new_user_factory(db):
    def create_user(username):
        user = User.objects.create_user(
            username=username
        )
        return user

    return create_user


@pytest.fixture
def user1(db, new_user_factory):
    return new_user_factory('user_1')


@pytest.fixture
def user2(db, new_user_factory):
    return new_user_factory('user_2')
