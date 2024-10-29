#
#       pip install pyside6
#
import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MainTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Universal stylesheet.
        universal_stylesheet =  """font-size: 32px; font-family: Times New Roman; background-color: green;"""
        # Exit button.
        self.exit_button = QtWidgets.QPushButton("Exit")
        self.exit_button.setStyleSheet(universal_stylesheet)

        self.text = QtWidgets.QLabel("Hello World",
                                     alignment=QtCore.Qt.AlignCenter)
        self.text.setStyleSheet(universal_stylesheet)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.exit_button)  # Terminate the program.
        
        self.exit_button.clicked.connect(self.exit_button_clicked) # Call termination function.

    @QtCore.Slot()
    
    # Termination function to finish program.
    def exit_button_clicked(self):
        sys.exit() # Is that right termination?
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MainTab()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())