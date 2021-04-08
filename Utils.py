import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import datetime
import os

def make_saveCancel(caller, exportOption = 0):
    layout = QHBoxLayout()
    save = QPushButton("Save")
    save.setStyleSheet("background-color: #54e86c")
    save.clicked.connect(lambda: caller.buttons("Save", None))
    cancel = QPushButton("Cancel")
    cancel.setStyleSheet("background-color: #e6737e")
    cancel.clicked.connect(lambda: caller.buttons("Cancel", None))
    if exportOption:
        export = QPushButton("Export Current Configuration to XML")
        export.setStyleSheet("background-color: #49d1e3")
        export.clicked.connect(lambda: caller.buttons("Export", None))
    layout.addStretch()
    
    layout.addWidget(cancel)
    if exportOption: 
        layout.addWidget(export)
    layout.addWidget(save)
    layout.addStretch()

    container = QWidget()
    container.setLayout(layout)
    return container
    
# pad a widget with horizontal spacing or stretching
def make_HBox(widget, spacingType):
    layout = QHBoxLayout()
    if spacingType == 1:
        layout.addSpacing(2)
    else:
        layout.addStretch()
    layout.addWidget(widget)
    if spacingType == 1:
        layout.addSpacing(2)
    else:
        layout.addStretch()
    container = QWidget()
    container.setLayout(layout)
    return container
#Makes a Text orlabel
def orLabel():
    orLabel = QLabel()
    orLabel.setText("-OR-")
    orLabel.setAlignment(Qt.AlignCenter)
    serifFont = QFont("TimesNewRoman", 14)
    orLabel.setFont(serifFont)
    return orLabel

