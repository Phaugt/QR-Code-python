from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow,
            QMessageBox, QLabel, qApp, QPushButton, QRadioButton)
from PyQt5.QtCore import (QFile, Qt)
from PyQt5.QtGui import (QIcon, QPixmap)
from barcode import Code128
from barcode.writer import ImageWriter
import pyqrcode
import png, os, sys
from pyqrcode import QRCode

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'QRCODE.python.generator.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

qrgui = resource_path("./gui/main.ui")
qrlogo = resource_path("./gui/logo.png")
appbg = resource_path("./gui/app.png")
savedcodes = resource_path("./saved/")


#QR.png('pythonexplained.png', scale =  10)



class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        UIFile = QFile(qrgui)
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()

        bppbg = QPixmap(appbg)
        self.bgapp.setPixmap(bppbg)

        self.createqr.clicked.connect(self.cmdcreatecode)

    
    def cmdcreatecode(self):
        QRText = self.qrtext.toPlainText()
        try:
            if self.qrbox.isChecked():
                if QRText != "":
                    QR = pyqrcode.create(QRText)
                    QR.png(savedcodes+QRText+'.png', scale=8)
                    image = QPixmap(savedcodes+QRText+".png")
                    qrscaled = image.scaled(261, 261, Qt.KeepAspectRatio)
                    self.qrcode.setPixmap(qrscaled)

            elif self.barbox.isChecked():
                if QRText != "":
                    barout = Code128(QRText, writer=ImageWriter())
                    barout.save("saved/"+QRText+"-bar")
                    image = QPixmap("saved/"+QRText+"-bar"+".png")
                    qrscaled = image.scaled(261, 261, Qt.KeepAspectRatio)
                    self.qrcode.setPixmap(qrscaled)
        
        except Exception:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle("codegenerator")
            msgBox.setText("Error! code could not be created")
            msgBox.exec()


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(qrlogo))
window = GUI()
window.show()
app.exec_()
