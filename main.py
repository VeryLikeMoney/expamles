import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QVBoxLayout, QWidget, QPushButton
from dirview import tree


class TextEditExample(QWidget):
    def __init__(self):
        super().__init__()# w   w   w.  b    o o  k 2  s    .  co   m 
        self.setWindowTitle('QLineEdit Text Example')

        layout = QVBoxLayout()

        self.treeveiw = tree
        # Create a QLineEdit widget
        self.line_edit = QLineEdit()
        layout.addWidget(self.line_edit)
        layout.addWidget(self.treeveiw)
        self.setLayout(layout)

    def set_text(self):
        text = input('Enter text to set: ')
        self.line_edit.setText(text)

    def get_text(self):
        text = self.line_edit.text()
        print('Text in QLineEdit:', text)


if  __name__ == "__main__":
    app = QApplication(sys.argv)
    example = TextEditExample()
    example.show()
    sys.exit(app.exec_())