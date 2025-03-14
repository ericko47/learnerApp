import time

import cv2
import filetype as filetype
from kivy.config import Config
import sys
import os

# Automatically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from check import Check
from database.stores import dbs

#Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 500)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.animation import Animation
from kivy.core.window import Window
import sqlite3 as sql

Window.clearcolor = (1, 1, 1, 1)


# Builder.load_file('manager.kv')


class managerScreen(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = ""
        self.pic_name = ""
        self.email = ""
        self.yob = 0
        self.idNO = ""
        self.phone = ""
        self.gender = ""
        self.regNO = ""
        self.course = ""
        self.dep = ""
        self.fac = ""
        self.group = ''
        self.r_info = self.ids.left_info
        self.l_info = self.ids.right_info

    def set_gender(self, value):
        self.gender = value

    def anim(self, widget):
        nim = Animation(pos_hint={'center_x': 0.5, 'top': 1})
        nim.start(widget)

    def setError(self, elem, err):
        if not err:
            err = ""
        elem.text = err

    def validateEmail(self):
        e = self.ids.em
        self.email = e.text
        return Check.isEmail(self.email)

    def validateId(self):
        i = self.ids.idn
        self.idNO = i.text.strip()
        return Check.isId(self.idNO)

    def validatePhone(self):
        p = self.ids.ph
        self.phone = p.text.strip()
        return Check.isPhone(self.phone)

    def validateYob(self):
        y = self.ids.yob
        self.yob = y.text.strip()
        return Check.isYob(self.yob)

    def validateName(self):
        st = self.ids.nm
        self.name = st.text.strip()
        return Check.isName(self.name, 6)

    def validateReg(self):
        regn = self.ids.reg
        self.regNO = regn.text.strip()
        res = Check.isReg(self.regNO)
        year = res[-3:]
        self.group = "Group" + year
        localtime = time.localtime(time.time())
        now = str(localtime.tm_year)
        reNow = now[-3:]
        if int(year) > int(reNow):
            return "Invalid Year of study"
        return True

    def validateCourse(self):
        cos = self.ids.cor
        self.course = cos.text.strip().upper()

        facultie = ['School of Business and Economics', 'School of Science and applied Technology']

        res = Check.isCourse(self.course)
        if res == False:
            return "The course you entered is not valid"

        for i in facultie:
            if i is facultie:
                self.course = res
                return True
        self.dep = res[1]
        self.fac = res[0]
        self.course = res[2]
        if self.validateName() == self.validateEmail() == self.validatePhone() == self.validateReg() == True:
            self.ids.camera.disabled = False
        else:
            self.ids.camera.disabled = True
        return True

    def validateGender(self):
        if self.gender == "":
            return "Please select your gender to proceed"
        return Check.isGender(self.gender)

    def cameraOn(self):
        face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        webcam = cv2.VideoCapture(0)
        color = (128 / 255, 128 / 255, 128 / 255, 1)
        cropped = ''

        while True:
            success, frame = webcam.read()
            resized = cv2.resize(frame, None, fx=.5, fy=.5)
            grayimg = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            face = face_data.detectMultiScale(grayimg, scaleFactor=1.3, minNeighbors=5)
            for (x, y, w, h) in face:
                cv2.rectangle(resized, (x, y), (x + w, y + h), color, 2)
                cropped = resized[y - 35:y + h + 35, x - 30: x + w + 30]
                self.validateName()
                self.validateReg()
                self.pic_name = self.name + self.regNO
                print(self.pic_name)
                cv2.imshow(self.name, cropped)
                cv2.waitKey(300)
                if self.pic_name:
                    cv2.imwrite('../imgs/student_profiles/' + self.pic_name + '.jpg', cropped)
                    cv2.imshow(self.name, self.cropped)
                    cv2.waitKey(300)
                else:
                    print('no pic name')
                    break

            cv2.waitKey(300)
            if filetype.image(cropped):
                webcam.release()
                break
        cv2.destroyAllWindows()

    def validation(self):
        print('Erick')
        res = self.validateName()
        elem = self.l_info
        if res == True:
            res = self.validateEmail()
            if res == True:
                res = self.validateYob()
                if res == True:
                    res = self.validateId()
                    if res == True:
                        res = self.validatePhone()
                        if res == True:
                            res = self.validateGender()
                            if res == True:
                                self.setError(elem, "")
                                elem = self.r_info
                                res = self.validateReg()
                                if res == True:
                                    res = self.validateCourse()
                                    if res == True:
                                        self.setError(elem, '')
                                        name = self.name
                                        email = self.email
                                        yob = self.yob
                                        idn = self.idNO
                                        phone = self.phone
                                        gen = self.gender
                                        reg = self.regNO
                                        cos = self.course
                                        department = self.dep
                                        school = self.fac
                                        group = self.group

                                        dbs.database1()
                                        con = sql.connect('school.db')
                                        cur = con.cursor()
                                        get_st = ("SELECT * FROM students WHERE Email =? AND RegNo = ?")
                                        cur.execute(get_st, [email, reg])
                                        result = cur.fetchone()
                                        if not result:
                                            sql1 = ("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?)")
                                            cur.execute(sql1,
                                                        [name, email, yob, idn, phone, gen, reg, cos, department,
                                                         school, group])
                                            res = 'The Student was registered successfully'
                                            self.setError(elem, res)
                                            self.r_info = elem
                                            # time.sleep(3)
                                        else:
                                            res = 'The Student Already Exists'
                                        self.setError(elem, res)
                                        self.r_info = elem

                                        # all database operation done here.
                                        return

            self.setError(elem, res)


class other_details(BoxLayout):
    pass


class WindowManager(ScreenManager):
    pass


class managerApp(App):
    def build(self):
        self.title = 'Student registration'

        self.windomanager = ScreenManager(transition=FallOutTransition())

        self.manager = managerScreen()
        screen = Screen(name="sr")
        screen.add_widget(self.manager)
        self.windomanager.add_widget(screen)

        self.mare_info = other_details()
        screen = Screen(name="moreinfo")
        screen.add_widget(self.mare_info)
        self.windomanager.add_widget(screen)

        return self.windomanager


if __name__ == '__main__':
    LearnerApp = managerApp()
    LearnerApp.run()
