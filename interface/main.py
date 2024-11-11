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

        # Settings button.
        self.settings_menu_button = QtWidgets.QPushButton("SETTINGS")   # Create a button.
        self.settings_menu_button.setStyleSheet(universal_stylesheet)   # Add style to a button.

        # Exit button.
        self.exit_button = QtWidgets.QPushButton("EXIT") # Create a button.
        self.exit_button.setStyleSheet(universal_stylesheet) # Add style to a button.

        # Layout.
        self.layout = QtWidgets.QVBoxLayout(self)    # Create layout.
        self.layout.addWidget(self.program_name)    # Add text label to the layout.
        self.layout.addWidget(self.characters_menu_button)  # Add characters button to the layout.
        self.layout.addWidget(self.settings_menu_button)    # Add settings button to the layout.
        self.layout.addWidget(self.exit_button)     # Add exit button to the layout.

        # Button clicks handlers
        self.characters_menu_button.clicked.connect(self.characters_menu_button_clicked) # Go to characters menu.
        self.settings_menu_button.clicked.connect(self.settings_menu_button_clicked)    # Go to settings menu.
        self.exit_button.clicked.connect(self.exit_button_clicked) # Call exit function.

    @QtCore.Slot()

    def characters_menu_button_clicked(self):
        '''
            characters_menu_button_clicked() - characters menu open function.
        '''
        self.stacked_widget.setCurrentIndex(1)

    def settings_menu_button_clicked(self):
        '''
            settings_menu_button_clicked() - opens settings tab.
        '''
        self.stacked_widget.setCurrentIndex(2)

    def exit_button_clicked(self):
        '''
            exit_button_clicked() - termination function to finish program.
        '''
        sys.exit()

class SettingsTab(QtWidgets.QWidget):
    '''
        SettingsTab class is designed to hold the program parameters that user wants to see.
    '''
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget    # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Settings", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Screen mode settings.
        self.fullscreen_mode = QtWidgets.QCheckBox("Fullscreen mode")
        self.fullscreen_mode.setStyleSheet(universal_stylesheet)
        self.fullscreen_mode.stateChanged.connect(self.toggle_fullscreen_checkbox)

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)    # Create layout.
        layout.addWidget(self.menu_name)    # Add the tab name to the layout.
        layout.addWidget(self.fullscreen_mode)  #Add the fullscreen mode checkbox.
        layout.addWidget(self.back_button)  # Add the back button to the layout.
    
    def toggle_fullscreen_checkbox(self, state):
        '''
            toggle_fullscreen_checkbox() - changes the screen mode:
                - Fullscreen if checkbox is checked.
                - Window mode if checkbox is not checked.
        '''
        if self.fullscreen_mode.isChecked():
            self.stacked_widget.showFullScreen()
        else:
            # self.stacked_widget.resize(1280, 720)
            self.stacked_widget.showNormal()

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.stacked_widget.setCurrentIndex(0)

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

    # Add the main tab to the list.
    main_tab = MainTab(tabs_list)
    tabs_list.addWidget(main_tab)

    # Add the characters tab to the list.
    characters_tab = CharactersTab(tabs_list)
    tabs_list.addWidget(characters_tab)

    # Add the settings tab to the list.
    settings_tab = SettingsTab(tabs_list)
    tabs_list.addWidget(settings_tab)
    
    # Show in normal (window) mode.
    tabs_list.resize(800, 600)
    tabs_list.showNormal()

    sys.exit(app.exec())