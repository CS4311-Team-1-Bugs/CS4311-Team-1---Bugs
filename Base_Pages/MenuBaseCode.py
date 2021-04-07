# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        #Set the Window Title
        self.setWindowTitle("Tool Run List")
        
        
        
        #set menu layout
        menuLayout = QVBoxLayout()
        
        #Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("SEA Menu")
        menuTitle.setAlignment(Qt.AlignCenter)
        
        
        #button component of menu
        hLayout = QHBoxLayout()
        runButton = QPushButton("Run")
        toolButton = QPushButton("Tools")
        hLayout.addStretch()
        hLayout.addWidget(runButton)
        hLayout.addStretch()
        hLayout.addWidget(toolButton)
        hLayout.addStretch()
        
        #Add the widgets we created to the menu layout
        menuLayout.addWidget(menuTitle)
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)
        
        
        #Make a Widget to hold the layout and set it as the window's menu
        menuWidget = QWidget()
        menuWidget.setLayout(menuLayout)
        self.setMenuWidget(menuWidget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())