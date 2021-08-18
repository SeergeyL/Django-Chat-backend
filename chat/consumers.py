from channels.generic.websocket import AsyncJsonWebsocketConsumer

from chat.constants import MESSAGE_SEND
from chat.utils import get_user_by_username, get_friend_status, get_group_name, save_dialog_message


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            username = self.scope['url_route']['kwargs'].get('username', None)
            self.friend = await get_user_by_username(username)

            friend_status = await get_friend_status(self.scope['user'], self.friend)
            if friend_status:
                self.group_name = get_group_name(self.scope['user'], self.friend)
                await self.channel_layer.group_add(self.group_name, self.channel_name)
                await self.accept()
            else:
                await self.close()

    async def disconnect(self, code):
        if not self.scope['user'].is_anonymous:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        command = content.get('command', None)

        if command == 'MESSAGE:SEND':
            message = content.get('message', '')
            await self.send_dialog_message(message)

    async def send_dialog_message(self, message):
        await save_dialog_message(self.scope['user'], self.friend, message)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        await self.send_json(
            {
                'msg_type': MESSAGE_SEND,
                'message': event['message']
            }
        )
