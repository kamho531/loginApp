# -*- coding: utf-8 -*-
"""
Created on Sat May 15 21:33:17 2021

@author: Kam
"""

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty
from kivymd.uix.dialog import MDDialog
from kivy.core.window import Window
from database import DataBase

Window.size = (350, 600)


class LoginScreen(Screen):
    pass  
      


class DetailScreen(Screen):
    name_label = ObjectProperty(None)
    created_on_label = ObjectProperty(None)
    email_label = ObjectProperty(None)
    current = ""
    
    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.ids.name_label.text = "Account Name: " + name
        self.ids.email_label.text = "Email: " + self.current
        self.ids.created_on_label.text = "Created On: " + created


class CreateScreen(Screen):
    pass


def invalidLogin():
    dialog = MDDialog(title='Invalid username or password',
                  size_hint=(0.5, 0.2), 
                  )
    dialog.open()


def invalidForm():
    dialog = MDDialog(title='Please fill in all inputs with valid information.',
                  #content=MDLabel(text='Please fill in all inputs with valid information.'),
                  size_hint=(0.6, 0.2),
                  )

    dialog.open()



    


db = DataBase("users.txt")

# Create the screen manager
sm = ScreenManager()
sm.add_widget(LoginScreen(name='login'))
sm.add_widget(DetailScreen(name='detail'))
sm.add_widget(CreateScreen(name='create'))



#sample color palette:
#"Read", "Pink", "Purple", "DeepPurple",
#"Indigo", "Blue", "LightBlue", "Cyan",
#"Teal", "Green", "LightGreen", "Lime",
#"Yellow", "Amber", "Orange", "DeepOrange",
#"Brown", "Gray", "BlueGray"
class MainApp(MDApp):
    
    dialog = ObjectProperty(None)
        
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        return Builder.load_file('login.kv')   

    def loginBtn(self):
        if db.validate(self.root.get_screen('login').ids.un.text, self.root.get_screen('login').ids.pw.text):
            DetailScreen.current = self.root.get_screen('login').ids.un.text
            self.createBtn()
            self.root.current = "detail"
            self.root.transition.direction = "right"
        else:
            invalidLogin()
            self.createBtn()
            
    
    def createBtn(self):
        self.root.get_screen('login').ids.un.text = ""
        self.root.get_screen('login').ids.pw.text = ""

    def clear(self):
        self.root.get_screen('create').ids.email_txt.text = ""
        self.root.get_screen('create').ids.password_txt.text = ""
        self.root.get_screen('create').ids.name_txt.text = ""


    def submit(self):
        if self.root.get_screen('create').ids.name_txt.text != "" and self.root.get_screen('create').ids.email_txt.text != "" and self.root.get_screen('create').ids.email_txt.text.count("@") == 1 and self.root.get_screen('create').ids.email_txt.text.count(".") > 0:
            if self.root.get_screen('create').ids.password_txt.text != "" and len(self.root.get_screen('create').ids.password_txt.text) >= 8:
                db.add_user(self.root.get_screen('create').ids.email_txt.text, self.root.get_screen('create').ids.password_txt.text, self.root.get_screen('create').ids.name_txt.text)
                self.root.current = "login"
                self.root.transition.direction = 'down'
                self.createBtn()
                self.clear()

            else:
                invalidForm()
               
        else:
            invalidForm()
            


    
    
    
MainApp().run()