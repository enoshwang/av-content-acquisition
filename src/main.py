import pyaudio
import wave
import threading
import queue

g_quit = False
g_audio_queue = queue.Queue()

class AudioOutput(object):
    def __init__(self):
        pass
    def wav_output(self):
        global g_quit
        global g_audio_queue

        wf = wave.open("test.wav", 'wb')

        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)

        while not g_quit:
            try:
                data = g_audio_queue.get(timeout=0.1)
                wf.writeframes(data)
                print(f"Wrote audio data size: {len(data)}")
            except queue.Empty:
                continue

        wf.close()

class AudioCapture(object):
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=16000):
        self.format = format
        self.channels = channels
        self.rate = rate
    def capture_audio_from_mic(self):
        global g_quit
        global g_audio_queue

        pa = pyaudio.PyAudio()
        chunk = int(self.rate * 0.01)
        stream = pa.open(format=self.format, channels=self.channels, 
                     rate=self.rate, input=True, frames_per_buffer=chunk)
        while True:
            if g_quit:
                break
            data = stream.read(chunk)
            g_audio_queue.put(data)
            print(f"Recorded audio data size: {len(data)}")

        stream.stop_stream()
        stream.close()
        pa.terminate()
def main():
    # 音频获取
    audio_capture = AudioCapture()
    audio_capture_thread = threading.Thread(target=audio_capture.capture_audio_from_mic)
    audio_capture_thread.start()

    # 音频输出
    audio_output = AudioOutput()
    audio_output.wav_output()

if __name__ == '__main__':
    main()