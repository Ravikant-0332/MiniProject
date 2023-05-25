# from wav2vec2_inference import Wave2Vec2Inference
from .wav2vec2_inference import Wave2Vec2Inference
import numpy as np
import threading
import copy
import time
from sys import exit
import contextvars
from queue import  Queue


class LiveWav2Vec2():
    exit_event = threading.Event()
    def __init__(self, model_name, device_name="default"):
        self.model_name = model_name
        self.device_name = device_name
        self.frames = b''

    def stop(self):
        """stop the asr process"""
        LiveWav2Vec2.exit_event.set()
        self.asr_input_queue.put("close")
        print("asr stopped")

    def start(self):
        """start the asr process"""
        self.asr_output_queue = Queue()
        self.asr_input_queue = Queue()
        self.asr_process = threading.Thread(target=LiveWav2Vec2.asr_process, args=(
            self.model_name, self.asr_input_queue, self.asr_output_queue,))
        self.asr_process.start()
        time.sleep(5)  # start vad after asr model is loaded
        self.vad_process = threading.Thread(target=LiveWav2Vec2.vad_process, args=(
            self.device_name, self.asr_input_queue, self.frames))
        self.vad_process.start()

    def vad_process(device_name, asr_input_queue, frames):        
        if len(frames) > 1:
            asr_input_queue.put(frames)

    def asr_process(model_name, in_queue, output_queue):
        wave2vec_asr = Wave2Vec2Inference(model_name, use_lm_if_possible=True)

        print("\nlistening to your voice\n")
        while True:
            audio_frames = in_queue.get()
            if audio_frames == "close":
                break

            float64_buffer = np.frombuffer(
                audio_frames, dtype=np.int16) / 32767
            start = time.perf_counter()
            text, confidence = wave2vec_asr.buffer_to_text(float64_buffer)
            text = text.lower()
            inference_time = time.perf_counter()-start
            sample_length = len(float64_buffer) / 16000  # length in sec
            if text != "":
                output_queue.put([text,sample_length,inference_time,confidence])

    def get_last_text(self):
        """returns the text, sample length and inference time in seconds."""
        return self.asr_output_queue.get()
    
    def getText(self,frames):
        self.frames = frames
        text,sample_length,inference_time, confidence= self.get_last_text()
        return text


    

if __name__ == "__main__":
    print("my ASR Live ASR")

    asr = LiveWav2Vec2("anjulRajendraSharma/wav2vec2-indian-english")

    asr.start()

    # try:
    #     while True:
    #         text,sample_length,inference_time, confidence= asr.get_last_text()
    #         print(f"{sample_length:.3f}s\t{inference_time:.3f}s\t{confidence}\t{text}")

    # except KeyboardInterrupt:
    #     asr.stop()
    #     exit()
    print(asr.getText(asr.frames))
    asr.stop()
    exit()
