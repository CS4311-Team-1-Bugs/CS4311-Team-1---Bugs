# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 00:15:23 2021

@author: Emil
"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class ToolContent(QWidget):
    def __init__(self, *args, **kwargs):
        #init the window
        super(ToolContent, self).__init__(*args, **kwargs)

        #Set the Window Title
        self.setWindowTitle("Tool List")
        
        #Create Outer Base layer
        outerLayout = QVBoxLayout()
        
        menuLayout = QVBoxLayout()
        
        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("Tool List")
        menuTitle.setAlignment(Qt.AlignCenter)
        
        
        
        # Add the widgets we created to the menu layout
        menuLayout.addWidget(menuTitle)


        # Create Tool Content Details layer
        toolContentLayout = QVBoxLayout()
        tableWidget =  QTableWidget(4,3)
        nameSortButton = QToolButton()                                     
                              
        nameSortButton.setArrowType(Qt.DownArrow)
        tableWidget.setCellWidget(0,0,nameSortButton)
        tableWidget.setHorizontalHeaderLabels(("Tool Name; Description of tool; ").split(";"))
        tableWidget.setVerticalHeaderLabels(("; ; ; ;").split(";"))
        
        # Add  buttons to the table
        for i in range(1,4):
                    tableWidget.setCellWidget(i,2, QPushButton("Remove"))

        toolContentLayout.insertWidget(0,tableWidget,1)
        
        # Handle buttons associated with the table
        toolTableButtonLayout = QHBoxLayout()
        toolTableButtonLayout.addStretch(1)
        toolTableButtonLayout.addWidget(QPushButton("Add Tool"))
        toolContentLayout.addLayout(toolTableButtonLayout)


        
        outerLayout.addLayout(menuLayout)
        outerLayout.addLayout(toolContentLayout)

        self.setLayout(outerLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToolContent()
    window.show()
    sys.exit(app.exec_())