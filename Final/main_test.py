from PySide2.QtWidgets import QApplication,QFileDialog,QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap,QIcon
from PySide2.QtCore import Qt
from PIL import Image

class DetectionUI:
    """stats UI
    """

    def __init__(self):
        """init stats UI
        """
        self.ui = QUiLoader().load('ui/main.ui')
        self.ui.setStyleSheet(open('ui/qss.css', 'r').read())
        self.ui.setWindowIcon = QIcon('img/icon.png')
        self.ui.Button_Select.clicked.connect(self.selectImage)
        self.ui.Button_Detect.clicked.connect(self.detect)
        self.ui.Slider_Tran.valueChanged.connect(self.changeSlider)
        
    def selectImage(self):
        self.filePath, _  = QFileDialog.getOpenFileName(
            self.ui,
            "选择你要检测的图片", 
            r"../",        
            "图片类型 (*.png *.jpg)"
        )
        print(self.filePath)
        if self.filePath:
            image=QPixmap(self.filePath)
            self.ui.Label_Source.setPixmap(image.scaled(self.ui.Label_Source.size(), Qt.KeepAspectRatio))
            self.ui.Text_Information.setText("Image path:" + self.filePath)

    def detect(self):
        try:
            self.image = Image.open(self.filePath)
        except:
            msg = QMessageBox(QMessageBox.Critical, 'Failed!',
                              'Please select an image!', QMessageBox.Ok, self.ui)
            msg.exec_()
        else:
            self.r_image = detect_image(image)
            self.r_image.save('./predictimg.jpg')
            self.resultImg=QPixmap('./predictimg.jpg')
            self.showImg(self.resultImg)
            
    def changeSlider(self):
        try:
            tran=self.ui.Slider_Tran.value()/100    # transparency
            # call image processing function
            img=blend_image(self.image,self.r_image,tran)
            img.save('./mixed.jpg')
            print("mixed img saved")
            # show
            mixedImg=QPixmap('./mixed.jpg')
            self.showImg(mixedImg)
        except:
            msg = QMessageBox(QMessageBox.Critical, 'Failed!',
                              'Please select an image!', QMessageBox.Ok, self.ui)
            msg.exec_()
        
        
    def showImg(self,img):
        self.ui.Label_Result.setPixmap(img.scaled(self.ui.Label_Result.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication([])

    # create window
    main = DetectionUI()
    # show window
    main.ui.show()
    app.exec_()
