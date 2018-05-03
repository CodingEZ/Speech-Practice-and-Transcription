from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
import math

CHARFIT = 25

def setCharFit(length):
    global CHARFIT
    CHARFIT = length // 24

def showText(app, xFactor, yFactor, widthFactor, heightFactor, width, styleBound, styleText, text, textCenter=True):
    """Shows text with surrounding box"""
    labelOut = QLabel(app)     # outside label
    labelOut.resize(app.width*widthFactor + width, app.height*heightFactor + width)
    labelOut.move(app.width*xFactor - labelOut.width()/2, app.height*yFactor - labelOut.height()/2)
    labelOut.setStyleSheet(styleBound)

    labelIn = QLabel(app)      # inside label, with text
    labelIn.resize(app.width*widthFactor, app.height*heightFactor)
    labelIn.move(app.width*xFactor - labelIn.width()/2, app.height*yFactor - labelIn.height()/2)
    labelIn.setStyleSheet(styleText)
    if textCenter:
        labelIn.setAlignment(Qt.AlignCenter)
    else:
        labelIn.setAlignment(Qt.AlignLeft)
    labelIn.setText(text)
    return [labelOut, labelIn]

def showBound(app, xFactor, yFactor, widthFactor, heightFactor, width, styleBound, styleBoundIn):
    """Shows surrounding box"""
    labelBound = QLabel(app)   # outside label
    labelBound.resize(app.width*widthFactor + width, app.height*heightFactor + width)
    labelBound.move(app.width*xFactor - labelBound.width()/2, app.height*yFactor - labelBound.height()/2)
    labelBound.setStyleSheet(styleBound)
    
    labelBoundIn = QLabel(app) # inside label
    labelBoundIn.resize(app.width*widthFactor, app.height*heightFactor)
    labelBoundIn.move(app.width*xFactor - labelBoundIn.width()/2, app.height*yFactor - labelBoundIn.height()/2)
    labelBoundIn.setStyleSheet(styleBoundIn)
    return [labelBound, labelBoundIn]

def showLog(app):
    return showText(app, 1/2, 7/24, 3/4, 2/5, 30, app.boundStyle, app.logStyle, app.log, False)

def showTranscribeInfo(app):
    if app.url != None:
        pieces = [app.url[i*CHARFIT:(i+1)*CHARFIT] for i in range(math.ceil(len(app.url)/CHARFIT))]
        showUrl = '\n'.join(pieces)
    else:
        showUrl = str(app.url)
    app.transcribeInfo = "Chosen file name: \n" + str(app.audioFileName) + '\n\n' + \
                         "Chosen URL: \n" + showUrl
    return showText(app, 1/3, 3/4, 2/5, 1/3, 30, app.boundStyle, app.logStyle, app.transcribeInfo)

def showPracticeInfo(app):
    app.practiceInfo = "Chosen script: \n" + str(app.scriptName) + '\n\n' + \
                       "Chosen starting word number: \n" + str(app.textStart) + '\n\n' + \
                       "Chosen period length: \n" + str(app.period)
    return showText(app, 1/3, 3/4, 2/5, 1/3, 30, app.boundStyle, app.logStyle, app.practiceInfo)
