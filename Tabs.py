import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, \
    QLineEdit, QFormLayout, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        # Tab Size Dimension
        self.left = 0
        self.top = 0
        self.width = 700
        self.height = 500
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize Tab Screens
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tab5 = QWidget()
        self.tab6 = QWidget()
        self.tabs.resize(300, 200)

        # Tab Titles
        self.tabs.addTab(self.tab1, "Scan A")
        self.tabs.addTab(self.tab2, "Scan B")
        self.tabs.addTab(self.tab3, "Scan C")
        self.tabs.addTab(self.tab4, "Scan D")
        self.tabs.addTab(self.tab5, "Scan E")
        self.tabs.addTab(self.tab6, "Scan F")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab2.layout = QVBoxLayout(self)
        self.tab3.layout = QVBoxLayout(self)
        self.tab4.layout = QVBoxLayout(self)
        self.tab5.layout = QVBoxLayout(self)
        self.tab6.layout = QVBoxLayout(self)

        # Editable Scan Output Textbox Tab 1
        self.textbox1 = QPlainTextEdit(self)
        self.textbox1.insertPlainText("Scan A Output...")
        self.textbox1.move(20, 20)
        self.textbox1.resize(280, 40)
        self.tab1.layout.addWidget(self.textbox1)
        # Editable Scan Output Textbox Tab 2
        self.textbox2 = QPlainTextEdit(self)
        self.textbox2.insertPlainText("Scan B Output...")
        self.textbox2.move(20, 20)
        self.textbox2.resize(280, 40)
        self.tab2.layout.addWidget(self.textbox2)
        # Editable Scan Output Textbox Tab 3
        self.textbox3 = QPlainTextEdit(self)
        self.textbox3.insertPlainText("Scan A Output...")
        self.textbox3.move(20, 20)
        self.textbox3.resize(280, 40)
        self.tab3.layout.addWidget(self.textbox3)
        # Editable Scan Output Textbox Tab 4
        self.textbox4 = QPlainTextEdit(self)
        self.textbox4.insertPlainText("Scan B Output...")
        self.textbox4.move(20, 20)
        self.textbox4.resize(280, 40)
        self.tab4.layout.addWidget(self.textbox4)
        # Editable Scan Output Textbox Tab 5
        self.textbox5 = QPlainTextEdit(self)
        self.textbox5.insertPlainText("Scan A Output...")
        self.textbox5.move(20, 20)
        self.textbox5.resize(280, 40)
        self.tab5.layout.addWidget(self.textbox5)
        # Editable Scan Output Textbox Tab 6
        self.textbox6 = QPlainTextEdit(self)
        self.textbox6.insertPlainText("Scan B Output...")
        self.textbox6.move(20, 20)
        self.textbox6.resize(280, 40)
        self.tab6.layout.addWidget(self.textbox6)

        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.setLayout(self.tab3.layout)
        self.tab4.setLayout(self.tab4.layout)
        self.tab5.setLayout(self.tab5.layout)
        self.tab6.setLayout(self.tab6.layout)


        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
