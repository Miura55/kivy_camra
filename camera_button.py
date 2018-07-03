# -*- coding: utf-8 -*-


from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.label import Label
from kivy.uix.button import Button


import cv2
import numpy as np

class CameraApp(App):

    def build(self):
        self.filtro= 0   #0 = no imagem, 1 = graus de cinza 2 = filter vermelho 3 = azul filter 4 = green filter


        self.img1 = Image()


        label1= Label(text="Experimentos com vídeo (III)",pos_hint={'x': .45, 'center_y': .98}, size_hint=(None, None))  #label superior
        label2= Label(text="www.cadernodelaboratorio.com.br",pos_hint={'x': .45, 'center_y': .92}, size_hint=(None, None)) #label inferior

        button3C=  Button(text='Normal', size_hint=(0.5,0.1))    #criamos or the world that chooses 3 cores
        button3C.bind(on_press= self.seleciona3Cores)
        buttonCinza=  Button(text='Gray', size_hint=(0.5,0.1))     #criamos or bohemian who chooses cinnamon

        buttonCinza.bind(on_press= self.selecionaCinza)
        buttonVermelho=  Button(text='Red Filter', size_hint=(0.5,0.1))     #criamos or the world that chooses a vermelho
        buttonVermelho.bind(on_press= self.filtraVermelho)
        buttonAzul=  Button(text='Blue Filter', size_hint=(0.5,0.1))     #criamos o botao que seleciona a azul
        buttonAzul.bind(on_press= self.filtraAzul)
        buttonVerde=  Button(text='Green Filter', size_hint=(0.5,0.1))     #criamos or blossom that chooses to green
        buttonVerde.bind(on_press= self.filtraVerde)


        layoutVideo= FloatLayout()
        layoutBotoes= BoxLayout(orientation= 'horizontal')  #posicionamento dos botoes

        layoutBotoes.add_widget(button3C) #acrescentamos o botao cinza numa linha horizontal
        layoutBotoes.add_widget(buttonCinza) #acrescentamos o botao cinza numa linha horizontal
        layoutBotoes.add_widget(buttonVermelho) #acrescentamos o botao vermelho na mesma linha horizontal
        layoutBotoes.add_widget(buttonAzul) #acrescentamos o botao azul na mesma  linha horizontal
        layoutBotoes.add_widget(buttonVerde) #acrescentamos o botao verde na mesma linha horizontal

        layoutVideo.add_widget(label1)
        layoutVideo.add_widget(label2)
        layoutVideo.add_widget(self.img1)
        layoutVideo.add_widget(layoutBotoes)

        self.capture = cv2.VideoCapture(0)  #criamos um objeto de capture de vídeo. Associamos à primeira camera
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,1024)

        Clock.schedule_interval(self.atualizaImagem, 1.0/30.0)   #criamos um clock para atualizar a imagem a cada 1/320 de segundo
        return layoutVideo

    def seleciona3Cores(self,button):
        self.filtro= 0

    def selecionaCinza(self,button):
        self.filtro= 1

    def filtraVermelho(self,button):    #elimina a componente vermelho
        self.filtro= 2

    def filtraAzul(self,button):    #elimina a componente azul
        self.filtro= 3

    def filtraVerde(self,button):    #elimina a componente azul
        self.filtro= 4

    def filtroRGB(self,src,r,g,b):
        if r == 0:
            src[:,:,2] = 0    #elimina o vermelho
        if g == 0:
            src[:,:,1] = 0    #elimina o verde
        if b == 0:
            src[:,:,0] = 0    #elimina o azul


    def atualizaImagem(self, dt):
        ret, frame = self.capture.read()   #captura uma imagem da camera

        if self.filtro ==0:
            frame1= frame

        if self.filtro == 1:       #converte para graus de cinza
            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.filtro ==2 :   #filtra a componente vermelho
            self.filtroRGB(frame,0,1,1)
            verdeazul_inferior = np.array([127,127,0])
            verdeazul_superior = np.array([255,255,255])
            mascara = cv2.inRange(frame, verdeazul_inferior, verdeazul_superior)
            frame1 = cv2.bitwise_and(frame,frame, mask= mascara)

        if self.filtro == 3: #filtra a componente azul
            self.filtroRGB(frame,1,1,0)
            vermelhoverde_inferior = np.array([0,127,127])
            vermelhoverde_superior = np.array([255,255,255])
            mascara = cv2.inRange(frame, vermelhoverde_inferior, vermelhoverde_superior)
            frame1 = cv2.bitwise_and(frame,frame, mask= mascara)

        if self.filtro == 4:  #filtra a componente verde
            self.filtroRGB(frame,1,0,1)
            vermelhoazul_inferior = np.array([127,0,127])
            vermelhoazul_superior = np.array([255,255,255])
            mascara = cv2.inRange(frame, vermelhoazul_inferior, vermelhoazul_superior)
            frame1 = cv2.bitwise_and(frame,frame, mask= mascara)


        buf1 = cv2.flip(frame1, 0)   #inverte para não ficar de cabeça para baixo

        buf2 = buf1.tostring() # converte em textura

        if self.filtro == 1:    #em graus de cinza
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='luminance' )   #colorfmt='bgr'
            texture1.blit_buffer(buf2, colorfmt='luminance', bufferfmt='ubyte')

        else:
            texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr' )   #colorfmt='bgr'
            texture1.blit_buffer(buf2, colorfmt='bgr', bufferfmt='ubyte')


        self.img1.texture = texture1 #apresenta a imagem

if __name__ == '__main__':
    CameraApp().run()
