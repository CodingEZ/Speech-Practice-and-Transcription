import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLineEdit     # for input boxes
from PyQt5.QtWidgets import QMessageBox                 # for message boxes
from PyQt5.QtWidgets import QLabel          # for images
from PyQt5.QtGui import QPixmap             # for images
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import Qt                 # for text
import Transcribe
import Download
import ImageEdit
import Recording
import TextSearch

class Window(QWidget):
 
    def __init__(self, width=800, height=800):
        super().__init__()
        self.title = 'Youtube Transcriptor'
        self.left = 100
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Images/word.jpg'
        self.boundStyle = "QLabel { background-color : orange; }"
        self.boundInStyle = "QLabel { background-color : gray; }"

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.showBackground()
        self.buttons = []
        self.labels = []
        self.log = "LOG : \n"
        
        self.script = None      # script information
        self.numWords = 0
        self.textStart = 0
        
        self.initStart()        # begin application in the start menu
        self.show()
        
        self.audioFileName = None
        self.url = None

    def showBackground(self):
        labelBack = QLabel(self)
        name = ImageEdit.resize_image(self.background, (self.width, self.height))
        pixmap = QPixmap(name)
        labelBack.setPixmap(pixmap)

    def showText(self, xFactor, yFactor, widthFactor, heightFactor, width, styleBound, styleText, text):
        labelOut = QLabel(self)
        labelOut.resize(self.width*widthFactor + width,
                        self.height*heightFactor + width)
        labelOut.move(self.width*xFactor - labelOut.width()/2,
                      self.height*yFactor - labelOut.height()/2)
        labelOut.setStyleSheet(styleBound)
        
        labelIn = QLabel(self)
        labelIn.resize(self.width*widthFactor,
                       self.height*heightFactor)
        labelIn.move(self.width*xFactor - labelIn.width()/2,
                     self.height*yFactor - labelIn.height()/2)
        labelIn.setStyleSheet(styleText)
        labelIn.setAlignment(Qt.AlignCenter)
        labelIn.setText(text)
        return [labelIn, labelOut]

    def showBound(self, xFactor, yFactor, widthFactor, heightFactor, width, styleBound, styleBoundIn):
        labelBound = QLabel(self)
        labelBound.resize(self.width*widthFactor + width,
                          self.height*heightFactor + width)
        labelBound.move(self.width*xFactor - labelBound.width()/2,
                        self.height*yFactor - labelBound.height()/2)
        labelBound.setStyleSheet(styleBound)

        labelBoundIn = QLabel(self)
        labelBoundIn.resize(self.width*widthFactor,
                          self.height*heightFactor)
        labelBoundIn.move(self.width*xFactor - labelBoundIn.width()/2,
                        self.height*yFactor - labelBoundIn.height()/2)
        labelBoundIn.setStyleSheet(styleBoundIn)
        return [labelBound, labelBoundIn]

    @staticmethod
    def showButtons(buttons):
        for button in buttons:  button.show()

    @staticmethod
    def hideButtons(buttons):
        for button in buttons:  button.hide()

    @staticmethod
    def showLabels(labels):
        for label in labels:    label.show()

    @staticmethod
    def hideLabels(labels):
        for label in labels:    label.hide()

    def updateLog(self, message):
        self.log += message
        #error below here
        self.labels[-1].hide()
        self.labels[-1].setText(self.log)
        self.labels[-1].show()

    def resetLog(self):
        self.log = "LOG : \n"
        self.labels[-1].hide()
        self.labels[-1].setText(self.log)
        self.labels[-1].show()

    def displayMessage(self, message):
        buttonReply = QMessageBox.information(self, 'Message Display', message, QMessageBox.Ok)

    def displayWarning(self, message):
        buttonReply = QMessageBox.warning(self, 'Warning Display', message, QMessageBox.Ok)

    def initStart(self):
        self.buttons = []
        buttonNames = ['Transcribe', 'Practice', 'Quit']
        buttonTips = ['Goes to Transcription Menu',
                      'Practice a Speech',
                      'Exit the Application']

        self.labels = []
        self.labels += self.showText(1/2, 1/3, 3/4, 1/8, 50, self.boundStyle,
                                     "QLabel { background-color : gray; color : yellow; font : 14pt; }",
                                     'Welcome to the Transcriptor!')
        self.labels += self.showBound(1/2, 5/8, 1/5, 1/5, 20,
                                     self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setObjectName(buttonNames[index])
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           (5/4)*self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Transcribe':
                newButton.clicked.connect(self.onClickMenu)
            elif buttonNames[index] == 'Practice':
                newButton.clicked.connect(self.onClickPracticeMenu)
            elif buttonNames[index] == 'Quit':
                newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initMenu(self):
        self.buttons = []
        buttonNames = ['Choose File', 'Choose URL', 'Transcribe', 'Download', 'Back to Start', 'Quit']
        buttonTips = ['Choose a video from your computer to transcribe',
                      'Choose a video from Youtube to transcribe',
                      'Makes a full transcription of audio',
                      'Downloads a video from a given Youtube url',
                      'Returns to the Start Menu',
                      'Exit the Application']

        self.labels = []
        self.labels += self.showBound(1/2, 3/4, 1/5, 1/3, 20, self.boundStyle, self.boundInStyle)
        self.labels += self.showText(1/2, 7/24, 3/4, 2/5, 20, self.boundStyle,
                                     "QLabel { background-color : gray; color : yellow; font : 11pt; }",
                                     self.log)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width*(1/2) - newButton.width()/2 - 5,
                           self.height*(3/4) - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Choose File':
                newButton.clicked.connect(self.onClickChooseFile)
            elif buttonNames[index] == 'Choose URL':
                newButton.clicked.connect(self.onClickChooseURL)
            elif buttonNames[index] == 'Transcribe':
                newButton.clicked.connect(self.onClickTranscribe)
            elif buttonNames[index] == 'Download':
                newButton.clicked.connect(self.onClickDownload)
            elif buttonNames[index] == 'Back to Start':
                newButton.clicked.connect(self.onClickStart)
            elif buttonNames[index] == 'Quit':
                newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initPracticeMenu(self):
        self.buttons = []
        buttonNames = ['Start Practice', 'Instructions', 'Back to Start', 'Quit']
        buttonTips = ['Begin the game!',
                      'Gives a brief explanation of how to play',
                      'Returns to the Start Menu',
                      'Exit the Application']

        self.labels = []
        self.labels += self.showBound(1/2, 1/2, 1/5, 1/4, 20, self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Start Practice':
                newButton.clicked.connect(self.onClickPractice)
            if buttonNames[index] == 'Instructions':
                newButton.clicked.connect(self.onClickInstructions)
            elif buttonNames[index] == 'Back to Start':
                newButton.clicked.connect(self.onClickStart)
            elif buttonNames[index] == 'Quit':
                newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initPractice(self):
        self.buttons = []
        buttonNames = ['Record', 'Pick Script', 'Pick Start', 'Back', 'Quit']
        buttonTips = ['Practice your speech!',
                      'Pick the script you want to practice.',
                      'Pick the starting word at which you want to practice.',
                      'Returns Practice Menu',
                      'Exit the Application']

        self.labels = []
        self.labels += self.showBound(1/2, 1/2, 1/5, 1/4, 20, self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Record':
                newButton.clicked.connect(self.onClickRecord)
            elif buttonNames[index] == 'Pick Script':
                newButton.clicked.connect(self.onClickPickScript)
            elif buttonNames[index] == 'Pick Start':
                newButton.clicked.connect(self.onClickPickStart)
            elif buttonNames[index] == 'Back to Start':
                newButton.clicked.connect(self.onClickStart)
            elif buttonNames[index] == 'Quit':
                newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initInstructions(self):
        self.buttons = []
        buttonNames = ['Back', 'Quit']
        buttonTips = ['Returns to the Practice Menu',
                      'Exit the Application']
        
        self.labels = []
        self.labels += self.showText(1/2, 5/16, 7/8, 5/16, 20, self.boundStyle,
                                     "QLabel { background-color : gray; color : yellow; font : 11pt; }",
                                     'Instructions:\n\n' + \
                                     '  When ready, click the record button and speak into your \n' + \
                                     '  microphone.  Given a text document, the program will \n' + \
                                     '  transcribe what you say and compare that with the given \n' + \
                                     '  text, noting areas of error. There is also the option \n' + \
                                     '  of splitting up the text to practice small chunks.')
        self.labels += self.showBound(1/2, 11/16, 1/5, 1/8, 20, self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           (11/8)*self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Back':
                newButton.clicked.connect(self.onClickPracticeMenu)
            elif buttonNames[index] == 'Quit':
                newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    @pyqtSlot()
    def onClick(self):
        pass

    @pyqtSlot()
    def onClickStart(self):
        __class__.hideButtons(self.buttons)
        __class__.hideLabels(self.labels)
        self.initStart()
        __class__.showLabels(self.labels)
        __class__.showButtons(self.buttons)

    @pyqtSlot()
    def onClickMenu(self):
        __class__.hideButtons(self.buttons)
        __class__.hideLabels(self.labels)
        self.initMenu()
        __class__.showLabels(self.labels)
        __class__.showButtons(self.buttons)

    @pyqtSlot()
    def onClickPracticeMenu(self):
        __class__.hideButtons(self.buttons)
        __class__.hideLabels(self.labels)
        self.initPracticeMenu()
        __class__.showLabels(self.labels)
        __class__.showButtons(self.buttons)

    @pyqtSlot()
    def onClickPractice(self):
        __class__.hideButtons(self.buttons)
        __class__.hideLabels(self.labels)
        self.initPractice()
        __class__.showLabels(self.labels)
        __class__.showButtons(self.buttons)

    @pyqtSlot()
    def onClickInstructions(self):
        __class__.hideButtons(self.buttons)
        __class__.hideLabels(self.labels)
        self.initInstructions()
        __class__.showLabels(self.labels)
        __class__.showButtons(self.buttons)

    ########################################################################
        # Edit
    ########################################################################
    @pyqtSlot()
    def onClickRecord(self):
        Recording.recordTo('output.wav')
        # do the checking here
        # need to handle self in Recording file:
            # Recording.recordTo('output.wav', self)

    ########################################################################

    @pyqtSlot()
    def onClickPickScript(self):
        file, okPressed = QInputDialog.getText(self, "File name input",
                'Type in the name of the file you want.\n' + \
                'Do not forget the extension!',
                QLineEdit.Normal, "")
        if okPressed:
            error, text = TextSearch.getText(file)
            if error == None:
                self.script = text
            else:
                self.displayWarning(error)
    
    @pyqtSlot()
    def onClickPickStart(self):
        if self.script == None:
            self.displayWarning('You have not yet selected a script!\n' + \
                                'You must select your script before picking a starting point.')
            return
        
        num, okPressed = QInputDialog.getInt(self, "Pick Starting Point",
                "Pick what number word to start checking for memorization", QLineEdit.Normal, 0)
        if okPressed:
            if num < 0:
                self.displayWarning('You cannot start at a negative word!')
                return
            elif num >= self.numWords:
                self.displayWarning('You cannot start at a word beyond \n' + \
                                    'the end of the transcript!')
                return
            self.textStart = num
        
    @pyqtSlot()
    def onClickChooseFile(self):
        self.hide()
        file, okPressed = QInputDialog.getText(self, "File name input",
                'Type in the name of the file you want.\n' + \
                'The file should be located in the Audio folder,\n' + \
                'but you do not need to include "Audio" in the path.\n' + \
                'Do not forget the extension!',
                QLineEdit.Normal, "")
        if okPressed:
            self.audioFileName = 'Audio/' + file
            self.displayMessage('Name chosen: ' + self.audioFileName)
        self.show()

    @pyqtSlot()
    def onClickChooseURL(self):
        self.hide()
        url, okPressed = QInputDialog.getText(self, "URL input",
                'Type in the url of the Youtube video you want.\n' + \
                'The file will be downloaded to the Audio folder.',
                QLineEdit.Normal, "")
        if okPressed:
            self.url = 'Audio/' + url
            self.displayMessage('URL chosen: ' + self.url)
        self.show()

    @pyqtSlot()
    def onClickTranscribe(self):
        if self.audioFileName == None:
            self.displayWarning('Error: no file chosen!')
            return

        fileList = os.listdir('Audio')
        if self.audioFileName.split('/')[1] in fileList:
            error = Transcribe.full_transcribe(self.audioFileName, self)
            if error != None:
                self.displayWarning('Error! : ' + error)
                return
            self.displayMessage('No errors in transcription!')
            return
        self.displayWarning('Fetched file does not exist! Fetch a different file.')

    @pyqtSlot()
    def onClickDownload(self):
        errorCode = Download.downloadYoutube(self.url)
        if isinstance(errorCode, str):
            self.audioFileName = errorCode
            self.displayMessage('Downloaded file: ' + self.audioFileName)
        elif errorCode == 0:
            self.displayWarning('Invalid url. Perhaps you spelled it wrong?')
        elif errorCode == 1:
            self.displayWarning('Unable to download. Perhaps video was taken down?')

def onClickQuit():
    sys.exit(app.exec_())
    print('Thank you for using this application!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(600, 600)
    onClickQuit()
