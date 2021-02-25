# -*- coding: utf-8 -*-

import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        #Set the Window Title
        self.setWindowTitle("SEA Tool")
        
        #Make our menu
        menuWidget = QWidget()
        menuLayout = self.make_menuLayout()
        menuWidget.setLayout(menuLayout)
        self.setMenuWidget(menuWidget)
        
        #Make our main area
        mainWidget = QWidget()
        mainLayout = self.make_mainLayout()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        
        
        
    def make_menuLayout(self):
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
        return menuLayout
    
    def make_mainLayout(self):
        #make our run list
        runList = self.make_runList()
        
        #Add spacing to the page and add our widgets
        mainLayout = QVBoxLayout()
        mainLayout.addStretch()
        mainLayout.addWidget(self.make_HBox(runList, 1))
        mainLayout.addStretch()
        mainLayout.addWidget(self.make_HBox(QPushButton("Add"), 0))
        return mainLayout
        
    #Make the table that will hold the runs
    def make_runList(self):
        #make the table
        runList = QTableWidget()
        runList.setRowCount(1)
        runList.setColumnCount(4)
        
        #column 1
        col1Title = QLabel()
        col1Title.setText("Name of Run")
        upButton = QPushButton()
        upButton.setIcon(QtGui.QIcon("up.png"))
        downButton = QPushButton()
        downButton.setIcon(QtGui.QIcon("down.png"))
        col1Layout = QHBoxLayout()
        col1Layout.addStretch()
        col1Layout.addWidget(col1Title)
        col1Layout.addWidget(upButton)
        col1Layout.addWidget(downButton)
        col1Layout.addStretch()
        
        col1Widget = QWidget()
        col1Widget.setLayout(col1Layout)
        
        
        #Set the headers and their resize modes
        runList.setCellWidget(0,0,col1Widget)
        runList.setItem(0,1,QTableWidgetItem("Description of Run"))
        runList.setItem(0,2,QTableWidgetItem("Result with Timestamp"))
        runList.setItem(0,3,QTableWidgetItem("Control"))
        runList.horizontalHeader().hide()
        runList.verticalHeader().hide()
        #runList.resizeColumnsToContents()
        header = runList.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)

        return runList
    
    #pad a widget with horizontal spacing or stretching
    def make_HBox(self, widget, spacingType):
        layout = QHBoxLayout()
        if spacingType:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        layout.addWidget(widget)
        if spacingType:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        container = QWidget()
        container.setLayout(layout)
        return container
        

        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())