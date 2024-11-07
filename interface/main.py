'''
        To install pyside6 run: pip install pyside6
'''
import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Universal stylesheet - uses CSS syntax.
universal_stylesheet =  """font-size: 32px;
                           font-family: Times New Roman;
                        """

class MainTab(QtWidgets.QWidget):
    '''
        MainTab class is designed to contain the main menu of the program.
    '''
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget    # The tabs list.

        # Program name.
        self.program_name = QtWidgets.QLabel("D&D AI CHATBOTS", # Create a text label.
                                     alignment=QtCore.Qt.AlignCenter)
        self.program_name.setStyleSheet(universal_stylesheet) # Add style to text.

        # Characters button.
        self.characters_menu_button = QtWidgets.QPushButton("CHARACTERS") # Create a button.
        self.characters_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.

        # Exit button.
        self.exit_button = QtWidgets.QPushButton("EXIT") # Create a button.
        self.exit_button.setStyleSheet(universal_stylesheet) # Add style to a button.

        # Layout.
        self.layout = QtWidgets.QVBoxLayout(self)    # Create layout.
        self.layout.addWidget(self.program_name)    # Add text label to the layout.
        self.layout.addWidget(self.characters_menu_button)  # Add characters button to the layout.
        self.layout.addWidget(self.exit_button)     # Add exit button to the layout.

        # Button clicks handlers
        self.exit_button.clicked.connect(self.exit_button_clicked) # Call exit function.
        self.characters_menu_button.clicked.connect(self.characters_menu_button_clicked) # Go to characters menu.

    @QtCore.Slot()

    def exit_button_clicked(self):
        '''
            exit_button_clicked() - termination function to finish program.
        '''
        sys.exit()

    def characters_menu_button_clicked(self):
        '''
            characters_menu_button_clicked() - characters menu open function.
        '''
        self.stacked_widget.setCurrentIndex(1)

class CharactersTab(QtWidgets.QWidget):
    '''
        CharactersTab class is designed to hold the characters widgets that user has at the moment.
    '''
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget    # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Characters Menu", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)    # Create layout.
        layout.addWidget(self.menu_name)    # Add the tab name to the layout.
        layout.addWidget(self.back_button)  # Add the back button to the layout.

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.stacked_widget.setCurrentIndex(0)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create a QStackedWidget - a list that will hold all the tabs we have.
    tabs_list = QtWidgets.QStackedWidget()

    # Add the main tab to list.
    main_tab = MainTab(tabs_list)
    tabs_list.addWidget(main_tab)

    # Add the characters tab.
    characters_tab = CharactersTab(tabs_list)
    tabs_list.addWidget(characters_tab)

    # Choose one of next showing modes:

    # Show in window mode.
    # tabs_list.resize(1280, 720)
    # tabs_list.show()

    # Show in fullscreen mode.
    tabs_list.showFullScreen()

    sys.exit(app.exec())