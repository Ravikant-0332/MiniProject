import json
import random
import os
import wave
import io
from channels.generic.websocket import WebsocketConsumer

class AudioStream(WebsocketConsumer):
	def connect(self):
		self.accept()

	def disconnect(self, close_code):
		self.close()

	def receive(self, text_data=None, bytes_data=None):
		
		# print(type(bytes_data))
		# print(bytes_data)
		# print(os.path.join('path', 'to', 'save', 'audio', 'file.wav'))

		# print(os.listdir())
		# print(os.getcwd())

		audio_file = io.BytesIO(bytes_data)

		channels = 1
		sample_width = 2
		frame_rate = 44100
		frame_count = len(bytes_data) // (channels*sample_width)

		# file_path = os.path.join('audiostream','stream.wav')
		file_path = os.getcwd()+'/stream.wav'
		with wave.open(file_path, 'wb') as file:
			file.setparams((channels, sample_width, frame_rate, frame_count, 'NONE', 'not compressed'))
			file.writeframes(audio_file.getvalue())

		self.send(text_data=json.dumps({
			'result': chr(random.randrange(1,255))
		}))
		self.close()

	def receive_binary(self, content):
		self.send(text_data=json.dump({'result':chr(random.randrange(1,255))}))

