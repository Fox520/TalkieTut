#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy import Config
Config.set('graphics', 'multisamples', '0')

from kivy.utils import get_color_from_hex
import List
from List import MDList
from label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.image import AsyncImage
from navigationdrawer import NavigationDrawer

############

import socket
import threading
import json
import string
import random
from os.path import expanduser
import os
import requests
global s
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.42.11'
port = 5005

#######

global name
name = 'Kiran'
was_here = False
path_images = "."#expanduser('~\\Pictures')
avail_image_extensions = ['*.jpg', '*.png', '*.gif']  # filter
avail_image_extensions_selection = ['.jpg', '.png', '.gif']

Builder.load_string("""
#:import get_color_from_hex __main__.get_color_from_hex
#:import path_images __main__.path_images
#:import avail_image_extensions __main__.avail_image_extensions


<Chat>:
    NavigationDrawer:
        id: nav_draw
        GridLayout:
            cols: 1
            Label:
                text: "sample"
            Button:
                text: "text"
                on_release:
                    root.manager.current = "image_select_screen"
                    nav_draw.toggle_state()
        GridLayout:
            rows: 2
            
            GridLayout:
                cols: 1
                rows: 0
                canvas:
                    Color:
                        rgba: get_color_from_hex("#ffffff")  
                    Rectangle:
                        pos: self.pos
                        size: self.size
                ScrollView:
                    do_scroll_x: False
                    MDList:
                        id: ml

            GridLayout:
                size_hint_y: None
                height: 40
                spacing: 15
                rows: 1
                cols: 2

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
                TextInput:
                    id: pvt_name
                    hint_text: "name of person to pvt"
                    multiline: False

<ImageSelectScreen>:
    GridLayout:
        rows: 3
        cols: 1
        BoxLayout:
            size_hint_y: None
            Button:
                text: "Icon View"
                on_release: filechooser.view_mode = "icon"
            Button:
                text: "List View"
                on_release: filechooser.view_mode = "list"
        BoxLayout:
            canvas:
                Color:
                    rgba: get_color_from_hex("#000000")  
                Rectangle:
                    pos: self.pos
                    size: self.size
            FileChooser:
                id: filechooser
                path: path_images
                filters: avail_image_extensions
                on_selection: root.select(filechooser.selection)
                FileChooserIconLayout
                FileChooserListLayout
        BoxLayout:
            size_hint_y: None
            height: 30
            spacing: 10
            canvas:
                Color:
                    rgba: get_color_from_hex("#ffffff")  
                Rectangle:
                    pos: self.pos
                    size: self.size
            Button:
                text: "Send"
                on_release: root.send_it()
            Button:
                text: "Back"
                on_release: root.manager.current = "main_screen"


""")


class Chat(Screen):

    global s

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)
        self.ml = self.ids['ml']
        self.pvt_name = self.ids['pvt_name']

    def add_two_line(self, from_who, msg_to_add):

        self.ml.add_widget(List.TwoLineListItem(
            text=msg_to_add,
            secondary_text=from_who,
            markup=True,
            text_size=(self.width, None),
            size_hint_y=None,
            font_size=self.height / 23,
            ))

    def on_enter(self):  # only run this once, not everytime we switch back to it(main_screen)
        global was_here
        if was_here == False:
            was_here = True
            s.connect((host, port))
            welcome = s.recv(512)

            # self.msg_log.text += str(welcome + "\n")

            self.add_two_line('Admin', welcome)
            temp_template = {'name': name}
            s.send(json.dumps(temp_template))
            threading.Thread(target=self.handle_messages).start()

    def send_message(self, to_send_out):
        try:
            if self.pvt_name.text != '':
                type_msg = 'private_message'
                pvt_receiver = self.pvt_name.text
            else:
                type_msg = 'broadcast'
                pvt_receiver = ''

            template = {}
            template['msg_type'] = type_msg
            template['from'] = name
            template['msg'] = to_send_out
            template['pvt_receiver'] = pvt_receiver
            s.send(json.dumps(template))
        except Exception, e:

            print 'Error sending: ', e

    def download_file_arbi(self, url):
        local_filename = url.split('/')[-1]

        # NOTE the stream=True parameter

        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

                    # f.flush() commented by recommendation from J.F.Sebastian

        return local_filename

    def handle_image_download(self, url_img):

        # create file downloader function for arbitrary files

        print 'starting downlad'
        saved_img = self.download_file_arbi(url_img)
        self.add_two_line('self', 'File saved as ' + saved_img)
        print 'download complete'
        self.pop_image_saved(saved_img)

    def pop_image_saved(self, src):
        the_pic = AsyncImage(source=src)
        self.pop1(the_pic)

    def pop1(self, src):
        popup = Popup(title='Image loading', content=src)
        popup.open()

    def handle_messages(self):
        while True:
            try:
                data = json.loads(s.recv(1024))
                if data['msg_type'] == 'broadcast':

                    # self.msg_log.text += data["from"] + " - " + data["msg"] + "\n"

                    self.add_two_line(data['from'], data['msg'])

                if data['msg_type'] == 'image':

                    # thread it

                    threading.Thread(target=self.handle_image_download,
                            args=(data['link'], )).start()
            except Exception, e:

                print e


class A:

    # class to return the name

    def get_the_name(self):
        return name


class ImageSelectScreen(Screen):

    global s

    def select(self, filename):
        try:
            self.filename = filename[0]
            self.preview_img(self.filename)
        except Exception, e:
            print e

    def preview_img(self, src):

        # do image popup    import popup & async image later

        popup = Popup(title='Preview', content=AsyncImage(source=src))
        popup.open()

    def upload_image(
        self,
        fname,
        urlll,
        some_dict,
        ):
        with open(fname, 'rb') as f:
            files = {'testname': f}
            r = requests.post(urlll, files=files)  # import requests
        s.send(json.dumps(some_dict))
        self.remove_file(fname)  # delete the temp file

    def remove_file(self, fname):
        try:
            os.remove(fname)
            print 'temp file removed'
        except Exception, e:
            print e

    def send_it(self):

        # this is upload part

        print 'upload part'
        if len(self.filename) > 5:
            try:
                host = 'http://192.168.42.11/'
                url_for_img = host + 'man_images.php'
                url_for_img_no_php = host + 'img/'
                print 'inside'
                c_extension = os.path.splitext(self.filename)[1]  # get file extension
                if c_extension in avail_image_extensions_selection:
                    extesion = c_extension

                    # create temp file for randomness of filename

                    my_name = A().get_the_name()
                    temp_img_file = my_name + '-' \
                        + ''.join([random.choice(string.ascii_letters
                                  + string.digits) for n in xrange(7)]) \
                        + extesion
                    with open(self.filename, 'rb') as f:
                        orag = f.read()  # read image
                    with open(temp_img_file, 'wb') as fb:
                        fb.write(orag)  # write image to temp file

                    link_img = url_for_img_no_php + temp_img_file
                    some_dict = {'msg_type': 'image', 'link': link_img,
                                 'from': my_name}
                    threading.Thread(target=self.upload_image,
                            args=(temp_img_file, url_for_img,
                            some_dict)).start()
                    sm.current = 'main_screen'
            except Exception, e:
                print e


class Talkie(App):

    def build(self):
        return sm


sm = ScreenManager()

sm.add_widget(Chat(name='main_screen'))
sm.add_widget(ImageSelectScreen(name='image_select_screen'))

if __name__ == '__main__':
    Talkie().run()

            