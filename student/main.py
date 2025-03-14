import time

from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.lang import Builder


import sys
import os

# Automatically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from database.stores import sdata
import sqlite3 as sql
from helper import KV, sigin
from admin.check import Check
import socket
from student import videoShow

Window.size = (305, 480)


class projectAppp(MDApp):

    def change_screen(self, name):
        screen_manager.current = name

    def checkDb(self):
        try:
            sdata.learner()
            con = sql.connect('learnerapp.db')
            cur = con.cursor()
            get_st = ("SELECT * FROM student")
            cur.execute(get_st)
            result = cur.fetchall()
            con.commit()
            con.close()
            return result
        except:
            pass

    def build(self):
        global screen_manager
        screen_manager = ScreenManager()
        data = self.checkDb()
        if data:
            self.signin = Builder.load_string(sigin)
            screen_manager.add_widget(self.signin)
        else:
            self.login = Builder.load_string(KV)
            screen_manager.add_widget(self.login)

        return screen_manager

    def anim(self, widget):
        anim = Animation(pos_hint={"center_y": 1.06})
        anim.start(widget)

    def anim1(self, widget):
        anim = Animation(duration=1.5, pos_hint={"center_y": .85})
        anim.start(widget)

    def icons(self, widget):
        anim = Animation(duration=1.5, pos_hint={"center_y": .8})
        anim += Animation(pos_hint={"center_y": .85})
        anim.start(widget)

    def text(self, widget):
        anim = Animation(opacity=0, duration=2)
        anim += Animation(opacity=1)
        anim.start(widget)

    def comServer(self):
        email = self.login.ids.email.text
        if email == '':
            print('Fill in the blank boxes')

        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host_name = socket.gethostname()
            host_p = socket.gethostbyname(host_name)

            while True:
                try:
                    s.connect((host_p, 9998))
                    message = 'student'
                    s.send(bytes(message, 'utf-8'))
                    time.sleep(1)
                    s.send(bytes(email, 'utf-8'))
                    time.sleep(1)
                    server = s.recv(1024).decode('utf-8')
                    s.close()
                    if server == 'Exists':
                        return email
                    elif server == 'Error':
                        print('Please enter the correct class group')
                except:
                    pass


    def getData(self):
        reg = self.login.ids.reg.text
        pas1 = self.login.ids.pas1.text
        pas2 = self.login.ids.pas2.text

        regn = Check.isReg(reg)
        em = self.comServer()
        if pas1 != pas2:
            print('Password mismatch')
        elif len(pas1) < 6:
            print('Password must be 6 characters long')
        else:
            if em and regn:
                sdata.learner()
                con = sql.connect('learnerapp.db')
                cur = con.cursor()
                sql1 = ("INSERT INTO student VALUES (?,?,?)")
                cur.execute(sql1, [em, regn, pas1])
                con.commit()
                con.close()
                print('Account created successfully')
            else:
                print("account not created, try again")

    def signIn(self):
        self.reg = self.signin.ids.reg.text
        pas1 = self.signin.ids.pas1.text
        regn = Check.isReg(self.reg)

        sdata.learner()
        con = sql.connect('learnerapp.db')
        cur = con.cursor()
        get_st = ("SELECT Class_Group FROM student WHERE RegNo =? AND password = ?")
        cur.execute(get_st, [regn, pas1])
        result = cur.fetchone()
        if result:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = socket.gethostbyname(socket.gethostname())
            s.connect((host, 9998))
            message = 'signed_student'
            s.send(bytes(message, 'utf-8'))
            time.sleep(1)
            msg2 = str(result[0])
            s.send(bytes(msg2, 'utf-8'))
            from student import testReceiver
        else:
            print('invalid data')
        con.commit()
        con.close()

    def veryFicationData(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 9998))
        while True:
            message = self.reg
            s.send(message.encode())
            print("N", s.recv(1024).decode())
            break
        s.close()


if __name__ == "__main__":
    app = projectAppp()
    app.run()
