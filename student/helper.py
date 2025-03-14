
KV = """
MDScreen:
    name : "signin"
    on_enter:
        app.anim(back)
        app.anim1(back1)
        app.text(label)
        app.icons(icon)
    MDFloatLayout:
        MDFloatLayout:
            id: back
            size_hint_y: .4
            pos_hint:{"center_y": 0.8}
            radius: [0,0,0,40]
            canvas:
                Color:
                    rgb:(0.404, 0.227, 0.718, 1)
                Rectangle:
                    size: self.size
                    pos : self.pos
        MDFloatLayout:
            id: back1
            size_hint_y: .4
            pos_hint:{"center_y": 1.8}
            radius: [0,0,0,40]
            canvas:
                Color:
                    rgb:(0.404, 0.227, 0.718, 1)
                Ellipse:
                    size: self.size
                    pos : self.pos
        MDIconButton:
            id:icon
            icon:"account-circle"                            
            pos_hint:{"center_x":.5 , "center_y": .8}
            user_font_size: "60sp"
            theme_text_color: "Custom"
            text_color:(0.85, 0.85, 0.85, 1)
        MDLabel:
            id:label
            text: f"[font=Arial]SignUp page[/font]"
            markup:True
            pos_hint:{"center_y": .75}
            halign: "center"
            theme_text_color: "Custom"
            text_color:(1,1,1, 1)
            font_style: "H5"
            opacity: 0
        MDTextField:
            id:email
            hint_text:"Group format(BICTGroup017)"
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .56}
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
            on_text_validate:
                reg.focus = True
        MDTextField:
            id:reg
            hint_text:"Enter your ReG No."
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .46}
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
            on_text_validate:
                pas1.focus = True
                app.comServer()
        MDTextField:
            id:pas1
            hint_text:"Enter your password"
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .36}
            password: True
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
            on_text_validate:
                pas2.focus = True
        MDTextField:
            id:pas2
            hint_text:"Confirm password"
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .26}
            #current_hint_text_color: 0,0,0,1
            password:True
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
        MDRaisedButton:
            text: "SignUp"
            size_hint_x: .8
            bold:True
            pos_hint:{"center_x":.5 , "center_y": .14}
            md_bg_color:(0.404, 0.227, 0.718,1)
            on_release:app.getData()
"""
sigin = """
MDScreen:
    name : "login"
    on_enter:
        app.anim(back)
        app.anim1(back1)
        app.icons(icon)
        app.text(label)
    MDFloatLayout:
        MDFloatLayout:
            id: back
            size_hint_y: .4
            pos_hint:{"center_y": 0.8}
            radius: [0,0,0,40]
            canvas:
                Color:
                    rgb:(0.404, 0.227, 0.718, 1)
                Rectangle:
                    size: self.size
                    pos : self.pos
        MDFloatLayout:
            id: back1
            size_hint_y: .4
            pos_hint:{"center_y": 1.8}
            radius: [0,0,0,40]
            canvas:
                Color:
                    rgb:(0.404, 0.227, 0.718, 1)
                Ellipse:
                    size: self.size
                    pos : self.pos
        MDIconButton:
            id:icon
            icon:"account-circle"                            
            pos_hint:{"center_x":.5 , "center_y": .8}
            user_font_size: "60sp"
            theme_text_color: "Custom"
            text_color:(0.85, 0.85, 0.85, 1)
        MDLabel:
            id:label
            text: f"[font=Arial]SignIn page[/font]"
            markup:True
            pos_hint:{"center_y": .75}
            halign: "center"
            theme_text_color: "Custom"
            text_color:(1,1,1, 1)
            font_style: "H5"
            opacity: 0
        MDTextField:
            id:reg
            hint_text:"Enter your ReG No."
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .52}
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
            focus:True
            on_text_validate:pas1.focus = True
        MDTextField:
            id:pas1
            hint_text:"Enter your password"
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .40}
            password: True
            color_mode: "custom"
            line_color_focus: (0.404, 0.227, 0.718,1)
        MDRaisedButton:
            text: "SignIn"
            size_hint_x: .8
            pos_hint:{"center_x":.5 , "center_y": .28}
            md_bg_color:(0.404, 0.227, 0.718,1)
            on_release:app.signIn()
        MDTextButton:
            text: "forgot password?"
            pos_hint:{"center_x":.5 , "center_y": .16}
            theme_text_color: "Custom"
            text_color:(0.404, 0.227, 0.718,1)
            #custom_color:(0.85, 0.85, 0.85, 1)


"""