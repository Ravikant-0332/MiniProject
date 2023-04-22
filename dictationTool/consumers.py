import json
import random

from channels.generic.websocket import WebsocketConsumer

class AudioStream(WebsocketConsumer):
	def connect(self):
		self.accept()

	def disconnect(self, close_code):
		self.close()

	def receive(self, text_data):
		text_data_json = json.loads(text_data)
		audioStream = text_data_json['audioStream']
		# try:
        #     # Convert blob stream to required audio stream
		# 	result = "success"
		# except Exception as e:
		# 	result = "failure"
        # result = random.randrange(1,255)

		self.send(text_data=json.dumps({
			'result': chr(random.randrange(1,255))
		}))

