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
        self.edit()
        self.importFile()

    def run_config(self):

        # Establish Connection to MongoDB - Run Config
        client = pymongo.MongoClient(
            "mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client[ 'Test' ]
        self.config = db[ "Run Config" ]

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
        orLabel1 = util.orLabel()
        orLabel2 = util.orLabel()

        # Run Name
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%I:%M %m/%d/%Y %p")
        self.runName = QLabel()
        self.runName.setAlignment(Qt.AlignLeft)
        self.runName.setText(timestampStr)
        serifFont = QFont("TimesNewRoman", 15)
        self.runName.setFont(serifFont)
        runConfigLayout.addRow("Run Name:", self.runName)

        # Run Description
        self.runDesc = QPlainTextEdit()
        self.runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", self.runDesc)

        # Whitelist
        self.WLIPtext = QPlainTextEdit()
        self.WLIPtext.setPlaceholderText("Whitelist IP Default")

        BrowseChoiceLayout = QHBoxLayout()
        BrowseChoiceLayout.addWidget(self.WLIPtext)
        BrowseChoiceLayout.addWidget(orLabel)
        BrowseChoiceLayout.addWidget(QLabel("Browse for Whitelist Files"))
        self.path = QLineEdit()
        BrowseChoiceLayout.addWidget(self.path)
        wlipBrowse = QPushButton("Browse")
        BrowseChoiceLayout.addWidget(wlipBrowse)
        # buttonConfigFile = QPushButton("Browse")
        wlipBrowse.clicked.connect(lambda: self.buttons("Browse", self.path))
        BrowseWidget = QWidget()
        BrowseWidget.setLayout(BrowseChoiceLayout)

        self.BLIPtext = QPlainTextEdit()
        self.BLIPtext.setPlaceholderText("Blacklist IP Default")

        BrowseChoiceLayout2 = QHBoxLayout()
        BrowseChoiceLayout2.addWidget(self.BLIPtext)
        BrowseChoiceLayout2.addWidget(orLabel1)
        BrowseChoiceLayout2.addWidget(QLabel("Browse for Blacklist Files"))
        self.bPath = QLineEdit()
        BrowseChoiceLayout2.addWidget(self.bPath)
        blipBrowse = QPushButton("Browse")
        BrowseChoiceLayout2.addWidget(blipBrowse)
        blipBrowse.clicked.connect(lambda: self.buttons("Browse", self.bPath))
        BrowseWidget2 = QWidget()
        BrowseWidget2.setLayout(BrowseChoiceLayout2)

        runConfigLayout.addRow("Whitelisted IP Target:", BrowseWidget)
        runConfigLayout.addRow("Blacklisted IP Target:", BrowseWidget2)

        ScanType = QComboBox()
        scanList = [ "Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3" ]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addWidget(orLabel2)
        self.ConfigFile = QLineEdit()
        self.ConfigFile.setPlaceholderText("Run Configuration File")
        runConfigLayout.addRow("Browse for Run Configuration File:", self.ConfigFile, )
        configButton = QPushButton("Browse")
        runConfigLayout.addWidget(configButton)
        configButton.clicked.connect(lambda: self.buttons("Browse", self.ConfigFile))

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

    def edit(self):
        menuTitle = QLabel()
        menuTitle.setText("  Run Table  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        editLayout = QFormLayout()
        editLayout.addWidget(QLabel("***** TEST *****"))
        editLayout.addWidget(QLabel("***** ADD Table with Run,Pause,Stop buttons*****"))

        editContainer = QWidget()
        editContainer.setLayout(editLayout)

        self.table = QDockWidget()
        self.table.setTitleBarWidget(menuTitle)
        self.table.setWidget(editContainer)
        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.table)
        self.table.setVisible(False)

    def importFile(self):
        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText(" Run Configuration File Import ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        browsingLayout = QHBoxLayout()
        browseLabel = QLabel(" Run Configuration File ")
        browsingLayout.addStretch()
        browsingLayout.addWidget(browseLabel)

        self.importFile = QLineEdit()
        self.importFile.setAlignment(Qt.AlignLeft)
        browsingLayout.addWidget(self.importFile)

        browse = QPushButton("Browse")
        browse.clicked.connect(lambda: self.buttons("Browse2", self.importFile))

        browsingLayout.addWidget(browse)
        browsingLayout.addStretch()
        browsing = QWidget()
        browsing.setLayout(browsingLayout)

        filePath = "file:///{}/SampleTool.xml".format(os.getcwd())
        sample = QLabel("<a href = {}>Open Run Configuration Specification File</a>".format(filePath))
        sample.setOpenExternalLinks(True)

        importer = QPushButton("Import")
        importer.setStyleSheet("background-color: #54e86c")
        importer.clicked.connect(lambda: self.buttons("Import", self.importFile))
        importerWidget = util.make_HBox(importer, 0)

        importLayout = QVBoxLayout()
        importLayout.addWidget(browsing)
        importLayout.addWidget(sample)
        importLayout.addWidget(importerWidget)
        importLayout.addStretch()

        importContainer = QWidget()
        importContainer.setLayout(importLayout)

        self.toolImport = QDockWidget()
        self.toolImport.setTitleBarWidget(menuTitle)
        self.toolImport.setWidget(importContainer)
        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.toolImport)
        self.toolImport.setVisible(False)

    def buttons(self, buttonName, button, NULL=None):
        if "Browse" in buttonName:
            if buttonName == "Browse":
                fname = QFileDialog.getExistingDirectory(None, "Select a Directory...")
            else:
                fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter="All files (*)")
            if isinstance(fname, tuple):
                button.setText(str(fname[ 0 ]))
            else:
                button.setText(str(fname))
        elif "Save" in buttonName:
            name = self.runName.text()
            description = self.runDesc.toPlainText()
            wlipText = self.WLIPtext.toPlainText()
            wlipFile = self.path.text()
            blipText = self.BLIPtext.toPlainText()
            blipFile = self.bPath.text()
            runFile = self.importFile.text()
            inputStr = {"Run Name": name, "Run Description": description, "Target Whitelist": wlipText,
                        "Whitelist File": wlipFile, "Target Blacklist": blipText, "Blacklist File": blipFile,
                        "Run Configuration File": runFile}
            self.config.insert_one(inputStr)
        elif "Cancel" in buttonName:
            self.runName.setText("")
            self.runDesc.setPlainText("")
            self.WLIPtext.setPlainText("")
            self.BLIPtext.setPlainText("")
            self.bPath.setText("")
            self.path.setText("")
            self.ConfigFile.setText("")
            self.importFile.text("")




    def hide(self):
        self.runConfiguration.setVisible(False)
        self.table.setVisible(False)
        self.toolImport.setVisible(False)

    def show(self):
        self.runConfiguration.setVisible(True)
        self.table.setVisible(True)
        self.toolImport.setVisible(True)
