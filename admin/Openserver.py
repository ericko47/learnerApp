import base64
import os
import pickle
import pyaudio
import queue
import shutil
import socket
# from database.stores import dbs
import sqlite3 as sql
import struct
import threading
import wave
import numpy as np
import cv2
import imutils
import time


# import tests
class dbs:
    @staticmethod
    def database1():
        con = sql.connect('school.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS students(
        Stname text NOT NULL ,
        Email text NOT NULL,
        YOB int NOT NULL,
        stid int,
        stPhone int NOT NULL,
        gender text NOT NULL,
        RegNo text NOT NULL,
        Course text NOT NULL,
        Department text NOT NULL,
        School text NOT NULL,
        Ac_Group text NOT NULL,
        Clas_Group text NOT NULL
        )
        """)
        con.commit()
        con.close()
        return

    @staticmethod
    def learners():
        con = sql.connect('learnerapp.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS student(
        Email text,
        RegNo text,
        Password text
        )
        """)
        con.commit()
        con.close()
        return

    @staticmethod
    def Class_videos():
        con = sql.connect('school.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS videos(
        Class_Time text NOT NULL,
        Video_name text NOT NULL,
        Class_Group text NOT NULL
        )
        """)
        con.commit()
        con.close()
        return

    @staticmethod
    def studentGroups():
        con = sql.connect('school.db')
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS ready_videos(
        Class_Time text NOT NULL,
        Video_name text NOT NULL,
        Class_Group text NOT NULL
            )
            """)
        con.commit()
        con.close()
        return


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = socket.gethostbyname(socket.gethostname())
port = 9998
socket_addr = (host_ip, port)
server_socket.bind(socket_addr)
server_socket.listen()
print("TCP Listens at: ", socket_addr)
q = queue.Queue(maxsize=10)

global c_tim
c_tim = ''

"""def openvideo():
    command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename, 'temp.wav')
    os.system(command)"""
def categoriseStudent(addr, client_socket):
    gr = client_socket.recv(1024).decode('utf-8')
    tim = time.time()
    dbs.database1()
    dbs.Class_videos()
    con = sql.connect('school.db')
    cur = con.cursor()
    get_st = ("SELECT Clas_Group FROM students WHERE Clas_Group =?")
    cur.execute(get_st, [gr])
    con.commit()
    result = cur.fetchone()
    #try:
    if result:
        #client_socket.send(bytes('Exists', 'utf-8'))
        get_vid = ("SELECT Class_Time,Video_name FROM videos WHERE (? - Class_Time) <= 3600 AND Class_Group =?")
        cur.execute(get_vid, [tim, gr])
        con.commit()
        result1 = cur.fetchone()
        print(result1)
        if result1:
            filename = "./temp_files/" + result1[0] + '.mp4'
            the_audio = "./temp_files/" + result1[0] + '.wav'

            BUFF_SIZE = 65536
            server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
            host = socket.gethostbyname(socket.gethostname())
            por = 9688
            socket_address = (host, por)
            server.bind(socket_address)

            vid = cv2.VideoCapture(filename)
            FPS = vid.get(cv2.CAP_PROP_FPS)
            global TS
            TS = (0.5 / FPS)
            BREAK = False
            print('FPS:', FPS, TS)
            totalNoFrames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
            durationInSeconds = float(totalNoFrames) / float(FPS)
            d = vid.get(cv2.CAP_PROP_POS_MSEC)
            print(durationInSeconds / 60, d)

            def video_stream_gen():
                WIDTH = 400
                while (vid.isOpened()):
                    try:
                        _, frame = vid.read()
                        frame = imutils.resize(frame, width=WIDTH)
                        q.put(frame)
                    except:
                        os._exit(1)
                print('Video Off')
                BREAK = True
                vid.release()

            def video_stream():
                global TS
                fps, st, frames_to_count, cnt = (0, 0, 1, 0)
                cv2.namedWindow('TRANSMITTING VIDEO')
                cv2.moveWindow('TRANSMITTING VIDEO', 10, 30)
                while True:

                    print('In video stream')
                    msg, client = server.recvfrom(BUFF_SIZE)
                    WIDTH = 800

                    while (True):
                        frame = q.get()
                        encoded, buffer = cv2.imencode('.jpeg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                        message = base64.b64encode(buffer)
                        server.sendto(message, client)
                        frame = cv2.putText(frame, 'FPS: ' + str(round(fps, 1)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                                            0.7,
                                            (0, 0, 255), 2)
                        if cnt == frames_to_count:
                            try:
                                fps = (frames_to_count / (time.time() - st))
                                st = time.time()
                                cnt = 0
                                if fps > FPS:
                                    TS += 0.001
                                elif fps < FPS:
                                    TS -= 0.001
                                else:
                                    pass
                            except:
                                pass
                        cnt += 1

                        cv2.imshow('TRANSMITTING VIDEO', frame)
                        key = cv2.waitKey(int(1000 * TS)) & 0xFF
                        if key == ord('q'):
                            os._exit(1)
                            TS = False
                            break

            def audio_stream():
                s = socket.socket()
                s.bind((host, (por - 1)))
                print('In audio stream')
                s.listen(5)
                CHUNK = 1024
                wf = wave.open(the_audio, 'rb')
                p = pyaudio.PyAudio()
                print('Listening at:', (host, (por - 1)))
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                input=True,
                                frames_per_buffer=CHUNK)

                client, add = s.accept()

                while True:
                    if client:
                        while True:
                            data = wf.readframes(CHUNK)
                            a = pickle.dumps(data)
                            message = struct.pack("Q", len(a)) + a
                            client.sendall(message)

            from concurrent.futures import ThreadPoolExecutor

            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(audio_stream)
                executor.submit(video_stream_gen)
                executor.submit(video_stream)
    else:
        client_socket.send(bytes('Error', 'utf-8'))
    #except:
        #pass
    con.close()



def recievevideoData(addr, client_socket):
    global c_tim
    try:
        print('Connected to: {}'.format(addr))
        while True:
            vid_t = client_socket.recv(1024)
            c_time = str(vid_t.decode("utf-8"))
            vid_name = client_socket.recv(1024)
            name = str(vid_name.decode("utf-8"))
            vid_data = client_socket.recv(1024)
            classg = str(vid_data.decode("utf-8"))
            time.sleep(1)
            print(c_time, name, classg)
            format_list = ['%d.%m.%Y %H:%M', '%m.%d.%Y %H:%M', '%Y.%m.%d %H:%M', '%Y-%m-%d %H:%M',
                           '%d-%m-%Y %H:%M', '%m-%d-%Y %H:%M', '%m/%d/%Y %H:%M', '%d/%m/%Y %H:%M',
                           '%m/%d/%Y %H:%M']
            epoch = ''
            now = time.time()
            for fmt in format_list:
                try:
                    epoch = int(time.mktime(time.strptime(c_time, fmt)))
                    c_tim = epoch
                    break
                except:
                    epoch = 'invalid input'
                    pass
            # dt_obj = datetime.fromtimestamp(epoch)
            if epoch == 'invalid input':
                client_socket.send(bytes('Time error: Please check on your input time'))
                client_socket.close()
            else:
                dbs.database1()
                dbs.Class_videos()
                con = sql.connect('school.db')
                cur = con.cursor()
                get_st = ("SELECT Clas_Group FROM students WHERE Clas_Group =?")
                cur.execute(get_st, [classg])
                result = cur.fetchone()
                print(result)
                if result:
                    sql1 = ("INSERT INTO videos VALUES (?,?,?)")
                    cur.execute(sql1, [epoch, name, classg])
                    con.commit()
                return True

    finally:
        pass


def receivelecVideo(addr, client_socket):
    n = 0
    global c_tim
    server_vidName = str(c_tim)
    print(server_vidName)
    try:
        if os.path.isdir("C:\\LearnerApp_Server_Videos"):
            pass
        else:
            os.mkdir("C:\\LearnerApp_Server_Videos")
    except:
        pass
    nname = 'C:\\LearnerApp_Server_Videos\\'
    nn = './temp_files/' + server_vidName + '.mp4'
    try:
        buffer = client_socket.recv(4 * 1024)
        with open(nn, "wb") as video:
            n += 1
            i = 0
            while buffer:
                video.write(buffer)
                i += 1
                buffer = client_socket.recv(4 * 1024)
        print('done')
        shutil.copy(nn, nname)
        client_socket.close()
    except KeyboardInterrupt:
        if client_socket:
            client_socket.close()


def classTimer():
    tim = time.time()
    dbs.database1()
    dbs.Class_videos()
    con = sql.connect('school.db')
    cur = con.cursor()
    get_st = ("SELECT Class_Time,Video_name FROM videos WHERE (? - Class_Time) <= 3600 ")
    cur.execute(get_st, [tim])
    con.commit()
    result = cur.fetchall()
    for clases in result:
        vid_time = clases[0]
        dif = float(tim) - float(vid_time)
        if -3590 > dif >= -3600:
            print('Alert the student that the class is about to start')
        if 0 <= dif < 5:
            try:
                clas = vid_time + '.mp4'
                clas_audio = vid_time + '.wav'
                filename = "./temp_files/" + clas
                file_audio = "./temp_files/" + clas_audio
                command = "ffmpeg -i {} -ab 160k -ac 2 -ar 44100 -vn {}".format(filename, file_audio)
                os.system(command)

            except:
                pass
    con.close()
    threading.Timer(5.0, classTimer).start()


def catStudent(addr, client_socket):
    group = client_socket.recv(1024).decode('utf-8')
    print(group)
    tim = time.time()
    dbs.database1()
    dbs.Class_videos()
    con = sql.connect('school.db')
    cur = con.cursor()
    get_st = ("SELECT Clas_Group FROM students WHERE Clas_Group =?")
    cur.execute(get_st, [group])
    con.commit()
    result = cur.fetchone()
    print(result)
    if result:
        print('inside...')
        client_socket.sendall(bytes('Exists', 'utf-8'))
        print('sent the message')
    else:
        client_socket.sendall(bytes('Error', 'utf-8'))

def liveClass():
    BUFF_SIZE = 65536

    BREAK = False
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = '192.168.1.1'  # socket.gethostbyname(host_name)
    print(host_ip)
    port = 9699
    message = b'Hello'

    client_socket.sendto(message, (host_ip, port))

    def get_message():

        # TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_address = (host_ip, port - 1)
        print('server listening at', socket_address)
        client_socket.connect(socket_address)
        print("CLIENT CONNECTED TO", socket_address)
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
                print('SERVER TEXT RECEIVED:', frame, end='\n')
                print('CLIENT TEXT SENDING:')
            except:

                break

        client_socket.close()
        print('Audio closed')
        os._exit(1)

    def send_message():

        # create socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_address = (host_ip, port - 2)
        print('server listening at', socket_address)
        client_socket.connect(socket_address)
        print("msg send CLIENT CONNECTED TO", socket_address)
        while True:
            if client_socket:
                while (True):
                    print('CLIENT TEXT SENDING:')
                    data = input()
                    a = pickle.dumps(data)
                    message = struct.pack("Q", len(a)) + a
                    client_socket.sendall(message)

    def get_video():

        cv2.namedWindow('RECEIVING VIDEO')
        cv2.moveWindow('RECEIVING VIDEO', 10, 360)
        fps, st, frames_to_count, cnt = (0, 0, 20, 0)
        while True:
            packet, _ = client_socket.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet, ' /')
            npdata = np.fromstring(data, dtype=np.uint8)

            frame = cv2.imdecode(npdata, 1)
            frame = cv2.putText(frame, 'FPS: ' + str(fps), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                client_socket.close()
                os._exit(1)
                break

            if cnt == frames_to_count:
                try:
                    fps = round(frames_to_count / (time.time() - st), 1)
                    st = time.time()
                    cnt = 0
                except:
                    pass
            cnt += 1

        client_socket.close()
        cv2.destroyAllWindows()

    t1 = threading.Thread(target=get_message, args=())
    t2 = threading.Thread(target=send_message, args=())
    t3 = threading.Thread(target=get_video, args=())
    t1.start()
    t2.start()
    t3.start()

while True:
    client_socket, addr = server_socket.accept()
    msg = client_socket.recv(1024)
    classTimer()
    info = msg.decode("utf-8")
    print(info)
    if info == 'hello server':
        client_socket.send(bytes('ready', 'utf-8'))
        thread = threading.Thread(target=recievevideoData, args=(addr, client_socket))
        thread.start()
        time.sleep(4)
        client_socket.send(bytes('send video', 'utf-8'))
        thread2 = threading.Thread(target=receivelecVideo, args=(addr, client_socket))
        thread2.start()
        print('Active lecturers', threading.active_count() - 1)

    if info == "student":
        t1 = threading.Thread(target=catStudent, args=(addr, client_socket))
        t1.start()
    if info == "signed_student":
        t3 = threading.Thread(target=categoriseStudent, args=(addr, client_socket))
        t3.start()
