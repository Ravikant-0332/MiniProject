import json
from channels.generic.websocket import WebsocketConsumer
from .static.dictationTool.asr.live_asr_custom import LiveWav2Vec2
from queue import Queue
import numpy as np

class AudioStream(WebsocketConsumer):

	def connect(self):
		self.accept()
		# self.asr_output_queue = Queue()
		# self.asr_input_queue = Queue()
		# self.wave2vec_asr = Wave2Vec2Inference(
		# 	"anjulRajendraSharma/wav2vec2-indian-english", 
		# 	use_lm_if_possible=True
		# )

		self.asr = LiveWav2Vec2("anjulRajendraSharma/wav2vec2-indian-english")
		# try:
		# 	self.asr.stop()
		# except:
		# 	pass
		self.asr.start()

		try:
			while True:
				text,sample_length,inference_time, confidence= self.asr.get_last_text()
				# print(f'{text} : [{confidence}]')
				# self.send(text)
				if confidence > 0.85:
					self.send(text_data = json.dumps({
						'result' : text
					}))

		except KeyboardInterrupt:
			self.asr.stop()
			exit()

	def disconnect(self, close_code):
		self.asr.stop()
		self.close()

	def receive(self, text_data=None, bytes_data=None):
		if bytes_data!=None:
			
			audio_frame = bytes_data
			if audio_frame == "close":
				self.close()

			else:
				float64_buffer = np.frombuffer(
					audio_frame, dtype=np.int16
				)/32767

				text, conf = self.wave2vec_asr.buffer_to_text(float64_buffer)
				text = text.lower()

				if text!="":
					self.send(text_data=json.dumps({
						'result': text
					}))
