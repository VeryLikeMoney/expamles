
from PyQt5 import QtWidgets, QtCore

class TreeButtonDelegate(QtWidgets.QStyledItemDelegate):
        
        buttonClicked = QtCore.pyqtSignal(QtCore.QModelIndex)
        minimumButtonWidth = 32
        
        def __init__(self, fsModel, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.fsModel = fsModel
                self.clickedPaths = {}

        def check_point_dir(self, index) -> bool:
                """ Исключение скрытых файлов с названием . и .. """
                dirPath = self.fsModel.filePath(index)[-2::]
                return dirPath != '..'  and dirPath[-1] != '.'

        def editorEvent(self, event, model, option, index):
                if event.type() == QtCore.QEvent.MouseButtonRelease:
                        self.buttonClicked.emit(index)
                return 0
        
        def getOption(self, option, index):
                """ Отрисовка кнопок в заданном стиле"""
                self.btnOption = QtWidgets.QStyleOptionButton()
                self.btnOption.initFrom(option.widget)
                
                clickedCount = self.clickedPaths.get(self.fsModel.filePath(index), 0)
                if clickedCount:
                        self.btnOption.text = '{}'.format(clickedCount)
                else:
                        self.btnOption.text = 'Обновить'

                self.btnOption.rect = QtCore.QRect(option.rect)
                self.btnOption.rect.setLeft(option.rect.right() - self.minimumButtonWidth)
                style = option.widget.style()
                textRect = style.subElementRect(
                QtWidgets.QStyle.SE_PushButtonContents, self.btnOption)
                margin = style.pixelMetric(
                QtWidgets.QStyle.PM_ButtonMargin, self.btnOption) * 2
                textWidth = self.btnOption.fontMetrics.width(self.btnOption.text)
                if textRect.width() < textWidth + margin:

                        self.btnOption.rect.setLeft(self.btnOption.rect.left() - (
                                textWidth - textRect.width() + margin))

                return self.btnOption
        
        def paint(self, painter, option, index):
                super().paint(painter, option, index)
                srcIndex = index
                if self.fsModel.isDir(srcIndex) and self.check_point_dir(index):
                        btnOption = self.getOption(option, srcIndex)
                        option.widget.style().drawControl(
                                QtWidgets.QStyle.CE_PushButton, btnOption, painter)



