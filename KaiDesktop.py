# coding=utf-8

# MIT License

# Copyright (c) 2017 Kaikyu

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# 888    d8P  d8b 888                                                .d8888b.                888
# 888   d8P   Y8P 888                                               d88P  Y88b               888
# 888  d8P        888                                               888    888               888
# 888d88K     888 888888 .d8888b  888  888 88888b.   .d88b.         888         .d88b.   .d88888  .d88b.
# 8888888b    888 888    88K      888  888 888 "88b d8P  Y8b        888        d88""88b d88" 888 d8P  Y8b
# 888  Y88b   888 888    "Y8888b. 888  888 888  888 88888888  8888  888    888 888  888 888  888 88888888
# 888   Y88b  888 Y88b.       X88 Y88  888 888  888 Y8b.            Y88b  d88P Y88..88P Y88b 888 Y8b.
# 888    Y88b 888  "Y888  88888P'  "Y88888 888  888  "Y8888          "Y8888P"   "Y88P"   "Y88888  "Y8888


import win32con
import Logger as log

log.init()
log.setType(1)
log.i("Avvio Kai Desktop...")

import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from KaiUtils import *
from PyQt5.QtCore import Qt
from threading import Thread
log.d("Elementi base per la splash screen importati correttamente")

app = QApplication(sys.argv)
screen_resolution = app.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()
log.i("Rilevato monitor %s*%s" % (width, height))

KeepRatio = Qt.KeepAspectRatio
SmoothTrans = Qt.SmoothTransformation
IgnoreTrans = Qt.IgnoreAspectRatio
log.i("Setting qualità impostati a: High")


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.splashPixmap = QPixmap('./Images/splash.png')
        self.setPixmap(self.splashPixmap.scaled((width/2.2), (height/2.2), KeepRatio, SmoothTrans))
        self.setWindowOpacity(0)
        self.show()
        Thread(target=fade_in, args=(self,)).start()

Splash = SplashScreen()
log.d("Splash screen creata")

import random
import STTModule as Sr
import pyqtgraph
import SWHear
import os
import subprocess
import numpy as np

from win32gui import SetWindowPos
from socket import *

np.seterr(all="ignore")

from requests import get
from pyqtgraph import PlotWidget
from psutil import users
UserName = str(users()[0][0]).capitalize()
log.i("Username rilevato: %s" % UserName)

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QMessageBox, QMenu
from PyQt5.QtCore import QRect, QTimer, QThread
from PyQt5.QtGui import QFont, QImage, QPainter
from time import sleep
from win32api import WinExec
log.i("Import e settings: OK")


def setVolume(val):
    subprocess.Popen("nircmd.exe setsysvolume %s" % (65535/100*val),
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE,
                     stdin=subprocess.PIPE)


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.oldPositionX = None
        self.oldPositionY = None
        self.setMouseTracking(True)
        self.setWindowTitle("Crediti")

        self.activateWindow()

        self.setGeometry(300, 300, 500, 300)
        self.move(width / 2 - self.width()/2, height / 2 - self.height()/2)

        self.textLabel = QLabel(self)
        self.textLabel.setText("Made by Kaikyu")
        self.textLabel.setFont(QFont('SansSerif', width / 100))
        self.textLabel.setStyleSheet('color: White')
        self.textLabel.setGeometry(QRect(300, 300, 500, 300))
        self.textLabel.move(0, 0)
        self.textLabel.show()
        self.pixmapLogo = QPixmap('./Images/small_logo.png').scaled(100, 100, KeepRatio, SmoothTrans)
        self.pixmapBar = QPixmap('./Images/top_bar.png').scaled(self.width(), 30, IgnoreTrans, SmoothTrans)

        self.barLabel = QLabel(self)
        self.barLabel.setPixmap(self.pixmapBar)
        self.barLabel.move(0, 0)
        self.barLabel.mouseMoveEvent = self.windowStartMove
        self.barLabel.mouseReleaseEvent = self.windowStopMove
        self.logoLabel = QLabel(self)
        self.logoLabel.setPixmap(self.pixmapLogo)

        self.logoLabel.move(self.width() - self.pixmapLogo.width() - 10,
                            self.height() - self.pixmapLogo.height() - 10)

        self.closeLabel = QLabel(self)
        self.closeLabel.move(self.width() - 30, 2)
        self.closeLabel.mousePressEvent = self.closeWindow
        self.closeLabel.setPixmap(QPixmap('./Images/close.png').scaled(26, 26, IgnoreTrans, SmoothTrans))
        self.Palette = self.palette()
        self.Palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(self.Palette)
        self.initUI()
        # self.animateOpen()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0)
        self.show()
        Thread(target=self.fadeIn).start()

    def closeWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.fadeOut()
            self.close()

    def windowStopMove(self, event):
        self.oldPositionX = None

    def windowStartMove(self, event):
        if not self.oldPositionX:
            self.oldPositionX = event.x()
        if not self.oldPositionY:
            self.oldPositionY = event.y()

        x = event.x() - self.oldPositionX
        y = event.y() - self.oldPositionY
        self.move(self.x() + x, self.y() + y)

    def fadeIn(self):
        for i in reversed(range(1, 10)):
            self.setWindowOpacity(1/i)
            sleep(0.01)

    def fadeOut(self):
        for i in reversed(range(1, 20)):
            self.setWindowOpacity(i*5/100)
            sleep(0.01)


class KaiDesktop(QWidget):
    def __init__(self):
        super().__init__()
        self.isStarted = False
        self.isFlipped = False
        self.isStopped = False
        self.isTalking = False
        self.hasWarned = False
        self.oldSignal = False
        self.hasMic = True
        self.isConnected = None
        self.Frames = None
        self.flippedFrames = None
        self.oldPositionX = None
        self.isBusy = False
        self.waitTime = 0
        self.CPU = 0
        self.RAM = 0
        self.checkCount = 0
        Thread(target=self.checkConnection).start()
        self.voiceHanlder = KaiHandler()
        self.Windows = {}
        self.Menu = QMenu()
        self.Settings = self.Menu.addAction("Impostazioni")
        self.Credits = self.Menu.addAction("Crediti")
        self.closeKai = self.Menu.addAction("Chiudi")
        self.loadFrames()
        self.VBox = QVBoxLayout()
        self.busy = QPixmap('./Images/busy.png').scaled(20, 20, KeepRatio, SmoothTrans)
        self.free = QPixmap('./Images/free.png').scaled(20, 20, KeepRatio, SmoothTrans)
        w = width / 1.5
        h = height / 1.5
        self.main = QPixmap('./Images/main.png').scaled(w, h, KeepRatio, SmoothTrans)
        self.mainF = QPixmap.fromImage(QImage('./Images/main.png').mirrored(True, False).scaled(w, h, KeepRatio, SmoothTrans))
        self.closeMouth = QPixmap('./Images/mouth_close.png').scaled(w, h, KeepRatio, SmoothTrans)
        self.transMouth = QPixmap('./Images/mouth_trans.png').scaled(w, h, KeepRatio, SmoothTrans)
        self.closeMouthF = QPixmap.fromImage(QImage('./Images/mouth_close.png').mirrored(True, False).scaled(w, h, KeepRatio, SmoothTrans))
        self.transMouthF = QPixmap.fromImage(QImage('./Images/mouth_trans.png').mirrored(True, False).scaled(w, h, KeepRatio, SmoothTrans))
        self.pixmapFumetto = QPixmap('./Images/fumetto.png')
        self.pixmapFumettoFlipped = QPixmap.fromImage(QImage('./Images/fumetto.png').mirrored(True, False))
        pixh = self.main.height()
        pixw = self.main.width()
        self.resize(pixw + height / 2, pixh)
        self.mainLabel = QLabel(self)
        self.mainLabel.resize(pixw + height / 2, pixh)
        self.mainLabel.move(self.width() / 2 - pixw / 2, 0)
        self.mouthLabel = QLabel(self)
        self.mouthLabel.resize(pixw + height / 2, pixh)
        self.mouthLabel.move(self.width() / 2 - pixw / 2, 0)
        self.eyesLabel = QLabel(self)
        self.eyesLabel.resize(pixw + height / 2, pixh)
        self.eyesLabel.move(self.width() / 2 - pixw / 2, 0)
        self.MessageManager = Message(self)
        self.MessageManager.setAlignment(Qt.AlignCenter)
        self.VBox.addWidget(self.MessageManager, alignment=Qt.AlignCenter)
        self.textLabel = QLabel(self)
        self.textLabel.setFont(QFont('SansSerif', width/100))
        self.textLabel.setStyleSheet('color: Black')
        self.textLabel.setAlignment(Qt.AlignCenter)
        self.VBox.addWidget(self.textLabel, alignment=Qt.AlignCenter)
        self.stateLabel = QLabel(self)
        self.stateLabel.setAlignment(Qt.AlignCenter)
        self.stateLabel.setGeometry(QRect(width / 100, width / 100, width * 0.38, height * 1.2))
        self.VBox.addWidget(self.stateLabel, alignment=Qt.AlignCenter)
        self.audioLabel = PlotWidget(self)
        a_range = height * 9
        log.d("Range impostato a %s" % a_range)
        self.audioLabel.plotItem.setRange(yRange=[-a_range, a_range])
        self.audioLabel.resize(pixw/3, pixh/2)
        self.audioLabel.move(self.width() / 2, self.height()-pixh/3)
        self.VBox.addWidget(self.audioLabel, alignment=Qt.AlignCenter)
        self.VBox.addWidget(self.mouthLabel, alignment=Qt.AlignCenter)
        self.VBox.addWidget(self.eyesLabel, alignment=Qt.AlignCenter)
        self.VBox.addStretch()
        pyqtgraph.setConfigOption('background', 't')  # before loading widget
        self.audioLabel.setStyleSheet("background: transparent")
        try:
            self.ear = SWHear.SWHear(rate=44100, updatesPerSecond=30)
            self.ear.stream_start()
        except:
            log.w("Nessun microfono rilevato, disattivo le funzioni vocali")
            self.hasMic = False
        self.mouseMoveEvent = self.kaiMove
        self.mouseReleaseEvent = self.kaiStopMove
        self.mousePressEvent = self.onClick
        self.closeEvent = self.onExit
        self.setWindowTitle('KaiDesktop')
        self.activateWindow()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)
        self.mainLabel.setPixmap(self.main)

        self.move(-width / 7, height / 3)
        self.setWindowOpacity(0)
        self.show()
        self.isStarted = True
        self.onReady()

    def update(self):
        if self.isStopped or not self.hasMic:
            self.audioLabel.close()
            return
        if not (self.ear.data is None or self.ear.fft is None):
            if self.waitTime > 0: show = True
            elif np.max(np.abs(self.ear.data)) > 1000:
                show = True
                self.waitTime = 300
            else:
                show = False
            if show:
                self.audioLabel.plot(self.ear.datax, self.ear.data, pen=pyqtgraph.mkPen(color='w'), clear=True)
            elif self.waitTime == 0:
                self.audioLabel.plot(self.ear.datax, self.ear.data, pen=pyqtgraph.mkPen(color='t'), clear=True)
            self.waitTime -= 5
        QTimer.singleShot(10, self.update)

    def loadFrames(self):
        w = width / 1.5
        h = height / 1.5
        self.flippedFrames = [QPixmap.fromImage(QImage('./Images/%s.png' % i).mirrored(True, False).scaled(w, h,
                                                                                                           KeepRatio,
                                                                                                           SmoothTrans))
                              for i in range(1, 5)]
        self.Frames = [QPixmap('./Images/%s.png' % i).scaled(w, h, KeepRatio, SmoothTrans) for i in range(1, 5)]

    def kaiMove(self, MouseEvent):
        if not self.oldPositionX:
            self.oldPositionX = MouseEvent.x()

        x = MouseEvent.x() - self.oldPositionX
        self.move(self.x() + x, self.y())
        self.MessageManager.resetLabelPos()
        if self.pos().x() + self.width() / 2 > width / 2:
            self.onFlipSignal(True)
        else:
            self.onFlipSignal(False)

    def kaiStopMove(self, MouseEvent):
        self.oldPositionX = None

    def onClick(self, ClickEvent):
        if ClickEvent.buttons() == Qt.RightButton:
            self.Menu.move(self.mapToParent(ClickEvent.pos()))
            action = self.Menu.exec()
            if action == self.Settings:
                pass
            if action == self.Credits:
                NewWindow()
            if action == self.closeKai:
                self.close()
        else:
            self.Say(self.getClickResponse(ClickEvent.pos), lowPriority=True)

    def onExit(self, CloseEvent):
        if self.isStopped:
            self.isStopped = True
            fade_out(self)
            CloseEvent.accept()
            return

        quit_msg = "Sei sicuro di voler chiudere Kai?"

        reply = QMessageBox.question(self, 'Chiudi', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.isStopped = True
            fade_out(self)
            CloseEvent.accept()
        else:
            CloseEvent.ignore()
            self.Say("Yay... ^^")

    def Animator(self):
        double = False
        while not self.isStopped:
            for i in range(8):
                if self.isStopped:
                    break
                if not self.isFlipped:
                    self.eyesLabel.setPixmap(self.Frames[i if i < 4 else 7 - i])
                else:
                    self.eyesLabel.setPixmap(self.flippedFrames[i if i < 4 else 7 - i])
                sleep(0.025)
            if not double:
                if random.randint(1, 7) == 1:
                    sleep(0.06)
                    double = True
                else:
                    sleep(3)
            else:
                double = False
                sleep(3)

    def Say(self, text, lowPriority=False):
        try:
            if not self.isTalking:
                if not lowPriority:
                    SetWindowPos(self.winId(),
                                 win32con.HWND_TOPMOST,
                                 # always on top. only reliable way to bring it to the front on windows
                                 0, 0, 0, 0,
                                 win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

                    SetWindowPos(self.winId(),
                                 win32con.HWND_NOTOPMOST,
                                 # disable the always on top, but leave window at its top position
                                 0, 0, 0, 0,
                                 win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
                self.MessageManager.sendMessage(text)
        except Exception as err:
            log.e(err)

    def getClickPercentage(self, pos):
        return int(pos().x()/(self.width()/100)), int(pos().y()/(self.height()/100))

    def getClickResponse(self, pos):
        x, y = self.getClickPercentage(pos)
        log.d("Click x: %s, y: %s" % (str(x) + "%", str(y) + "%"))
        if self.isFlipped:
            return "Click!"
        return "Click"
        if 53 < x < 60 and y <= 7:
            return "N-nyah? :3"
        if 67 <= x:
            return "*muove l'orecchio sinistro*"
        if 21 <= y <= 25 and 52 <= x <= 56:
            return "Il mio occhio, b-baka ><"
        if 26 <= y <= 30 and 59 <= x <= 61:
            return "Mi fai male T^T"
        return "Click >w<"
        # ToDo: Continuare questo metodo

    def setBusy(self):
        self.stateLabel.setPixmap(self.busy)
        self.isBusy = True

    def setFree(self):
        self.stateLabel.setPixmap(self.free)
        self.isBusy = False

    def onCPUhigh(self):
        self.Say("%s, l'utilizzo della CPU è al %s" % (UserName, str(self.CPU) + "%!"))
        self.hasWarned = True

    def onRAMhigh(self):
        self.Say("%s, stai utilizzando la RAM al %s >~>" % (UserName, str(self.RAM) + "%!"))
        self.hasWarned = True

    def HWMonitor(self):
        self.CPU = get_usage()
        if self.CPU >= 95 and not self.hasWarned:
            self.onCPUhigh()

        self.RAM = get_ram()
        if self.RAM >= 80 and not self.hasWarned:
            self.onRAMhigh()

        if self.checkCount == 10:
            Thread(target=self.checkConnection).start()
            self.checkCount = 0
            self.hasWarned = False

        self.checkCount += 1
        QTimer.singleShot(1000, self.HWMonitor)

    def checkConnection(self):
        old = self.isConnected
        try: self.isConnected = True if get('http://canihazip.com/s').status_code == 200 else False
        except: self.isConnected = False
        if old != self.isConnected and old is not None:
            if self.isConnected: self.Say("Dovrebbe essere tornata la connessione!")
            else: self.Say("Dev'essere andata via la connessione...")

    def onReady(self):
        while not self.isStarted:
            pass
        Thread(target=fade_in, args=(self,), name="FadeIn").start()
        Thread(target=self.Animator, name="Animator").start()
        Thread(target=self.comunicate, name="comunicate").start()
        self.voiceHanlder.start()
        self.update()
        self.HWMonitor()
        fade_out(Splash)
        Splash.close()
        self.Say("Eccomi, %s~" % UserName, lowPriority=True)

    def onFlip(self):
        if self.isFlipped:
            self.stateLabel.setGeometry(QRect(width / 100, width / 100, width * 0.38, height * 1.2))
            self.mouthLabel.setPixmap(self.closeMouthF)
            self.eyesLabel.setPixmap(self.flippedFrames[0])
            self.mainLabel.setPixmap(self.mainF)
        else:
            self.stateLabel.setGeometry(QRect(width / 100, width / 100, width * 0.2, height * 1.2))
            self.mouthLabel.setPixmap(self.closeMouth)
            self.eyesLabel.setPixmap(self.Frames[0])
            self.mainLabel.setPixmap(self.main)

    def onFlipSignal(self, Fbool):
        if self.oldSignal != Fbool:
            self.isFlipped = Fbool
            self.oldSignal = Fbool
            self.onFlip()

    def comunicate(self):
        try:
            usr = "52962566"
            passw = "12345"
            mysocket = socket()
            mysocket.connect(("35.163.181.229", 5000))
            m = '{"username": "%s", "password": "%s"}' % (usr, passw)
            mysocket.send(m.encode())
            msg = mysocket.recv(1024).decode()
            if msg == "handshake":
                log.i("Collegato a Kai Telegram")
                while True:
                    command = mysocket.recv(1024).decode()
                    if "vol:" in command:
                        perc = int(command.split(":")[1])
                        setVolume(perc)
                        log.d("Volume impostato a %s" % perc)
                        Kai.Say("Volume impostato a %s!" % perc)
                        sleep(0.1)
                    if "spegni" in command:
                        Kai.Say("Spengo il computer, ciao %s!" % UserName)
                        sleep(0.2)
                        WinExec("shutdown.exe /p /f")
                        Kai.isStopped = True
        except Exception as err:
            sleep(4)
            Kai.Say("Si è verificato un errore: " + str(err))
            log.e("Errore nel socket")


class Message(QLabel):
    def __init__(self, caller):
        super().__init__(caller)
        self.kaiInstance = caller
        self.noText = "Dovrei dire qualcosa, ma non ricordo cosa..."
        self.text = "Qualcosa non va... c.c"
        self.waitTime = 3
        self.final_h = 100
        self.final_w = 100
        self.PixmapBaloon = QPixmap('./Images/fumetto.png')
        self.setAlignment(Qt.AlignCenter)
        self.TextLabel = QLabel(caller)
        self.TextLabel.setAlignment(Qt.AlignCenter)
        self.TextLabel.setFont(QFont('SansSerif', width / 100))
        self.TextLabel.setStyleSheet('color: Black')
        self.setGeometry(QRect(caller.width() / 8.5, caller.height() / 6, caller.width(), caller.height()))
        self.TextLabel.setGeometry(QRect(caller.width() / 9, caller.height() / 6, caller.width(), caller.height()))

    def resetLabelPos(self):
        if self.kaiInstance.isFlipped:
            args = [QRect(-self.kaiInstance.width()/9.5, self.kaiInstance.height()/6, self.kaiInstance.width(), self.kaiInstance.height()),
                    QRect(-self.kaiInstance.width()/10, self.kaiInstance.height()/6, self.kaiInstance.width(), self.kaiInstance.height())]
        else:
            args = [QRect(self.kaiInstance.width()/9, self.kaiInstance.height()/6, self.kaiInstance.width(), self.kaiInstance.height()),
                    QRect(self.kaiInstance.width()/8.5, self.kaiInstance.height()/6, self.kaiInstance.width(), self.kaiInstance.height())]

        self.TextLabel.setGeometry(args[0])
        self.setGeometry(args[1])

    def fadeOut(self):
        self.setPixmap(self.PixmapBaloon.scaled(self.final_h, self.final_w, IgnoreTrans, SmoothTrans))
        for i in range(1, 6):
            sleep(0.04)
            tmp = QImage('./Images/fumetto.png').scaled(self.final_h, self.final_w, IgnoreTrans, Qt.FastTransformation)
            painter = QPainter()
            painter.begin(tmp)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationOut)
            painter.setOpacity(i/5)
            painter.fillRect(tmp.rect(), 0)
            self.setPixmap(QPixmap.fromImage(tmp))
            painter.end()

    def fadeIn(self):
        for i in reversed(range(5)):
            sleep(0.04)
            tmp = QImage('./Images/fumetto.png').scaled(self.final_h, self.final_w, IgnoreTrans, Qt.FastTransformation)
            painter = QPainter()
            painter.begin(tmp)
            painter.setCompositionMode(QPainter.CompositionMode_DestinationOut)
            painter.setOpacity(i/5)
            painter.fillRect(tmp.rect(), 0)
            self.setPixmap(QPixmap.fromImage(tmp))
            painter.end()
        self.setPixmap(self.PixmapBaloon.scaled(self.final_h, self.final_w, IgnoreTrans, SmoothTrans))

    def animateImage(self):
        self.kaiInstance.isTalking = True
        self.resetLabelPos()
        self.fadeIn()
        self.TextLabel.setText(self.text)
        for i in range(0, int(len(self.text)/3)):
            self.kaiInstance.mouthLabel.setPixmap(self.kaiInstance.transMouthF
                                                  if self.kaiInstance.isFlipped
                                                  else self.kaiInstance.transMouth)
            sleep(0.1)

            self.kaiInstance.mouthLabel.setPixmap(self.kaiInstance.closeMouthF
                                                  if self.kaiInstance.isFlipped
                                                  else self.kaiInstance.closeMouth)
            sleep(0.13)
        self.TextLabel.setText("")
        self.fadeOut()
        self.kaiInstance.isTalking = False

    def sendMessage(self, text=None, timeout=3):
        if not text: text = self.noText
        if self.kaiInstance.isTalking: return
        self.kaiInstance.isTalking = True
        log.d("say: %s" % text)
        final, lines, t = text_formatter(text)
        self.final_h = t * (height / 75)
        self.final_w = (t * 1.2) * (width / 260)
        self.text = final
        self.waitTime = timeout
        Thread(target=self.animateImage).start()


class KaiHandler(QThread):
    def __init__(self):
        QThread.__init__(self)
        try:
            self.r = Sr.Recognizer()
            self.m = Sr.Microphone()
            with self.m as source:
                self.r.adjust_for_ambient_noise(source)
            log.i("Ambient noise impostato a %s" % self.r.energy_threshold)
        except:
            pass

    def __del__(self):
        self.wait()

    def listen(self):
        try:
            with self.m as source:
                Kai.setFree()
                audio = self.r.listen(source)
                length = len(audio.get_flac_data())
                if length > 150000 or length < 40000: return "skip"
                Kai.setBusy()
                what_i_said = self.r.recognize_google(audio, language="it-IT")
                log.d("Risultato: %s" % what_i_said)
                return what_i_said
        except Sr.UnknownValueError: return "Non ho capito..."
        except Sr.RequestError: return "skip"

    def elabResponse(self, command):
        log.i("Ho capito: %s" % command)
        log.d("Comando vocale ricevuto")
        if "ciao" in command:
            Kai.Say("Ciao %s!" % UserName)
        elif "sto andando via" in command:
            Kai.Say("Okay, " + UserName)
            sleep(1)
            os.system("nircmd.exe monitor off")
            return
        elif "muta" in command or "butta" in command:
            setVolume(0)
            Kai.Say("Audio mutato")
            print("Riconiscuto")
        elif "alza" in command and "volume" in command:
            setVolume(100)
            Kai.Say("Volume impostato al 100%!")
        elif "kill yourself" in command:
            Kai.Say("kys scrub")
        elif "130 martin garrix" in command:
            Kai.Say("SI VOLAAAAA!")
        elif "spegni il computer" in command:
            WinExec("shutdown.exe /p /f")
            Kai.isStopped = True
        elif "Non ho capito..." in command:
            Kai.Say("Non ho capito...", lowPriority=True)
        elif "sei bella" in command:
            Kai.Say("Grazie %s.. >.<" % UserName)

        if "apri" in command:
            if "telegram" in command:
                WinExec("C:\\Users\\Kaikyu\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
                Kai.Say("Telegram aperto!")

            if "chrome" in command:
                WinExec("C:\\Program Files (x86)\Google\Chrome\Application\chrome.exe")
                Kai.Say("Chrome aperto!")

            if "google" in command:
                WinExec("C:\\Program Files (x86)\Google\Chrome\Application\chrome.exe", "www.google.com")
                Kai.Say("Google aperto!")

            if "youtube" in command:
                WinExec("C:\\Program Files (x86)\Google\Chrome\Application", 'chrome.exe "www.youtube.com"')
                Kai.Say("Youtube aperto!")

            if "osu" in command:
                WinExec("C:\\Program Files\osu!\osu!.exe")
                Kai.Say("osu! aperto!")

        elif "cerca" in command:
            try:
                Kai.Say("Cerco: " + command.split("cerca ")[1])
                sleep(0.9)
                WinExec("\"C:\\Program Files (x86)\Google\Chrome\Application\chrome.exe\""
                        " \"https://www.google.it/?gfe_rd=cr&ei=OE0bWfL1CYf38AfRiLWYBw#q=%s\"" %
                        command.split("cerca")[1])
            except:
                Kai.Say("Cosa dovrei cercare...?")

        elif "chiudi" in command:
            if "osu" in command or "o su" in command:
                os.system("Taskkill /IM osu!.exe /F")
                Kai.Say("osu! chiuso!")

    def checkMic(self):
        try:
            tmp = SWHear.SWHear()
            tmp.initiate()
            tmp.stream_start()
            Kai.hasMic = True
            tmp.close()
            return True
        except Exception as err:
            return False

    def run(self):
        try:
            sleep(2)
            while True:
                if Kai.isStopped:
                    log.i("Stopping KaiHandler runner")
                    break

                if not Kai.hasMic:
                    if not self.checkMic():
                        sleep(3)
                        continue
                    else:
                        Kai.Say("Microfono rilevato!")

                if not Kai.isConnected:
                    sleep(3)
                    continue

                try:
                    log.d("Entro in attesa di un comando...")
                    com = self.listen().lower()
                    self.elabResponse(com)
                except:

                    if not Kai.isConnected:
                        log.w("Non sono connessa")
                        sleep(5)
                        continue

                    if Kai.hasMic:
                        if not self.checkMic():
                            Kai.Say("Non ho rilevato alcun microfono...")
                            Kai.hasMic = False
                            sleep(5)

        except Exception as err:
            log.e(err)

Kai = KaiDesktop()
log.i("Istanza di Kai pronta")
os._exit(app.exec_())
log.i("App terminata.")

