import json
import random
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        nickname = self.generate_random_nickname()
        self.nickname = nickname
        
        uid = self.generate_user_id()
        self.user_id = uid

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Send the nickname and user ID to the new peer
        await self.accept()
        await self.send_user_info()

        # send info about new peer in the room to everyone
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'system.message',
                'data': {
                    'subtype': 'new_user_joined',
                    'nickname': nickname
                }
            }
        )

        print(f"NEW PEER JOINING with nickname: {self.nickname}, user ID: {self.user_id}")

    async def disconnect(self, close_code):
        # Leave room group
        print(f"PEER DISCONNECTING: {self.nickname}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(f"SOME DATA RECEIVED {text_data_json}")

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'text_data_json': text_data_json,
                'nickname': self.nickname,
                'user_id': self.user_id
            }
        )

    # only to one user
    async def send_user_info(self):
        await self.send(text_data=json.dumps({
            'type': 'chat.info',
            'nickname': self.nickname,
            'userId': self.user_id,
        }))

    def generate_random_nickname(self):
        adjectives = ['Clever', 'Witty', 'Brave', 'Adventurous', 'Cheerful']
        nouns = ['Explorer', 'Dreamer', 'Pioneer', 'Voyager', 'Optimist']
        return f"{random.choice(adjectives)}_{random.choice(nouns)}"

    def generate_user_id(self):
        user_id_prefix = 'USER'
        random_characters = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789') for _ in range(28))
        return f"{user_id_prefix}{random_characters}"

    
    # layer functions !! sent to everyone !!
    async def chat_message(self, event):
        print("DOING CHAT MSG")
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': event['text_data_json']['message'],
            'nickname': event['nickname'],
            'user_id': event['user_id']
        }))
    
    # message for sending game / system informations 
    async def system_message(self, event):
        print("DOING SYSTEM MESSAGE")
        await self.send(text_data=json.dumps({
            'type': 'system.message',
            'data': event['data']
        }))
