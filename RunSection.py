import sys
import time
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo
from bson.objectid import ObjectId
import state
import datetime
import os
import lxml.etree as xml
import Utils as util
# from ToolSection import QTablePush
import subprocess
import psutil


class QTablePush(QPushButton):
    def __init__(self, id, text, toolSection):
        # init the window
        super(QPushButton, self).__init__()
        self.setIcon(QIcon(QPixmap(text)))
        self.setIconSize(QSize(16, 16))
        self.id = str(id)
        self.setToolTip(text[ :-4 ])
        self.section = toolSection
        self.clicked.connect(lambda: self.section.buttons(text[ :-4 ], self))


class RunSection():
    def __init__(self, window):
        self.win = window
        self.run_config()
        self.edit()
        self.importFile()
        self.make_scanTable()
        self.runningRun = None
        self.processes = list()
    def run_config(self):

        # Establish Connection to MongoDB - Run Config
        client = pymongo.MongoClient(
            "mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client[ 'Test' ]
        self.tools = db[ "Tools" ]
        self.config = db[ "Runs" ]
        self.scans = db[ "Scans" ]
        self.scanOutputs = db[ "scanOutput" ]
        self.optionsDB = db["Options"]

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
        self.runDesc = QLineEdit()
        self.runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", self.runDesc)

        # Whitelist
        self.WLIPtext = QLineEdit()
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

        self.BLIPtext = QLineEdit()
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

        self.scanChoices = QVBoxLayout()
        self.scanType = QComboBox()

        scanUpdate = QHBoxLayout()
        scanUpdate.addWidget(self.scanType)
        adder = QPushButton()
        adder.setText("Add")
        scanUpdate.addWidget(adder)
        scanUpdate.addStretch()
        adder.clicked.connect(lambda: self.buttons("AddScan", adder))
        self.update_ScanTypes()
        updateHolder = QWidget()
        updateHolder.setLayout(scanUpdate)

        self.scanChoices.addWidget(updateHolder)
        scanHolder = QWidget()
        scanHolder.setLayout(self.scanChoices)
        runConfigLayout.addRow("Scan Type(s):", scanHolder)
        buttonWidget = util.make_saveCancel(self, 1)

        runConfigLayout.addWidget(buttonWidget)
        runConfigLayout.setVerticalSpacing(20)
        runConfigLayout.setHorizontalSpacing(10)

        main = QWidget()
        main.setLayout(runConfigLayout)

        self.runConfiguration = QDockWidget()
        self.runConfiguration.setTitleBarWidget(menuTitle)

        self.runConfiguration.setWidget(main)
        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.runConfiguration)
        self.runConfiguration.setVisible(False)
        return

    def edit(self):
        menuTitle = QLabel()
        menuTitle.setText("  Run Table  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        self.tableWidget = QTableWidget(1, 4)
        self.tableWidget.setColumnHidden(4, True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        col1Title = QLabel()
        col1Title.setText("Run Name")
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
        self.tableWidget.setCellWidget(0, 1, QLabel(" Description of Run "))
        self.tableWidget.setCellWidget(0, 2, QLabel(" Status "))
        self.tableWidget.setCellWidget(0, 3, QLabel(" Scan "))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()

        # Add button
        addLayout = QHBoxLayout()
        addLayout.addStretch(1)
        self.push = QPushButton("View Scan Ouput")
        self.push.setStyleSheet("background-color: #54e86c")
        self.currMode = 1
        self.push.clicked.connect(lambda: self.buttons("Switcher", None))
        addLayout.addWidget(self.push)
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
        self.win.addDockWidget(Qt.RightDockWidgetArea, self.toolList)
        self.toolList.setVisible(False)

    def update_ScanTypes(self):
        self.scansToAdd = []
        for x in self.tools.find():
            self.scansToAdd.append(x[ "Name" ])
        self.scanType.clear()
        self.scanType.addItems(self.scansToAdd)

    def drawTable(self, reversed=0):
        table = self.tableWidget
        index = 1
        tools = self.config.find()
        maxInd = self.config.count_documents({})
        self.RunId = None
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
            table.setCellWidget(index, 2, QLabel(tool["Status"]))
            Buttons = QWidget()
            ButtonLayout = QHBoxLayout()
            start = QTablePush(tool[ "_id" ], "play.png", self)
            pause = QTablePush(tool[ "_id" ], "pause.png", self)
            stop = QTablePush(tool[ "_id" ], "stop.png", self)
            output = QTablePush(tool[ "_id" ], "output2.png", self)
            ButtonLayout.addWidget(start)
            ButtonLayout.addWidget(pause)
            ButtonLayout.addWidget(stop)
            ButtonLayout.addWidget(output)
            Buttons.setLayout(ButtonLayout)
            table.setCellWidget(index, 3, Buttons)
            # table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 4, QLabel(str(tool[ "_id" ])))
            index += 1

        for i in range(1, self.tableWidget.rowCount()):
            self.tableWidget.verticalHeader().setSectionResizeMode(i, QHeaderView.Stretch)

    def make_scanTable(self):

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Scan List  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        # Create Tool Content Details layer
        self.scanTable = QTableWidget(1, 7)
        self.scanTable.setColumnHidden(6, True)
        self.scanTable.setEditTriggers(QTableWidget.NoEditTriggers)

        # column 1
        col1Title = QLabel()
        col1Title.setText("Scan Type")
        self.ScanSort = "down"
        nameSortButton = QToolButton()
        nameSortButton.setArrowType(Qt.DownArrow)
        nameSortButton.clicked.connect(lambda: self.buttons("Sort", nameSortButton))
        col1Layout = QHBoxLayout()
        col1Layout.addStretch()
        col1Layout.addWidget(col1Title)
        col1Layout.addWidget(nameSortButton)
        col1Layout.addStretch()

        # column 1
        col2Title = QLabel()
        col2Title.setText("Execution#")
        self.ExecSort = "down"
        ExecSortButton = QToolButton()
        ExecSortButton.setArrowType(Qt.DownArrow)
        ExecSortButton.clicked.connect(lambda: self.buttons("Sort", nameSortButton))
        col2Layout = QHBoxLayout()
        col2Layout.addStretch()
        col2Layout.addWidget(col2Title)
        col2Layout.addWidget(ExecSortButton)
        col2Layout.addStretch()

        # Set Columns for the table
        col1Widget = QWidget()
        col1Widget.setLayout(col1Layout)
        col2Widget = QWidget()
        col2Widget.setLayout(col2Layout)
        self.scanTable.setCellWidget(0, 0, col1Widget)
        self.scanTable.setCellWidget(0, 1, col2Widget)
        self.scanTable.setCellWidget(0, 2, QLabel("Start"))
        self.scanTable.setCellWidget(0, 3, QLabel("End"))
        self.scanTable.setCellWidget(0, 4, QLabel("Status"))
        self.scanTable.setCellWidget(0, 5, QLabel("Control"))
        header = self.scanTable.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.scanTable.verticalHeader().hide()
        self.scanTable.horizontalHeader().hide()

        self.ScanId = None
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabPosition(QTabWidget.West)
        self.tabWidget.addTab(QWidget(), "Sample")

        mainLayout = QVBoxLayout()
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.scanTable)
        mainLayout.addSpacing(10)
        mainLayout.addWidget(self.tabWidget)

        main = QWidget()
        main.setLayout(mainLayout)

        self.drawScanTable()

        self.scanList = QDockWidget()
        self.scanList.setTitleBarWidget(menuTitle)
        self.scanList.setWidget(main)
        self.win.addDockWidget(Qt.LeftDockWidgetArea, self.scanList)
        self.scanList.setVisible(False)

    def drawScanTable(self, reversed=0):
        if self.RunId is not None:
            print("here")
            query = {"Run_id": ObjectId(self.RunId)}
            table = self.scanTable
            index = 1
            scans = self.scans.find(query)
            maxInd = self.scans.count_documents({})

            if reversed:
                start, end, increment = maxInd - 1, -1, -1
            else:
                start, end, increment = 0, maxInd, 1
            for i in range(start, end, increment):
                scan = scans[ i ]
                if index < table.rowCount():
                    pass
                else:
                    table.insertRow(index)
                tool_query = {"_id": scan[ "Tool_id" ]}
                name = self.tools.find_one(tool_query)[ "Name" ]
                table.setCellWidget(index, 0, QLabel(name))
                table.setCellWidget(index, 1, QLabel(scan[ "Exec#" ]))
                table.setCellWidget(index, 2, QLabel(scan[ "Start" ]))
                table.setCellWidget(index, 3, QLabel(scan[ "End" ]))
                table.setCellWidget(index, 4, QLabel(scan[ "Status" ]))

                Buttons = QWidget()
                ButtonLayout = QHBoxLayout()
                start = QTablePush(scan[ "_id" ], "play.png", self)
                # start.clicked.connect(lambda:self.buttons("Start",None))
                pause = QTablePush(scan[ "_id" ], "pause.png", self)
                # pause.clicked.connect(lambda:self.buttons("Pause",None))
                stop = QTablePush(scan[ "_id" ], "stop.png", self)
                # stop.clicked.connect(lambda:self.buttons("Stop",None))
                output = QTablePush(scan[ "_id" ], "output.png", self)
                ButtonLayout.addWidget(start)
                ButtonLayout.addWidget(pause)
                ButtonLayout.addWidget(stop)
                ButtonLayout.addWidget(output)
                Buttons.setLayout(ButtonLayout)
                table.setCellWidget(index, 5, Buttons)
                # table.setCellWidget(index, 2, QPushButton("Remove"))
                table.setCellWidget(index, 6, QLabel(str(scan[ "_id" ])))
                index += 1

            for i in range(1, self.scanTable.rowCount()):
                self.scanTable.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)

    def draw_tabs(self):
        for i in range(self.tabWidget.count()):
            self.tabWidget.removeTab(0);

        query = {"Scan_id": ObjectId(self.ScanId)}
        outputs = self.scanOutputs.find(query)

        for i in outputs:
            tab = QWidget()
            layout = QVBoxLayout()
            text = QTextEdit()
            text.insertPlainText(i[ "Data" ])
            text.setReadOnly(True)
            
            layout.addWidget(text)
            tab.setLayout(layout)
            self.tabWidget.addTab(tab, i[ "Specification" ])

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
        #Check if there's new output
        self.check_processes()
        if "Browse" in buttonName:
            if buttonName == "Browse":
                fname = QFileDialog.getExistingDirectory(None, "Select a Directory...")
            else:
                fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter="All files(*)")
            if isinstance(fname, tuple):
                button.setText(str(fname[ 0 ]))
            else:
                button.setText(str(fname))
        elif "play" in buttonName:
            print("Here in start area")
            if self.runningRun is None:
                
                run_query = {"_id": ObjectId(button.id)}
                run = self.config.find_one(run_query)
                scan_query = {"Run_id": run["_id"]}
                for scan in self.scans.find(scan_query):
                    
                    print(scan)
                    tool_query = {"_id": scan["Tool_id"]}
                    tool = self.tools.find_one(tool_query)
                    
                    argumentList = list()
                    pathStr = """{}/{}""".format(tool["Path"], tool["Name"])
                    print(pathStr)
                    argumentList.append(pathStr)
                    argument_query = {"Tool_id": tool["_id"]}
                    arguments = self.optionsDB.find(argument_query)
                    for i in arguments:
                        argumentList.append(i["Option"])
                        
                    print(argumentList)
                    #Need to put arguments in the outputdatabase
                    inserter = {"Scan_id": scan["_id"], "Specification": "Tool Arguments", "Data": self.toString(argumentList)}
                    self.scanOutputs.insert_one(inserter)
                    self.processes.append([scan["_id"], 0, subprocess.Popen(argumentList, stdout = subprocess.PIPE)])
            else: 
                run_query = {"_id": self.runningRun}
                run = self.config.find_one(run_query)
                self.dialogs("Unable to execute Run", "Unable to execute requested run. Run {} is still in progress".format(run["Run Name"]), 1)

        elif buttonName == "Remove":
            ret = self.dialogs("Scan Type Removal", "Remove {} from the selected scans?".format(button))
            if ret == QMessageBox.Yes:
                for i in range(1, self.scanChoices.count()):
                    if self.scanChoices.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                        print("match at ", i)
                        self.scanChoices.itemAt(i).widget().setParent(None)
                        return
        elif buttonName == "AddScan":
            choice = str(self.scanType.currentText())
            # make layout to hold name and button
            hLayout = QHBoxLayout()
            addedLabel = QLabel(choice)
            removeButt = QPushButton("Remove")
            hLayout.addWidget(addedLabel)
            hLayout.addWidget(removeButt)

            # make a holder
            holder = QWidget()
            holder.setLayout(hLayout)
            # add it
            self.scanChoices.addWidget(holder)
            removeButt.clicked.connect(lambda: self.buttons("Remove", choice))
        elif "pause" in buttonName:
            for i in range(len(self.processes)):
                if self.processes[i][1] == 0:
                    self.processes[i][1] = 1
                    p = psutil.Process(self.processes[i][2].pid)
                    p.suspend()
                else: 
                     self.processes[i][1] = 0
                     p = psutil.Process(self.processes[i][2].pid)
                     p.resume()
        elif "stop" in buttonName: 
            for i in reversed(range(len(self.processes))): 
                self.processes[i][2].terminate()
                self.processes.pop(i)
            self.runningRun = None

        elif "Save" in buttonName:
            name = self.runName.text()
            description = self.runDesc.text()
            wlipText = self.WLIPtext.text()
            wlipFile = self.path.text()
            blipText = self.BLIPtext.text()
            blipFile = self.bPath.text()
            runFile = self.importFile.text()

            inputStr = {"Run Name": name, "Run Description": description, "Target Whitelist": wlipText,
                        "Whitelist File": wlipFile, "Target Blacklist": blipText, "Blacklist File": blipFile,
                        "Run Configuration File": runFile, "Status": "Configured"}
            runid = self.config.insert(inputStr)
            print(runid)
            for i in range(1, self.scanChoices.count()):
                scanQuery = {"Name": str(self.scanChoices.itemAt(i).widget().layout().itemAt(0).widget().text())}
                tool = self.tools.find_one(scanQuery)
                print(tool)
                tool_id = tool[ "_id" ]
                inputScan = {"Tool_id": tool_id, "Exec#": "7", "Run_id": runid, "Start": "n/a", "End": "n/a",
                             "Status": "Configured"}
                z = self.scans.insert_one(inputScan)
            for i in reversed(range(1, self.scanChoices.count())):
                self.scanChoices.itemAt(i).widget().setParent(None)
            self.drawTable()
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
                wlip = xml.SubElement(root, "TargetWhitelistIP")
                path = xml.SubElement(root, "WhitelistPath")
                blip = xml.SubElement(root, "TargetBlacklistIP")
                blipPath = xml.SubElement(root, "BlacklistPath")
                scanType = xml.SubElement(root, "ScanType")

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
        elif buttonName == "Switcher":
            if self.currMode == 1:
                self.currMode = 0
                self.runConfiguration.setVisible(False)
                self.toolImport.setVisible(False)
                self.scanList.setVisible(True)
                self.push.setText("Configure a Run")
            else: 
                self.currMode = 1
                self.runConfiguration.setVisible(True)
                self.toolImport.setVisible(True)
                self.scanList.setVisible(False)
                self.push.setText("View Scan Output")
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
        elif "output" in buttonName:
            if buttonName == "output":
                self.ScanId = button.id
                self.draw_tabs()
            else:
                self.RunId = button.id
                self.ScanId = None
                self.drawScanTable()
    def check_processes(self): 
        print("Checking processes")
        for i in reversed(range(len(self.processes))):
            if self.processes[i][1] == 1: 
                print("Paused status")
                continue
            else: 
                print(len(self.processes))
                print(self.processes[i][2])
                poll = self.processes[i][2].poll()
                print(poll)
                #Still running, ignore
                if poll is None: 
                    print("Still running")
                    try:
                        out, err = self.processes[i][2].communicate(timeout = 1)
                        if err is None: 
                            err = b" No Errors"
                        self.handleOutput(self.processes[i][0],str(out.decode("utf-8")), str(err.decode("utf-8")))
                        self.processes.pop(i)
                    except: 
                        pass    
                    continue
                else: 
                    #Give output to output handler
                    print("Output will be handled")
                    out, err = self.processes[i][2].communicate()
                    if err is None: 
                        err = b"No Errors"
                    self.handleOutput(self.processes[i][0],str(out.decode("utf-8")), str(err.decode("utf-8")))
                    self.processes.pop(i)
        if len(self.processes) < 1: 
            print("Now empty")
            self.runningRun = None
                    
    #Inserts Data Into the output section
    def handleOutput(self, scan_id, output, errors):
        print("Gonna Insert the Data!")
        inserter1 = {"Scan_id": scan_id, "Specification": "General Output", "Data": output}
        inserter2 = {"Scan_id": scan_id, "Specification": "Errors", "Data": errors}
        self.scanOutputs.insert_one(inserter1)
        self.scanOutputs.insert_one(inserter2)
    def dialogs(self, windowTitle, text, option= 0):
        if option == 0:
            ret = QMessageBox.information(self.win, windowTitle, text, QMessageBox.Yes | QMessageBox.Abort,
                                      QMessageBox.Abort)
        else: 
            ret = QMessageBox.information(self.win, windowTitle, text, QMessageBox.Ok)
        return ret
    #makes arguments go to string so it can be viewed in the gui
    def toString(self, arguments):
        baseStr = "Tool Path and command: {}\n".format(arguments[0])
        for i in arguments[1:]: 
            baseStr = baseStr + "{}\n".format(i)
        return baseStr
    def hide(self):
        self.runConfiguration.setVisible(False)
        self.toolImport.setVisible(False)
        self.toolList.setVisible(False)
        self.scanList.setVisible(False)

    def show(self):
        if self.currMode == 1:
            self.runConfiguration.setVisible(True)
            self.toolImport.setVisible(True)
        else: 
            self.scanList.setVisible(True)
        self.toolList.setVisible(True)
        self.update_ScanTypes()
