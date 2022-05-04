from queue import Queue
from PySide2.QtWidgets import QApplication,  QTableWidgetItem, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PIL import Image

from resolution import Term, Sentence, KB
from tree import TreeCreator


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
        self.ui.Button_ShowPath.clicked.connect(self.showPath)
        self.ui.Button_Clear.clicked.connect(self.clear)
        self.ui.Text_Condition.setPlaceholderText("Every line represents a sentence.\
                                                  The relationship between line is AND.\n\
                                                   Function name is one upper case letter.\
                                                   Constant name is one upper case letter.\
                                                   Variable name is one lower case letter.\n\
                                                   Format like this:\
                                                   S(a,b)\
                                                   S(A,B) V F(c,D) \
                                                   ~S(A,B) V ~S(c,d)\
                                                   ")
        self.setupTable(self.ui.Table)
        self.ui.Button_ShowPath.setEnabled(False)

    def setupTable(self, table):
        """set table

        Args:
            table (_type_): _description_
        """
        table.setColumnWidth(0, 50)
        table.setColumnWidth(1, 160)
        table.setColumnWidth(2, 460)

    def start(self):
        """start resolution,read condition, create knowledge base, solve and show steps
        """
        self.ui.Table.clearContents()
        self.ui.Table.setRowCount(0)
        self.ui.Label_Result.clear()
        if self.ui.Text_Condition.toPlainText() == '':
            msg = QMessageBox(QMessageBox.Critical, 'Failed!',
                              'Please input condition!', QMessageBox.Ok, self.ui)
            msg.exec_()

        kb = self.readCondition()

        self.isSolved, self.final = kb.resolution()
        if self.isSolved:
            self.ui.Label_Result.setText('Resolution Successful!')
            self.ui.Label_Result.setStyleSheet('color: green')
        else:
            self.ui.Label_Result.setText('Resolution Failed!')
            self.ui.Label_Result.setStyleSheet('color: red')

        self.showSteps(kb)
        self.ui.Button_ShowPath.setEnabled(True)

    def clear(self):
        """clear all
        """
        self.ui.Text_Condition.clear()
        self.ui.Table.clearContents()
        self.ui.Table.setRowCount(0)
        self.ui.Label_Result.clear()
        self.ui.Button_ShowPath.setEnabled(False)

    def readCondition(self):
        """read condition from text box

        Returns:
            KB: knowledge base
        """
        kb = KB([])
        lines = self.ui.Text_Condition.toPlainText().split('\n')
        count = 0
        for line in lines:
            count += 1
            sentence = Sentence([], 'C'+str(count), 'Given')
            # split line by OR
            terms = line.split('V')
            for term in terms:
                # delete blank
                term = term.strip()
                # create term instance
                if term[0] == '~':
                    # if is upper case, it is a constant
                    if term[3].isupper():
                        kb.constantSet.add(term[3])
                    if term[5].isupper():
                        kb.constantSet.add(term[5])
                    term = Term(term[1], term[3], term[5], True)

                else:
                    if term[2].isupper():
                        kb.constantSet.add(term[2])
                    if term[4].isupper():
                        kb.constantSet.add(term[4])
                    term = Term(term[0], term[2], term[4], False)
                # add term to sentence
                sentence.append(term)
            # add sentence to KB
            kb.append(sentence)
        print(kb)
        return kb

    def showSteps(self, kb):
        """show steps in table

        Args:
            kb (KB): knowledge base
        """
        self.ui.Table.clearContents()

        count = 0
        for sentence in kb:
            count += 1
            self.ui.Table.insertRow(self.ui.Table.rowCount())
            self.ui.Table.setItem(count-1, 0, QTableWidgetItem(sentence.label))
            if sentence.source == 'Given':
                self.ui.Table.setItem(count-1, 1, QTableWidgetItem('Given'))
            else:
                if sentence.source[0] == 'Unify':
                    self.ui.Table.setItem(
                        count-1, 1, QTableWidgetItem('Unify '+sentence.source[1].label))
                else:
                    self.ui.Table.setItem(
                        count-1, 1, QTableWidgetItem((sentence.source[0].label+' '+sentence.source[1].label)))
            self.ui.Table.setItem(count-1, 2, QTableWidgetItem(str(sentence)))

    def showPath(self):
        """set and show path. Only show when resolution is successful
        """
        if not self.isSolved:
            msgBox = QMessageBox(QMessageBox.Critical, 'Failed!',
                                 'Resolution failed, can not show path!', QMessageBox.Ok, self.ui)
            msgBox.exec_()
        tree = TreeCreator()
        q = Queue()
        q.put(self.final)
        while not q.empty():
            node = q.get()
            if node.source != 'Given':
                # get parent
                if node.source[0] != 'Unify':
                    tree.setParent(node.source[0].label, node.label)
                    tree.setParent(node.source[1].label, node.label)
                    q.put(node.source[0])
                    q.put(node.source[1])
                else:
                    tree.setParent(node.source[1].label, node.label)
                    q.put(node.source[1])
        tree.create()
        self.showImg()

    def showImg(self):
        """show image by system default image viewer
        """
        filePath = 'img/tree.png'
        try:
            img = Image.open(filePath)
            img.show()
        except:
            self.ui.Text_Information.setText(
                "Error: Can't open image\nPlease check if you have begun to solve puzzle")


if __name__ == "__main__":
    app = QApplication([])
    # set style sheet

    # create window
    main = Resolutions()
    # show window
    main.ui.show()
    app.exec_()
