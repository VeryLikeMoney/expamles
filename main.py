import sys

from PyQt5.QtCore import (QCommandLineOption, QCommandLineParser,
        QCoreApplication, QDir, QT_VERSION_STR, QDir, QThread)
from PyQt5.QtWidgets import (QApplication, QFileIconProvider, QFileSystemModel,
        QTreeView, QLineEdit, QMainWindow, QVBoxLayout, QWidget)

from PyQt5.QtGui import QStandardItemModel
from delegete import TreeButtonDelegate
from threed import Worker

class MyWindow(QMainWindow):

        def __init__(self) -> None:
                super(MyWindow, self).__init__()
                self.setWindowTitle("Dir View")

                # adding basic widgets adn model
                self.line_edit = QLineEdit(self)
                self.tree = QTreeView(self)
                central_widget = QWidget(self)
                self.item_model = QStandardItemModel()

                self.line_edit.setPlaceholderText('Поиск')
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
                self.clicked_paths = {}
                #QFileModel
                self.add_model_and_delegate()
                self.line_edit.textChanged.connect(self.update_filter)          
                self.thread = QThread()

        def setting_model(self):
                """ Настройка model"""
                self.model = QFileSystemModel()
                self.model.setNameFilterDisables(False)
                self.model.setFilter(QDir.Files | QDir.Dirs | QDir.Hidden)
                index = self.model.setRootPath(self.user_path)
                self.tree.setModel(self.model)
                self.tree.setRootIndex(index)

        def setting_delegate(self):
                """ Настройка delegate"""
                if hasattr(self, "delegate"):
                        self.clicked_paths = self.delegate.clickedPaths
                self.delegate = TreeButtonDelegate(self.model, self.tree)
                self.tree.setItemDelegateForColumn(1, self.delegate)       
                self.tree.setMouseTracking(True)
                self.delegate.clickedPaths = self.clicked_paths
                self.delegate.buttonClicked.connect(self.treeButtonClicked)
      
        def add_model_and_delegate(self):
                """ Вызов настройки model и delegate"""
                self.setting_model()
                self.setting_delegate()

        def treeButtonClicked(self, index):
                """ Обработка нажатия кнопки во втором стобце для подсчета размера папки"""
                self.dir_path = self.model.filePath(index)
                self.worker = Worker(self.dir_path)
                self.worker.moveToThread(self.thread)
                self.thread.started.connect(self.worker.run)
                self.worker.result_ready.connect(self.handle_result)
                self.thread.start()   
                     
                self.add_model_and_delegate()       
                self.update_filter()
                
        def handle_result(self, size):
                """ Обрабатываем результат, полученный из рабочего потока """
                size = self.convert(size)
                self.delegate.clickedPaths.setdefault(self.dir_path, size)
                self.thread.quit()
                self.thread.wait()

        def convert(self, size) -> str:
                """Перевод из байтов"""
                i = 0
                name_size = ('байта','KB', 'MB', 'GB', 'TB')
                while size>1024.0:
                        i += 1
                        size = round(size / 1024.0, 2)
                return f'{size} {name_size[i]}'    
                
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