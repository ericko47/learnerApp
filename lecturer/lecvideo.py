from __future__ import print_function, division

import base64
import pickle
import socket
import struct
import queue as q
import time
import wave

import cv2
import imutils
import plyer
import pyautogui
from kivy import Config
from kivy.app import App
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.lang import Builder


import sys
import os
import shutil
from pathlib import Path

# Automatically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from admin.check import Check

Config.set('graphics', 'width', 380)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'resizable', False)
from lecturer import recordCam, recordSc
from kivy.uix.popup import Popup
from kivy.core.window import Window
from lecturer import client

Builder.load_file("lectureVideos.kv")
import threading
import time
import subprocess

global vars
global cam
global scren
global name
global close
global stt
cam = False
vars = False
scren = False
name = ""

global un
global gr
global tm
un = ""
gr = ""
tm = ""


class Mypopup(Popup):
    def __init__(self, base_dir=None, **kwargs):
        super().__init__(**kwargs)  # Call Popup's constructor

        if base_dir is None:
            base_dir = Path.home() / "LearnerApp_Temp"  # Set a default path

        self.base_dir = Path(base_dir).resolve()
        self.temp_dir = self.base_dir / "temp_files"
        self.final_dir = self.base_dir / "final_files"
        self.video_file = self.temp_dir / "video.mp4"
        self.learner_videos_dir = Path.home() / "LearnerApp_Videos"  # Cross-platform


    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.video = ""

    def getVidname(self):
        global name
        vid = self.ids.vid_name
        name = vid.text.strip()
        self.startRecording()
        self.dismiss()

    def startRecording(self, base_dir):
        global vars
        vars = True

        # Ensure UI is initialized before recording starts
        lay = mylayout(base_dir=base_dir)
        lay.manageInterface()
        Window.minimize()
        print("Recording started...")

        try:
            # Initialize Video Recorder
            print("Initializing video recording...")
            video_thread = recordSc.VideoRecorder(fps=30, output_file=str(base_dir / "output.mp4"))

            if not isinstance(video_thread, recordSc.VideoRecorder):
                print("Error: VideoRecorder did not initialize correctly!")
                return

            # Initialize Audio Recorder
            print("Initializing audio recording...")
            audio_thread = recordSc.AudioRecorder(str(base_dir / "audio.wav"))

            if not isinstance(audio_thread, recordSc.AudioRecorder):
                print("Error: AudioRecorder did not initialize correctly!")
                return

            # Store threads in self for stopping later
            self.video_thread = video_thread
            self.audio_thread = audio_thread

            print("Video and Audio threads initialized successfully!")

            # Start recording in a separate thread
            recording_thread = threading.Thread(target=recordSc.start_AVrecording, args=(video_thread, audio_thread))
            recording_thread.start()

        except Exception as e:
            print(f"Error starting recording: {e}")
            self.video_thread = None
            self.audio_thread = None

    
    def check_ffmpeg_installed(self):
        """Checks if FFmpeg is installed."""
        try:
            subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return True
        except FileNotFoundError:
            print("Error: FFmpeg is not installed. Please install it to continue.")
            return False

    def create_videos_list(self):
        """Creates a videos.txt file with a list of MP4 files in temp_files."""
        video_list = [f"file '{vid.name}'" for vid in self.temp_dir.glob("*.mp4")]

        if video_list:
            with open(self.video_list_file, 'w') as f:
                f.write("\n".join(video_list))
            print("videos.txt created successfully.")
        else:
            print("No videos found to list.")

    def concat_videos(self, output_name):
        """Concatenates video files using FFmpeg."""
        if not self.check_ffmpeg_installed():
            return
        
        self.create_videos_list()  # Ensure videos.txt is up to date
        output_path = self.learner_videos_dir / f"{output_name}.mp4"
        self.learner_videos_dir.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists

        try:
            cmd = ["ffmpeg","-f", "concat","-safe", "0","-i", str(self.video_list_file),"-c", "copy",str(output_path)            ]
            subprocess.run(cmd, check=True)
            print(f"Video concatenation successful: {output_path}")

            # Cleanup temp video files after processing
            for vid in self.temp_dir.glob("*.mp4"):
                vid.unlink()
                print(f"Deleted: {vid}")

        except subprocess.CalledProcessError as e:
            print(f"Error during video concatenation: {e}")

    def rename_vid(self, old_name, new_name):
        """Renames a video file and moves it to the final directory."""
        old_path = self.temp_dir / f"{old_name}.mp4"
        new_path = self.final_dir / f"{new_name}.mp4"
        
        self.final_dir.mkdir(parents=True, exist_ok=True)  # Ensure final directory exists

        if old_path.exists():
            old_path.rename(new_path)
            print(f"Renamed and moved video to: {new_path}")
        else:
            print("Error: Video file does not exist.")


# Example Usage
# if __name__ == "__main__":
#     processor = VideoProcessor(base_dir="C:/Users/Bella/PycharmProjects/learnerApp/lecturer")
#     processor.rename_vid("new_video_name")
#     processor.concat_videos("new_video_name")
#     processor.file_handler()


    # def renameVid(self):
    #     path_dir = "C:\\Users\\Bella\\PycharmProjects\\learnerApp\\lecturer\\temp_files\\video.mp4"
    #     #print(os.listdir(path_dir))
    #     try:
    #         if path_dir:
    #             os.rename(path_dir, './final_files/' + name + '.mp4')
    #         else:
    #             pass
    #     except:
    #         pass

    # def conCat(self):
    #     global name
    #     os.chdir("C:\\Users\\Bella\\PycharmProjects\\learnerApp\\lecturer\\temp_files")
    #     filename = "C:/Users/Bella/PycharmProjects/learnerApp/lecturer/temp_files"
    #     # cmd = "ffmpeg -f concat -safe 0 -i videos.txt -c copy " + filename
    #     # subprocess.call(cmd, shell=True)
    #     try:
    #         if os.path.isdir("C:\\LearnerApp_Videos"):
    #             pass
    #         else:
    #             os.mkdir("C:\\LearnerApp_Videos")
    #     except:
    #         pass
    #     nname = 'C:\\LearnerApp_Videos\\' + name + '.mp4'
    #     print(os.listdir(filename))
    #     # os.rename(filename, nname)
    #     os.rename('../temp_files/', './final_files/' + name + '.mp4')
    #     fl = os.listdir("../temp_files/")
    #     for vid in fl:
    #         if vid.endswith('.mp4'):
    #             os.remove('../temp_files/' + vid)

    # @staticmethod
    # def fileHandler():
    #     fl = os.listdir("./temp_files/")
    #     data = ""
    #     for elem in fl:
    #         if elem.endswith('.mp4'):
    #             data = data + "file " + elem + "\n"
    #     handle = open("./temp_files/videos.txt", 'w')
    #     handle.write(data)
    #     handle.close()


class mylayout(Widget):
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video = ""
        self.group = ''
        self.info = self.ids.err
        self.report = self.ids.rep
        self.tim = ""
        self.grp = ""

    def setError(self, elem, error):
        if not error:
            error = ""
        elem.text = error

    def setInfo(self, wid, info):
        if not info:
            error = ""
        wid.text = info

    def manageInterface(self):
        self.ids.close.disabled = False
        self.ids.stt.disabled = False
        return False, False
    
    def stopScreenWrapper(self):
        """Wrapper function to call stopScreen with necessary arguments."""
        video_name = "recorded_video"

        print("Attempting to stop recording...")

        # Debug print: Check if attributes exist
        print(f"Has 'video_thread'? {'video_thread' in self.__dict__}")
        print(f"Has 'audio_thread'? {'audio_thread' in self.__dict__}")

        # Ensure threads exist
        if not hasattr(self, 'video_thread') or not hasattr(self, 'audio_thread'):
            print("Error: No recording threads found!")
            return

        # Ensure threads are properly initialized
        if self.video_thread is None or self.audio_thread is None:
            print("Error: Recording threads were not initialized properly!")
            return

        # Ensure recording is actually running
        if not getattr(self.video_thread, "open", False) or not getattr(self.audio_thread, "open", False):
            print("Error: Recording was not started properly or has already stopped!")
            return

        print("Stopping recording...")
        self.stopScreen(self.video_thread, self.audio_thread, video_name)


    def stopScreen(self):
        pop = Mypopup()
        global cam
        global vars
        if cam:
            pyautogui.press("q")
        threading.Thread(target=recordSc.stop_AVrecording())
        # threading.Thread(target=pop.fileHandler())
        while threading.active_count() > 1:
            time.sleep(1)
        recordSc.file_manager()
        pop.renameVid()
        cam = False
        vars = False

    def camStart(self):
        global cam
        cam = True
        if vars:
            cam = threading.Thread(target=recordCam.VideoCamera().record())
            cam.start()
        else:
            return "Please start recording before you start Camera"

    def checkTime(self):
        tm = self.ids.lec_time
        tim = tm.text.strip()
        format_list = ('%d.%m.%Y %H:%M', '%m.%d.%Y %H:%M', '%Y.%m.%d %H:%M',
                       '%Y-%m-%d %H:%M', '%d-%m-%Y %H:%M', '%m-%d-%Y %H:%M',
                       '%m/%d/%Y %H:%M', '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M')
        for fmt in format_list:
            try:
                time.strptime(tim, fmt)
                return tim
            except:
                pass

    def checkInputs(self):
        elem = self.info
        unit = self.ids.unit
        unitn = unit.text.strip()
        grp = self.validateCourse()
        tim = self.checkTime()
        if not tim:
            err = 'Invalid time format'
            self.setError(elem, err)
        elif not grp:
            err = 'Invalid group format'
            self.setError(elem, err)
        else:
            return tim, unitn, grp

    def validateCourse(self):
        group = self.ids.gr
        self.course = group.text.strip().upper()
        clsgrp = ['BICTGROUP017','BICTGROUP018', 'BICTGROUP019', 'BICTGROUP020', 'BICTGROUP021', 'GEOGROUP018', 'GEOGROUP019',
                  'GEOGROUP020', 'GEOGROUP021', 'BOTAGROUP018', 'BOTAGROUP019', 'BOTAGROUP020', 'BOTAGROUP021',
                  'BIO CHEMGROUP018', 'BIO CHEMGROUP019', 'BIO CHEMGROUP020', 'BIO CHEMGROUP021', 'STATGROUP018',
                  'STATGROUP019', 'STATGROUP020', 'STATGROUP021', 'ENVI SCIGROUP018', 'ENVI SCIGROUP019',
                  'ENVI SCIGROUP020', 'ENVI SCIGROUP021', 'NRMGROUP018', 'NRMGROUP019', 'NRMGROUP020', 'NRMGROUP021',
                  'AGECGROUP018', 'AGECGROUP019', 'AGECGROUP020', 'AGECGROUP021', 'BIO MEDGROUP018', 'BIO MEDGROUP019',
                  'BIO MEDGROUP020', 'BIO MEDGROUP021', 'PHYSICSGROUP018', 'PHYSICSGROUP019', 'PHYSICSGROUP020',
                  'PHYSICSGROUP021', 'BIOLOGYGROUP018', 'BIOLOGYGROUP019', 'BIOLOGYGROUP020', 'BIOLOGYGROUP021',
                  'MATHEMATICSGROUP018', 'MATHEMATICSGROUP019', 'MATHEMATICSGROUP020', 'MATHEMATICSGROUP021',
                  'BCOMGROUP018', 'BCOMGROUP019', 'BCOMGROUP020', 'BCOMGROUP021', 'AGBMGROUP018', 'AGBMGROUP019',
                  'AGBMGROUP020', 'AGBMGROUP021', 'ECON STATGROUP018', 'ECON STATGROUP019', 'ECON STATGROUP020',
                  'ECON STATGROUP021', 'ECON SOCIGROUP018', 'ECON SOCIGROUP019', 'ECON SOCIGROUP020',
                  'ECON SOCIGROUP021', 'ECON HISTGROUP018', 'ECON HISTGROUP019', 'ECON HISTGROUP020',
                  'ECON HISTGROUP021', 'COMPSGROUP018', 'COMPSGROUP019', 'COMPSGROUP020', 'COMPSGROUP021',
                  'DICTGROUP018', 'DICTGROUP019', 'DICTGROUP020', 'DICTGROUP021']

        for i in clsgrp:
            if i == self.course:
                return i

    def fileChooser(self):
        wid = self.report
        global name
        try:
            if name == '':
                selected_file = plyer.filechooser.open_file(select=True)
                name = str(selected_file[0])
            elif IndexError:
                pass
            elif KeyboardInterrupt:
                os.abort()
            else:
                inf = 'You already have a recorded video, just click connect'
                self.setInfo(wid, inf)
        except:
            pass

    def connection(self):
        global name
        elem = self.info
        wid = self.report
        con = False
        now = time.time()
        waiting_time = 120
        if name == '':
            inf = 'You have not recorded any video or selected one'
            self.setInfo(wid, inf)
            time.sleep(1)
            self.fileChooser()
        else:
            stop_time = now + waiting_time
            vid_info = self.checkInputs()
            try:
                tim = vid_info[0]
                unit = vid_info[1]
                classg = vid_info[2]
            except:
                err = 'Invalid group format'
                self.setError(elem, err)
                return
            host_name = socket.gethostname()
            host_p = socket.gethostbyname(host_name)
            port = 9998
            socadr = (host_p, port)
            print(socadr)
            message = 'hello server'

            while now < stop_time:
                while not con:
                    try:
                        check = client_socket.connect(socadr)
                        inf = 'connected'
                        self.setInfo(wid, inf)
                        client_socket.sendall(bytes(message, 'utf-8'))
                        msg = client_socket.recv(1024)
                        info = msg.decode("utf-8")
                        self.ids.con.disabled = True
                        if info == 'ready':
                            client_socket.send(bytes(str(tim), 'utf-8'))
                            time.sleep(1)
                            client_socket.send(bytes(str(unit), 'utf-8'))
                            time.sleep(1)
                            client_socket.send(bytes(str(classg), 'utf-8'))
                            time.sleep(1)
                            s = client_socket.recv(1024)
                            s_msg = s.decode('utf-8')
                            if s_msg == 'send video':
                                self.ids.sd_btn.disabled = False
                                time.sleep(2)
                                inf = 'sending...'
                                self.setInfo(wid, inf)
                                t1 = threading.Thread(target=self.sending())
                                t1.start()
                                inf = 'sent'
                                self.setInfo(wid, inf)

                    except:
                        pass

    def sending(self):
        global name
        if name.endswith('.mp4'):
            pass
        else:
            name = './final_files/' + name + '.mp4'
            print(os.getcwd())
        with open(name, "rb") as video:
            buffer = video.read()
            client_socket.sendall(buffer)
            time.sleep(2)
        print("sent")
        client_socket.close()

    def liveClass(self):
        vid_info = self.checkInputs()
        print(vid_info)
        BUFF_SIZE = 65536
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print(host_ip)
        port = 9699
        socket_address = (host_ip, port)
        server_socket.bind(socket_address)
        print('Listening at:', socket_address)

        vid = cv2.VideoCapture(1)

        def generate_video():

            WIDTH = 400
            while (vid.isOpened()):
                try:
                    _, frame = vid.read()
                    frame = imutils.resize(frame, width=WIDTH)
                    q.put(frame)
                except:
                    os._exit(1)
            print('Player closed')
            BREAK = True
            vid.release()

        def send_video():
            fps, st, frames_to_count, cnt = (0, 0, 1, 0)
            cv2.namedWindow('TRANSMITTING VIDEO')
            cv2.moveWindow('TRANSMITTING VIDEO', 10, 30)
            while True:
                msg, client_addr = server_socket.recvfrom(BUFF_SIZE)
                print('GOT connection from ', client_addr)
                WIDTH = 400
                while (True):
                    frame = q.get()
                    encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    message = base64.b64encode(buffer)
                    server_socket.sendto(message, client_addr)
                    frame = cv2.putText(frame, 'FPS: ' + str(round(fps, 1)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                        (0, 0, 255), 2)

                    cv2.imshow('TRANSMITTING VIDEO', frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        os._exit(1)
                        TS = False
                        break

        def send_message():
            s = socket.socket()
            s.bind((host_ip, (port - 1)))
            s.listen(5)
            client_socket, addr = s.accept()
            cnt = 0
            while True:
                if client_socket:
                    while True:
                        print('SERVER TEXT SENDING:')
                        data = input()
                        a = pickle.dumps(data)
                        message = struct.pack("Q", len(a)) + a
                        client_socket.sendall(message)

                        cnt += 1

        def get_message():
            s = socket.socket()
            s.bind((host_ip, (port - 2)))
            s.listen(5)
            client_socket, addr = s.accept()
            data = b""
            payload_size = struct.calcsize("Q")

            while True:
                try:
                    while len(data) < payload_size:
                        packet = client_socket.recv(4 * 1024)  # 4K
                        if not packet: break
                        data += packet
                    packed_msg_size = data[:payload_size]
                    data = data[payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]
                    while len(data) < msg_size:
                        data += client_socket.recv(4 * 1024)
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = pickle.loads(frame_data)
                    print('', end='\n')
                    print('CLIENT TEXT RECEIVED:', frame, end='\n')
                    print('SERVER TEXT SENDING:')


                except Exception as e:
                    print(e)
                    pass

            client_socket.close()
            print('Audio closed')

        t1 = threading.Thread(target=send_message, args=())
        t2 = threading.Thread(target=get_message, args=())
        t3 = threading.Thread(target=generate_video, args=())
        t4 = threading.Thread(target=send_video, args=())
        t1.start()
        t2.start()
        t3.start()
        t4.start()


class lectureVideosApp(App):
    def build(self):
        return mylayout()


if __name__ == '__main__':
    lectureVideosApp().run()
