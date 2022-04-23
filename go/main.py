from PySide2.QtWidgets import QApplication,QWidget,QMainWindow,QLabel,QVBoxLayout,QPushButton,QTextBrowser
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer,Qt,QPoint,QSize,QRect,QCoreApplication,QMetaObject
from PySide2.QtGui import QPixmap,QPainter,QPen,QColor,QImage,QFont
from PIL import Image
from random import shuffle

class Gobang(QMainWindow):
    """main UI
    """    
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 650)
        Form.setMinimumSize(QSize(800, 650))
        Form.setMaximumSize(QSize(800, 650))
        self.Label_Title = QLabel(Form)
        self.Label_Title.setObjectName(u"Label_Title")
        self.Label_Title.setGeometry(QRect(50, 0, 701, 71))
        font = QFont()
        font.setFamily(u"Lucida Handwriting")
        font.setPointSize(24)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Label_Title.setFont(font)
        self.Label_Title.setStyleSheet(u"font: 24pt \"Lucida Handwriting\";")
        self.Label_Title.setAlignment(Qt.AlignCenter)
        self.Label_Copyright = QLabel(Form)
        self.Label_Copyright.setObjectName(u"Label_Copyright")
        self.Label_Copyright.setGeometry(QRect(50, 610, 691, 41))
        self.Label_Copyright.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(600, 450, 139, 65))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Button_Withdraw = QPushButton(self.layoutWidget)
        self.Button_Withdraw.setObjectName(u"Button_Withdraw")

        self.verticalLayout.addWidget(self.Button_Withdraw)

        self.Button_Reset = QPushButton(self.layoutWidget)
        self.Button_Reset.setObjectName(u"Button_Reset")

        self.verticalLayout.addWidget(self.Button_Reset)

        self.Text_Information = QTextBrowser(Form)
        self.Text_Information.setObjectName(u"Text_Information")
        self.Text_Information.setGeometry(QRect(560, 150, 221, 211))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.Label_Title.setText(QCoreApplication.translate("Form", u"Gobang", None))
        self.Label_Copyright.setText(QCoreApplication.translate("Form", u"Copyright \u00a9 2022 LPH. All Rights Reserved", None))
        self.Button_Withdraw.setText(QCoreApplication.translate("Form", u"Withdraw", None))
        self.Button_Reset.setText(QCoreApplication.translate("Form", u"Restart", None))
    # retranslateUi

    def paintEvent(self,e):
        leftMargin=30
        topMargin=80
        print("draw")
        qp = QPainter(self)

        
        board=QImage("img/board.png")
        qp.drawImage(leftMargin,topMargin,board)
        black=QImage("img/black.png")
        qp.drawImage(leftMargin,topMargin,black)
   
            
    def a(self):
        print("aaaaa")
        

        
    
    
        
        



if __name__ == "__main__":
    app = QApplication([])
    # set style sheet

    # create window
    main = Gobang()
    # main.setWindowIcon('img/icon.png')
    main.show()
    app.exec_()
