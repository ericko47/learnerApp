from __future__ import print_function, division
import numpy as np
import cv2
import pyaudio
import wave
import threading
import time
import subprocess
import os
import pyautogui
from kivy.core.window import Window

import queue


# from accounts.lecvideo import Mypopup

screen_width, screen_height = Window.system_size


class VideoRecorder():
    """Video class based on openCV"""

    def __init__(self, name="temps_video.avi", sizex=screen_width, sizey=screen_height, fps=20):
        self.open = True
        self.fps = fps
        self.frameSize = (sizex, sizey)
        self.video_filename = name
        self.video_writer = cv2.VideoWriter_fourcc(*'XVID')
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        self.start_time = time.time()
        self.frame_counts = 1
        self.video_filename = ""

    def record(self):
        """Video starts being recorded"""
        timer_start = time.time()
        timer_current = 0
        fpc = 60
        while self.open:
            time_elapsed = time.time() - timer_current
            img = pyautogui.screenshot()
            if time_elapsed > 1.0 / self.fps:
                timer_current = time.time()
                vid_fr = np.array(img)
                vid_fr = cv2.cvtColor(vid_fr, cv2.COLOR_BGR2RGB)
                self.video_out.write(vid_fr)
                time.sleep(1 / self.fps)
            else:
                break

    def stop(self):
        # "Finishes the video recording therefore the thread too"
        if self.open:
            self.open = False
            self.video_out.release()
            cv2.destroyAllWindows()

    def start(self):
        video_thread = threading.Thread(target=self.record, daemon=True)
        video_thread.start()
        return video_thread


class AudioRecorder:
    def __init__(self, filename="temps_audio.wav", rate=44100, fpb=512, channels=2):
        self.open = True
        self.rate = rate
        self.frames_per_buffer = fpb
        self.channels = channels
        self.format = pyaudio.paInt16
        self.audio_filename = filename
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.frames_per_buffer)
        self.audio_frames = []
        self.audio_queue = queue.Queue()  # Queue to avoid buffer overflow

    def record(self):
        self.stream.start_stream()
        while self.open:
            try:
                data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)
                self.audio_queue.put(data)  # Store in queue
            except OSError as e:
                print(f"Audio error: {e}")

    def process_audio(self):
        while self.open:
            if not self.audio_queue.empty():
                self.audio_frames.append(self.audio_queue.get())

    def start(self):
        audio_thread = threading.Thread(target=self.record, daemon=True)
        process_thread = threading.Thread(target=self.process_audio, daemon=True)
        audio_thread.start()
        process_thread.start()
        return audio_thread, process_thread


# class AudioRecorder():
#     # "Audio class based on pyAudio and Wave"

#     def __init__(self, filename="temps_audio.wav", rate=44100, fpb=1024, channels=2):
#         self.open = True
#         self.rate = rate
#         self.frames_per_buffer = fpb
#         self.channels = channels
#         self.format = pyaudio.paInt16
#         self.audio_filename = filename
#         self.audio = pyaudio.PyAudio()
#         self.stream = self.audio.open(format=self.format,
#                                       channels=self.channels,
#                                       rate=self.rate,
#                                       input=True,
#                                       frames_per_buffer=self.frames_per_buffer)
#         self.audio_frames = []

#     def record(self):
#         # "Audio starts being recorded"
#         self.stream.start_stream()
#         while self.open:
#             data = self.stream.read(self.frames_per_buffer)
#             self.audio_frames.append(data)
#             if not self.open:
#                 break

    def stop(self):
        # "Finishes the audio recording therefore the thread too"
        if self.open:
            self.open = False
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate()
            waveFile = wave.open(self.audio_filename, 'wb')
            waveFile.setnchannels(self.channels)
            waveFile.setsampwidth(self.audio.get_sample_size(self.format))
            waveFile.setframerate(self.rate)
            waveFile.writeframes(b''.join(self.audio_frames))
            waveFile.close()

#     def start(self):
#         # "Launches the audio recording function using a thread"
#         audio_thread = threading.Thread(target=self.record)
#         audio_thread.start()
#         return audio_thread

def start_AVrecording():
    global audio_thread
    global video_thread
    audio_thread = AudioRecorder()
    audio_thread.start()
    time.sleep(0.01)
    video_thread = VideoRecorder()
    video_thread.start()


def start_video_recording(filename):
    global video_thread
    video_thread = VideoRecorder()
    video_thread.start()
    return filename


def start_audio_recording(filename):
    global audio_thread
    audio_thread = AudioRecorder()
    audio_thread.start()
    return filename


def stop_AVrecording():
    audio_thread.stop()
    frame_counts = video_thread.frame_counts
    elapsed_time = time.time() - video_thread.start_time
    recorded_fps = frame_counts / elapsed_time
    video_thread.stop()
    filename = "./temp_files/video"

    while threading.active_count() > 1:
        time.sleep(1)

    cmd = "ffmpeg -y -ac 2 -channel_layout stereo -i temps_audio.wav -i temps_video.avi -pix_fmt yuv420p -shortest " + filename + ".mp4"
    subprocess.call(cmd, shell=True)

def file_manager(filename="test"):
    local_path = os.getcwd()
    if os.path.exists(str(local_path) + "/temps_audio.wav"):
        os.remove(str(local_path) + "/temps_audio.wav")
    if os.path.exists(str(local_path) + "/temps_video.avi"):
        os.remove(str(local_path) + "/temps_video.avi")


if __name__ == '__main__':
    start_AVrecording()
    time.sleep(5)
    stop_AVrecording()
    file_manager()
