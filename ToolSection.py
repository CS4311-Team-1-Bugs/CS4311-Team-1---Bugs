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
#import xml.etree.ElementTree as xml
import lxml.etree as xml
import numpy as np

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
    
class ToolSection():
    
    def __init__(self, window):
        #database setup
        client = pymongo.MongoClient("mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['Test']
        self.tools = db["Tools"]

    
        self.optionsDB = db["Options"]
        self.outputDB = db["Output"]
    
        #variable setup
        self.win = window
        self.editMode = 0
        self.currId = 0
        
        #make all of our windows
        self.make_toolTable()
        self.make_toolImport()
        self.make_toolConfig()
        


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
        saveButt = util.make_saveCancel(self, 1)

        # Add spacing to the page and add our widgets
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(util.make_HBox(specTitle, 0))
        mainLayout.addWidget(util.make_HBox(toolSpec, 1))
        mainLayout.addWidget(util.make_HBox(depTitle, 0))
        mainLayout.addWidget(util.make_HBox(toolDep, 1))
        mainLayout.addWidget(saveButt)
        mainLayout.addStretch()

        main = QWidget()
        main.setLayout(mainLayout)

        self.toolEdit = QDockWidget()
        self.toolEdit.setTitleBarWidget(self.AddTitle)
        self.toolEdit.setWidget(main)
        self.win.addDockWidget(Qt.RightDockWidgetArea, self.toolEdit)

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
        pathBrowse.clicked.connect(lambda: self.buttons("Browse", self.path))
        browser.addWidget(pathBrowse)
        browser.addStretch()

        browserWidg = QWidget()
        browserWidg.setLayout(browser)

        opt_layout = QHBoxLayout()
        opt = QLineEdit()
        self.options = QVBoxLayout()
        opt.setAlignment(Qt.AlignLeft)
        opt_layout.addWidget(opt)
        add_opt = QPushButton("Add")
        add_opt.clicked.connect(lambda: self.buttons("Add", opt))
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
        addOutSpec.clicked.connect(lambda: self.buttons("AddS", outSpec),)
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

    def make_tool_dropdowns(self):
        self.model.clear()
        tools = self.tools.find()
        for tool in tools: 
            Id = tool["_id"]
            toolName = QStandardItem(tool["Name"])
            self.model.appendRow(toolName)
            
            out_query = {"Tool_id": Id}
            for i in self.outputDB.find(out_query):
                outputSpec = QStandardItem(i["OutputSpec"])
                toolName.appendRow(outputSpec)
        
    def updateToolDropdown(self, index):
        indx = self.model.index(index, 0, self.toolSelections.rootModelIndex())
        self.outputSelections.setRootModelIndex(indx)
        self.outputSelections.setCurrentIndex(0)
        
    def make_toolDep(self):
        layout = QVBoxLayout()
        self.model = QStandardItemModel()

        hButton = QHBoxLayout()
        
        
        self.toolSelections = QComboBox()
        self.toolSelections.setModel(self.model)
        
        self.outputSelections = QComboBox()
        self.outputSelections.setModel(self.model)
        self.make_tool_dropdowns()
        
        self.toolSelections.currentIndexChanged.connect(self.updateToolDropdown)
        self.updateToolDropdown(0)
        
        self.fieldPath = QLineEdit()
        
        self.operator = QComboBox()
        operatorOption = ["<",">","<=",">=","==","~="]
        self.operator.addItems(operatorOption)
        
        self.value = QLineEdit()
        
        
        hButton.addWidget(QLabel("Tool Name"))
        hButton.addWidget(self.toolSelections)
        hButton.addWidget(QLabel("Output Specification"))
        hButton.addWidget(self.outputSelections)
        hButton.addWidget(QLabel("Field Path "))
        hButton.addWidget(self.fieldPath)
        hButton.addWidget(QLabel("Operator"))
        hButton.addWidget(self.operator)
        hButton.addWidget(QLabel("Value"))
        hButton.addWidget(self.value)

        hButtonHolder = QWidget()
        hButtonHolder.setLayout(hButton)
        add = QPushButton("ADD")
        layout.addWidget(hButtonHolder)
        layout.addWidget(util.make_HBox(add, 0))


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
        browse.clicked.connect(lambda: self.buttons("Browse2", self.importFile))
        
        browsingLayout.addWidget(browse)
        browsingLayout.addStretch()
        browsing = QWidget()
        browsing.setLayout(browsingLayout)
        
        filePath = "file:///{}/SampleTool.xml".format(os.getcwd())
        sample = QLabel("<a href = {}>Open Sample Tool Specification File</a>".format(filePath))
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
        
    def hide(self):
        self.toolList.hide()
        self.toolEdit.hide()
        self.toolImport.hide()
    def show(self):
        self.toolImport.show()
        self.toolList.show()
        self.toolEdit.show()                        

    def buttons(self, buttonName, button):

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
                removeButt.clicked.connect(lambda: self.buttons("Remove", label))
            else:
                self.outputSpec.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda: self.buttons("RemoveS", label))

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
                            self.outputDB.delete_many(removeOpts)
                            self.make_tool_dropdowns()
                            return

        elif buttonName == "Cancel":
            self.name.setText("")
            self.description.setText("")
            self.path.setText("")
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
            if not self.editMode:
                inputStr = {"Name": name, "Description": description, "Path": path}
                self.tools.insert_one(inputStr)
               
                #tool id for options and output specifications
                tool_id = self.tools.find(inputStr)[0]["_id"]
                
                #for options
                for i in reversed(range(self.options.count())):
                    if i == 0: 
                        pass
                    else:
                        option = self.options.itemAt(i).widget().layout().itemAt(0).widget().text()
                        inputter = {"Tool_id": tool_id, "Option": option}
                        self.optionsDB.insert_one(inputter)
                        
                        
                #for output Specification
                for i in reversed(range(self.outputSpec.count())):
                    if i == 0: 
                        pass
                    else:
                        outputSpec = self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text()
                        inputter = {"Tool_id": tool_id, "OutputSpec": outputSpec}
                        self.outputDB.insert_one(inputter)
            else:
                self.editMode = 0
                self.AddTitle.setText("  Add a Tool  ")
                self.tools.update_one({"_id": self.currId}, { "$set": {"Name": name, "Description": description, "Path": path}})
                #options update
                deletelist = list()
                currentToolFilter = {"Tool_id": self.currId}
                for i in self.optionsDB.find(currentToolFilter): 
                    delete_flag = 1
                    for j in range(1, self.options.count()):
                        option = self.options.itemAt(j).widget().layout().itemAt(0).widget().text()
                        if i["Option"] == option:
                            delete_flag = 0
                            break 
                        
                    if delete_flag:    
                        delete_key = {"Tool_id": self.currId, "Option": i["Option"]}
                        deletelist.append(delete_key)
                
                for i in deletelist: 
                    self.optionsDB.delete_one(i)
                
                for i in range(1, self.options.count()):
                    option = self.options.itemAt(i).widget().layout().itemAt(0).widget().text()
                    inputter = {"Tool_id": self.currId, "Option": option}
                    self.optionsDB.update_one(inputter, { "$setOnInsert": inputter}, upsert = True)

                    
                        
                        
                deletelist = list()
                for i in self.outputDB.find(currentToolFilter): 
                    delete_flag = 1
                    for j in range(1, self.outputSpec.count()):
                        outputStr = self.outputSpec.itemAt(j).widget().layout().itemAt(0).widget().text()
                        if i["OutputSpec"] == outputStr:
                            delete_flag = 0
                            break 
                        
                    if delete_flag:    
                        delete_key = {"Tool_id": self.currId, "OutputSpec": i["OutputSpec"]}
                        deletelist.append(delete_key)
                
                for i in deletelist: 
                    self.outputDB.delete_one(i)
                
                for i in range(1, self.outputSpec.count()):
                    outputStr = self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text()
                    inputter = {"Tool_id": self.currId, "OutputSpec": outputStr}
                    self.outputDB.update_one(inputter, { "$setOnInsert": inputter}, upsert = True)
                        
            
            #Redraw the table and erase the text boxes
            self.drawTable()
            self.make_tool_dropdowns()
            self.buttons("Cancel", None)
        elif buttonName == "Switcher":
            self.editMode = 0
            self.AddTitle.setText("  Add a Tool  ")
            self.buttons("Cancel", None)
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
                removeButt.clicked.connect(lambda checked,  a = label:self.buttons("Remove", a))
                
                
            for i in self.outputDB.find(opt_query):
                label = i["OutputSpec"]
                # make layout to hold name and button
                hLayout = QHBoxLayout()
                addedLabel = QLabel(label)
                removeButt = QPushButton("Remove")
                hLayout.addWidget(addedLabel)
                hLayout.addWidget(removeButt)

                # make a holder
                holder = QWidget()
                holder.setLayout(hLayout)
           
                self.outputSpec.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda checked,  a = label: self.buttons("RemoveS", a))
                
                
                
        elif buttonName == "Export":
            fileName, _ = QFileDialog.getSaveFileName(self.win,"Export File Name","./","*.xml")
            if fileName:
                file = open(fileName, "wb")
                root = xml.Element("Tool")
                
                name = xml.SubElement(root, "Name")
                desc = xml.SubElement(root, "Description")
                path = xml.SubElement(root, "Path")
                
                name.text = self.name.text()
                desc.text = self.description.text()
                path.text = self.path.text()
                
                options = xml.SubElement(root, "Options")
                optStr = ""
                for i in range(1, self.options.count()):
                    optStr += self.options.itemAt(i).widget().layout().itemAt(0).widget().text() + ";"
                options.text = optStr
                
                output = xml.SubElement(root, "OutputSpec")
                outputStr = ""
                for i in range(1, self.outputSpec.count()):
                    outputStr += self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text() + ";"
                output.text = outputStr
                
                tree = xml.ElementTree(root)
                tree.write(file, pretty_print = True)
                file.close()
        elif buttonName == "Import": 
            filename = button.text()
            root = xml.parse(filename).getroot()
            name = root.find("Name")
            description = root.find("Description")
            path = root.find("Path")
            option = root.find("Options")
            if option is not None:
                optionsArr = option.text.split(";")[:-1]
            else:
                optionsArr = []
            output = root.find("OutputSpec")
            if output is not None:
                outputSpecArr = output.text.split(";")[:-1]
            else:
                outputSpecArr = []
            
            if name is not None:
                self.name.setText(name.text)
            if description is not None:
                self.description.setText(description.text)
            if path is not None:
                self.path.setText(path.text)
                
            for label in optionsArr:
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
                removeButt.clicked.connect(lambda checked,  a = label:self.buttons("Remove", a))
                
                
            for label in outputSpecArr:
                # make layout to hold name and button
                hLayout = QHBoxLayout()
                addedLabel = QLabel(label)
                removeButt = QPushButton("Remove")
                hLayout.addWidget(addedLabel)
                hLayout.addWidget(removeButt)

                # make a holder
                holder = QWidget()
                holder.setLayout(hLayout)
           
                self.outputSpec.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda checked,  a = label: self.buttons("RemoveS", a))
                

    def drawTable(self, reversed = 0):
        table = self.tableWidget
        index = 1
        tools = self.tools.find()
        maxInd = self.tools.count_documents({})
        
        if reversed:
            start, end, increment = maxInd-1, -1, -1
        else: 
            start, end, increment = 0, maxInd, 1
        for i in range(start, end, increment):
            tool = tools[i]
            if index < table.rowCount():
                pass
            else:
                table.insertRow(index)
            table.setCellWidget(index, 0, QLabel(tool[ "Name" ]))
            table.setCellWidget(index, 1, QLabel(tool[ "Description" ]))
            Buttons = QWidget()
            ButtonLayout = QHBoxLayout()
            edit = QTablePush(tool["_id"], "Edit.png", self)
            remove = QTablePush(tool["_id"],"RemoveT.png", self)
            ButtonLayout.addWidget(edit)
            ButtonLayout.addWidget(remove)
            Buttons.setLayout(ButtonLayout)
            table.setCellWidget(index, 2, Buttons)
            #table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 3, QLabel(str(tool[ "_id" ])))
            index += 1
            
        for i in range(1, self.tableWidget.rowCount()):
            self.tableWidget.verticalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
            

    def dialogs(self, windowTitle, text):
        ret = QMessageBox.question(self.win, windowTitle, text, QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)
        return ret


