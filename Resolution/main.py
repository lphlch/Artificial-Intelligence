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
                                                   S(A,B) OR F(c,D) 
                                                   !S(A,B) OR !S(c,d)
                                                   """)
        self.setupTable(self.ui.Table)
        
    def setupTable(self,table):
        table.setColumnWidth(0,50)
        table.setColumnWidth(1,100)
        table.setColumnWidth(2,320)

    
    def start(self):
        conditions=self.readCondition()
        self.showConditions(conditions)
    
    def showTree(self):
        pass
    
    def clear(self):
        self.ui.Text_Condition.clear()
        self.ui.Table.clearContents()
        self.ui.Label_Result.clear()
        
        
    def readCondition(self):
        kb=KB([])
        lines=self.ui.Text_Condition.toPlainText().split('\n')
        for line in lines:
            sentence=Sentence([])
            # split line by OR
            terms=line.split('OR')
            for term in terms:
                # delete blank
                term=term.strip()
                # create term instance
                if term[0]=='!' :
                    term=Term(term[1],term[3],term[5],True)
                else:
                    term=Term(term[0],term[2],term[4],False)
                # add term to sentence
                sentence.append(term)
            # add sentence to KB
            kb.append(sentence)
        
        print(kb)
        return kb
        
    def showConditions(self,conditions):
        # self.ui.Table.insertRow(self.ui.Table.rowCount()+1)
        # self.ui.Table.clearContents()
        # item=QTableWidgetItem()
        # item.setText('sentence')
        # self.ui.Table.setItem(0,0,QTableWidgetItem(item))
        count=0
        for sentence in conditions:
            count+=1
            s='C'+str(count)+': '+str(sentence)
            self.ui.Table.insertRow(self.ui.Table.rowCount())
            itemID=QTableWidgetItem()
            itemID.setText(s)
            self.ui.Table.setItem(count-1,0,QTableWidgetItem('C'+str(count)))
            self.ui.Table.setItem(count-1,1,QTableWidgetItem('Given'))
            self.ui.Table.setItem(count-1,2,QTableWidgetItem(str(sentence)))
            


if __name__ == "__main__":
    app = QApplication([])
    # set style sheet

    # create window
    main = Resolutions()
    # show window
    main.ui.show()
    app.exec_()
