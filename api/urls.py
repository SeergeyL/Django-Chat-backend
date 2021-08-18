from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()

router.register('me/friends',
                views.FriendViewSet,
                basename='friends')

router.register('me/friend_requests',
                views.FriendRequestViewSet,
                basename='friend-requests')

router.register('me/sent_friend_requests',
                views.SentFriendRequestViewSet,
                basename='sent-friend-request')

urlpatterns = [
    path('me/', views.UserInfo.as_view()),
    path('users/', views.UserList.as_view()),
    path('dialogs/', views.DialogAPIView.as_view()),
    path('dialogs/<int:dialog_id>/messages/', views.MessageAPIView.as_view()),
    path('dialogs/<int:dialog_id>/messages/<int:message_id>/', views.MessageDetailAPIView.as_view()),
    path('register/', views.UserRegister.as_view()),
    path('api-token-auth/', obtain_auth_token),
]

urlpatterns += router.urls
