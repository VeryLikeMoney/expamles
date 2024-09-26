from PyQt5.QtWidgets import QApplication, QTreeView, QVBoxLayout, QWidget, QFileSystemModel
from PyQt5.QtCore import QSortFilterProxyModel

from PyQt5.QtGui import QStandardItemModel , QStandardItem
from PyQt5.QtCore import  QDir

class CustomModel(QSortFilterProxyModel):
    def __init__(self, file_model, extra_data_model):
        super(QSortFilterProxyModel, self).__init__()
        self.file_model = file_model
        self.extra_data_model = extra_data_model

    def columnCount(self, parent=None):
        return self.file_model.columnCount(parent) + 1  # Добавляем одну колонку

    def data(self, index, role):
        if index.column() < self.file_model.columnCount():
            return self.file_model.data(index, role)
        else:
            # Пользовательские данные
            custom_index = self.extra_data_model.index(index.row(), 0)
            return self.extra_data_model.data(custom_index, role)

    def rowCount(self, parent=None):
        return self.file_model.rowCount(parent)

# Инициализация приложения
app = QApplication([])

# Виджет с вертикальной компоновкой
widget = QWidget()
layout = QVBoxLayout(widget)

# Модель файловой системы
file_model = QFileSystemModel()
file_model.setRootPath(QDir.homePath())  # Путь к корневой папке

# Пользовательская модель данных для дополнительной колонки
extra_data_model = QStandardItemModel()
extra_data_model.setHorizontalHeaderLabels(['Custom Data'])
for i in range(100):  # Пример данных
    extra_data_model.appendRow(QStandardItem(f'Custom Data {i}'))

# Прокси-модель для объединения данных
custom_model = CustomModel(file_model, extra_data_model)

# Создание и настройка TreeView
tree_view = QTreeView()
tree_view.setModel(custom_model)
tree_view.setRootIndex(file_model.index(file_model.rootPath()))

# Добавляем TreeView в компоновку
layout.addWidget(tree_view)

# Показываем виджет
widget.show()

# Запуск приложения
app.exec_()