from kivy.config import Config

Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'height', 500)
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.lang.builder import Builder


# Builder.load_file('mainClass.kv')

class studentForm(BoxLayout):
    pass


class mainClass(App):
    def build(self):
        self.title = 'student admission'
        return studentForm()


if __name__ == "__main__":
    sa = mainClass()
    sa.run()
