import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFormLayout
class RunConfigWindow(QWidget):
    def __init__(self, *args, **kwargs):
        # init the window
        super(RunConfigWindow, self).__init__(*args, **kwargs)

        # Set the Window Title
        self.setWindowTitle("Configuration of the Selected Run")

        # Create Outer base layer
        outerLayout = QVBoxLayout()

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

        # Create Run Config Details layer
        runConfigLayout = QFormLayout()
        runName = QLineEdit()
        runName.setAlignment(Qt.AlignLeft)
        runName.setPlaceholderText("Run Name Default")
        runConfigLayout.addRow("Run Name:", runName)
        runDesc= QLineEdit()
        runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", runDesc)
        WLIPtext = QLineEdit()
        WLIPtext.setPlaceholderText("Whitelist IP Default")
        runConfigLayout.addRow("Whitelisted IP Target:", WLIPtext)
        BLIPtext = QLineEdit()
        BLIPtext.setPlaceholderText("Blacklist IP Default")
        runConfigLayout.addRow("Blacklisted IP Target:", BLIPtext)
        ScanType = QComboBox()
        scanList = ["Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3"]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addRow("OR", QLabel())
        buttonConfigFile = QPushButton("Browse ...")
        ConfigFile = QLineEdit()
        ConfigFile.setPlaceholderText("Run Configuration File")
        runConfigLayout.addRow("Run Configuration File", ConfigFile)
        runConfigLayout.addWidget(buttonConfigFile)

        # set button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(QPushButton("Save"))
        buttonLayout.addWidget(QPushButton("Cancel"))


        outerLayout.addLayout(menuLayout)
        outerLayout.addLayout(runConfigLayout)
        outerLayout.addLayout(buttonLayout)
        self.setLayout(outerLayout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RunConfigWindow()
    window.show()
    sys.exit(app.exec_())
