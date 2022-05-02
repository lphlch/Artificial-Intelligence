from PySide2.QtWidgets import QApplication,QTableView,QTableWidgetItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QTimer
from PySide2.QtGui import QPixmap,QIcon,QStandardItemModel
from PIL import Image

from resolution import Term,Sentence,KB

class Resolutions:
    """main UI
    """

    def __init__(self):
        """init UI
        """

        self.ui = QUiLoader().load('ui/main.ui')
        self.ui.setWindowIcon(QIcon('img/icon.png'))
        self.ui.setStyleSheet(open('other/qss.css', 'r').read())
        
        self.ui.Button_Start.clicked.connect(self.start)
        self.ui.Button_ShowTree.clicked.connect(self.showTree)
        self.ui.Button_Clear.clicked.connect(self.clear)
        self.ui.Text_Condition.setPlaceholderText("""
                                                   Every line represents a sentence.
                                                   The relationship between line is AND.
                                                   Format like this:
                                                   S(a,b)
                                                   S(A,B) V F(c,D) 
                                                   ~S(A,B) V ~S(c,d)
                                                   """)
        self.setupTable(self.ui.Table)
        
    def setupTable(self,table):
        table.setColumnWidth(0,40)
        table.setColumnWidth(1,120)
        table.setColumnWidth(2,300)

    
    def start(self):
        self.ui.Table.clearContents()
        self.ui.Label_Result.clear()
        kb=self.readCondition()
        kb.resolution()
        self.showSteps(kb)
    
    def showTree(self):
        pass
    
    def clear(self):
        self.ui.Text_Condition.clear()
        self.ui.Table.clearContents()
        self.ui.Label_Result.clear()
        
        
    def readCondition(self):
        kb=KB([])
        lines=self.ui.Text_Condition.toPlainText().split('\n')
        count=0
        for line in lines:
            count+=1
            sentence=Sentence([],'C'+str(count),'Given')
            # split line by OR
            terms=line.split('V')
            for term in terms:
                # delete blank
                term=term.strip()
                # create term instance
                if term[0]=='~' :
                    term=Term(term[1],term[3],term[5],True)
                else:
                    term=Term(term[0],term[2],term[4],False)
                # add term to sentence
                sentence.append(term)
            # add sentence to KB
            kb.append(sentence)
        
        print(kb)
        return kb
        
    def showSteps(self,kb):
        self.ui.Table.clearContents()

        count=0
        for sentence in kb:
            count+=1
            self.ui.Table.insertRow(self.ui.Table.rowCount())
            self.ui.Table.setItem(count-1,0,QTableWidgetItem(sentence.label))
            self.ui.Table.setItem(count-1,1,QTableWidgetItem(str(sentence.source)))
            self.ui.Table.setItem(count-1,2,QTableWidgetItem(str(sentence)))
            


if __name__ == "__main__":
    app = QApplication([])
    # set style sheet

    # create window
    main = Resolutions()
    # show window
    main.ui.show()
    app.exec_()
