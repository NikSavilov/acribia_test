import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class EventConsumer(WebsocketConsumer):
	def connect(self):
		self.key = self.scope['url_route']['kwargs']['key']
		async_to_sync(self.channel_layer.group_add)(
			self.key,
			self.channel_name
		)
		self.accept()

	def disconnect(self, code):
		async_to_sync(self.channel_layer.group_discard)(
			self.key,
			self.channel_name
		)

	def channel_message(self, event):
		self.send(text_data=json.dumps(event))
