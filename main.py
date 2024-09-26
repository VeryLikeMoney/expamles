import sys

from PyQt5.QtCore import (QCommandLineOption, QCommandLineParser,
        QCoreApplication, QDir, QFileInfo, QT_VERSION_STR)
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
        QTreeView, QLineEdit, QMainWindow, QVBoxLayout, QWidget)

from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import  QDir
from delegete import TreeButtonDelegate


class MyWindow(QMainWindow):

        def __init__(self) -> None:
                super(MyWindow, self).__init__()
                self.setWindowTitle("Dir View")

                # adding basic widgets adn model
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

                
                self.user_path = QDir.homePath()
                self.clickedPaths = {}
                #QFileModel
                self.add_model_and_delegate()
        
        def setting_model(self):
                """ Настройка model"""
                self.model = QFileSystemModel()
                self.tree.setModel(self.model)
                self.model.setNameFilterDisables(False)
                self.model.setFilter(QDir.Files | QDir.Dirs | QDir.Hidden)
                index = self.model.setRootPath(self.user_path)
                self.tree.setRootIndex(index)
        
        def setting_delegate(self):
                """ Настройка delegate"""
                if hasattr(self, "delegate"):
                        self.clickedPaths = self.delegate.clickedPaths
                self.delegate = TreeButtonDelegate(self.model, self.tree)
                self.tree.setItemDelegateForColumn(1, self.delegate)       
                self.tree.setMouseTracking(True)
                self.delegate.clickedPaths = self.clickedPaths
                self.delegate.buttonClicked.connect(self.treeButtonClicked)
               
        def add_model_and_delegate(self):
                """ Вызов настройки model и delegate"""
                self.setting_model()
                self.setting_delegate()

        def treeButtonClicked(self, index):
                """ Обработка нажатия кнопки во втором стобце для подсчета размера папки"""
                dirPath = self.model.filePath(index)
                sizePath = self.dirSize(dirPath)
                sizePath = self.convert(sizePath)
                
                self.delegate.clickedPaths.setdefault(dirPath, sizePath)
                self.add_model_and_delegate()       
                self.tree.setCurrentIndex(index)           
                self.update_filter()

        def convert(self, size) -> str:
                """Перевод из байтов"""
                i = 0
                name_size = ('байта','KB', 'MB', 'GB', 'TB')
                while size>1024.0:
                        i += 1
                        size = round(size / 1024.0, 2)
                return f'{size} {name_size[i]}'    
                
        def dirSize(self, dirPath: str):
                """ Подсчет размера папки """
                sizePath = 0
                dir = QDir(dirPath)
                for filePath in dir.entryList(QDir.Files | QDir.Hidden):
                        sizePath += QFileInfo(dir, filePath).size()
                for childDirPath in dir.entryList(QDir.Dirs | QDir.NoDotAndDotDot | QDir.Hidden):
                        sizePath += self.dirSize(dirPath + QDir.separator() + childDirPath)
                return sizePath

        def update_filter(self):
                """ Добавление фильтра поиска"""
                if self.line_edit.text():
                        window.model.setNameFilters([f"*{self.line_edit.text()}*"])         
                else:
                        window.model.setNameFilters(["*"])
                
                
app = QApplication(sys.argv)
window = MyWindow()

#Код из начального файла
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
#КОнец кода из начального файла

window.show()
sys.exit(app.exec_())