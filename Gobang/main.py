from threading import Thread
from PySide2.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QVBoxLayout, QPushButton, QTextBrowser, QMessageBox, QComboBox, QLCDNumber
from PySide2.QtCore import Qt, QSize, QRect, QCoreApplication, QMetaObject, Signal, QObject
from PySide2.QtGui import QPainter, QImage, QFont, QIcon

from board import MAXSIZE, board, EASY, NORMAL, HARD, MASTER, deepcopy
global EACH_POS
EACH_POS = 102.7


class AiSignal(QObject):
    aiWin = Signal()
    aiDone = Signal()


aiSignal = AiSignal()


class Gobang(QMainWindow):
    """main UI
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(open('other/qss.css', 'r').read())
        self.setWindowIcon(QIcon('img/icon.png'))
        self.humanAction = True

        self.Button_Withdraw.clicked.connect(self.withdraw)
        self.Combo_Difficulty.currentIndexChanged.connect(
            self.changeDifficulty)
        self.Button_Reset.clicked.connect(self.reset)
        aiSignal.aiDone.connect(self.aiDone)
        aiSignal.aiWin.connect(self.aiWin)

        levelText = self.Combo_Difficulty.currentText()
        self.level = self.getLevel(levelText)
        self.whitePos = (None, None)
        self.reset()

    def setupUi(self, Gobang):
        if not Gobang.objectName():
            Gobang.setObjectName(u"Gobang")
        Gobang.resize(800, 650)
        Gobang.setMinimumSize(QSize(800, 650))
        Gobang.setMaximumSize(QSize(800, 650))
        self.Label_Title = QLabel(Gobang)
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
        self.Label_Copyright = QLabel(Gobang)
        self.Label_Copyright.setObjectName(u"Label_Copyright")
        self.Label_Copyright.setGeometry(QRect(50, 610, 691, 41))
        self.Label_Copyright.setAlignment(Qt.AlignCenter)
        self.layoutWidget = QWidget(Gobang)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(560, 480, 211, 111))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Button_Withdraw = QPushButton(self.layoutWidget)
        self.Button_Withdraw.setObjectName(u"Button_Withdraw")

        self.verticalLayout.addWidget(self.Button_Withdraw)

        self.Button_Reset = QPushButton(self.layoutWidget)
        self.Button_Reset.setObjectName(u"Button_Reset")

        self.verticalLayout.addWidget(self.Button_Reset)

        self.Text_Information = QTextBrowser(Gobang)
        self.Text_Information.setObjectName(u"Text_Information")
        self.Text_Information.setGeometry(QRect(560, 130, 211, 221))
        self.Label_SelectFunction = QLabel(Gobang)
        self.Label_SelectFunction.setObjectName(u"Label_SelectFunction")
        self.Label_SelectFunction.setGeometry(QRect(560, 410, 201, 31))
        self.Label_SelectFunction.setWordWrap(True)
        self.Combo_Difficulty = QComboBox(Gobang)
        self.Combo_Difficulty.addItem("")
        self.Combo_Difficulty.addItem("")
        self.Combo_Difficulty.addItem("")
        self.Combo_Difficulty.addItem("")
        self.Combo_Difficulty.setObjectName(u"Combo_Difficulty")
        self.Combo_Difficulty.setGeometry(QRect(560, 440, 211, 31))
        self.Combo_Difficulty.setFocusPolicy(Qt.WheelFocus)
        self.Combo_Difficulty.setAutoFillBackground(False)
        self.Combo_Difficulty.setSizeAdjustPolicy(
            QComboBox.AdjustToContentsOnFirstShow)
        self.label = QLabel(Gobang)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(560, 380, 141, 21))
        self.LCD_Value = QLCDNumber(Gobang)
        self.LCD_Value.setObjectName(u"LCD_Value")
        self.LCD_Value.setGeometry(QRect(700, 370, 71, 41))
        self.Label_Turn = QLabel(Gobang)
        self.Label_Turn.setObjectName(u"Label_Turn")
        self.Label_Turn.setGeometry(QRect(560, 70, 211, 51))
        font1 = QFont()
        font1.setFamily(u"Agency FB")
        font1.setPointSize(16)
        font1.setBold(True)
        font1.setWeight(75)
        self.Label_Turn.setFont(font1)
        self.Label_Turn.setTextFormat(Qt.AutoText)
        self.Label_Turn.setAlignment(Qt.AlignCenter)
        self.Label_Turn.setWordWrap(True)

        self.retranslateUi(Gobang)

        QMetaObject.connectSlotsByName(Gobang)
    # setupUi

    def retranslateUi(self, Gobang):
        Gobang.setWindowTitle(
            QCoreApplication.translate("Gobang", u"Gobang", None))
        self.Label_Title.setText(
            QCoreApplication.translate("Gobang", u"Gobang", None))
        self.Label_Copyright.setText(QCoreApplication.translate(
            "Gobang", u"Copyright \u00a9 2022 LPH. All Rights Reserved", None))
        self.Button_Withdraw.setText(
            QCoreApplication.translate("Gobang", u"Withdraw", None))
        self.Button_Reset.setText(
            QCoreApplication.translate("Gobang", u"Restart", None))
        self.Label_SelectFunction.setText(
            QCoreApplication.translate("Gobang", u"Select difficulty:", None))
        self.Combo_Difficulty.setItemText(
            0, QCoreApplication.translate("Gobang", u"Easy", None))
        self.Combo_Difficulty.setItemText(
            1, QCoreApplication.translate("Gobang", u"Normal", None))
        self.Combo_Difficulty.setItemText(
            2, QCoreApplication.translate("Gobang", u"Hard", None))
        self.Combo_Difficulty.setItemText(
            3, QCoreApplication.translate("Gobang", u"Master", None))

        self.Combo_Difficulty.setCurrentText(
            QCoreApplication.translate("Gobang", u"Easy", None))
        self.Combo_Difficulty.setProperty("placeholderText", "")
        self.label.setText(QCoreApplication.translate(
            "Gobang", u"Evaluation value\uff1a", None))
        self.Label_Turn.setText(QCoreApplication.translate(
            "Gobang", u"YOUR TURN!", None))
    # retranslateUi

    def withdraw(self):
        """withdraw last step
        """        
        if self.humanAction == False:
            msgBox = QMessageBox(QMessageBox.Warning, 'Wait',
                                 'You must wait AI', QMessageBox.Ok, self)
            msgBox.exec_()
            return
        if self.currBoard.previous is None:
            msgBox = QMessageBox(QMessageBox.Critical, 'Are you kidding?',
                                 'The board is already empty!', QMessageBox.Ok, self)
            msgBox.exec_()
            return
        self.currBoard = self.currBoard.previous
        self.updateLCD(self.currBoard.evaluate())
        self.Text_Information.append("Withdraw!")
        self.update()

    def reset(self):
        """reset board
        """        
        if self.humanAction == False:
            msgBox = QMessageBox(QMessageBox.Warning, 'Wait',
                                 'You must wait AI', QMessageBox.Ok, self)
            msgBox.exec_()
            return
        self.Text_Information.clear()
        self.updateLCD(0)
        self.currBoard = board([['O']*15 for _ in range(15)], self.level)
        self.update()   # clear the board

    def aiWin(self):
        """signal process for AI win
        """        
        msgBox = QMessageBox(QMessageBox.Information,
                             'WHITE win', 'You LOSE!', QMessageBox.Ok, self)
        msgBox.exec_()
        self.humanAction = True

    def aiDone(self):
        """signal process for AI done
        """        
        self.humanAction = True

    def getLevel(self, levelText):
        """convert level text to level number

        Args:
            levelText (str): text of level

        Returns:
            int: int
        """        
        if levelText == 'Easy':
            return EASY
        elif levelText == 'Normal':
            return NORMAL
        elif levelText == 'Hard':
            return HARD
        elif levelText == 'Master':
            return MASTER

    def changeDifficulty(self):
        """change difficulty
        """        
        self.level = self.getLevel(self.Combo_Difficulty.currentText())

    def paintEvent(self, e):
        """override paintEvent to draw the board

        Args:
            e (_type_): _description_
        """        
        leftMargin = 30
        topMargin = 80
        # print("draw")
        qp = QPainter(self)

        board = QImage("img/board.png")
        qp.drawImage(leftMargin, topMargin, board)
        black = QImage("img/black.png")
        white = QImage("img/white.png")
        bR = QImage("img/blackRed.png")
        wR = QImage("img/whiteRed.png")

        for x in range(MAXSIZE):
            for y in range(MAXSIZE):
                if self.currBoard.status[x][y] == 'X':
                    qp.drawImage((x*EACH_POS/3)+leftMargin,
                                 (y*EACH_POS/3)+topMargin, black)
                elif self.currBoard.status[x][y] == '@':
                    qp.drawImage((x*EACH_POS/3)+leftMargin,
                                 (y*EACH_POS/3)+topMargin, white)

        lastStepPos = self.currBoard.whitePos
        if lastStepPos != (None, None):
            if self.currBoard.status[lastStepPos[0]][lastStepPos[1]] == 'X':
                qp.drawImage((lastStepPos[0]*EACH_POS/3)+leftMargin,
                             (lastStepPos[1]*EACH_POS/3)+topMargin, bR)
            elif self.currBoard.status[lastStepPos[0]][lastStepPos[1]] == '@':
                qp.drawImage((lastStepPos[0]*EACH_POS/3)+leftMargin,
                             (lastStepPos[1]*EACH_POS/3)+topMargin, wR)
        qp.end()

    def mousePressEvent(self, e) -> None:
        """override mousePressEvent to handle mouse click

        Args:
            e (_type_): _description_
        """        
        if e.buttons() == Qt.LeftButton and self.humanAction:
            x = e.x()
            y = e.y()
            posX = posY = -1
            if x >= 30 and x <= 530 and y >= 80 and y <= 580:
                posX = int((x-30)/EACH_POS*3)
                posY = int((y-80)/EACH_POS*3)

            print("click x:", e.x(), "y:", e.y(), "posX:", posX, "posY:", posY)
            if posX != -1 and posY != -1:
                # update status
                # check if the position is empty
                if self.currBoard.status[posX][posY] == 'O':

                    # make new board
                    self.Text_Information.append(
                        "BLACK: x:"+str(posX)+" y:"+str(posY))
                    newStatus = deepcopy(self.currBoard.status)
                    newBoard = board(newStatus, self.level,
                                     self.currBoard, (posX, posY))
                    newBoard.status[posX][posY] = 'X'
                    self.currBoard = newBoard

                    self.update()
                    isBlackWin = self.currBoard.isFinish()
                    if isBlackWin:
                        msgBox = QMessageBox(
                            QMessageBox.Information, 'BLACK win', 'You WIN!', QMessageBox.Ok, self)
                        msgBox.exec_()
                    else:
                        self.humanAction = False
                        thread = Thread(target=self.aiMove)
                        # self.aiMove()
                        thread.start()

    def updateLCD(self, value):
        """update LCD display

        Args:
            value (_type_): _description_
        """        
        if(value >= 0):
            self.LCD_Value.setSegmentStyle(QLCDNumber.Flat)
            self.LCD_Value.setStyleSheet("color: rgb(255, 0, 0);")

        else:
            self.LCD_Value.setSegmentStyle(QLCDNumber.Flat)
            self.LCD_Value.setStyleSheet("color: rgb(0, 255, 0);")
        self.LCD_Value.display(-value)

    def aiMove(self):
        """ai move process
        """        
        # let ui pause
        self.Label_Turn.setText(
            QCoreApplication.translate("Form", u"AI TURN...", None))
        self.update()

        # get ai move
        aiPos, value = self.currBoard.search()
        # put ai move
        newStatus = self.currBoard.status
        newStatus[aiPos[0]][aiPos[1]] = '@'
        newBoard = board(self.currBoard.status,
                         self.level, self.currBoard, aiPos)
        self.currBoard.whitePos = aiPos

        # update LCD
        self.updateLCD(value)

        # check if ai win
        isWhiteWin = newBoard.isFinish()
        if isWhiteWin:
            aiSignal.aiWin.emit()

        # show ai move
        self.Text_Information.append(
            "WHITE: x:"+str(aiPos[0])+" y:"+str(aiPos[1]))

        self.Label_Turn.setText(
            QCoreApplication.translate("Form", u"YOUR TURN!", None))
        self.update()
        aiSignal.aiDone.emit()


if __name__ == "__main__":
    app = QApplication([])
    # set style sheet

    # create window
    main = Gobang()
    # main.setWindowIcon('img/icon.png')
    main.show()
    app.exec_()
