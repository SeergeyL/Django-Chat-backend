from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from chat.models import Message, Dialog
from friend.models import FriendRequest, User


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'error': 'Password fields doesnt match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'first_name', 'last_name', 'email']


class FriendRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['pk', 'user', 'friend']


class IncomingFriendRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FriendRequest
        fields = ['pk', 'user']


class OutcomingFriendRequestSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = ['pk', 'user']

    def get_user(self, obj):
        return UserSerializer(obj.friend).data


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Message
        fields = ['pk', 'author', 'message', 'time']


class DialogSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    friend = serializers.SerializerMethodField()

    class Meta:
        model = Dialog
        fields = ['pk', 'user', 'friend', 'active', 'last_message']

    def get_last_message(self, obj):
        return MessageSerializer(obj.messages.order_by('-time').first()).data

    def get_user(self, obj):
        return obj.user1.username

    def get_friend(self, obj):
        return obj.user2.username

