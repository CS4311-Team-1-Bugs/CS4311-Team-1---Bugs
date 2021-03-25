# -*- coding: utf-8 -*-

import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)
        client = pymongo.MongoClient("mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client['Test']

        self.tools = db["Tools"]
        self.optionsDB = db["Options"]
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
        self.make_toolConfig()

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
        mainTitle = QLabel()
        mainTitle.setText("  Add a Tool  ")
        mainTitle.setFont(QFont("Times", 16))
        mainTitle.setStyleSheet("background-color: #49d1e3")
        mainTitle.setAlignment(Qt.AlignLeft)

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
        saveButt = self.make_saveCancel()

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
        self.toolEdit.setTitleBarWidget(mainTitle)
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

        orLabel = QLabel("OR")

        specFile_container = QHBoxLayout()
        self.specFile = QLineEdit()
        self.specFile.setAlignment(Qt.AlignLeft)
        specFile_container.addWidget(self.specFile)

        browse = QPushButton("Browse")
        browse.clicked.connect(lambda: self.tool_buttons("Browse", self.specFile))
        specFile_container.addWidget(browse)
        specFile_container.addStretch()
        specFile_widg = QWidget()
        specFile_widg.setLayout(specFile_container)

        layout.addRow(QLabel("Tool Name"), self.name)
        layout.addRow(QLabel("Tool Description"), self.description)
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
        operatorOption = ["N/A","<",">","<=",">=","==","~="]
        logicalOption = ["N/A","AND","OR","NOT"]
        options2.addItems(operatorOption)
        option3 = QComboBox()
        option4 = QComboBox()
        hButton.addWidget(options2)
        hButton.addWidget(option3)
        hButton.addWidget(option4)
        option3.addItems(logicalOption)
        option4.addItems(operatorOption)
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

    def make_saveCancel(self):
        layout = QHBoxLayout()
        save = QPushButton("Save")
        save.setStyleSheet("background-color: #54e86c")
        save.clicked.connect(lambda: self.tool_buttons("Save", None))
        cancel = QPushButton("Cancel")
        cancel.setStyleSheet("background-color: #e6737e")
        cancel.clicked.connect(lambda: self.tool_buttons("Cancel", None))
        layout.addSpacing(20)
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(cancel)
        layout.addWidget(save)

        container = QWidget()
        container.setLayout(layout)
        return container
        # pad a widget with horizontal spacing or stretching

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
        nameSortButton = QToolButton()
        nameSortButton.setArrowType(Qt.DownArrow)
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
        self.tableWidget.setCellWidget(0, 2, QLabel("Modify"))
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
        addLayout.addWidget(push)
        holder = QWidget()
        holder.setLayout(addLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addWidget(holder)
        mainLayout.addStretch()

        main = QWidget()
        main.setLayout(mainLayout)

        self.drawTable()

        self.toolList = QDockWidget()
        self.toolList.setTitleBarWidget(menuTitle)
        self.toolList.setWidget(main)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolList)

        # Quick code to make the menu buttons work

    def menu_buttons(self, button):
        if button == "Run":
            self.toolList.hide()
            self.toolEdit.hide()
        else:
            self.toolList.show()
            self.toolEdit.show()

    def tool_buttons(self, buttonName, button):

        if buttonName == "Browse":
            fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter="All files (*)")
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
                for i in range(self.options.count()):
                    if i == 0:
                        continue
                        # print(i)
                    # print(self.options.itemAt(i).widget().layout().itemAt(0).widget().text())
                    # print("button text is", button)
                    if self.options.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                        # print("match at ", i)
                        self.options.itemAt(i).widget().setParent(None)
                        return

            elif buttonName == "RemoveS":
                for i in range(self.outputSpec.count()):
                    if i == 0:
                        continue
                    if self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                        self.outputSpec.itemAt(i).widget().setParent(None)
                        return
            else:

                for i in range(self.tableWidget.rowCount()):
                    if i == 0:
                        continue
                    print("target", button)
                    print("actual", self.tableWidget.cellWidget(i, 3).text())
                    if self.tableWidget.cellWidget(i, 3).text() == button:
                        print("Going to remove row", i)
                        self.tableWidget.removeRow(i)
                        removeDict = {"_id": button}
                        self.tools.delete_one(removeDict)
                        return

        elif buttonName == "Cancel":
            self.name.setText("")
            self.description.setText("")
            self.path.setText("")
            self.option.setText("")
            self.specFile.setText("")
            for i in reversed(range(self.options.count())):
                if i != 0:
                    self.options.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.options.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.outputSpec.count())):
                if i != 0:
                    self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.outputSpec.itemAt(i).widget().setParent(None)
        elif buttonName == "Save":
            name = self.name.text()
            description = self.description.text()
            path = self.path.text()
            spec = self.specFile.text()
            inputStr = {"Name": name, "Description": description, "Path": path, "Options": "{1}", "Output": "{222}",
                        "Specification": spec}
            self.tools.insert_one(inputStr)
            self.drawTable()
            self.tool_buttons("Cancel", None)

    def drawTable(self):
        table = self.tableWidget
        index = 1
        for i in self.tools.find():
            if index < table.rowCount():
                pass
            else:
                table.insertRow(index)
            table.setCellWidget(index, 0, QLabel(i[ "Name" ]))
            table.setCellWidget(index, 1, QLabel(i[ "Description" ]))
            table.setCellWidget(index, 2, QPushButton("Remove"))
            table.setCellWidget(index, 3, QLabel(str(i[ "_id" ])))
            index += 1
        for i in range(1, self.tableWidget.rowCount()):
            string = table.cellWidget(i, 3).text()
            table.cellWidget(i, 2).clicked.connect(lambda: self.tool_buttons("RemoveT", string))

if __name__ == "__main__":
        app = QApplication(sys.argv)
        win = MainWindow()
        win.show()
        sys.exit(app.exec())
