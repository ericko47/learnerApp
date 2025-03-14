
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 500)
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
Window.clearcolor = (230/255, 230/255, 1, 1)

#Builder.load_file('office.kv')
class masterscreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def validateAdmin(self):
        user = self.ids.vc_user.text
        password = self.ids.vc_pass.text
        if user == 'admin' and password == 'Admin':
            from admin import Openserver

class office(App):
    def build(self):
        self.title = 'SCHOOL MANAGEMENT'
        return masterscreen()


if __name__ == '__main__':
    office().run()
