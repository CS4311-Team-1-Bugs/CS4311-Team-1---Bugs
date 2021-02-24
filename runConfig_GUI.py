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
    textFieldRunName.setPlaceholderText("Run Name Default")

    # [SRS 7c]
    textRunDes = QLabel(runConfigWin)
    textRunDes.setText("Run Description: ")
    textRunDes.move(15, 45)
    textFieldRunDes = QLineEdit(runConfigWin)
    textFieldRunDes.move(120, 50)
    textFieldRunDes.adjustSize()
    textFieldRunDes.setPlaceholderText("Run Description Default")
    # [SRS 7d]
    textWLIP = QLabel(runConfigWin)
    textWLIP.setText("Whitelisted IP Target: ")
    textWLIP.move(15, 90)
    textWLIP.adjustSize()
    textFieldWLIP = QLineEdit(runConfigWin)
    textFieldWLIP.move(150, 85)
    textFieldWLIP.adjustSize()
    textFieldWLIP.setPlaceholderText("Whitelist IP Default")
    # [SRS 7e]
    textBLIP = QLabel(runConfigWin)
    textBLIP.setText("Blacklisted IP Target: ")
    textBLIP.move(15, 120)
    textBLIP.adjustSize()
    textFieldBLIP = QLineEdit(runConfigWin)
    textFieldBLIP.move(150, 120)
    textFieldBLIP.setPlaceholderText("Blacklist IP Default")
    textFieldBLIP.adjustSize()

    # [SRS 7f]
    textScanType = QLabel(runConfigWin)
    textScanType.setText("Scan Type:")
    textScanType.move(15, 160)
    ScanType = QComboBox(runConfigWin)
    # [SRS 7g]
    ScanType.addItem("Scan Type")
    ScanType.addItem("Scan Type 1")
    ScanType.addItem("Scan Type 2")
    ScanType.move(95,160)
    ScanType.adjustSize()

    # [SRS 7h]
    textOr = QLabel(runConfigWin)
    textOr.setText("OR")
    textOr.move(75, 190)

    # [SRS 7i]
    textConfigFile = QLineEdit(runConfigWin)
    textConfigFile.move(165, 220)
    textConfigFile.adjustSize()
    textConfigFile.setPlaceholderText("Configuration File Default")

    textFileTitle = QLabel(runConfigWin)
    textFileTitle.setText("Run Configuration File")
    textFileTitle.move(15,225)
    textFileTitle.adjustSize()
    # RunConfigFile Button
    buttonConfigFile = QPushButton(runConfigWin)
    buttonConfigFile.setText("Browse...")
    buttonConfigFile.move(295, 215)
    buttonConfigFile.adjustSize()

    #[SRS 7j]
    buttonSave = QPushButton(runConfigWin)
    buttonSave.setText("Save")
    buttonSave.move(280, 260)


    buttonCancel = QPushButton(runConfigWin)
    buttonCancel.setText("Cancel")
    buttonCancel.move(380, 260)


    ScanType.show()
    runConfigWin.show()
    sys.exit(app.exec())
runConfigWindow()
