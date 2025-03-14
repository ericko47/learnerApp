import socket, cv2, pickle, struct
import imutils, numpy as np, time, os
import base64
import threading, wave, pyaudio


class classON():
    def __init__(self):
        self.message = b'Hello'
        self.port = 9998
        self.hostname = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.hostname)
        self.socket_ddr = (self.host_ip,(self.port))
        self.BUFF_SIZE = 65536
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.BREAK = False
        self.width = 2

    def recve(self):
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)
        print(self.host_ip)
        self.client_socket.sendto(self.message, (self.host_ip, self.port))

    def videoStream(self):
        print('student video stream started')
        #self.socket_ddr = (self.host_ip, (self.port))
        self.client_socket.connect(self.socket_ddr)
        cv2.namedWindow('Receiving')
        cv2.moveWindow('Receiving', 10, 10)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            packet, _ = self.client_socket.recvfrom(self.BUFF_SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)

            frame = cv2.imdecode(npdata, 1)
            cv2.imshow('Receiving', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.client_socket.close()
                os._exit(1)
                break
            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st))
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1
        self.client_socket.close()
        cv2.destroyAllWindows()

    def start1(self):
        t1 = threading.Thread(target=self.videoStream())
        t1.start()

    def audioStream(self):
        p = pyaudio.PyAudio()
        CHUNK = 1024
        stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True, frames_per_buffer=CHUNK)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_ddr = (self.host_ip,(self.port)-1)
        print('sever listning at:', self.socket_ddr)
        self.client_socket.connect(self.socket_ddr)
        print("Client connected to:",self.socket_ddr)
        data = b''
        payload_size = struct.calcsize("Q")
        while True:
            try:
                while len(data) < payload_size:
                    packet = self.client_socket.recv(4*1024)
                    if not packet:
                        break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]
                while len(data) < msg_size:
                    data += self.client_socket.recv(4*1024)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                stream.write(frame)
            except:
                break
        self.client_socket.close()
        print('audio closed', self.BREAK)
        os._exit(1)

    def start2(self):
        t2 = threading.Thread(target=self.audioStream())
        t2.start()

    def runClient(self):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executer:
            executer.submit(self.recve())
            #executer.submit(self.start2())
            executer.submit(self.start1())

    @staticmethod
    def starClass():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_p = socket.gethostbyname(host_name)
        port = 9999
        client_socket.connect((host_p, port))
        data = b""
        payload_size = struct.calcsize("Q")
        print("waiting for connection")
        while True:
            print("Connected")
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet: break
                data += packet
            packed_ms_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_ms_size)[0]

            while len(data) < msg_size:
                data = client_socket.recv(4 * 1024)
            fram_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(fram_data)
            cv2.imshow("Receiving Lecture fro The School Server", frame)
            if not frame:
                break
        client_socket.close()


if __name__ == '__main__':
    classON().runClient()
    #classON().starClass()

