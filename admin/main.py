import time

import cv2
from kivy.config import Config
from kivy.lang import Builder

import sys
import os

# Automatically add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from check import Check
from database.stores import dbs

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 500)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FallOutTransition
from kivy.animation import Animation
from kivy.core.window import Window
import sqlite3 as sql

Window.clearcolor = (1, 1, 1, 1)


# Builder.load_file('../admin/manager.kv')


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
        self.cosabr = ''
        self.classGroup = ''
        self.group = ''
        self.r_info = self.ids.left_info
        self.l_info = self.ids.right_info

    def set_gender(self, value):
        self.gender = value

    def setError(self, elem, err):
        if not err:
            err = ""
        elem.text = err

    def Clear_Form(self):
        self.ids.nm.text = ""
        self.ids.em.text = ""
        self.ids.idn.text = ""
        self.ids.ph.text = ""
        self.ids.yob.text = ""
        self.ids.reg.text = ""
        self.ids.cor.text = ""
        self.l_info.text = ""
        self.r_info.text = ""

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
        self.group = "GROUP" + year
        localtime = time.localtime(time.time())
        now = str(localtime.tm_year)
        reNow = now[-3:]
        # if int(year) > int(reNow):
        # return "Invalid Year of study"

        if self.validateCourse() == self.validateEmail() == self.validatePhone() == True:
            self.ids.camera.disabled = False
        else:
            self.ids.camera.disabled = True
        return True

    def validateCourse(self):
        cos = self.ids.cor
        self.course = cos.text.strip().upper()
        self.cosabr = self.course
        facultie = ['School of Business and Economics', 'School of Science and applied Technology']

        res = Check.isCourse(self.course)
        if res == False:
            return "The course is not valid"
        self.dep = res[1]
        self.fac = res[0]
        self.course = res[2]
        return True

    def genClassGroup(self):
        cos = self.course
        cos_abrvs = ['GEO', 'BOTA', 'BIO CHEM', 'STAT', 'ENVI SCI', 'NRM', 'AGEC', 'BIO MED', 'PHYSICS',
                     'CHEMESTRY', 'BIOLOGY', 'MATHEMATICS', 'BCOM', 'AGBM', 'ECON STAT', 'ECON SOCI',
                     'ECON HIST', 'BICT', 'COMPS', 'DICT']

        group = self.group
        for i in cos_abrvs:
            if i is cos_abrvs:
                self.cosabr = cos
                return self.cosabr
        self.classGroup = self.cosabr + group
        return self.classGroup

    def validateGender(self):
        if self.gender == "":
            return "Please select your gender to proceed"
        return Check.isGender(self.gender)

        
    def cameraOn(self):
        # Load Haar Cascade before the loop
        face_data = cv2.CascadeClassifier('/home/erick/projects/learnerApp/admin/haarcascade_frontalface_default.xml')
        
        # Open webcam
        webcam = cv2.VideoCapture(0)
        
        # Validate registration and get pic name
        self.validateReg()
        self.pic_name = self.regNO
        
        # Define rectangle color (B, G, R)
        color = (128, 128, 128)
        
        # Ensure save directory exists
        save_dir = '/home/erick/projects/learnerApp/imgs/student_profiles/'
        os.makedirs(save_dir, exist_ok=True)

        while True:
            success, frame = webcam.read()
            if not success:
                print("Failed to capture frame")
                break

            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_data.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            
            # Show video feed
            cv2.imshow('Video', frame)

            # Capture key press
            k = cv2.waitKey(1) & 0xFF
            
            # Save image when 's' is pressed
            if k == ord('s'):
                img_path = os.path.join(save_dir, self.pic_name + '.jpg')
                cv2.imwrite(img_path, frame)
                print(f"Image saved to {img_path}")
                break

            # Exit when 'q' is pressed
            elif k == ord('q'):
                break

        # Release camera and close windows
        webcam.release()
        cv2.destroyAllWindows()


    def validation(self):
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
                                res = self.validateCourse()
                                elem = self.r_info
                                if res == True:
                                    res = self.validateReg()
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
                                        classg = self.genClassGroup()

                                        dbs.database1()
                                        con = sql.connect('school.db')
                                        cur = con.cursor()
                                        get_st = ("SELECT * FROM students WHERE Email =? AND RegNo = ?")
                                        cur.execute(get_st, [email, reg])
                                        result = cur.fetchone()
                                        if not result:
                                            sql1 = ("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
                                            cur.execute(sql1,
                                                        [name, email, yob, idn, phone, gen, reg, cos, department,
                                                         school, group, classg])
                                            con.commit()
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


"""
class other_details(BoxLayout):
    pass"""


class WindowManager(ScreenManager):
    pass


class other_details(ScreenManager):
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
