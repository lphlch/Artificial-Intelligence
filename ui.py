from PySide2.QtWidgets import QApplication
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer
from PIL import Image

from main import solve


class EightDigitsUI:

    def __init__(self):

        self.ui = QUiLoader().load('form.ui')
        

        self.ui.Button_Show.clicked.connect(self.showImg)
        self.ui.Button_NextStep.clicked.connect(self.nextStep)
        self.ui.Button_PerviousStep.clicked.connect(self.perviousStep)
        self.ui.Button_Auto.clicked.connect(self.autoStartTimer)
        self.ui.Button_Init.clicked.connect(self.initLCD)
        self.ui.Check_GetTree.clicked.connect(self.clickCheckGetTree)

        self.LCDList = [self.ui.LCD_1, self.ui.LCD_2, self.ui.LCD_3,
                        self.ui.LCD_4, self.ui.LCD_5, self.ui.LCD_6, self.ui.LCD_7, self.ui.LCD_8, self.ui.LCD_9]

        self.currentStep = 0
        self.path = []

        # set ui
        self.ui.Button_Show.setEnabled(False)
        self.ui.Button_Auto.setEnabled(False)
        self.ui.Button_NextStep.setEnabled(False)
        self.ui.Button_PerviousStep.setEnabled(False)
        self.updateLCD([1, 2, 3, 4, 5, 6, 7, 8, 9])

    def updateLCD(self, step):
        # number change
        for i in range(0, 9):
            self.LCDList[i].display(step[i])

        # color change
        for num in self.LCDList:
            if num.value() == 9:
                num.hide()
            else:
                num.show()
                if num.value() == 1:
                    num.setStyleSheet("color:red")
                if num.value() == 2:
                    num.setStyleSheet("color:blue")
                if num.value() == 3:
                    num.setStyleSheet("color:green")
                if num.value() == 4:
                    num.setStyleSheet("color:yellow")
                if num.value() == 5:
                    num.setStyleSheet("color:cyan")
                if num.value() == 6:
                    num.setStyleSheet("color:magenta")
                if num.value() == 7:
                    num.setStyleSheet("color:black")
                if num.value() == 8:
                    num.setStyleSheet("color:white")

    def showImg(self):
        # show image by system default image viewer
        filePath = 'img/tree.png'
        try:
            img = Image.open(filePath)
            img.show()
        except:
            self.ui.Text_Information.setText("Error: Can't open image\nPlease check if you have begun to solve puzzle")
            
    def initLCD(self):
        solution = {}

        self.currentStep = 0
        self.ui.Progress_Steps.setValue(0)
        
        # this is just for test if auto timer exist
        try:
            self.autoTimer.stop()
        except:
            pass
        
        function=self.ui.Combo_Function.currentText()
        
        # check if need to get tree view
        if self.ui.Check_GetTree.isChecked():
            solution = solve(isTreeNeed=True,function=function)
        else:
            solution = solve(isTreeNeed=False,function=function)

        self.path = solution['path']
        step = self.path[0]
        self.updateLCD(step)

        # check if is solvable
        if not solution['isSolvable']:
            self.ui.Button_PerviousStep.setEnabled(False)
            self.ui.Button_NextStep.setEnabled(False)
            self.ui.Button_Auto.setEnabled(False)
            self.ui.Text_Information.setText("No solution")
            return

        # information show
        self.ui.Text_Information.setText("There are {} steps\n\nGenerated nodes: {}\nExpanded nodes:{}\n\nTime used: {} ms"
                                         .format(len(self.path)-1, solution['generationCount'], solution['expandCount'], int(solution['time']*1000)))

        # set ui ability
        if self.ui.Check_GetTree.isChecked():
            self.ui.Button_Show.setEnabled(True)
        self.ui.Button_PerviousStep.setEnabled(False)
        self.ui.Button_NextStep.setEnabled(True)
        self.ui.Button_Auto.setEnabled(True)

    def nextStep(self):
        self.currentStep += 1

        # set ui
        self.ui.Button_PerviousStep.setEnabled(True)
        self.ui.Progress_Steps.setValue(
            self.currentStep/(len(self.path)-1)*100)

        step = self.path[self.currentStep]
        self.updateLCD(step)

        # ! there is no more step, and if statement has to be here
        if self.currentStep >= len(self.path)-1:
            self.currentStep = len(self.path)-1
            self.ui.Button_NextStep.setEnabled(False)
            self.ui.Button_Auto.setEnabled(False)

    def perviousStep(self):

        self.currentStep -= 1

        # set ui
        self.ui.Button_NextStep.setEnabled(True)
        self.ui.Button_Auto.setEnabled(True)
        self.ui.Progress_Steps.setValue(
            self.currentStep/(len(self.path)-1)*100)

        step = self.path[self.currentStep]
        self.updateLCD(step)

        if self.currentStep <= 0:
            self.currentStep = 0
            self.ui.Button_PerviousStep.setEnabled(False)
            
    def clickCheckGetTree(self):
        if self.ui.Check_GetTree.isChecked():
            self.ui.Button_Show.setEnabled(True)
        else:
            self.ui.Button_Show.setEnabled(False)

    def autoStartTimer(self):
        print("Timer start")
        self.autoTimer = QTimer()
        self.autoTimer.start(350)
        self.autoTimer.timeout.connect(self.autoNextStep)

    def autoNextStep(self):
        print("time reached")

        self.nextStep()

        if self.currentStep >= len(self.path)-1:
            print("Timer stop")
            self.autoTimer.stop()

    # def test(self):
    #     self.ui.LCD_4.display(4)
    #     self.ui.LCD_5.hide()


# global path
# path = [[4, 1, 2, 5, 9, 3, 7, 8, 6], [4, 1, 2, 9, 5, 3, 7, 8, 6], [9, 1, 2, 4, 5, 3, 7, 8, 6],
#         [1, 9, 2, 4, 5, 3, 7, 8, 6], [1, 2, 9, 4, 5,
#                                       3, 7, 8, 6], [1, 2, 3, 4, 5, 9, 7, 8, 6],
#         [1, 2, 3, 4, 5, 6, 7, 8, 9]]

app = QApplication([])
# set style sheet
app.setStyleSheet(open('other/qss.css', 'r').read())
# create window
window = EightDigitsUI()
# show window
window.ui.show()
app.exec_()
