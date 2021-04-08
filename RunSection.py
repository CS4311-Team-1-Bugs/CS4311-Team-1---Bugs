import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo
from bson.objectid import ObjectId
import datetime
import os
import lxml.etree as xml
import Utils as util
from ToolSection import QTablePush


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
        self.tools = db["Tools"]
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
        file = "whitelistSample.txt"
        filePath = file.format(os.getcwd())
        sample = QLabel("<a href = {}>Open Sample Whitelist File</a>".format(filePath))
        sample.setOpenExternalLinks(True)
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
        BrowseChoiceLayout.addWidget(sample)

        self.BLIPtext = QPlainTextEdit()
        self.BLIPtext.setPlaceholderText("Blacklist IP Default")
        file2 = "blacklistSample.txt"
        filePath2 = file2.format(os.getcwd())
        sample2 = QLabel("<a href = {}>Open Sample Blacklist File</a>".format(filePath))
        sample2.setOpenExternalLinks(True)

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
        BrowseChoiceLayout2.addWidget(sample2)
        runConfigLayout.addRow("Whitelisted IP Target:", BrowseWidget)
        runConfigLayout.addRow("Blacklisted IP Target:", BrowseWidget2)

        self.ScanType = QComboBox()
        scanList = [ ]
        for x in self.tools.find({},{'_id':0,'Name':1}):
            string = str(x)
            string1 = string[10:len(string)-2]
            scanList.append(string1)
        self.ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", self.ScanType)
        buttonWidget = util.make_saveCancel(self,1)

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

        self.tableWidget = QTableWidget(1,4)
        self.tableWidget.setColumnHidden(3,True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        col1Title = QLabel()
        col1Title.setText("Run Configuration Name")
        self.sortArrow = "down"
        nameSortButton = QToolButton()
        nameSortButton.setArrowType(Qt.DownArrow)
        nameSortButton.clicked.connect(lambda: self.buttons("Sort", nameSortButton))
        col1Layout = QHBoxLayout()
        col1Layout.addStretch()
        col1Layout.addWidget(col1Title)
        col1Layout.addWidget(nameSortButton)
        col1Layout.addStretch()

        # Set Columns for the table
        col1Widget = QWidget()
        col1Widget.setLayout(col1Layout)
        self.tableWidget.setCellWidget(0, 0, col1Widget)
        self.tableWidget.setCellWidget(0, 1, QLabel("Description of Run"))
        self.tableWidget.setCellWidget(0, 2, QLabel(" Scan "))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()

        # Add button
        addLayout = QHBoxLayout()
        addLayout.addStretch(1)
        push = QPushButton("Add Tool")
        push.setStyleSheet("background-color: #54e86c")
        push.clicked.connect(lambda: self.buttons("Switcher", None))
        addLayout.addWidget(push)
        holder = QWidget()
        holder.setLayout(addLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addWidget(holder)
        mainLayout.addSpacing(10)

        main = QWidget()
        main.setLayout(mainLayout)

        self.drawTable()

        self.toolList = QDockWidget()
        self.toolList.setTitleBarWidget(menuTitle)
        self.toolList.setWidget(main)
        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.toolList)
        self.toolList.setVisible(False)

    def drawTable(self, reversed=0):
        table = self.tableWidget
        index = 1
        tools = self.config.find()
        maxInd = self.config.count_documents({})

        if reversed:
            start, end, increment = maxInd - 1, -1, -1
        else:
            start, end, increment = 0, maxInd, 1
        for i in range(start, end, increment):
            tool = tools[ i ]
            if index < table.rowCount():
                pass
            else:
                table.insertRow(index)
            table.setCellWidget(index, 0, QLabel(tool[ "Run Name" ]))
            table.setCellWidget(index, 1, QLabel(tool[ "Run Description" ]))

            Buttons = QWidget()
            ButtonLayout = QHBoxLayout()
            start = QTablePush(tool[ "_id" ], "play.png", self)
            pause= QTablePush(tool[ "_id" ], "pause.png", self)
            stop = QTablePush(tool[ "_id" ], "stop.png", self)
            ButtonLayout.addWidget(start)
            ButtonLayout.addWidget(pause)
            ButtonLayout.addWidget(stop)
            Buttons.setLayout(ButtonLayout)
            table.setCellWidget(index, 2, Buttons)
            # table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 3, QLabel(str(tool[ "_id" ])))
            index += 1

        for i in range(1, self.tableWidget.rowCount()):
            self.tableWidget.verticalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)


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

    def buttons(self, buttonName, button):
        if "Browse" in buttonName:
            if buttonName == "Browse":
                fname = QFileDialog.getExistingDirectory(None, "Select a Directory...")
            else:
                fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter="All files(*)")
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
            scan = self.ScanType.currentText()

            inputStr = {"Run Name": name, "Run Description": description, "Target Whitelist": wlipText,
                        "Whitelist File": wlipFile, "Target Blacklist": blipText, "Blacklist File": blipFile,"Scan Type":scan,
                        "Run Configuration File": runFile}
            self.config.insert_one(inputStr)
        elif "Cancel" in buttonName:
            self.runName.setText("")
            self.runDesc.setPlainText("")
            self.WLIPtext.setPlainText("")
            self.BLIPtext.setPlainText("")
            self.bPath.setText("")
            self.path.setText("")
            self.importFile.setText("")

        elif buttonName == "Export":
            fileName, _ = QFileDialog.getSaveFileName(self.win, "Export File Name", "./", "*.xml")
            if fileName:
                file = open(fileName, "wb")
                root = xml.Element("RunConfiguration")

                name = xml.SubElement(root, "RunName")
                desc = xml.SubElement(root, "RunDescription")
                wlip = xml.SubElement(root,"TargetWhitelistIP")
                path = xml.SubElement(root, "WhitelistPath")
                blip = xml.SubElement(root,"TargetBlacklistIP")
                blipPath = xml.SubElement(root, "BlacklistPath")
                scanType = xml.SubElement(root,"ScanType")

                name.text = self.runName.text()
                desc.toPlainText = self.runDesc.toPlainText()
                wlip.toPlainText = self.WLIPtext.toPlainText()
                path.text = self.path.text()
                blip.toPlainText = self.BLIPtext.toPlainText()
                blipPath.text = self.bPath.text()
                scanType.text = self.ScanType.currentText()
                tree = xml.ElementTree(root)
                tree.write(file, pretty_print=True)
                file.close()
        elif buttonName == "Import":
            filename = button.text()
            root = xml.parse(filename).getroot()
            name = root.find("RunName")
            description = root.find("RunDescription")
            whitelist = root.find("TargetWhitelistIP")
            path = root.find("WhitelistPath")
            blacklist = root.find("TargetBlacklistIP")
            path2 = root.find("BlacklistPath")
            scanType = root.find("ScanType")

            if name is not None:
                self.runName.setText(name.text)
            if description is not None:
                self.runDesc.toPlainText()
            if path is not None:
                self.path.setText(path.text)
            if whitelist is not None:
                self.WLIPtext.toPlainText()
            if blacklist is not None:
                self.BLIPtext.toPlainText()
            if path2 is not None:
                self.bPath.setText(path2)
            if scanType is not None:
                self.ScanType.setText(scanType)




    def hide(self):
        self.runConfiguration.setVisible(False)
        self.toolImport.setVisible(False)
        self.toolList.setVisible(False)

    def show(self):
        self.runConfiguration.setVisible(True)
        self.toolImport.setVisible(True)
        self.toolList.setVisible(True)

