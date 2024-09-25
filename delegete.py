from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton, QStyle, QHBoxLayout, QApplication, QStyleOptionButton
from PyQt5.QtCore import QModelIndex, Qt, QPersistentModelIndex, QRect, QEvent, pyqtSignal
import os


class SizeDelegate(QStyledItemDelegate):
    buttonClicked = pyqtSignal(QModelIndex, int)
    
    def __init__(self, fsModel, *args, **kwargs):
        QStyledItemDelegate.__init__(self, *args, **kwargs)
        self.fsModel = fsModel

        self.clickedPaths = {}
        self._mousePos = None
        self._pressed = False
        self.minimumButtonWidth = 32
    
    def getOption(self, option, index):
        btnOption = QStyleOptionButton()
        # initialize the basic options with the view
        btnOption.initFrom(option.widget)

        clickedCount = self.clickedPaths.get(self.fsModel.filePath(index), 0)
        if clickedCount:
            btnOption.text = '{}'.format(clickedCount)
        else:
            btnOption.text = 'Обновить'

        # the original option properties should never be touched, so we can't
        # directly use it's "rect"; let's create a new one from it
        btnOption.rect = QRect(option.rect)

        # adjust it to the minimum size
        btnOption.rect.setLeft(option.rect.right() - self.minimumButtonWidth)

        style = option.widget.style()
        # get the available space for the contents of the button
        textRect = style.subElementRect(
            QStyle.SE_PushButtonContents, btnOption)
        # get the margins between the contents and the border, multiplied by 2
        # since they're used for both the left and right side
        margin = style.pixelMetric(
            QStyle.PM_ButtonMargin, btnOption) * 2

        # the width of the current button text
        textWidth = btnOption.fontMetrics.width(btnOption.text)

        if textRect.width() < textWidth + margin:
            # if the width is too small, adjust the *whole* button rect size
            # to fit the contents
            btnOption.rect.setLeft(btnOption.rect.left() - (
                textWidth - textRect.width() + margin))

        return btnOption
    
    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        srcIndex = index
        if self.fsModel.isDir(srcIndex):
            btnOption = self.getOption(option, srcIndex)

            # remove the focus rectangle, as it will be inherited from the view
            btnOption.state &= ~QStyle.State_HasFocus
            if self._mousePos is not None and self._mousePos in btnOption.rect:
                # if the style supports it, some kind of "glowing" border
                # will be shown on the button
                btnOption.state |= QStyle.State_MouseOver
                if self._pressed == Qt.LeftButton:
                    # set the button pressed state
                    btnOption.state |= QStyle.State_On
            else:
                # ensure that there's no mouse over state (see above)
                btnOption.state &= ~QStyle.State_MouseOver

            # finally, draw the virtual button
            option.widget.style().drawControl(
                QStyle.CE_PushButton, btnOption, painter)
    
    
    def createEditor(self, event, model, option, index):
        srcIndex = index.model().mapToSource(index)
                # I'm just checking if it's a file, if you want to check the extension
                # you might need to use fsModel.fileName(srcIndex)
        if self.fsModel.isDir(srcIndex):
            print(1)
        return super().editorEvent(event, model, option, index)

    def setEditorData(self, editor, index):
        if index.model().isDir(index):
            super(SizeDelegate, self).setEditorData(editor, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def calculate_folder_size(self, index):
        folder_path = index.model().filePath(index)
        folder_size = self.get_folder_size(folder_path)
        button = self.buttons.get(QPersistentModelIndex(index))
        if button:
            button.setText(f"{folder_size / 1024 / 1024:.2f} MB")

    def get_folder_size(self, folder):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size
