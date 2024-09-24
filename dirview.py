#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2017 Riverbank Computing Limited.
## Copyright (C) 2017 Hans-Peter Jansen <hpj@urpla.net>
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################


import sys

from PyQt5.QtCore import (QCommandLineOption, QCommandLineParser,
        QCoreApplication, QDir, QT_VERSION_STR)
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
        QTreeView, QLineEdit, QMainWindow, QVBoxLayout, QWidget)


from PyQt5.QtGui import QStandardItemModel

class MyWindow(QMainWindow):  
        
   def __init__(self) -> None:
        super(MyWindow, self).__init__()
        self.setWindowTitle("Dir View")
        
        self.line_edit = QLineEdit(self)
        self.tree = QTreeView(self)
        
        central_widget = QWidget(self)
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name'])
        self.tree.setModel(self.model)
        layout = QVBoxLayout(central_widget)
        
        layout.addWidget(self.line_edit)
        layout.addWidget(self.tree)

        self.setCentralWidget(central_widget)  
        
        availableSize = QApplication.desktop().availableGeometry(self.tree).size()
        self.resize(availableSize / 2)
        self.tree.setColumnWidth(0, int(self.width() / 4))
        
        # Demonstrating look and feel features.
        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

app = QApplication(sys.argv)

QCoreApplication.setApplicationVersion(QT_VERSION_STR)
parser = QCommandLineParser()
parser.setApplicationDescription("Qt Dir View Example")
parser.addHelpOption()
parser.addVersionOption()

dontUseCustomDirectoryIconsOption = QCommandLineOption('c',
        "Set QFileIconProvider.DontUseCustomDirectoryIcons")
parser.addOption(dontUseCustomDirectoryIconsOption)
parser.addPositionalArgument('directory', "The directory to start in.")
parser.process(app)

try:
    rootPath = parser.positionalArguments().pop(0)
except IndexError:
    rootPath = None

model = QFileSystemModel()
model.setRootPath(' ')
if parser.isSet(dontUseCustomDirectoryIconsOption):
    model.iconProvider().setOptions(
            QFileIconProvider.DontUseCustomDirectoryIcons)


window = MyWindow()
window.tree.setModel(model)

# ?
if rootPath is not None:
    rootIndex = model.index(QDir.cleanPath(rootPath))
    if rootIndex.isValid():
        window.tree.setRootIndex(rootIndex)

window.show()
sys.exit(app.exec_())
