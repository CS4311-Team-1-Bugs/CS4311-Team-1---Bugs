# -*- coding: utf-8 -*-

import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        #Set the Window Title
        self.setWindowTitle("SEA Tool")
        self.setStyleSheet('background-color:000000;color:ffffff')
        #Make our menu
        menuWidget = QWidget()
        menuLayout = self.make_menuLayout()
        menuWidget.setLayout(menuLayout)
        palette = QPalette()
        palette.setColor(QtGui.QPalette.Background, QColor("#99ccff"))
        menuWidget.setPalette(palette)
        menuWidget.setAutoFillBackground(1)
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
        menuTitle.setText("  SEA Menu  ")
        menuTitle.setFont(QFont("Times", 20))
        menuTitle.setStyleSheet("border: 3px solid black; color: #000000")
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
        menuLayout.addWidget(self.make_HBox(menuTitle, 0))
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)

        
        return menuLayout
    
    def make_mainLayout(self):
        #Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Tool Specification  ")
        menuTitle.setFont(QFont("Times", 18))
        menuTitle.setStyleSheet("border: 2px solid black; color: #000000")
        menuTitle.setAlignment(Qt.AlignCenter)
        
        
        #make our tool spec
        toolSpec = self.make_toolSpec()
        
        
        #Title component of menu
        menuTitle2 = QLabel()
        menuTitle2.setText("  Tool Dependency  ")
        menuTitle2.setFont(QFont("Times", 18))
        menuTitle2.setStyleSheet("border: 2px solid black; color: #000000")
        menuTitle2.setAlignment(Qt.AlignCenter)
        toolDep = self.make_toolDep()
        
        saveButt = self.make_saveCancel()
        
        
        
        #Add spacing to the page and add our widgets
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.make_HBox(menuTitle, 0))
        mainLayout.addWidget(self.make_HBox(toolSpec, 1))
        mainLayout.addWidget(self.make_HBox(menuTitle2, 0))
        mainLayout.addWidget(self.make_HBox(toolDep, 1))
        mainLayout.addWidget(saveButt)
        mainLayout.addStretch()
        
        return mainLayout
        
    def make_toolSpec(self):
        layout = QFormLayout()
        
        name = QLineEdit()
        name.setAlignment(Qt.AlignLeft)
        
        description = QLineEdit()
        description.setAlignment(Qt.AlignLeft)
        
        browser = QHBoxLayout()
        browse = QLineEdit()
        browse.setAlignment(Qt.AlignLeft)
        browser.addWidget(browse)
        browser.addWidget(QPushButton("Browse"))
        browser.addStretch()
        
        browserWidg = QWidget()
        browserWidg.setLayout(browser)
       
        opt_container = QHBoxLayout()
        opt = QLineEdit()
        opt.setAlignment(Qt.AlignLeft)
        opt_container.addWidget(opt)
        opt_container.addWidget(QPushButton("Add"))
        opt_container.addStretch()
        opt_widg = QWidget()
        opt_widg.setLayout(opt_container)
        
        outSpec_container = QHBoxLayout()
        outSpec = QLineEdit()
        outSpec.setAlignment(Qt.AlignLeft)
        outSpec_container.addWidget(outSpec)
        outSpec_container.addWidget(QPushButton("Add"))
        outSpec_container.addStretch()
        outSpec_widg = QWidget()
        outSpec_widg.setLayout(outSpec_container)
        
        orLabel = QLabel("OR")
        
        specFile_container = QHBoxLayout()
        specFile = QLineEdit()
        specFile.setAlignment(Qt.AlignLeft)
        specFile_container.addWidget(specFile)
        specFile_container.addWidget(QPushButton("Browse"))
        specFile_container.addStretch()
        specFile_widg = QWidget()
        specFile_widg.setLayout(specFile_container)
        
        layout.addRow(QLabel("Tool Name"), name)
        layout.addRow(QLabel("Tool Description"), description)
        layout.addRow(QLabel("Tool Path"), browserWidg)
        layout.addRow(QLabel("Option and Argument"), opt_widg)
        layout.addRow(QLabel("Output Specification"), outSpec_widg)
        layout.addRow(orLabel)
        layout.addRow(QLabel("Tool  Specification File"), specFile_widg)
        
        layoutHolder = QWidget()
        layoutHolder.setLayout(layout)
        return layoutHolder
        
    
    def make_toolDep(self):
        layout = QVBoxLayout()
        
        hButton = QHBoxLayout()
        hButton.addWidget(QLabel("Dependent Data"))
        options = QComboBox()
        options.addItem("Dependent Ex")
        hButton.addWidget(options)
        hButton.addWidget(QLabel("Operator"))
        options2 = QComboBox()
        options2.addItem("Operator Ex")
        hButton.addWidget(options2)
        hButton.addWidget(QLabel("Value"))
        hButton.addWidget(QLineEdit())
        hButton.addWidget(QPushButton("Remove"))
        hButtonHolder = QWidget()
        hButtonHolder.setLayout(hButton)



        
        layout.addWidget(hButtonHolder)
        layout.addWidget(self.make_HBox(QPushButton("Add"), 0))
        
        depLayout = QHBoxLayout()
        dep = QLineEdit()
        depLayout.addWidget(QLabel("Dependency Expression"))
        depLayout.addWidget(dep)
        depLayout.addStretch()
        depHolder = QWidget()
        depHolder.setLayout(depLayout)
       
        
        
        layout.addWidget(depHolder)
        
        layoutHolder = QWidget()
        layoutHolder.setLayout(layout)
        return layoutHolder
    def make_saveCancel(self):
        layout = QHBoxLayout()
        save = QPushButton("Save")
        cancel = QPushButton("Cancel")
        layout.addStretch()
        layout.addWidget(save)
        layout.addWidget(cancel)
        layout.addStretch()
        
        container = QWidget()
        container.setLayout(layout)
        return container
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