from PySide2.QtWidgets import QApplication,QFileDialog,QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QPixmap,QIcon
from PySide2.QtCore import Qt
from PIL import Image
from random import shuffle



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
        
    def selectImage(self):
        self.filePath, _  = QFileDialog.getOpenFileName(
            self.ui,             # 父窗口对象
            "选择你要上传的图片", # 标题
            r"../",        # 起始目录
            "图片类型 (*.png *.jpg)" # 选择类型过滤项，过滤内容在括号中
        )
        print(self.filePath)
        if self.filePath:
            image=QPixmap(self.filePath)
            self.ui.Label_Source.setPixmap(image.scaled(self.ui.Label_Source.size(), Qt.KeepAspectRatio))
            self.ui.Text_Information.setText("Image path:" + self.filePath)

    def detect(self):
        try:
            image = Image.open(self.filePath)
        except:
            msg = QMessageBox(QMessageBox.Critical, 'Failed!',
                              'Please select an image!', QMessageBox.Ok, self.ui)
            msg.exec_()
        else:
            # r_image = detect_image(image)
            # r_image.save('./predictimg.jpg')
            resultImg=QPixmap('./predictimg.jpg')
            
            self.ui.Label_Result.setPixmap(resultImg.scaled(self.ui.Label_Result.size(), Qt.KeepAspectRatio))
            


if __name__ == "__main__":
    app = QApplication([])

    # create window
    main = DetectionUI()
    # show window
    main.ui.show()
    app.exec_()
