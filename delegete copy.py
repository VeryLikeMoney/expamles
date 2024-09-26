
from PyQt5 import QtWidgets, QtCore

class TreeButtonDelegate(QtWidgets.QStyledItemDelegate):
        
    buttonClicked = QtCore.pyqtSignal(QtCore.QModelIndex)

    def __init__(self, fsModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fsModel = fsModel

        self.clickedPaths = {}
        self._mousePos = None
        self._pressed = False
        self.minimumButtonWidth = 32

    def check_point_dir(self, index) -> bool:
        dirPath = self.fsModel.filePath(index)[-2::]
        return dirPath != '..'  and dirPath[-1] != '.'
     
    def getOption(self, option, index):
        btnOption = QtWidgets.QStyleOptionButton()
        btnOption.initFrom(option.widget)
        SizeCount = self.clickedPaths.get(self.fsModel.filePath(index), 0)
        if SizeCount:
                btnOption.text = f'{SizeCount}'
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
        print("editorEvent")
        srcIndex = index

        if self.fsModel.isDir(srcIndex) and self.check_point_dir(srcIndex):
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
                        self.buttonClicked.emit(index)
                            
                self._pressed = False
                option.widget.update(index)  
                             
        return super().editorEvent(event, model, option, index)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        srcIndex = index
        if self.fsModel.isDir(srcIndex) and self.check_point_dir(srcIndex):
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