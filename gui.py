from sys import exit, argv
from PySide import QtGui, QtCore


class Dupy(QtGui.QWidget):

    def __init__(self):
        super(Dupy, self).__init__()
        self.initUI()

    def initUI(self):
        # self.resize(500, 400)
        # self.center()
        self.setGeometry(1400, 250, 500, 400)  # set for development
        self.setAcceptDrops(True)
        self.setWindowTitle('Dupy')

        # Elements
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        # Layout
        self.vbox = QtGui.QVBoxLayout(self)

        self.leftSide = QtGui.QFrame(self)
        self.leftLayout()

        self.rightSide = QtGui.QFrame(self)
        self.rightLayout()
        self.rightSide.hide()  # hide until user is done adding directories

        self.bottom = QtGui.QFrame(self)
        self.bottom.hide()

        splitter.addWidget(self.leftSide)
        splitter.addWidget(self.rightSide)

        self.vbox.addWidget(splitter)
        self.vbox.addWidget(self.bottom)
        self.setLayout(self.vbox)

    def leftLayout(self):
        # Elements
        empty = QtGui.QLabel("")  # empty elements can be useful

        self.addButton = QtGui.QPushButton("Add a directory")
        self.addButton.clicked.connect(self.dirDialog)

        addLabel = QtGui.QLabel("...or drag and drop some here.")
        addLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.pathList = QtGui.QListWidget()
        self.pathList.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.pathList.setMaximumHeight(125)

        removeButton = QtGui.QPushButton("Remove")
        removeButton.clicked.connect(self.removeDirs)
        clearButton = QtGui.QPushButton("Clear")
        clearButton.clicked.connect(self.clearDirs)

        self.findButton = QtGui.QPushButton("Find duplicates")
        self.findButton.clicked.connect(self.findDups)

        # Layout
        leftGrid = QtGui.QGridLayout()
        leftGrid.setSpacing(10)

        leftGrid.addWidget(self.addButton, 1, 0, 1, 2)
        leftGrid.addWidget(addLabel, 2, 0, 1, 2)
        leftGrid.addWidget(self.pathList, 3, 0, 1, 2)
        leftGrid.addWidget(removeButton, 4, 0)
        leftGrid.addWidget(clearButton, 4, 1)
        leftGrid.addWidget(self.findButton, 6, 0, 1, 2)

        # take up remaining space with an empty label
        leftGrid.addWidget(empty, 5, 0, 1, 2)
        leftGrid.addWidget(empty, 7, 0, 1000, 2)  # this is kind of a bug

        self.leftSide.setLayout(leftGrid)

    def rightLayout(self):
        # Elements
        empty = QtGui.QLabel("")  # empty elements can be useful

        self.resultCombo = QtGui.QComboBox()
        self.resultCombo.addItem("All")

        resultEdit = QtGui.QTextEdit()
        resultEdit.setReadOnly(True)

        self.resultList = QtGui.QListWidget()
        self.resultList.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)

        items = ['Item %s' % (i + 1)
                 for i in xrange(10)]
        self.resultList.addItems(items)

        self.trashButton = QtGui.QPushButton("Move to trash")
        self.trashButton.clicked.connect(self.trashEvent)

        # Layout
        rightGrid = QtGui.QGridLayout()
        rightGrid.setSpacing(10)

        rightGrid.addWidget(self.resultCombo, 0, 0, 1, 5)
        rightGrid.addWidget(self.resultList, 1, 0, 1, 5)
        rightGrid.addWidget(self.trashButton, 2, 4)

        # adjust layout with an empty label
        # rightGrid.addWidget(empty, 0, 1, 1, 4)
        rightGrid.addWidget(empty, 2, 0, 1, 4)

        self.rightSide.setLayout(rightGrid)

    def findDups(self):
        self.rightSide.show()
        self.resize(800, 400)

        self.updateCombo()

    def updateCombo(self):
        # Add directories to the combo box
        paths = []
        for i in xrange(self.pathList.count()):
            paths.append(self.pathList.item(i))
        dirs = [path.text().encode("utf-8") for path in paths]
        self.resultCombo.addItems(dirs)

    def trashEvent(self):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure you want to move "
                                           "these files to the trash?",
                                           QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            self.moveToTrash()
        else:
            pass

    def moveToTrash(self):
        self.bottom.show()

        selected = self.resultList.selectedItems()
        items = [item.text().encode("utf-8") for item in selected]

        # Elements
        hbox = QtGui.QHBoxLayout()

        self.pbar = QtGui.QProgressBar()
        self.pbar.setGeometry(30, 40, 200, 25)
        self.pbar.setMinimum(0)
        self.pbar.setMaximum(100)
        # set progress bar status
        self.pbar.setValue(75)

        self.cancelButton = QtGui.QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.cancelTrash)

        # Layout
        hbox.addWidget(self.pbar)
        hbox.addWidget(self.cancelButton)

        self.bottom.setLayout(hbox)

    def cancelTrash(self):
        # stop sending files to trash and stop progress bar
        self.bottom.hide()

    def dirDialog(self):
        title = self.addButton.text()
        dialogueDir = QtGui.QFileDialog.getExistingDirectory(self, title)
        self.pathList.addItem(dialogueDir)

    def removeDirs(self):
        paths = self.pathList.selectedItems()
        for path in paths:
            self.pathList.takeItem(self.pathList.row(path))

    def clearDirs(self):
        self.pathList.clear()

    # drag-and-drop directories into dupy
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            for url in event.mimeData().urls():
                drop_path = str(url.toLocalFile())
                self.pathList.addItem(drop_path)  # add the path
            self.emit(QtCore.SIGNAL("dropped"))
        else:
            event.ignore()

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
