from collections import OrderedDict

from django.core.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from chat.models import Dialog, Message
from friend.models import Friend, FriendRequest, User


class UserRegister(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    permission_classes = [AllowAny]


class UserInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class UserList(APIView):
    """ Return the list of registered users """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.all().exclude(username=request.user.username)
        serializer = serializers.UserSerializer(users, many=True)

        # For every user add fields:
        # friend_status - whether user in friend list of request.user
        # sent_request - whether friend request was sent by user
        # get_request - whether request.user received friend request from user
        data = []
        for ordered_dict in serializer.data:
            d = dict(ordered_dict)

            user = User.objects.get(username=ordered_dict['username'])

            friend_status = Friend.friend_objects.are_friends(request.user, user)
            friend_request = FriendRequest.objects.filter(user=request.user, friend=user).exists()
            get_request = FriendRequest.objects.filter(user=user, friend=request.user).exists()

            d['friend_status'] = friend_status
            d['sent_request'] = friend_request
            d['get_request'] = get_request

            data.append(OrderedDict(d))

        return Response(data)


class FriendViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Return list of all friends """
        user, _ = Friend.objects.get_or_create(user=request.user)
        serializer = serializers.UserSerializer(user.friends.all(), many=True)
        return Response(serializer.data)

    def create(self, request):
        """ Create friend request to user """

        friend_username = request.data.get('username')
        friend = get_object_or_404(User, username=friend_username)

        try:
            friend_request = Friend.friend_objects.add_friend(request.user, friend)
        except ValidationError as exc:
            return Response({
                'error': exc
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.FriendRequestSerializer(friend_request).data)

    def destroy(self, request, pk):
        """ Delete friend from the list """

        user = get_object_or_404(User, pk=pk)
        try:
            Friend.friend_objects.delete_friend(request.user, user)
        except ValidationError as exc:
            return Response({
                'error': exc
            })
        return Response(status=status.HTTP_204_NO_CONTENT)


class FriendRequestViewSet(viewsets.ViewSet):
    """ Incoming friend requests """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Return all outcoming friend requests from user """
        qs = FriendRequest.objects.filter(friend=request.user)
        serializer = serializers.IncomingFriendRequestSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reject')
    def reject_friend_request(self, request, pk):
        qs = get_object_or_404(FriendRequest.objects.filter(friend=request.user), pk=pk)
        qs.reject()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='accept')
    def accept_friend_request(self, request, pk):
        qs = get_object_or_404(FriendRequest.objects.filter(friend=request.user), pk=pk)
        qs.accept()
        return Response(status=status.HTTP_200_OK)


class SentFriendRequestViewSet(viewsets.ViewSet):
    """ Outcoming friend requests """

    permission_classes = [IsAuthenticated]

    def list(self, request):
        """ Return all outcoming friend requests from user """
        qs = FriendRequest.objects.filter(user=request.user)
        serializer = serializers.OutcomingFriendRequestSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reject')
    def reject_friend_request(self, request, pk):
        qs = get_object_or_404(FriendRequest.objects.filter(user=request.user), pk=pk)
        qs.reject()
        return Response(status=status.HTTP_200_OK)


class DialogAPIView(ListAPIView):
    queryset = Dialog.objects.all()
    serializer_class = serializers.DialogSerializer
    permission_classes = [IsAuthenticated]


class MessageAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        dialog_id = self.kwargs.get('dialog_id')
        dialog = get_object_or_404(Dialog, pk=dialog_id)
        return dialog.messages.order_by('time')


class MessageDetailAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        dialog_id = self.kwargs.get('dialog_id')
        dialog = get_object_or_404(Dialog, pk=dialog_id)
        return dialog

    def delete(self, request, dialog_id, message_id):
        dialog = self.get_queryset()
        message = get_object_or_404(Message, pk=message_id)
        dialog.messages.remove(message)
        return Response(status=status.HTTP_204_NO_CONTENT)



