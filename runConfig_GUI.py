import sys
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFormLayout
class RunConfigWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        # init the window
        super(RunConfigWindow, self).__init__(*args, **kwargs)

        # Set the Window Title
        self.setWindowTitle("Configuration of the Selected Run")

        menuWidget = QWidget()
        menuLayout = self.makeMenuLayout()
        menuWidget.setLayout(menuLayout)
        self.setMenuWidget(menuWidget)

        mainWidget = QWidget()
        mainLayout = self.makeMainLayout()

        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)


    def makeMenuLayout(self):
        menuLayout = QVBoxLayout()

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("SEA Menu")
        menuTitle.setAlignment(Qt.AlignCenter)

        # button component of menu
        hLayout = QHBoxLayout()
        runButton = QPushButton("Run")
        toolButton = QPushButton("Tools")
        hLayout.addStretch()
        hLayout.addWidget(runButton)
        hLayout.addStretch()
        hLayout.addWidget(toolButton)
        hLayout.addStretch()

        # Add the widgets we created to the menu layout
        menuLayout.addWidget(menuTitle)
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)
        return menuLayout


    def makeMainLayout(self):
        outerLayout = QVBoxLayout()
        # Create Run Config Details layer
        runConfigLayout = QFormLayout()
        orLabel = self.orLabel()
        orLabel1 =self.orLabel()
        orLabel2 = self.orLabel()
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%I:%M %m/%d/%Y %p")
        runName = QLabel()
        runName.setAlignment(Qt.AlignLeft)
        runName.setText(timestampStr)
        serifFont = QFont("Arial", 15)
        runName.setFont(serifFont)
        runConfigLayout.addRow("Run Name:", runName)
        runDesc= QLineEdit()
        runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", runDesc)
        buttonConfigFile = QPushButton("Browse")
        buttonConfigFile.setStyleSheet("background-color:rgb(144,184,239)")
        WLIPtext = QLineEdit()
        WLIPtextfile = QLineEdit()
        WLIPtext.setPlaceholderText("Whitelist IP Default")
        runConfigLayout.addRow("Whitelisted IP Target:", WLIPtext)
        runConfigLayout.addWidget(orLabel)
        runConfigLayout.addRow("Browse for Whitelist File:", WLIPtextfile)
        runConfigLayout.addWidget(QPushButton("Browse"))
        BLIPtext = QLineEdit()
        BLIPtextfile = QLineEdit()
        BLIPtext.setPlaceholderText("Blacklist IP Default")
        runConfigLayout.addRow("Blacklisted IP Target:", BLIPtext)
        runConfigLayout.addWidget(orLabel1)
        runConfigLayout.addRow("Browse for Blacklist File:", BLIPtextfile )
        runConfigLayout.addWidget(QPushButton("Browse"))
        ScanType = QComboBox()
        scanList = ["Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3"]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addWidget(orLabel2)
        ConfigFile = QLineEdit()
        ConfigFile.setPlaceholderText("Run Configuration File")
        runConfigLayout.addRow("Browse for Run Configuration File:", ConfigFile,)
        runConfigLayout.addWidget(buttonConfigFile)



        buttonWidget = QWidget()
        buttonLayout = self.makeButtonLayout()
        buttonWidget.setLayout(buttonLayout)

        runConfigLayout.addWidget(buttonWidget)
        runConfigLayout.setVerticalSpacing(20)
        runConfigLayout.setHorizontalSpacing(10)


        return runConfigLayout

    def makeButtonLayout(self):
        # set button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(QPushButton("Save"))
        buttonLayout.addWidget(QPushButton("Cancel"))
        buttonLayout.addSpacing(5)
        buttonLayout.setAlignment(Qt.AlignBottom)
        return buttonLayout

    def orLabel(self):
        orLabel = QLabel()
        orLabel.setText("OR")
        orLabel.setAlignment(Qt.AlignCenter)
        serifFont = QFont("Arial", 18)
        orLabel.setFont(serifFont)
        return orLabel


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RunConfigWindow()
    window.show()
    sys.exit(app.exec_())
