# -*- coding: utf-8 -*-

import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo
from bson.objectid import ObjectId
import datetime
import os

class QTablePush(QPushButton):
     global win
     def __init__(self, id, text):
        #init the window
        super(QPushButton, self).__init__()
        self.setIcon(QIcon(QPixmap(text)))
        self.setIconSize(QSize(16,16))
        self.id = str(id)
        self.setToolTip(text[:-4])
        self.clicked.connect(lambda: win.tool_buttons(text[:-4], self))
    
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)
        client = pymongo.MongoClient("mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['Test']

        self.tools = db["Tools"]
        self.optionsDB = db["options"]
        self.outputSpec = db["Output"]

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
        self.make_toolTable()
        self.make_toolImport()
        self.make_toolConfig()
        self.run_config()
        self.editMode = 0
        self.currId = 0
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
        runButton.clicked.connect(lambda: self.menu_buttons("Run"))
        toolButton = QPushButton("Tools")
        toolButton.clicked.connect(lambda: self.menu_buttons("Tool"))
        hLayout.addStretch()
        hLayout.addWidget(runButton)
        hLayout.addStretch()
        hLayout.addWidget(toolButton)
        hLayout.addStretch()

        # Add the widgets we created to the menu layout
        menuLayout.addWidget(self.make_HBox(menuTitle, 0))
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)

        return menuLayout

    def make_toolConfig(self):

        # Title component of menu
        self.AddTitle = QLabel()
        self.AddTitle.setText("  Add a Tool  ")
        self.AddTitle.setFont(QFont("Times", 16))
        self.AddTitle.setStyleSheet("background-color: #49d1e3")
        self.AddTitle.setAlignment(Qt.AlignLeft)

        # Title component of menu
        specTitle = QLabel()
        specTitle.setText("  Tool Specification  ")
        specTitle.setFont(QFont("Times", 12))
        specTitle.setStyleSheet("border: 1px solid black; color: #000000")
        specTitle.setAlignment(Qt.AlignCenter)

        # Tool Specification Section
        toolSpec = self.make_toolSpec()

        # Dependency Title
        depTitle = QLabel()
        depTitle.setText("  Tool Dependency  ")
        depTitle.setFont(QFont("Times", 12))
        depTitle.setStyleSheet("border: 1px solid black; color: #000000")
        depTitle.setAlignment(Qt.AlignCenter)

        # Tool Dependency Section
        toolDep = self.make_toolDep()

        # Save Button Section
        saveButt = self.make_saveCancel(1)

        # Add spacing to the page and add our widgets
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.make_HBox(specTitle, 0))
        mainLayout.addWidget(self.make_HBox(toolSpec, 1))
        mainLayout.addWidget(self.make_HBox(depTitle, 0))
        mainLayout.addWidget(self.make_HBox(toolDep, 1))
        mainLayout.addWidget(saveButt)
        mainLayout.addStretch()

        main = QWidget()
        main.setLayout(mainLayout)

        self.newTool = 1

        self.toolEdit = QDockWidget()
        self.toolEdit.setTitleBarWidget(self.AddTitle)
        self.toolEdit.setWidget(main)
        self.addDockWidget(Qt.RightDockWidgetArea, self.toolEdit)

    def make_toolSpec(self):
        layout = QFormLayout()

        self.name = QLineEdit()
        self.name.setAlignment(Qt.AlignLeft)

        self.description = QLineEdit()
        self.description.setAlignment(Qt.AlignLeft)

        browser = QHBoxLayout()
        self.path = QLineEdit()
        self.path.setAlignment(Qt.AlignLeft)
        browser.addWidget(self.path)
        pathBrowse = QPushButton("Browse")
        pathBrowse.clicked.connect(lambda: self.tool_buttons("Browse", self.path))
        browser.addWidget(pathBrowse)
        browser.addStretch()

        browserWidg = QWidget()
        browserWidg.setLayout(browser)

        opt_layout = QHBoxLayout()
        opt = QLineEdit()
        self.options = QVBoxLayout()
        self.option = opt
        opt.setAlignment(Qt.AlignLeft)
        opt_layout.addWidget(opt)
        add_opt = QPushButton("Add")
        add_opt.clicked.connect(lambda: self.tool_buttons("Add", opt))
        opt_layout.addWidget(add_opt)
        opt_layout.addStretch()

        editor = QWidget()

        editor.setLayout(opt_layout)
        self.options.addWidget(editor)

        opt_widg = QWidget()
        opt_widg.setLayout(self.options)

        self.outputSpec = QVBoxLayout()

        outSpecLayout = QHBoxLayout()
        outSpec = QLineEdit()
        outSpec.setAlignment(Qt.AlignLeft)
        outSpecLayout.addWidget(outSpec)
        addOutSpec = QPushButton("Add")
        addOutSpec.clicked.connect(lambda: self.tool_buttons("AddS", outSpec),)
        outSpecLayout.addWidget(addOutSpec)
        outSpecLayout.addStretch()

        holder = QWidget()
        holder.setLayout(outSpecLayout)
        self.outputSpec.addWidget(holder)
        outSpec_widg = QWidget()
        outSpec_widg.setLayout(self.outputSpec)

       

        layout.addRow(QLabel("Tool Name"), self.name)
        layout.addRow(QLabel("Tool Description"), self.description)
        layout.addRow(QLabel("Tool Path"), browserWidg)
        layout.addRow(QLabel("Option and Argument"), opt_widg)
        layout.addRow(QLabel("Output Specification"), outSpec_widg)

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
        operatorOption = ["N/A","<",">","<=",">=","==","~="]
        logicalOption = ["N/A","AND","OR","NOT"]
        options2.addItems(operatorOption)
        hButton.addWidget(options2)

        hButton.addWidget(QLabel("Value"))
        hButton.addWidget(QLineEdit())
        hButton.addWidget(QPushButton("Remove"))
        hButtonHolder = QWidget()
        hButtonHolder.setLayout(hButton)
        add = QPushButton("ADD")
        layout.addWidget(hButtonHolder)
        layout.addWidget(self.make_HBox(add, 0))


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

    def make_saveCancel(self, exportOption = 0):
        layout = QHBoxLayout()
        save = QPushButton("Save")
        save.setStyleSheet("background-color: #54e86c")
        save.clicked.connect(lambda: self.tool_buttons("Save", None))
        cancel = QPushButton("Cancel")
        cancel.setStyleSheet("background-color: #e6737e")
        cancel.clicked.connect(lambda: self.tool_buttons("Cancel", None))
        if exportOption:
            export = QPushButton("Export Current Configuration to XML")
            export.setStyleSheet("background-color: #49d1e3")
            export.clicked.connect(lambda: self.tool_buttons("Export", None))
            
            
        layout.addStretch()
        
        layout.addWidget(cancel)
        if exportOption: 
            layout.addWidget(export)
        layout.addWidget(save)
        layout.addStretch()

        container = QWidget()
        container.setLayout(layout)
        return container
        # pad a widget with horizontal spacing or stretching

    def make_HBox(self, widget, spacingType):
        layout = QHBoxLayout()
        if spacingType == 1:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        layout.addWidget(widget)
        if spacingType == 1:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        container = QWidget()
        container.setLayout(layout)
        return container

    def make_toolTable(self):

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Tool List  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        # Create Tool Content Details layer
        self.tableWidget = QTableWidget(1, 4)
        self.tableWidget.setColumnHidden(3, True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # column 1
        col1Title = QLabel()
        col1Title.setText("Tool Name")
        self.sortArrow = "down"
        nameSortButton = QToolButton()
        nameSortButton.setArrowType(Qt.DownArrow)
        nameSortButton.clicked.connect(lambda: self.tool_buttons("Sort", nameSortButton))
        col1Layout = QHBoxLayout()
        col1Layout.addStretch()
        col1Layout.addWidget(col1Title)
        col1Layout.addWidget(nameSortButton)
        col1Layout.addStretch()

        # Set Columns for the table
        col1Widget = QWidget()
        col1Widget.setLayout(col1Layout)
        self.tableWidget.setCellWidget(0, 0, col1Widget)
        self.tableWidget.setCellWidget(0, 1, QLabel("Description of Tool"))
        self.tableWidget.setCellWidget(0, 2, QLabel("  Modify"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()

        # Add button
        addLayout = QHBoxLayout()
        addLayout.addStretch(1)
        push = QPushButton("Add Tool")
        push.setStyleSheet("background-color: #54e86c")
        push.clicked.connect(lambda: self.tool_buttons("Switcher", None))
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
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolList)


    def make_toolImport(self):
         # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText(" Tool Import ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)
        
    
        browsingLayout = QHBoxLayout()
        browseLabel = QLabel("Tool Specification File ")
        browsingLayout.addStretch()
        browsingLayout.addWidget(browseLabel)
        
        self.importFile = QLineEdit()
        self.importFile.setAlignment(Qt.AlignLeft)
        browsingLayout.addWidget(self.importFile)
        
        browse = QPushButton("Browse")
        browse.clicked.connect(lambda: self.tool_buttons("Browse2", self.importFile))
        
        browsingLayout.addWidget(browse)
        browsingLayout.addStretch()
        browsing = QWidget()
        browsing.setLayout(browsingLayout)
        
        filePath = "file:///{}/SampleTool.xml".format(os.getcwd())
        sample = QLabel("<a href = {}>Open Sample Tool Specification File</a>".format(filePath))
        sample.setOpenExternalLinks(True)
        
        importer = QPushButton("Import")
        importer.setStyleSheet("background-color: #54e86c")
        importer.clicked.connect(lambda: self.tool_buttons("Import", self.importFile))
        importerWidget = self.make_HBox(importer, 0)
        
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
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolImport)
        
        
        
        
        
    # Quick code to make the menu buttons work
    def menu_buttons(self, button):
        if button == "Run":
            self.toolList.hide()
            self.toolEdit.hide()
            self.toolImport.hide()
            self.runConfiguration.show()
        else:
            self.toolImport.show()
            self.toolList.show()
            self.toolEdit.show()
            
            self.runConfiguration.hide()

    def tool_buttons(self, buttonName, button):

        if "Browse" in buttonName:
            if buttonName == "Browse":
                fname = QFileDialog.getExistingDirectory(None, "Select a Directory...")
            else: 
                fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter = "*.xml")
            if isinstance(fname, tuple):
                button.setText(str(fname[ 0 ]))
            else:
                button.setText(str(fname))
        elif "Add" in buttonName:
            label = button.text()
            button.setText("")
            # make layout to hold name and button
            hLayout = QHBoxLayout()
            addedLabel = QLabel(label)
            removeButt = QPushButton("Remove")
            hLayout.addWidget(addedLabel)
            hLayout.addWidget(removeButt)

            # make a holder
            holder = QWidget()
            holder.setLayout(hLayout)
            # add it
            if buttonName == "Add":
                self.options.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda: self.tool_buttons("Remove", label))
            else:
                self.outputSpec.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda: self.tool_buttons("RemoveS", label))

            button.setText("")

        elif "Remove" in buttonName:
            if buttonName == "Remove":
                ret = self.dialogs("Option Removal", "Remove {} from the options?".format(button))
                if ret == QMessageBox.Yes:
                    for i in range(self.options.count()):
                        if i == 0:
                            continue
                            # print(i)
                        if self.options.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                            # print("match at ", i)
                            self.options.itemAt(i).widget().setParent(None)
                            return

            elif buttonName == "RemoveS":
                ret = self.dialogs("Output Specification Removal", "Remove {} from the output specification? ".format(button))
                if ret == QMessageBox.Yes:
                    for i in range(self.outputSpec.count()):
                        if i == 0:
                            continue
                        if self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                            self.outputSpec.itemAt(i).widget().setParent(None)
                            return
            else:
                ret = self.dialogs("Tool Removal", "Remove the Selected Tool?")

                if ret == QMessageBox.Yes:
                    for i in range(1, self.tableWidget.rowCount()):
                        #print("target", button.id)
                        #print("actual", self.tableWidget.cellWidget(i, 3).text())
                        if self.tableWidget.cellWidget(i, 3).text() == button.id:
                            #print("Going to remove row", i)
                            self.tableWidget.removeRow(i)
                            removeDict = {"_id": ObjectId(button.id)}
                            self.tools.delete_one(removeDict)
                            
                            removeOpts = {"Tool_id": ObjectId(button.id)}
                            self.optionsDB.delete_many(removeOpts)
                            return

        elif buttonName == "Cancel":
            self.name.setText("")
            self.description.setText("")
            self.path.setText("")
            #self.option.setText("")
            self.specFile.setText("")
            for i in reversed(range(self.options.count())):
                if i == 0:
                    self.options.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.options.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.outputSpec.count())):
                if i == 0:
                    self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.outputSpec.itemAt(i).widget().setParent(None)
            if self.editMode == 1:
                self.editMode = 0
                self.AddTitle.setText("Add a Tool")
        elif buttonName == "Save":
            name = self.name.text()
            description = self.description.text()
            path = self.path.text()
            spec = self.specFile.text()
            if not self.editMode:
                inputStr = {"Name": name, "Description": description, "Path": path, "Options": "{1}", "Output": "{222}",
                            "Specification": spec}
                self.tools.insert_one(inputStr)
               
                #inserting all the options
                tool_id = self.tools.find(inputStr)[0]["_id"]
                for i in reversed(range(self.options.count())):
                    option = self.options.itemAt(i).widget().layout().itemAt(0).widget().text()
                    inputter = {"Tool_id": tool_id, "Option": option}
                    self.optionsDB.insert_one(inputter)
            else:
                self.editMode = 0
                self.AddTitle.setText("  Add a Tool  ")
                self.tools.update_one({"_id": self.currId}, { "$set": {"Name": name, "Description": description, "Path": path, "Specification": spec}})
                
                
                #options update
                self.optionsDB.delete_many({"Tool_id": self.currId})
                for i in reversed(range(self.options.count())):
                    option = self.options.itemAt(i).widget().layout().itemAt(0).widget().text()
                    inputter = {"Tool_id": self.currId, "Option": option}
                    self.optionsDB.insert_one(inputter)
            
            #Redraw the table and erase the text boxes
            self.drawTable()
            self.tool_buttons("Cancel", None)
        elif buttonName == "Switcher":
            self.editMode = 0
            self.AddTitle.setText("  Add a Tool  ")
            self.tool_buttons("Cancel", None)
        elif buttonName == "Sort":
            if self.sortArrow == "down":
                button.setArrowType(Qt.UpArrow)
                self.drawTable(1)
                self.sortArrow = "up"
            else:
                button.setArrowType(Qt.DownArrow)
                self.drawTable()
                self.sortArrow = "down"
                
        elif buttonName == "Edit":
            Id = ObjectId(button.id)
            self.currId = Id
            self.editMode = 1
            query = {"_id": Id}
            tool = self.tools.find(query)[0]
            self.name.setText(tool["Name"])
            self.description.setText(tool["Description"])
            self.path.setText(tool["Path"])
            self.specFile.setText(tool["Specification"])
            self.AddTitle.setText("  Edit a Tool  ")
            
            opt_query = {"Tool_id": Id}
            for i in self.optionsDB.find(opt_query):
                label = i["Option"]
                # make layout to hold name and button
                hLayout = QHBoxLayout()
                addedLabel = QLabel(label)
                removeButt = QPushButton("Remove")
                hLayout.addWidget(addedLabel)
                hLayout.addWidget(removeButt)

                # make a holder
                holder = QWidget()
                holder.setLayout(hLayout)
           
                self.options.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda checked,  a = label: self.tool_buttons("Remove", a))
        #elif buttonName == "Import": 
            #file = open()
            
            

    def drawTable(self, reversed = 0):
        table = self.tableWidget
        index = 1
        tools = self.tools.find()
        maxInd = self.tools.count_documents({})
        for i in range(1, maxInd):
            if reversed: 
                tool = tools[maxInd - i]
            else:
                tool = tools[i]
            if index < table.rowCount():
                pass
            else:
                table.insertRow(index)
            table.setCellWidget(index, 0, QLabel(tool[ "Name" ]))
            table.setCellWidget(index, 1, QLabel(tool[ "Description" ]))
            
            Buttons = QWidget()
            ButtonLayout = QHBoxLayout()
            edit = QTablePush(tool["_id"], "Edit.png")
            remove = QTablePush(tool["_id"],"RemoveT.png")
            ButtonLayout.addWidget(edit)
            ButtonLayout.addWidget(remove)
            Buttons.setLayout(ButtonLayout)
            table.setCellWidget(index, 2, Buttons)
            #table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 3, QLabel(str(tool[ "_id" ])))
            index += 1
            
        for i in range(1, self.tableWidget.rowCount()):
            self.tableWidget.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            
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
        orLabel = self.orLabel()
        orLabel1 =self.orLabel()
        orLabel2 = self.orLabel()
        
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



        
        buttonWidget = self.make_saveCancel()

        runConfigLayout.addWidget(buttonWidget)
        runConfigLayout.setVerticalSpacing(20)
        runConfigLayout.setHorizontalSpacing(10)
        main = QWidget()
        main.setLayout(runConfigLayout)
        
        self.runConfiguration = QDockWidget()
        self.runConfiguration.setTitleBarWidget(menuTitle)
        self.runConfiguration.setWidget(main)
        self.addDockWidget(Qt.RightDockWidgetArea, self.runConfiguration)
        self.runConfiguration.setVisible(False)
        return 
        
    
    def orLabel(self):
        
        orLabel = QLabel()
        orLabel.setText("-OR-")
        orLabel.setAlignment(Qt.AlignCenter)
        serifFont = QFont("TimesNewRoman", 14)
        orLabel.setFont(serifFont)
        return orLabel

    def dialogs(self, windowTitle, text):
        ret = QMessageBox.question(self, windowTitle, text, QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        return ret
if __name__ == "__main__":
        global win
        app = QApplication(sys.argv)
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
        
        #tacos = QTablePush(7)
        #print(tacos.id)

