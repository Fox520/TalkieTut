from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
Config.set('graphics', 'multisamples', '0') 
from kivy.utils import get_color_from_hex
############
import socket,threading
global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1";port = 5005;
#######
global name
name = "Kiran"

Builder.load_string("""
#:import get_color_from_hex __main__.get_color_from_hex

<Chat>:
    GridLayout:
        rows: 2
        
        GridLayout:
            cols: 1
            rows: 0
            ScrollView:
                size: self.size
                do_scroll_x: False
                Label:
                    id: msg_log
                    text_size: self.width,None
                    size_hint_y: None
                    height: self.texture_size[1]
                    font_size: root.height / 20

        BoxLayout:
            size_hint_y: None
            height: 40
            spacing: 15

            canvas:
                Color:
                    rgba: (0.746,0.8,0.86,1)
                Rectangle:
                    pos: self.pos
                    size: self.size
            TextInput:
                id: message
                hint_text: "Type here"
                multiline: False
                on_text_validate: root.send_message(message.text)
""")

class Chat(Screen):
    global s
    def __init__(self,**kwargs):
        super(Chat,self).__init__(**kwargs)
        self.msg_log = self.ids["msg_log"]
        
    def on_enter(self):
        s.connect((host,port))
        welcome = s.recv(512)
        self.msg_log.text += str(welcome + "\n")
        threading.Thread(target=self.handle_messages).start()

    def send_message(self,to_send_out):
        try:
            s.send(name+" - "+to_send_out)
        except Exception as e:
            print "Error sending: ",e
    def handle_messages(self):
        while True:
            try:
                data = s.recv(1024)
                self.msg_log.text += data + "\n"
            except Exception as e:
                print e

class  Talkie(App):
    def build(self):
        return sm

sm = ScreenManager()

sm.add_widget(Chat(name="main_screen"))

if __name__ == "__main__":
    Talkie().run()
