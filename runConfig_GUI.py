import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QComboBox, QLineEdit, QPushButton


def runConfigWindow():
    app = QApplication(sys.argv)
    runConfigWin = QMainWindow()

    # [SRS 7a]
    runConfigWin.setWindowTitle("Configuration of the Selected Run")
    runConfigWin.setGeometry(200, 200, 500, 300)

    # [SRS 7b]
    textRunName = QLabel(runConfigWin)
    textRunName.setText("Run Name: ")
    textRunName.move(15,15)
    textFieldRunName = QLineEdit(runConfigWin)
    textFieldRunName.move(95, 20)
    textFieldRunName.adjustSize()
    # [SRS 7c]
    textRunDes = QLabel(runConfigWin)
    textRunDes.setText("Run Description: ")
    textRunDes.move(15, 35)
    # [SRS 7d]
    textWLIP = QLabel(runConfigWin)
    textWLIP.setText("Whitelisted IP Target: ")
    textWLIP.move(15, 60)
    textWLIP.adjustSize()
    # [SRS 7e]
    textBLIP = QLabel(runConfigWin)
    textBLIP.setText("Blacklisted IP Target: ")
    textBLIP.move(15, 80)
    textBLIP.adjustSize()

    # [SRS 7f]
    textScanType = QLabel(runConfigWin)
    textScanType.setText("Scan Type:")
    textScanType.move(15, 100)
    ScanType = QComboBox(runConfigWin)
    # [SRS 7g]
    ScanType.addItem("Scan Type")
    ScanType.addItem("Scan Type 1")
    ScanType.addItem("Scan Type 2")
    ScanType.move(95,100)
    ScanType.adjustSize()

    # [SRS 7h]
    textOr = QLabel(runConfigWin)
    textOr.setText("OR")
    textOr.move(75, 130)

    # [SRS 7i]
    textConfigFile = QLineEdit(runConfigWin)
    textConfigFile.move(165, 160)
    textConfigFile.adjustSize()
    textConfigFile.setPlaceholderText("Configuration File Default")

    textFileTitle = QLabel(runConfigWin)
    textFileTitle.setText("Run Configuration File")
    textFileTitle.move(15,160)
    textFileTitle.adjustSize()
    # RunConfigFile Button
    buttonConfigFile = QPushButton(runConfigWin)
    buttonConfigFile.setText("Browse...")
    buttonConfigFile.move(295, 156)
    buttonConfigFile.adjustSize()

    #[SRS 7j]
    buttonSave = QPushButton(runConfigWin)
    buttonSave.setText("Save")
    buttonSave.move(200, 300)

    ScanType.show()
    runConfigWin.show()
    sys.exit(app.exec())
runConfigWindow()
