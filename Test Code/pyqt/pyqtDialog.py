import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon
 
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Input file name'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.initUI()
 
    def initUI(self):
        self.getText()
        self.show()
 
    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Input file name", "Input the file name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
