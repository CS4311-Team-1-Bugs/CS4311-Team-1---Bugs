import sys
from PyQt5.QtCore import left, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton, QHBoxLayout, \
    QVBoxLayout, QFormLayout

import MenuBaseCode


class RunConfigWindow(QWidget):
    def __init__(self, *args, **kwargs):
        # init the window
        super(RunConfigWindow, self).__init__(*args, **kwargs)

        # Set the Window Title
        self.setWindowTitle("Configuration of the Selected Run")

        # Create Outer base layer
        outerLayout = QVBoxLayout()

        #Create Run Config Details laer
        runConfigLayout = QFormLayout()
        runConfigLayout.addRow("Run Name:", QLineEdit())
        runConfigLayout.addRow("Run Description:", QLineEdit())
        runConfigLayout.addRow("Whitelisted IP Target:", QLineEdit())
        runConfigLayout.addRow("Blacklisted IP Target:", QLineEdit())
        ScanType = QComboBox()
        scanList = [ "Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3" ]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addRow("OR", QLabel())
        buttonConfigFile = QPushButton("Browse ...")
        runConfigLayout.addRow("Run Configuration File", QLineEdit())
        runConfigLayout.addWidget(buttonConfigFile)


        # set button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(QPushButton("Save"))
        buttonLayout.addWidget(QPushButton("Cancel"))

        outerLayout.addLayout(runConfigLayout)
        outerLayout.addLayout(buttonLayout)
        self.setLayout(outerLayout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RunConfigWindow()
    window.show()
    sys.exit(app.exec_())
