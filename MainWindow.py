import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import os
import Utils as util
import ToolSection as tool 
import RunSection as run

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set the Window Title
        self.setWindowTitle("SEA Tool")
        self.setStyleSheet('background-color:000000;color:ffffff')
        
        # Make our menu
        menuWidget = QWidget()
        menuLayout = self.make_menuLayout()
        menuWidget.setLayout(menuLayout)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#daf4f7"))
        menuWidget.setPalette(palette)
        menuWidget.setAutoFillBackground(1)
        self.setMenuWidget(menuWidget)
        
     
        self.toolSection = tool.ToolSection(self)
        self.runSection = run.RunSection(self)


    def make_menuLayout(self):
        # set menu layout
        menuLayout = QVBoxLayout()

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  SEA Menu  ")
        menuTitle.setFont(QFont("Times", 20))
        menuTitle.setStyleSheet("border: 3px solid black; color: #000000")
        menuTitle.setAlignment(Qt.AlignCenter)

        # button component of menu
        hLayout = QHBoxLayout()
        runButton = QPushButton("Run")
        runButton.clicked.connect(lambda: self.buttons("Run"))
        toolButton = QPushButton("Tools")
        toolButton.clicked.connect(lambda: self.buttons("Tool"))
        hLayout.addStretch()
        hLayout.addWidget(runButton)
        hLayout.addStretch()
        hLayout.addWidget(toolButton)
        hLayout.addStretch()

        # Add the widgets we created to the menu layout
        menuLayout.addWidget(util.make_HBox(menuTitle, 0))
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)
        return menuLayout
        
    # Quick code to make the menu buttons work
    def buttons(self, button):
        if button == "Run":
            self.toolSection.hide()
            self.runSection.show()
        else:
            self.toolSection.show()
            self.runSection.hide()
        
        
if __name__ == "__main__":
    def run_app():
        app = QtCore.QCoreApplication.instance()
        if app is None:
            app = QtWidgets.QApplication(sys.argv)
        win = MainWindow()
        win.show()
        app.exec_()
    run_app()
        