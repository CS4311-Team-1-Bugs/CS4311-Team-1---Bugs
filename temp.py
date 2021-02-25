import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        #init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        #Set the Window Title
        self.setWindowTitle("XML Report")
        
        
        
        #set menu layout
        menuLayout = QVBoxLayout()
        
        #Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("SEA Menu")
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
        
        #XML Title 
        XMLTitle=QLabel()
        XMLTitle.setText("XML Report")
        XMLTitle.setAlignment(Qt.AlignCenter)
        
        #XML  info name
        l1=QLabel()
        l1.setText("Report Name:")
        l1.setAlignment(Qt.AlignLeft)
        ReportName=QLineEdit()
    
         #XML info description
        l2=QLabel()
        l2.setText("Report Description:")
        l2.setAlignment(Qt.AlignLeft)
        ReportDescription=QTextEdit()

        #XML Run drop box
        self.run=QComboBox()
        self.run.addItem("Run")
        self.run.addItems(["02/21/2021 @1:30","02/21/2021 @3:30" ])
        
        #other OR label
        l3=QLabel()
        l3.setText("OR")
        l3.setAlignment(Qt.AlignCenter)
       
        orRow=QHBoxLayout()
       
       #XML Run drop box
        self.r=QComboBox()
        self.r.addItem("Run")
        self.r.addItems(["02/21/2021 @1:30","02/21/2021 @3:30" ])
        
        #XML scan drop box
        self.scan=QComboBox()
        self.scan.addItem("Scan")
        self.scan.addItems(["NESSUS","NMAP" ])
        
        #Remove button in row
        add=QPushButton("ADD")
       
        remove=QPushButton("REMOVE")
        orRow.addStretch()
        orRow.addWidget(self.r)
        orRow.addStretch()
        orRow.addWidget(self.scan)
        orRow.addStretch()
        orRow.addWidget(remove)
        orRow.addStretch()
        orRow.addWidget(add)
        add.clicked.connect(self.addRow)
      
            
         #last row of buttons generate and cancel
        XML = QHBoxLayout()
        oneButton = QPushButton("GENERATE")
      
        twoButton = QPushButton("CANCEL")
        XML.addStretch()
        XML.addWidget(twoButton)
        XML.addStretch()
        oneButton.setStyleSheet("background-color: green")
        XML.addWidget(oneButton)
     
        
        #Add the widgets we created to the menu layout
        menuLayout.addWidget(menuTitle)
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)
        
        #adding XML portions
        menuLayout.addWidget(XMLTitle)
        menuLayout.addWidget(l1)
        menuLayout.addWidget(ReportName)
        menuLayout.addWidget(l2)
        menuLayout.addWidget(ReportDescription)
        menuLayout.addWidget(self.run)
        menuLayout.addWidget(l3)
        
        #adding rows 
        orRows=QWidget()
        orRows.setLayout(orRow)
        menuLayout.addWidget(orRows)
        

        #adding buttons
        xmlButtons=QWidget()
        xmlButtons.setLayout(XML)
        menuLayout.addWidget(xmlButtons)
        
        #Make a Widget to hold the layout and set it as the window's menu
        menuWidget = QWidget()
        menuWidget.setLayout(menuLayout)               
        self.setMenuWidget(menuWidget)
        
    def addRow(self):
        addedRow=QHBoxLayout()
        l4=QLabel()
        l4.setText(self.r.currentText())
        l5=QLabel()
        l5.setText(self.scan.currentText())
        addedRow.addStretch()
        addedRow.addWidget(l4)
        addedRows=QWidget()
        addedRows.setLayout(addedRow)
       
        print(self.r.currentText()+self.scan.currentText())
        
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