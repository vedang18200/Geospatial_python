# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class HeatmapConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "heatmap_group"
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive heatmap data from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_data = text_data_json['data']

        # Broadcast the heatmap data to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_heatmap_data',
                'data': new_data
            }
        )

    # Receive message from room group
    async def send_heatmap_data(self, event):
        new_data = event['data']

        # Send data to WebSocket
        await self.send(text_data=json.dumps({
            'data': new_data
        }))
