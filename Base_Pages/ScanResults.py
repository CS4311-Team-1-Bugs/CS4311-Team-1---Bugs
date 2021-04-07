import sys
from collections import deque
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class view(QWidget):

    def __init__(self, data):
        super(view, self).__init__()
        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Scan Name', 'Results'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.importData(data)
        self.tree.expandAll()

    # Function to save populate treeview with a dictionary
    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}  # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['short_name']),
                QStandardItem(value['results']),
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)

            # Add style to tree rows
            item = self.model.item(0)
            for i in range(item.rowCount()):
                for j in range(7):
                    childitem = item.child(i, j)
                    if childitem != None:
                        childitem.setBackground(QColor(225, 225, 225))
                        childitem.setSizeHint(QSize(30, 25))
                        childitem.setTextAlignment(Qt.AlignBottom)
                        childitem.setFont(QFont("Times New Roman", weight=QFont.Bold))


if __name__ == '__main__':
    data = [
        {'unique_id': 1, 'parent_id': 0, 'short_name': '', 'results': ' '},
        {'unique_id': 2, 'parent_id': 1, 'short_name': 'Scan 1', 'results': ' '},
        {'unique_id': 3, 'parent_id': 2, 'short_name': 'Nmap', 'results': 'Results go here...'},
        {'unique_id': 4, 'parent_id': 2, 'short_name': 'Nessus', 'results': 'Results go here...'},
        {'unique_id': 5, 'parent_id': 1, 'short_name': 'Scan 2', 'results': ' '},
        {'unique_id': 6, 'parent_id': 5, 'short_name': 'Nmap', 'results': 'Results go here...'},
        {'unique_id': 7, 'parent_id': 5, 'short_name': 'Nikto', 'results': 'Results go here...'},
        {'unique_id': 8, 'parent_id': 1, 'short_name': 'Scan 3', 'results': ' '},
        {'unique_id': 9, 'parent_id': 8, 'short_name': 'Nessus', 'results': 'Results go here...'},
        {'unique_id': 10, 'parent_id': 8, 'short_name': 'Cutycapt', 'results': 'Results go here...'},
        {'unique_id': 11, 'parent_id': 1, 'short_name': 'Scan 4', 'results': ' '},
        {'unique_id': 12, 'parent_id': 11, 'short_name': 'Nmap', 'results': 'Results go here...'},
        {'unique_id': 13, 'parent_id': 11, 'short_name': 'SMBMap', 'results': 'Results go here...'},
        {'unique_id': 14, 'parent_id': 1, 'short_name': 'Scan 5', 'results': ' '},
        {'unique_id': 15, 'parent_id': 14, 'short_name': 'CrackMapExec', 'results': 'Results go here...'},
        {'unique_id': 16, 'parent_id': 1, 'short_name': 'Scan 6', 'results': ' '},
    ]
    app = QApplication(sys.argv)
    view = view(data)
    view.setGeometry(300, 100, 600, 300)
    view.setWindowTitle('Scan Results')
    view.show()
    sys.exit(app.exec_())
