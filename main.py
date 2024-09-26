import sys

from PyQt5.QtCore import (QCommandLineOption, QCommandLineParser,
        QCoreApplication, QDir, QFileInfo, QT_VERSION_STR)
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
        QTreeView, QLineEdit, QMainWindow, QVBoxLayout, QWidget, QAbstractItemView, QPushButton)


from PyQt5.QtGui import QStandardItemModel

from PyQt5.QtCore import  QDir, Qt

from delegete import TreeButtonDelegate



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

                #QFileModel
                self.model = QFileSystemModel()
                self.tree.setModel(self.model)
                self.model.setNameFilterDisables(False)
                self.model.setFilter(QDir.Files | QDir.Dirs | QDir.Hidden)

                self.user_path = QDir.homePath()
                index = self.model.setRootPath(self.user_path)
                self.tree.setRootIndex(index)
                self.line_edit.textChanged.connect(self.update_filter)
   
                self.delegate = TreeButtonDelegate(self.model, self.tree)
                self.tree.setItemDelegateForColumn(1, self.delegate)       
                self.tree.setMouseTracking(True)
                self.clickedPaths = {}

                self.delegate.buttonClicked.connect(self.treeButtonClicked)
                
        def treeButtonClicked(self, index):
                print("treeButtonClicked")
                dirPath = self.model.filePath(index)
                sizePath = self.dirSize(dirPath)
                sizePath = self.convert(sizePath)
                self.delegate.clickedPaths.setdefault(dirPath, sizePath)
                
                focus_index = index
                self.model = QFileSystemModel()
                self.tree.setModel(self.model)
                self.model.setNameFilterDisables(False)
                self.model.setFilter(QDir.Files | QDir.Dirs | QDir.Hidden)
                
                self.user_path = QDir.homePath()
                index = self.model.setRootPath(self.user_path)
                self.tree.setRootIndex(index)
                
                self.clickedPaths = self.delegate.clickedPaths
                self.delegate = TreeButtonDelegate(self.model, self.tree)
                self.tree.setItemDelegateForColumn(1, self.delegate)       
                self.tree.setMouseTracking(True)
                self.delegate.clickedPaths = self.clickedPaths
                self.delegate.buttonClicked.connect(self.treeButtonClicked)
                self.tree.setCurrentIndex(focus_index)
                
                self.update_filter()

        def convert(self, size) -> str:
                i = 0
                name_size = ('байта','KB', 'MB', 'GB', 'TB')
                while size>1024.0:
                        i += 1
                        size = int(size / 1024.0)
                return f'{size} {name_size[i]}'    
                

        def dirSize(self, dirPath: str):
            sizePath = 0
            dir = QDir(dirPath)

            for filePath in dir.entryList(QDir.Files | QDir.Hidden):
                sizePath += QFileInfo(dir, filePath).size()
            for childDirPath in dir.entryList(QDir.Dirs | QDir.NoDotAndDotDot | QDir.Hidden):
                sizePath += self.dirSize(dirPath + QDir.separator() + childDirPath)

            return sizePath

        def update_filter(self):
                if self.line_edit.text():
                        window.model.setNameFilters([f"*{self.line_edit.text()}*"])         
                else:
                        window.model.setNameFilters(["*"])
                

app = QApplication(sys.argv)
window = MyWindow()


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

if parser.isSet(dontUseCustomDirectoryIconsOption):
    window.model.iconProvider().setOptions(
            QFileIconProvider.DontUseCustomDirectoryIcons)

if rootPath is not None:
    rootIndex = window.model.index(QDir.cleanPath(rootPath))
    if rootIndex.isValid():
        window.tree.setRootIndex(rootIndex)



window.show()
sys.exit(app.exec_())