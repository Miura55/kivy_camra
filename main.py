# -*- coding: utf-8 -*-

import kivy

from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label

import time
import cv2
import numpy as np

class CaptureApp(App):
    def build(self):
        self.img1 = Image(source='logoCL.jpg')   #creates an image where we will insert the image of the camera
        label1= Label(text="Webcam motion")  #upper label
        label2= Label(text="www.cadernodelaboratorio.com.br") #lower label
        layout = BoxLayout(orientation='vertical')  #here we create a vertical layout
        layout.add_widget(label1)   #we insert the widgets in the order that we want to display them on the screen
        layout.add_widget(self.img1)
        layout.add_widget(label2)

        self.capture = cv2.VideoCapture(0)  #we created a video capture object. We joined the first camera
        ret, frame = self.capture.read() #we created a frame with this image
        Clock.schedule_interval(self.atualizaImagem, 1.0/30.0)   #we create a clock to refresh the image every 1/320 of a second
        return layout

    def atualizaImagem(self, dt):
        ret, frame = self.capture.read()   #captures an image from the camera

        buf1 = cv2.flip(frame, 0)   #reverse to not stay upside down
        buf = buf1.tostring() # converts to texture

        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        timestr = time.strftime("%Y%m%d_%H%M%S")
        path = '/Users/KokiMiura/Documents/python/application/camera/flame/IMG_{}.png'.format(timestr)
        cv2.imwrite(path, frame)

        self.img1.texture = texture1 #presents the image

if __name__ == '__main__':
    CaptureApp().run()
