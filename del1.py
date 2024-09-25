
from PyQt5 import QtWidgets, QtCore

class TreeButtonDelegate(QtWidgets.QStyledItemDelegate):
    buttonClicked = QtCore.pyqtSignal(QtCore.QModelIndex, int)

    def __init__(self, fsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fsModel = fsModel

        self.clickedPaths = {}
        self._mousePos = None
        self._pressed = False
        self.minimumButtonWidth = 32

    def getOption(self, option, index):
        btnOption = QtWidgets.QStyleOptionButton()
        btnOption.initFrom(option.widget)

        clickedCount = self.clickedPaths.get(self.fsModel.filePath(index), 0)
        if clickedCount:
            btnOption.text = '{}'.format(clickedCount)
        else:
            btnOption.text = 'Обновить'

        btnOption.rect = QtCore.QRect(option.rect)

        btnOption.rect.setLeft(option.rect.right() - self.minimumButtonWidth)

        style = option.widget.style()

        textRect = style.subElementRect(
            QtWidgets.QStyle.SE_PushButtonContents, btnOption)

        margin = style.pixelMetric(
            QtWidgets.QStyle.PM_ButtonMargin, btnOption) * 2

        textWidth = btnOption.fontMetrics.width(btnOption.text)

        if textRect.width() < textWidth + margin:

            btnOption.rect.setLeft(btnOption.rect.left() - (
                textWidth - textRect.width() + margin))

        return btnOption

    def editorEvent(self, event, model, option, index):

        srcIndex = index

        if self.fsModel.isDir(srcIndex):
            if event.type() in (QtCore.QEvent.Enter, QtCore.QEvent.MouseMove):
                self._mousePos = event.pos()
                option.widget.update(index)             
            elif event.type() == QtCore.QEvent.Leave:
                self._mousePos = None
            elif (event.type() in (QtCore.QEvent.MouseButtonPress, QtCore.QEvent.MouseButtonDblClick)
                and event.button() == QtCore.Qt.LeftButton):
                    if event.pos() in self.getOption(option, srcIndex).rect:
                        self._pressed = True
                    option.widget.update(index)
                    if event.type() == QtCore.QEvent.MouseButtonDblClick:

                        return True
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                
                if self._pressed and event.button() == QtCore.Qt.LeftButton:

                    if event.pos() in self.getOption(option, srcIndex).rect:
                        filePath = self.fsModel.filePath(srcIndex)

                        sizePath = self.dirSize(filePath)
                        self.clickedPaths.setdefault(filePath, sizePath)
                        self.buttonClicked.emit(index, sizePath)

                        
                self._pressed = False
                option.widget.update(index)
                
        return super().editorEvent(event, model, option, index)


    def dirSize(self, dirPath: str):
        sizePath = 0
        dir = QtCore.QDir(dirPath)
        for filePath in dir.entryList(QtCore.QDir.Files | QtCore.QDir.Hidden):
            sizePath += QtCore.QFileInfo(dir, filePath).size()
        for childDirPath in dir.entryList(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot |  QtCore.QDir.System | QtCore.QDir.Hidden):
            print(childDirPath)
            sizePath += self.dirSize(childDirPath)
        return sizePath

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        srcIndex = index
        if self.fsModel.isDir(srcIndex):
            btnOption = self.getOption(option, srcIndex)


            btnOption.state &= ~QtWidgets.QStyle.State_HasFocus
            if self._mousePos is not None and self._mousePos in btnOption.rect:

                btnOption.state |= QtWidgets.QStyle.State_MouseOver
                if self._pressed == QtCore.Qt.LeftButton:

                    btnOption.state |= QtWidgets.QStyle.State_On
            else:
                btnOption.state &= ~QtWidgets.QStyle.State_MouseOver

            option.widget.style().drawControl(
                QtWidgets.QStyle.CE_PushButton, btnOption, painter)