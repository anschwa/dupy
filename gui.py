from sys import exit, argv
from PySide import QtGui, QtCore


class Dupy(QtGui.QWidget):

    def __init__(self):
        super(Dupy, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        # self.center()

        self.setGeometry(1400, 250, 500, 400)  # set for development

        self.setAcceptDrops(True)

        # Active Directories
        self.addButton = QtGui.QPushButton("Add a directory")
        self.addButton.clicked.connect(self.dirDialog)

        descLable = QtGui.QLabel("...or drag and drop one into this window.")

        self.clearButton = QtGui.QPushButton("Clear")
        self.clearButton.clicked.connect(self.clearDirs)
        self.clearButton.hide()

        self.pathEdit = QtGui.QTextEdit()
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setMaximumHeight(100)
        self.pathEdit.hide()

        # Find Duplicates
        self.findButton = QtGui.QPushButton("Find Duplicates")
        self.findButton.hide()

        # Duplicate Results
        self.allLable = QtGui.QLabel('All Results')
        self.allLable.hide()

        self.oneLable = QtGui.QLabel('dir one Results')
        self.oneLable.hide()

        self.resultsEdit = QtGui.QTextEdit()
        self.resultsEdit.setReadOnly(True)
        self.resultsEdit.hide()

        # Initial Layout
        hbox = QtGui.QHBoxLayout(self)

        leftSide = QtGui.QFrame(self)
        rightSide = QtGui.QFrame(self)
        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(leftSide)
        splitter.addWidget(rightSide)

        # Left Side Layout
        leftGrid = QtGui.QGridLayout()
        leftGrid.setSpacing(10)

        leftGrid.addWidget(self.addButton, 2, 0)
        leftGrid.addWidget(descLable, 2, 1)

        leftGrid.addWidget(self.pathEdit, 3, 0, 1, 2)
        leftGrid.addWidget(self.clearButton, 4, 0)

        leftSide.setLayout(leftGrid)

        # Left Side Layout
        rightGrid = QtGui.QGridLayout()
        rightGrid.setSpacing(10)

        rightGrid.addWidget(self.findButton, 1, 0)
        rightGrid.addWidget(self.allLable, 2, 0)
        rightGrid.addWidget(self.oneLable, 2, 1)
        rightGrid.addWidget(self.resultsEdit, 3, 0)

        rightSide.setLayout(rightGrid)

        # Set Parent Layout
        hbox.addWidget(splitter)
        self.setLayout(hbox)

        self.setWindowTitle('Dupy')
        self.show()

    def mainLayout(self):
        self.pathEdit.show()
        self.clearButton.show()
        self.findButton.show()
        self.allLable.show()
        self.oneLable.show()
        self.resultsEdit.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def dirDialog(self):
        title = self.addButton.text()
        dialogueDir = QtGui.QFileDialog.getExistingDirectory(self, title)
        self.pathEdit.append(dialogueDir)
        self.mainLayout()

    def clearDirs(self):
        self.pathEdit.setText("")

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
                self.pathEdit.append(drop_path)  # add path to textbox
                self.mainLayout()  # show the main layout
            self.emit(QtCore.SIGNAL("dropped"))
        else:
            event.ignore()


def main():
    app = QtGui.QApplication(argv)
    name = Dupy()
    exit(app.exec_())


if __name__ == '__main__':
    main()
