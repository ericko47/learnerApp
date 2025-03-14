import cv2, imutils, time, numpy as np
import queue, os, pickle, struct
import threading, wave, pyaudio
import socket
import base64


class videoDistributor():
    # shows the video to the students
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.host_ip = ''
        self.port = 9998
        self.q = queue.Queue(maxsize=10)
        self.BUFF_SIZE = 65536
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.filename = "../lecturer/final_files/principles.mp4"
        self.vid = cv2.VideoCapture(self.filename)
        self.FPS = self.vid.get(cv2.CAP_PROP_FPS)
        print(self.FPS)
        self.BREAK = False

    def lectureShow(self):

        com = 'ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}'.format(self.filename, 'temp.wav')
        os.system(com)

    def vidStream(self):
        # video treame uses port 9998
        print('video stream started')
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(host_name)
        socket_adrr = (self.host_ip, self.port)
        self.server_socket.bind(socket_adrr)
        print('Listening at:', socket_adrr)
        print(self.FPS)
        TS = 1 / self.FPS
        print(TS)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)

        while True:
            msg, client_addr = self.server_socket.recvfrom(self.BUFF_SIZE)
            print("Got connection from:", client_addr)
            WITH = 400
            while (self.vid.isOpened()):
                _, frame = self.vid.read()
                frame = imutils.resize(frame, WITH)
                encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                message = base64.b64encode(buffer)
                self.server_socket.sendto(message, client_addr)
                if cnt == frames_to_count:
                    try:
                        fps = (frames_to_count / (time.time() - st))
                        st = time.time()
                        cnt = 0
                        if fps > self.FPS:
                            TS += 0.001
                        elif fps < self.FPS:
                            TS -= 0.001
                        else:
                            pass
                    except:
                        pass
                cnt += 1
                cv2.imshow('transmitting', frame)
                key = cv2.waitKey(100) & 0xFF
                if key == ord('q'):
                    self.server_socket.close()
                    break
                if cnt == frames_to_count:
                    try:
                        fps = round(frames_to_count / (time.time() - st))
                        st = time.time()
                        cnt = 0
                    except:
                        pass
                cnt += 1

    def start(self):
        thrVideo = threading.Thread(target=self.vidStream())
        thrVideo.start()


class audioDistributor():
    def audio_stream(self):
        # audio stream uses port 9997
        s = socket.socket()
        self.port = 9998
        self.host_ip = socket.gethostbyname(socket.gethostname())
        s.bind((self.host_ip, self.port-1))
        s.listen(5)
        CHUNK = 1024
        wf = wave.open("temp.wav", 'rb')
        p = pyaudio.PyAudio()
        print("listening at:", (self.host_ip, self.port-1))
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                        rate=wf.getframerate(), input=True, frames_per_buffer=CHUNK)
        client, addr = s.accept()
        while True:
            if client:
                while True:
                    data = wf.readframes(CHUNK)
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client.sendall(message)

    def start(self):
        trdAudio = threading.Thread(target=self.audio_stream())
        trdAudio.start()


def sendVideo():
    global trdAudio
    global thrVideo
    thrVideo = videoDistributor()
    trdAudio = audioDistributor()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(videoDistributor().lectureShow())
        executor.submit(trdAudio.start())
        executor.submit(thrVideo.start())

def start_video_recording(filename):
    global trdAudio
    trdAudio = audioDistributor()
    trdAudio.start()
    return filename


def start_audio_recording(filename):
    global thrVideo
    thrVideo = videoDistributor()
    thrVideo.start()
    return filename

class stdData():
    @staticmethod
    # Checks for the reg number in the system
    def cnServer():
        sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_p = socket.gethostbyname(host_name)
        port = 9999
        host_address = (host_p, port)
        sever_socket.bind(host_address)
        sever_socket.listen(5)
        c, adrr = sever_socket.accept()
        while True:
            reg = sever_socket.recv(1024).decode()
            print("S", reg)
            sms = "performing Checks... please wait"
            sever_socket.send(sms.encode())
            break
        print("connectios ")
        sever_socket.close()


class LecSentVideos():
    @staticmethod
    def RecLecVideo():
        # uses port 9999
        sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_p = socket.gethostbyname(host_name)
        port = 9999
        host_address = (host_p, port)
        sever_socket.bind(host_address)
        sever_socket.listen(5)
        n = 0
        filename = 'try.mp4'

        while True:
            print('listenning')
            conn, addr = sever_socket.accept()
            try:
                print('reading bytes')
                buffer = conn.recv(4 * 1024)
                print('buffering')
                with open("video.mp4", "wb") as video:
                    n += 1
                    i = 0
                    while buffer:
                        video.write(buffer)
                        i += 1
                        buffer = conn.recv(4 * 1024)
                print('done')
                conn.close()
            except KeyboardInterrupt:
                if conn:
                    conn.close()
                break
        sever_socket.close()


if __name__ == "__main__":
    # LecSentVideos().RecLecVideo()
    # stdData().cnServer()
    #videoDistributor().lectureShow()
    sendVideo()
