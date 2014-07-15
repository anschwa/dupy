from sys import exit, argv
from PySide import QtGui, QtCore


class Dupy(QtGui.QWidget):

    def __init__(self):
        super(Dupy, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        self.center()
        
        self.setAcceptDrops(True)

        okButton = QtGui.QPushButton("OK")
        cancelButton = QtGui.QPushButton("Cancel")

        title = QtGui.QLabel('Title')
        author = QtGui.QLabel('Author')
        review = QtGui.QLabel('Review')

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        self.reviewEdit = QtGui.QTextEdit()
        self.reviewEdit.setReadOnly(True)

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

        self.setWindowTitle('Dupy')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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
                # append path to textbox
                self.reviewEdit.append(drop_path)
            self.emit(QtCore.SIGNAL("dropped"))
        else:
            event.ignore()


def main():
    app = QtGui.QApplication(argv)
    name = Dupy()
    exit(app.exec_())


if __name__ == '__main__':
    main()
