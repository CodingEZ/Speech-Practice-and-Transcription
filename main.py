import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QInputDialog, QLineEdit     # for input boxes
from PyQt5.QtCore import pyqtSlot
from BackgroundPYQT import *
from TextPYQT import *
from ButtonClickPYQT import *
from DisplayPYQT import *
import Transcribe
import Download
import Recording
import TextCheck
import time


def fileToTranscript(speechFile):
    """Helper that finds the index for the extension of a file."""
    index = -1
    while speechFile[index] != '.' and index > -len(speechFile) + 1:
        index -= 1
    return speechFile[:index] + '/transcription.txt'

class Window(QWidget):
 
    def __init__(self, width=1000, height=800):
        super().__init__()
        self.title = 'Speech Practice and Transcription'
        self.left = 100
        self.top = 100
        self.width = self.left + width
        self.height = self.top + height
        self.background = 'Images/cherry.jpg'
        self.boundStyle = "QLabel { background-color : #FFFFFF; }"
        self.boundInStyle = "QLabel { background-color : #FBBBBB; }"
        self.titleStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 14pt; }"
        self.normalStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 11pt; }"
        self.logStyle = "QLabel { background-color : #FBBBBB; color : #000000; font : 9pt; }"

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        showBackground(self)
        self.buttons = []
        self.labels = []
        self.logInit = " LOG : \n"
        self.log = self.logInit     # starter text for log

        self.audioFileName = None
        self.url = None

        self.scriptName = None
        self.correctText = None      # script information
        self.numWords = 0
        self.textStartMin = 0      # default start at beginning of script
        self.textStart = self.textStartMin
        self.periodMin = 10        # default 10 seconds of recording
        self.period = self.periodMin

        self.recordText = None
        
        self.initStart()        # begin application in the start menu
        self.show()
        
        TextCheck.setCharFit(self.width)
        setCharFit(self.width)

    ######################################################################################
    # Log and Info update/reset functions
    ######################################################################################

    def updateLog(self, message):
        """Adds to activity log in transcription mode"""
        self.log += message
        self.labels[-1].hide()
        self.labels[-1] = showLog(self)[-1]
        self.labels[-1].show()

    def resetLog(self):
        """Resets activity log in transcription mode"""
        self.log = self.logInit
        self.labels[-1].hide()
        self.labels[-1] = showLog(self)[-1]
        self.labels[-1].show()

    def updateTranscribeInfo(self):
        """Adds to info in transcription mode"""
        self.labels[-3].hide()
        self.labels[-3] = showTranscribeInfo(self)[-1]
        self.labels[-3].show()

    def updatePracticeInfo(self):
        """Adds to info in practice mode"""
        self.labels[-3].hide()
        self.labels[-3] = showPracticeInfo(self)[-1]
        self.labels[-3].show()

    #####################################################################################################
    # Separate Menus
    #####################################################################################################

    def initStart(self):
        self.buttons = []
        buttonNames = ['Transcribe', 'Practice', 'Quit']
        buttonTips = ['Goes to Transcription Menu',
                      'Practice a Speech',
                      'Exit the Application']

        self.labels = []
        self.labels += showBound(self, 1/2, 5/8, 1/5, 1/5, 30, self.boundStyle, self.boundInStyle)
        self.labels += showText(self, 1/2, 1/3, 3/4, 1/8, 50, self.boundStyle, self.titleStyle, 'Speech Practice and Transcription')
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setObjectName(buttonNames[index])
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           (5/4)*self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Transcribe':      newButton.clicked.connect(self.onClickTranscribeMenu)
            elif buttonNames[index] == 'Practice':      newButton.clicked.connect(self.onClickPracticeMenu)
            elif buttonNames[index] == 'Quit':          newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initTranscribeMenu(self):
        self.buttons = []
        buttonNames = ['Instructions', 'Transcribe', 'Choose File', 'Choose URL',
                       'Download', 'Back to Start', 'Quit']
        buttonTips = ['Gives an explanation of what goes on in this menu',
                      'Makes a full transcription of audio',
                      'Choose a video from your computer to transcribe',
                      'Choose a video from Youtube to transcribe',
                      'Downloads a video from a given Youtube url',
                      'Returns to the Start Menu',
                      'Exit the Application']

        self.labels = []
        self.labels += showBound(self, 3/4, 3/4, 1/5, 1/3, 30, self.boundStyle, self.boundInStyle)
        self.labels += showTranscribeInfo(self)
        self.labels += showLog(self)

        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width*(3/4) - newButton.width()/2 - 5,
                           self.height*(3/4) - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Instructions':        newButton.clicked.connect(self.onClickTranscribeInstructions)
            elif buttonNames[index] == 'Transcribe':        newButton.clicked.connect(self.onClickTranscribe)
            elif buttonNames[index] == 'Choose File':       newButton.clicked.connect(self.onClickChooseFile)
            elif buttonNames[index] == 'Choose URL':        newButton.clicked.connect(self.onClickChooseURL)
            elif buttonNames[index] == 'Download':          newButton.clicked.connect(self.onClickDownload)
            elif buttonNames[index] == 'Back to Start':     newButton.clicked.connect(self.onClickStart)
            elif buttonNames[index] == 'Quit':              newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initTranscribeInstructions(self):
        self.buttons = []
        buttonNames = ['Back', 'Quit']
        buttonTips = ['Returns to the Practice Menu',
                      'Exit the Application']
        
        self.labels = []
        self.labels += showText(self, 1/2, 5/16, 7/8, 7/16, 30, self.boundStyle, self.normalStyle,
                                     'Instructions:\n\n' + \
                                     '  You have two options: choose a file on your hard drive \n' + \
                                     '  or choose a Youtube URL to download from. \n\n' + \
                                     '    1. Choose a file \n' + \
                                     '        Choose your file, then click "transcribe." \n' + \
                                     '    2. Choose a Youtube URL \n' + \
                                     '        Choose you URL, then click "download". Once the \n' + \
                                     '        file is downloaded, click "transcribe." \n')
        self.labels += showBound(self, 1/2, 11/16, 1/5, 1/8, 30, self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           (11/8)*self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Back':        newButton.clicked.connect(self.onClickTranscribeMenu)
            elif buttonNames[index] == 'Quit':      newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initPracticeMenu(self):
        self.buttons = []
        buttonNames = ['Instructions', 'Record', 'Pick Script', 'Pick Start',
                       'Pick Period', 'Check Errors', 'Back to Start', 'Quit']
        buttonTips = ['Gives an explanation of what to do in this menu',
                      'Practice your speech!',
                      'Pick the script you want to practice',
                      'Pick the starting word at which you want to practice',
                      'Pick the length of time you want to practice',
                      'Compares the previous recording transcription to the selected script',
                      'Returns Practice Menu',
                      'Exit the Application']

        self.labels = []
        self.labels += showBound(self, 3/4, 3/4, 1/5, 3/8, 30, self.boundStyle, self.boundInStyle)
        self.labels += showPracticeInfo(self)
        self.labels += showLog(self)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width*(3/4) - newButton.width()/2 - 5,
                           self.height*(3/4) - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Instructions':        newButton.clicked.connect(self.onClickPracticeInstructions)
            elif buttonNames[index] == 'Record':            newButton.clicked.connect(self.onClickRecord)
            elif buttonNames[index] == 'Pick Script':       newButton.clicked.connect(self.onClickPickScript)
            elif buttonNames[index] == 'Pick Start':        newButton.clicked.connect(self.onClickPickStart)
            elif buttonNames[index] == 'Pick Period':       newButton.clicked.connect(self.onClickPickPeriod)
            elif buttonNames[index] == 'Check Errors':      newButton.clicked.connect(self.onClickCheckErrors)
            elif buttonNames[index] == 'Back to Start':     newButton.clicked.connect(self.onClickStart)
            elif buttonNames[index] == 'Quit':              newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    def initPracticeInstructions(self):
        self.buttons = []
        buttonNames = ['Back', 'Quit']
        buttonTips = ['Returns to the Practice Menu',
                      'Exit the Application']
        
        self.labels = []
        self.labels += showText(self, 1/2, 5/16, 7/8, 7/16, 30, self.boundStyle, self.normalStyle,
                                     'Instructions:\n\n' + \
                                     '  1. Select the period which you intend to record. \n'
                                     '  2. Click the record button and speak into your microphone. \n' + \
                                     '  3. Select a text document that the program will check against \n' + \
                                     '  4. Select the starting word in the text you would like to check \n' + \
                                     '  5. Check your errors \n')
        self.labels += showBound(self, 1/2, 11/16, 1/5, 1/8, 30, self.boundStyle, self.boundInStyle)
        
        for index in range(len(buttonNames)):
            newButton = QPushButton(buttonNames[index], self)
            newButton.setToolTip(buttonTips[index])
            newButton.move(self.width/2 - newButton.width()/2 - 5,
                           (11/8)*self.height/2 - (len(buttonNames)*newButton.height())/2 + index*newButton.height())
            if buttonNames[index] == 'Back':        newButton.clicked.connect(self.onClickPracticeMenu)
            elif buttonNames[index] == 'Quit':      newButton.clicked.connect(onClickQuit)
            self.buttons.append(newButton)

    #########################################################################################
    # Click Redirect
    #########################################################################################

    @pyqtSlot()
    def onClick(self):
        pass

    @pyqtSlot()
    def onClickStart(self):
        hideButtons(self.buttons)
        hideLabels(self.labels)
        self.initStart()
        showLabels(self.labels)
        showButtons(self.buttons)

    @pyqtSlot()
    def onClickTranscribeMenu(self):
        hideButtons(self.buttons)
        hideLabels(self.labels)
        self.initTranscribeMenu()
        showLabels(self.labels)
        showButtons(self.buttons)

    @pyqtSlot()
    def onClickTranscribeInstructions(self):
        hideButtons(self.buttons)
        hideLabels(self.labels)
        self.initTranscribeInstructions()
        showLabels(self.labels)
        showButtons(self.buttons)

    @pyqtSlot()
    def onClickPracticeMenu(self):
        hideButtons(self.buttons)
        hideLabels(self.labels)
        self.initPracticeMenu()
        showLabels(self.labels)
        showButtons(self.buttons)

    @pyqtSlot()
    def onClickPracticeInstructions(self):
        hideButtons(self.buttons)
        hideLabels(self.labels)
        self.initPracticeInstructions()
        showLabels(self.labels)
        showButtons(self.buttons)

    ###########################################################################
    # Click functions in Transcribe Menu
    ###########################################################################

    @pyqtSlot()
    def onClickChooseFile(self):
        file, okPressed = QInputDialog.getText(self, "File name input",
                'Type in the name of the file you want.\n' + \
                'The file should be located in the Audio folder,\n' + \
                'but you do not need to include "Audio" in the path.\n' + \
                'Do not forget the extension!',
                QLineEdit.Normal, "")
        if okPressed:
            self.audioFileName = 'Audio/' + file
            displayMessage(self, 'Name chosen: ' + self.audioFileName)
            self.updateTranscribeInfo()

    @pyqtSlot()
    def onClickChooseURL(self):
        url, okPressed = QInputDialog.getText(self, "URL input",
                'Type in the url of the Youtube video you want.\n' + \
                'The file will be downloaded to the Audio folder.',
                QLineEdit.Normal, "")
        if okPressed:
            self.url = url
            displayMessage(self, 'URL chosen: ' + self.url)
            self.updateTranscribeInfo()

    @pyqtSlot()
    def onClickTranscribe(self):
        if self.audioFileName == None:
            displayWarning(self, 'Error: no file chosen!')
            return
        
        response = displayQuestion(self, 'Do you want to proceed with the transcription?')
        if response == QMessageBox.No:
            return

        self.resetLog()
        fileList = os.listdir('Audio')
        if self.audioFileName.split('/')[1] in fileList:
            start = time.time()
            error = Transcribe.full_transcribe(self.audioFileName, self)
            if error != None:
                displayWarning(self, 'Error! : ' + error)
                return
            self.updateLog('    Operation time: %2.3f seconds' % (time.time() - start))
            displayMessage(self, 'No errors in transcription!')
            return
        displayWarning(self, 'Chosen file does not exist! Chose a different file.')

    @pyqtSlot()
    def onClickDownload(self):
        try:
            errorCode = Download.downloadYoutube(self.url)
            if isinstance(errorCode, str):
                self.audioFileName = errorCode
                self.updateTranscribeInfo()
                displayMessage(self, 'Downloaded and chose file: ' + self.audioFileName)
            elif errorCode == None:
                displayMessage(self, 'File downloaded, replaced previous file of same name.')
            elif errorCode == 0:
                displayWarning(self, 'Invalid url. Perhaps you spelled it wrong?')
            elif errorCode == 1:
                displayWarning(self, 'Unable to download. Perhaps video was taken down?')
        except:
            displayMessage(self, 'Download had unknown error. Please try again.')

    ###########################################################################
    # Click functions in Practice Mode
    ###########################################################################

    @pyqtSlot()
    def onClickRecord(self):
        response = displayQuestion(self, 'Would you like to use the previous recording?')
        if response == QMessageBox.No:
            displayMessage(self, 'The program will start recording when you press the "ok" button.')
            outputName = "Audio/output.wav"
            start = time.time()
            Recording.recordTo(outputName, self, self.period)
            error = Transcribe.full_transcribe(outputName, self)
            if error != None:
                displayWarning(self, 'Error! : ' + error)
                return
            self.resetLog()
            self.updateLog('    Operation time: %2.3f seconds\n' % (time.time() - start))
        if not os.path.exists('Audio/output/transcription.txt'):
            displayWarning(self, 'You have not made a recording yet!')
            return
        self.recordText = TextCheck.getText('Audio/output/transcription.txt')
        TextCheck.displayText(self)

    @pyqtSlot()
    def onClickPickScript(self):
        file, okPressed = QInputDialog.getText(self, "File name input",
                'Type in the name of the file you want the transcription of.\n' + \
                'Input the file name, not the transcript name.\n' + \
                'Do not forget the extension!',
                QLineEdit.Normal, self.audioFileName)

        if okPressed:
            try:
                file = fileToTranscript(file)
            except:
                displayWarning(self, 'Invalid file name!')
                
            if not os.path.isfile(file):
                displayWarning(self, 'File does not exist! Choose a different file.')
                return
            try:
                self.scriptName = file
                self.correctText = TextCheck.getText(file)
                self.numWords = len(self.correctText)
                self.updatePracticeInfo()
            except:
                displayWarning(self, 'File could not be opened!')
    
    @pyqtSlot()
    def onClickPickStart(self):
        if self.correctText == None:
            displayWarning(self, 'You have not yet selected a script!\n' + \
                                 'You must select your script before picking a starting point.')
            return
        
        num, okPressed = QInputDialog.getInt(self, "Pick Starting Point",
                "Pick what number word to start checking for memorization", QLineEdit.Normal, self.textStartMin)
        if okPressed:
            if num < 0:
                displayWarning(self, 'You cannot start at a negative word!')
                return
            elif num >= self.numWords:
                displayWarning(self, 'You cannot start at a word beyond \n' + \
                                     'the end of the transcript!')
                return
            self.textStart = num
            self.updatePracticeInfo()

    @pyqtSlot()
    def onClickPickPeriod(self):
        num, okPressed = QInputDialog.getInt(self, "Pick Record Time",
                "Pick the length of time you want to practice, in seconds", QLineEdit.Normal, self.periodMin)
        if okPressed:
            if num < 0:
                displayWarning(self, 'You cannot start at a negative word!')
                return
            elif num > 3600:
                displayWarning(self, 'Sorry, the time limit is one hour.')
                return
            self.period = num
            self.updatePracticeInfo()

    @pyqtSlot()
    def onClickCheckErrors(self):
        if self.correctText == None:
            displayWarning(self, 'You have not yet selected a script!\n' + \
                                 'You must select your script before picking a starting point.')
            return
        
        wordList = self.recordText.split(' ')
        textList = self.correctText.split(' ')[self.textStart:]
        textSet = set(textList)

        longCommonIndices = TextCheck.longestCommonIndices(wordList, textList, textSet)
        commonIndices = TextCheck.commonIndices(wordList, textList, textSet)
        unMatched = TextCheck.allUnmatchedIndices(wordList, textSet)
        correctRatio = TextCheck.correctWordRatio(wordList, textList, textSet)

        longCommonStrings = [' '.join(wordList[pair[0]:pair[1]]) for pair in sorted(list(longCommonIndices))]
        commonStrings = [' '.join(wordList[pair[0]:pair[1]]) for pair in sorted(list(commonIndices))]
        unmatchedWords = ', '.join([wordList[index] for index in sorted(list(unMatched))])

        self.resetLog()
        TextCheck.displayLongestCommon(self, longCommonStrings)
        TextCheck.displayCommon(self, commonStrings)
        TextCheck.displayUnmatched(self, unmatchedWords)
        TextCheck.displayCorrectRatio(self, correctRatio)
        
def onClickQuit():
    sys.exit(app.exec_())
    print('Thank you for using this application!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window(1000, 800)
    onClickQuit()
