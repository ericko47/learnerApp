import socket
import time
from socket import SHUT_WR


class sendsVidToServer:
    @staticmethod
    def sendLecVideo():
        con = True

        #use port 9999
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = socket.gethostname()
        host_p = socket.gethostbyname(host_name)
        port = 9999
        client_socket.connect((host_p, port))
        print("sending")
        with open("try.mp4", "rb") as video:
            buffer = video.read()
            client_socket.sendall(buffer)
        print("sent")
        client_socket.close()


if __name__ == "__main__":
    sendsVidToServer().sendLecVideo()
