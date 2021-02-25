# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


# Method for table data
class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
            [1, 9, 2, 8, 5, 4, 8, 1],
            [1, 0, -1, 8, 5, 4, 8, 1],
            [3, 5, 2, 8, 5, 4, 8, 1],
            [3, 3, 2, 8, 5, 4, 8, 1],
            [5, 8, 9, 8, 5, 4, 8, 1],
        ], columns=['Scan', 'Name of Scan', 'Execution Number', 'Start Time', 'End Time', 'Scanned IPs',
                    'Successful Execution/Failure', 'Controls'], index=['Row 1', 'Row 2', 'Row 3', 'Row 4', 'Row 5'])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

#
class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        # Name of buttons in order
        names = ['Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop',
                 'Start', 'Pause', 'Stop']

        # Loop Sets 8 Rows and 3 Columns of buttons
        positions = [(i, j) for i in range(8) for j in range(3)]

        for position, name in zip(positions, names):
            button = QPushButton(name)
            grid.addWidget(button, *position)

        self.move(300, 150)
        self.setWindowTitle('Scan')
        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    ex = Example()
    sys.exit(app.exec())
