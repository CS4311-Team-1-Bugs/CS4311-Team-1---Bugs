# -*- coding: utf-8 -*-


import sys
from PyQt5 import *
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        # init the window
        super(MainWindow, self).__init__(*args, **kwargs)

        # Set the Window Title
        self.setWindowTitle("SEA Tool")

        # set menu layout
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

        ############################################## END OF HOME MENU ###############################################

        # Make a Widget to hold the layout and set it as the window's menu
        menuWidget = QWidget()
        menuWidget.setLayout(menuLayout)
        self.setMenuWidget(menuWidget)

        runList = QTableWidget()
        runList.setRowCount(6)
        runList.setColumnCount(8)



        # Initializes Start/Pause/Stop Buttons row 1
        startButton1 = QPushButton()
        startButton1 = QPushButton("Start")
        pauseButton1 = QPushButton()
        pauseButton1 = QPushButton("Pause")
        stopButton1 = QPushButton()
        stopButton1 = QPushButton("Stop")
        # Initializes Start/Pause/Stop Buttons row 2
        startButton2 = QPushButton()
        startButton2 = QPushButton("Start")
        pauseButton2 = QPushButton()
        pauseButton2 = QPushButton("Pause")
        stopButton2 = QPushButton()
        stopButton2 = QPushButton("Stop")
        # Initializes Start/Pause/Stop Buttons row 3
        startButton3 = QPushButton()
        startButton3 = QPushButton("Start")
        pauseButton3 = QPushButton()
        pauseButton3 = QPushButton("Pause")
        stopButton3 = QPushButton()
        stopButton3 = QPushButton("Stop")
        # Initializes Start/Pause/Stop Buttons row 4
        startButton4 = QPushButton()
        startButton4 = QPushButton("Start")
        pauseButton4 = QPushButton()
        pauseButton4 = QPushButton("Pause")
        stopButton4 = QPushButton()
        stopButton4 = QPushButton("Stop")
        # Initializes Start/Pause/Stop Buttons row 5
        startButton5 = QPushButton()
        startButton5 = QPushButton("Start")
        pauseButton5 = QPushButton()
        pauseButton5 = QPushButton("Pause")
        stopButton5 = QPushButton()
        stopButton5 = QPushButton("Stop")
        # Initializes Start/Pause/Stop Buttons row 6
        startButton6 = QPushButton()
        startButton6 = QPushButton("Start")
        pauseButton6 = QPushButton()
        pauseButton6 = QPushButton("Pause")
        stopButton6 = QPushButton()
        stopButton6 = QPushButton("Stop")

        # Layout for buttons on row 1
        col1Layout1 = QHBoxLayout()
        col1Layout1.addStretch()
        # Layout for buttons on row 2
        col1Layout2 = QHBoxLayout()
        col1Layout2.addStretch()
        # Layout for buttons on row 3
        col1Layout3 = QHBoxLayout()
        col1Layout3.addStretch()
        # Layout for buttons on row 4
        col1Layout4 = QHBoxLayout()
        col1Layout4.addStretch()
        # Layout for buttons on row 5
        col1Layout5 = QHBoxLayout()
        col1Layout5.addStretch()
        # Layout for buttons on row 6
        col1Layout6 = QHBoxLayout()
        col1Layout6.addStretch()

        # Adds buttons to row 1
        col1Layout1.addWidget(startButton1)
        col1Layout1.addWidget(pauseButton1)
        col1Layout1.addWidget(stopButton1)
        # Adds buttons to row 2
        col1Layout2.addWidget(startButton2)
        col1Layout2.addWidget(pauseButton2)
        col1Layout2.addWidget(stopButton2)
        # Adds buttons to row 3
        col1Layout3.addWidget(startButton3)
        col1Layout3.addWidget(pauseButton3)
        col1Layout3.addWidget(stopButton3)
        # Adds buttons to row 4
        col1Layout4.addWidget(startButton4)
        col1Layout4.addWidget(pauseButton4)
        col1Layout4.addWidget(stopButton4)
        # Adds buttons to row 5
        col1Layout5.addWidget(startButton5)
        col1Layout5.addWidget(pauseButton5)
        col1Layout5.addWidget(stopButton5)
        # Adds buttons to row 6
        col1Layout6.addWidget(startButton6)
        col1Layout6.addWidget(pauseButton6)
        col1Layout6.addWidget(stopButton6)

        # Widget to Layout row 1
        col1Widget1 = QWidget()
        col1Widget1.setLayout(col1Layout1)
        # Widget to Layout row 2
        col1Widget2 = QWidget()
        col1Widget2.setLayout(col1Layout2)
        # Widget to Layout row 3
        col1Widget3 = QWidget()
        col1Widget3.setLayout(col1Layout3)
        # Widget to Layout row 4
        col1Widget4 = QWidget()
        col1Widget4.setLayout(col1Layout4)
        # Widget to Layout row 5
        col1Widget5 = QWidget()
        col1Widget5.setLayout(col1Layout5)
        # Widget to Layout row 6
        col1Widget6 = QWidget()
        col1Widget6.setLayout(col1Layout6)

        # Column Titles
        runList.setItem(0, 0, QTableWidgetItem("Control"))
        runList.setItem(0, 1, QTableWidgetItem("Scan"))
        runList.setItem(0, 2, QTableWidgetItem("Name of Scan"))
        runList.setItem(0, 3, QTableWidgetItem("Execution Number"))
        runList.setItem(0, 4, QTableWidgetItem("Start Time"))
        runList.setItem(0, 5, QTableWidgetItem("End Time"))
        runList.setItem(0, 6, QTableWidgetItem("Scanned IPs"))
        runList.setItem(0, 7, QTableWidgetItem("Successful Execution/Failure"))
        # Dummy Data Row 1
        runList.setCellWidget(1, 0, col1Widget1)
        runList.setItem(1, 1, QTableWidgetItem("Scan 1"))
        runList.setItem(1, 2, QTableWidgetItem("Scan X"))
        runList.setItem(1, 3, QTableWidgetItem("4"))
        runList.setItem(1, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(1, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(1, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(1, 7, QTableWidgetItem("Successful"))
        # Dummy Data Row 2
        runList.setCellWidget(2, 0, col1Widget2)
        runList.setItem(2, 1, QTableWidgetItem("Scan 4"))
        runList.setItem(2, 2, QTableWidgetItem("Scan Y"))
        runList.setItem(2, 3, QTableWidgetItem("2"))
        runList.setItem(2, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(2, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(2, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(2, 7, QTableWidgetItem("Successful"))
        # Dummy Data Row 3
        runList.setCellWidget(3, 0, col1Widget3)
        runList.setItem(3, 1, QTableWidgetItem("Scan 3"))
        runList.setItem(3, 2, QTableWidgetItem("Scan Z"))
        runList.setItem(3, 3, QTableWidgetItem("6"))
        runList.setItem(3, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(3, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(3, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(3, 7, QTableWidgetItem("Failure"))
        # Dummy Data Row 4
        runList.setCellWidget(4, 0, col1Widget4)
        runList.setItem(4, 1, QTableWidgetItem("Scan 3"))
        runList.setItem(4, 2, QTableWidgetItem("Scan A"))
        runList.setItem(4, 3, QTableWidgetItem("6"))
        runList.setItem(4, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(4, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(4, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(4, 7, QTableWidgetItem("Successful"))
        # Dummy Data Row 5
        runList.setCellWidget(5, 0, col1Widget5)
        runList.setItem(5, 1, QTableWidgetItem("Scan 3"))
        runList.setItem(5, 2, QTableWidgetItem("Scan Z"))
        runList.setItem(5, 3, QTableWidgetItem("6"))
        runList.setItem(5, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(5, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(5, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(5, 7, QTableWidgetItem("Failure"))
        # Dummy Data Row 6
        runList.setCellWidget(6, 0, col1Widget6)
        runList.setItem(6, 1, QTableWidgetItem("Scan 3"))
        runList.setItem(6, 2, QTableWidgetItem("Scan A"))
        runList.setItem(6, 3, QTableWidgetItem("6"))
        runList.setItem(6, 4, QTableWidgetItem("12:00:00"))
        runList.setItem(6, 5, QTableWidgetItem("12:34:12"))
        runList.setItem(6, 6, QTableWidgetItem("127.0.0.0–127.255.255.255"))
        runList.setItem(6, 7, QTableWidgetItem("Successful"))

        runList.horizontalHeader().hide()
        runList.verticalHeader().hide()
        runList.resizeColumnsToContents()

        self.setCentralWidget(runList)

    # def addRow(runList):
    # runList.getRowCount()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
