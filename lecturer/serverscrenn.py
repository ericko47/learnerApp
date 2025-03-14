import socket
import numpy as np
import cv2, pickle, struct
import pyautogui


class serviceP():
    @staticmethod
    # live server the students
    def lecServer():
        sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_p = socket.gethostbyname(host_name) # this gets the ip addess
        print(host_p)
        port = 9999
        host_address = (host_p, port)
        sever_socket.bind(host_address)
        sever_socket.listen(5)
        print('listenig')
        while True:
            client, addrs = sever_socket.accept()
            print('Connected')
            if client:
                vid = pyautogui.screenshot()
                while vid:
                    vid_fr = np.array(vid)
                    vid_fr = cv2.cvtColor(vid_fr, cv2.COLOR_BGR2RGB)
                    a = pickle.dumps(vid_fr)
                    message = struct.pack('Q', len(a)) + a
                    client.sendall(message)
                    cv2.imshow("Sender", vid_fr)
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client.close()
