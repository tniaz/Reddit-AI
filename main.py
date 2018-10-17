# importing required modules
from gtts import gTTS
import speech_recognition as sr
import webbrowser
from pygame import mixer
from tempfile import TemporaryFile
import re
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QCoreApplication
from time import sleep

# importing ui file for .exe


# def resource_path(relative_path):
# try:
# PyInstaller creates a temp folder and stores path in _MEIPASS
#base_path = sys._MEIPASS
# except Exception:
#base_path = os.path.abspath(".")

# return os.path.join(base_path, relative_path)


# QMainWindow class from PyQt with custom .ui loaded from QT Designer
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        #uipath = resource_path('mainwindow.ui')
        uic.loadUi('mainwindow.ui', self)\
            # loading icon
        #iconpath = resource_path('icon.png')
        self.pixmap = QPixmap('icon.png')
        self.label.setPixmap(self.pixmap)
        # mapping button
        self.readyButton.clicked.connect(self.ready)
        self.show()
        self.chat.append("AI: Hello!")
        talkToMe("Hello!")
        QCoreApplication.processEvents()

    # method to refresh chat field dynamically
    def refresh_text(self, text):
        self.chat.append(text)  # append string
        QCoreApplication.processEvents()  # update gui for pyqt

    # method to carry out user command
    def ready(self):
        self .refresh_text("AI: Reddit bot is ready for your next command!")
        talkToMe("Reddit bot is ready for your next command!")
        # calls upon myCommand method for speech recognition
        command = myCommand()
        self.refresh_text("You: " + command)
        talkToMe(str("You said: " + command))

        # loop based on user command; either opens a reddit url or quits application
        while not mixer.get_busy():
            if "open Reddit" in command:
                reg_ex = re.search('open Reddit (.*)', command)
                url = 'https://www.reddit.com/'
                if reg_ex:
                    subreddit = reg_ex.group(1).replace(" ", "")
                    url = url + 'r/' + subreddit
                webbrowser.open(url)
                self.refresh_text("AI: Done!")
                break
            elif "quit" in command:
                self.refresh_text("AI: Goodbye!")
                talkToMe("Goodbye!")
                sleep(2)
                sys.exit()


# function to play audio from string
def talkToMe(audioString):
    tts = gTTS(text=audioString, lang="en")
    mixer.init()
    sf = TemporaryFile()
    tts.write_to_fp(sf)
    sf.seek(0)
    mixer.music.load(sf)
    mixer.music.play()

# function to use speech recognition to get user command


def myCommand():
    r = sr.Recognizer()
    command = ""

    with sr.Microphone() as source:
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)

    # loop back to listen to command if unrecognizable
    except sr.UnknownValueError:
        myCommand()

    return command


# main loop
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
