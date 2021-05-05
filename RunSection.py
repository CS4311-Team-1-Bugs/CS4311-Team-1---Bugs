import sys
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
#from ToolSection import QTablePush
import subprocess


class QTablePush(QPushButton):
     def __init__(self, id, text, toolSection):
        #init the window
        super(QPushButton, self).__init__()
        self.setIcon(QIcon(QPixmap(text)))
        self.setIconSize(QSize(16,16))
        self.id = str(id)
        self.setToolTip(text[:-4])
        self.section = toolSection
        self.clicked.connect(lambda: self.section.buttons(text[:-4], self))

class RunSection():
    def __init__(self, window):
        self.win = window
        self.run_config()
        self.edit()
        self.importFile()
        self.make_scanTable()


    def run_config(self):

        # Establish Connection to MongoDB - Run Config
        client = pymongo.MongoClient(
            "mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client[ 'Test' ]
        self.tools = db["Tools"]
        self.config = db[ "Run Config" ]
        self.scans = db["Scans"]
        self.scanOutputs = db["scanOutput"]
        


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
            start.clicked.connect(lambda:self.buttons("Start",None))
            pause= QTablePush(tool[ "_id" ], "pause.png", self)
            pause.clicked.connect(lambda:self.buttons("Pause",None))
            stop = QTablePush(tool[ "_id" ], "stop.png", self)
            stop.clicked.connect(lambda:self.buttons("Stop",None))
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
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
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
    
    def drawScanTable(self, reversed = 0):
        self.runID = "7"
        query = {"Run_ID": self.runID}
        table = self.scanTable
        index = 1
        scans = self.scans.find(query)
        maxInd = self.scans.count_documents({})
        
        if reversed:
            start, end, increment = maxInd-1, -1, -1
        else: 
            start, end, increment = 0, maxInd, 1
        for i in range(start, end, increment):
            scan = scans[i]
            if index < table.rowCount():
                pass
            else:
                table.insertRow(index)
            table.setCellWidget(index, 0, QLabel(scan[ "Name" ]))
            table.setCellWidget(index, 1, QLabel(scan[ "Exec#" ]))
            table.setCellWidget(index, 2, QLabel(scan[ "Start" ]))
            table.setCellWidget(index, 3, QLabel(scan[ "End" ]))
            table.setCellWidget(index, 4, QLabel(scan[ "Status" ]))
            
            Buttons = QWidget()
            ButtonLayout = QHBoxLayout()
            start = QTablePush(scan[ "_id" ], "play.png", self)
            #start.clicked.connect(lambda:self.buttons("Start",None))
            pause= QTablePush(scan[ "_id" ], "pause.png", self)
            #pause.clicked.connect(lambda:self.buttons("Pause",None))
            stop = QTablePush(scan[ "_id" ], "stop.png", self)
            #stop.clicked.connect(lambda:self.buttons("Stop",None))
            output = QTablePush(scan["_id"], "output.png", self)
            ButtonLayout.addWidget(start)
            ButtonLayout.addWidget(pause)
            ButtonLayout.addWidget(stop)
            ButtonLayout.addWidget(output)
            Buttons.setLayout(ButtonLayout)
            table.setCellWidget(index, 5, Buttons)
            #table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 6, QLabel(str(scan[ "_id" ])))
            index += 1
            
        for i in range(1, self.scanTable.rowCount()):
            self.scanTable.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            
        
    
    def draw_tabs(self): 
        for i in range(self.tabWidget.count()): 
                self.tabWidget.removeTab(0);
        print("here")
        
        query = {"tool_id": ObjectId(self.ScanId)}
        outputs = self.scanOutputs.find(query)
        print("just did the query")
  
        
        for i in outputs: 
            print("found some")
            tab = QWidget()
            layout = QVBoxLayout()
            text = QLineEdit()
            text.setText(i["Data"])
            layout.addWidget(text)
            tab.setLayout(layout)
            self.tabWidget.addTab(tab, i["Specification"])
            


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
        self.win.addDockWidget(Qt.RightDockWidgetArea, self.toolImport)
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
        elif "Start" in buttonName:
            #since the id is not working then i need to just pretend that i do have it.
            
  #          self.config.find()
            start = self.dialogs("Starting Run", "Run has been started")
  #          print(self.config)
            
            sampleS = self.tools.find()
            for i in sampleS:
                 print(i)
 #               print("_id", i['_id'])
  #              print("toolname " ,i['Scan Type'])
            

            
            #for testing
            Id = ObjectId('60842f0f29a941469eca411b') 
            path = r"C:/Program Files (x86)/Nmap" # this would be aquired from a query to the db instead
            
            
            self.currid = Id
            query = {"_id": Id}
            matchingRun = self.config.find_one(query)
    #        for runTools in matchingRun:  # i don't think i need this. 
            whitelist = matchingRun['Target Whitelist']
            whitelistFile = matchingRun['Whitelist File']
            blacklist = matchingRun['Target Blacklist']
            blacklistFile = matchingRun['Blacklist File']
            print(matchingRun)
            
            query = {"Run_id": Id}
            #toolquery ={"tool_id": ObjectId(self.ScanId)}
            tooloutputs =self.tools.find(query)
            
            
            if whitelist != None:
                whitelistargs = f"-il {whitelist}"
            else:
                whitelistargs = f"{whitelist}"
                # assemble blacklist args
                
                

#            if blacklist != NULL:
#                if isinstance(blacklist, file):
#                    blacklistargs

            argslist = f"{path} {whitelist}"
            print( argslist)
            p1 = subprocess.run([path, whitelist], capture_output =True )

            print(p1.stderr)
            print(p1.stdout.decode())
            
            
            
        elif "Pause" in buttonName:
            pause = self.dialogs("Pausing Run", "Run has been paused")
        elif "Stop" in buttonName:
            stop = self.dialogs("Stopping Run", "Run has been stopped")

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
        elif buttonName == "output": 
            self.ScanId = button.id
            self.draw_tabs()
            self.currRunRunning = 0;
        


    def dialogs(self, windowTitle, text):
        ret = QMessageBox.information(self.win, windowTitle, text, QMessageBox.Yes | QMessageBox.Abort, QMessageBox.Abort)
        return ret

    def hide(self):
        self.runConfiguration.setVisible(False)
        self.toolImport.setVisible(False)
        self.toolList.setVisible(False)
        self.scanList.setVisible(False)

    def show(self):
        self.runConfiguration.setVisible(True)
        self.toolImport.setVisible(True)
        self.toolList.setVisible(True)
        self.scanList.setVisible(True)
