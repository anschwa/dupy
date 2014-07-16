from sys import exit, argv
from PySide import QtGui, QtCore


class Dupy(QtGui.QWidget):

    def __init__(self):
        super(Dupy, self).__init__()
        self.initUI()

    def initUI(self):
        # self.center()
        self.setGeometry(1400, 250, 500, 400)  # set for development
        self.setAcceptDrops(True)
        self.setWindowTitle('Dupy')

        # Layout
        hbox = QtGui.QHBoxLayout(self)

        self.leftSide = QtGui.QFrame(self)
        self.leftLayout()

        self.rightSide = QtGui.QFrame(self)
        self.rightLayout()

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.leftSide)
        splitter.addWidget(self.rightSide)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        hbox.addWidget(splitter)
        self.setLayout(hbox)

    def leftLayout(self):
        # Elements
        empty = QtGui.QLabel("")  # empty elements can be useful

        addButton = QtGui.QPushButton("Add a directory")
        addLabel = QtGui.QLabel("...or drag and drop one here.")
        addLabel.setAlignment(QtCore.Qt.AlignCenter)

        pathList = QtGui.QListWidget()
        pathList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        pathList.addItem('/path/to/test/')
        pathList.setMaximumHeight(125)

        removeButton = QtGui.QPushButton("Remove")
        clearButton = QtGui.QPushButton("Clear")

        # Layout
        leftGrid = QtGui.QGridLayout()
        leftGrid.setSpacing(10)

        leftGrid.addWidget(addButton, 1, 0, 1, 2)
        leftGrid.addWidget(addLabel, 2, 0, 1, 2)
        leftGrid.addWidget(pathList, 3, 0, 1, 2)
        leftGrid.addWidget(removeButton, 4, 0)
        leftGrid.addWidget(clearButton, 4, 1)

        # take up remaining space with an empty label
        leftGrid.addWidget(empty, 5, 0, 1000, 2)  # this is kind of a bug

        self.leftSide.setLayout(leftGrid)

    def rightLayout(self):
        # Elements
        empty = QtGui.QLabel("")  # empty elements can be useful

        findButton = QtGui.QPushButton("Find duplicates")
        resultCombo = QtGui.QComboBox()
        resultCombo.addItem("All")
        resultCombo.addItem("Dir One")
        resultCombo.addItem("Dir Two")

        resultEdit = QtGui.QTextEdit()
        resultEdit.setReadOnly(True)

        self.resultList = QtGui.QListWidget()
        self.resultList.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)

        items = ['Item %s' % (i + 1)
                 for i in xrange(10)]
        self.resultList.addItems(items)

        self.trashButton = QtGui.QPushButton("Move to trash")
        self.trashButton.clicked.connect(self.selectedResults)

        # Layout
        rightGrid = QtGui.QGridLayout()
        rightGrid.setSpacing(10)

        rightGrid.addWidget(findButton, 0, 0)
        rightGrid.addWidget(resultCombo, 1, 0)
        rightGrid.addWidget(self.resultList, 2, 0, 1, 5)
        rightGrid.addWidget(self.trashButton, 3, 4)

        # adjust layout with an empty label
        rightGrid.addWidget(empty, 0, 1, 1, 4)
        rightGrid.addWidget(empty, 1, 1, 1, 4)
        rightGrid.addWidget(empty, 3, 0, 1, 4)

        self.rightSide.setLayout(rightGrid)

    def selectedResults(self):
        selected =  self.resultList.selectedItems()
        print [item.text() for item in selected]

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    app = QtGui.QApplication(argv)
    window = Dupy()
    window.show()
    exit(app.exec_())


if __name__ == '__main__':
    main()
