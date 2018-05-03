from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
import ImageEdit

def showBackground(app):
    """Takes the background file name in the __init__ function."""
    labelBack = QLabel(app)
    name = ImageEdit.resize_image(app.background, (app.width, app.height))
    pixmap = QPixmap(name)
    labelBack.setPixmap(pixmap)
