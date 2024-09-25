import os
import sys

from PyQt5.QtCore import (QCommandLineOption, QCommandLineParser, 
        QCoreApplication, QDir, QT_VERSION_STR)
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
        QTreeView, QLineEdit, QMainWindow, QVBoxLayout, QWidget)


from PyQt5.QtGui import QStandardItemModel

from PyQt5.QtCore import QSortFilterProxyModel, Qt, QRegExp, QDir



class MyWindow(QMainWindow):  
        
   def __init__(self) -> None:
        super(MyWindow, self).__init__()
        self.setWindowTitle("Dir View")
        
        self.line_edit = QLineEdit(self)
        self.tree = QTreeView(self)
        
        central_widget = QWidget(self)
        
        self.item_model = QStandardItemModel()
        self.item_model .setHorizontalHeaderLabels(['Name'])
        self.tree.setModel(self.item_model)
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
if parser.isSet(dontUseCustomDirectoryIconsOption):
    model.iconProvider().setOptions(
            QFileIconProvider.DontUseCustomDirectoryIcons)

user_path = QDir.homePath() 

window = MyWindow()
window.tree.setModel(model)

model.setNameFilterDisables(False)
model.setFilter(QDir.Files | QDir.Dirs | QDir.Hidden)
proxy_model = QSortFilterProxyModel()
proxy_model.setSourceModel(model)

proxy_index = proxy_model.mapFromSource(model.setRootPath(user_path))
window.tree.setModel(proxy_model)
window.tree.setRootIndex(proxy_index)



def filter_files():
        # Устанавливаем фильтр на основании текста из QLineEdit
        regex = QRegExp(f"{window.line_edit.text()}", Qt.CaseInsensitive)
        if regex.isValid():
                proxy_model.setFilterKeyColumn(0)
                proxy_model.setFilterRegExp(regex)

                
                s_index = model.setRootPath(user_path)
                model.setNameFilters([f"{regex}",])
                
                p_index = proxy_model.mapFromSource(s_index)
                window.tree.setRootIndex(p_index)
  



                
    

                

                


window.line_edit.textChanged.connect(filter_files)


# ?
if rootPath is not None:
    rootIndex = model.index(QDir.cleanPath(rootPath))
    if rootIndex.isValid():
        window.tree.setRootIndex(rootIndex)

window.show()
sys.exit(app.exec_())