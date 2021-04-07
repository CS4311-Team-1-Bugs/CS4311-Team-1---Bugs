import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo
from bson.objectid import ObjectId
import datetime
import os
import Utils as util

class RunSection():
    def __init__(self, window):
        self.win = window
        self.run_config()
        
    def run_config(self):
         # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Run Configuration  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)
    
        outerLayout = QVBoxLayout()
        # Create Run Config Details layer
        runConfigLayout = QFormLayout()
        orLabel = util.orLabel()
        orLabel1 =util.orLabel()
        orLabel2 = util.orLabel()
        
        #Run Name
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%I:%M %m/%d/%Y %p")
        runName = QLabel()
        runName.setAlignment(Qt.AlignLeft)
        runName.setText(timestampStr)
        serifFont = QFont("TimesNewRoman", 15)
        runName.setFont(serifFont)
        runConfigLayout.addRow("Run Name:", runName)
        
        #Run Description
        runDesc= QLineEdit()
        runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", runDesc)
        
        WLIPtext = QPlainTextEdit()
        WLIPtext.setPlaceholderText("Whitelist IP Default")
        
        BrowseChoiceLayout = QHBoxLayout()
        BrowseChoiceLayout.addWidget(WLIPtext)
        BrowseChoiceLayout.addWidget(orLabel)
        BrowseChoiceLayout.addWidget(QLabel("Browse for Whitelist Files"))
        BrowseChoiceLayout.addWidget(QLineEdit())
        BrowseChoiceLayout.addWidget(QPushButton("Browse"))
        #buttonConfigFile = QPushButton("Browse")
        BrowseWidget = QWidget()
        BrowseWidget.setLayout(BrowseChoiceLayout)
      
        
        BLIPtext = QPlainTextEdit()
        BLIPtext.setPlaceholderText("Blacklist IP Default")
        BrowseChoiceLayout2 = QHBoxLayout()
        BrowseChoiceLayout2.addWidget(BLIPtext)
        BrowseChoiceLayout2.addWidget(orLabel1)
        BrowseChoiceLayout2.addWidget(QLabel("Browse for Blacklist Files"))
        BrowseChoiceLayout2.addWidget(QLineEdit())
        BrowseChoiceLayout2.addWidget(QPushButton("Browse"))
        #buttonConfigFile = QPushButton("Browse")
        BrowseWidget2 = QWidget()
        BrowseWidget2.setLayout(BrowseChoiceLayout2)
 
        
        runConfigLayout.addRow("Whitelisted IP Target:", BrowseWidget)
        runConfigLayout.addRow("Blacklisted IP Target:", BrowseWidget2)
        
        
        ScanType = QComboBox()
        scanList = ["Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3"]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addWidget(orLabel2)
        ConfigFile = QLineEdit()
        ConfigFile.setPlaceholderText("Run Configuration File")
        runConfigLayout.addRow("Browse for Run Configuration File:", ConfigFile,)
        runConfigLayout.addWidget(QPushButton("Browse"))



        
        buttonWidget = util.make_saveCancel(self)

        runConfigLayout.addWidget(buttonWidget)
        runConfigLayout.setVerticalSpacing(20)
        runConfigLayout.setHorizontalSpacing(10)
        main = QWidget()
        main.setLayout(runConfigLayout)
        
        self.runConfiguration = QDockWidget()
        self.runConfiguration.setTitleBarWidget(menuTitle)
        self.runConfiguration.setWidget(main)
        self.win.addDockWidget(Qt.RightDockWidgetArea, self.runConfiguration)
        self.runConfiguration.setVisible(False)
        return 
    def hide(self):
        self.runConfiguration.setVisible(False)
    def show(self):
        self.runConfiguration.setVisible(True)