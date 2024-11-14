'''
        To install pyside6 run: pip install pyside6
'''
import sys
from PySide6 import QtCore, QtWidgets, QtGui

# Universal stylesheet - uses CSS syntax.
universal_stylesheet =  """font-size: 32px;
                           font-family: Times New Roman;
                        """

# List of characters.
# list_from_file = # TODO: add characters from file (that every user will have) to the list.
# characters_list = list_from_file
characters_list = []

class MainTab(QtWidgets.QWidget):
    '''
        MainTab class is designed to contain the main menu of the program, that consists of:
            - "CHARACTERS" button, which leads to the characters' page;
            - "SETTINGS" button, which leads to the settings menu;
            - "EXIT" button, which closes the program.
    '''
    def __init__(self, global_tabs_list):
        super().__init__()
        self.global_tabs_list = global_tabs_list    # The tabs list.

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

    def characters_menu_button_clicked(self):
        '''
            characters_menu_button_clicked() - opens characters menu tab.
        '''
        self.global_tabs_list.setCurrentIndex(1)

    def settings_menu_button_clicked(self):
        '''
            settings_menu_button_clicked() - opens settings tab.
        '''
        self.global_tabs_list.setCurrentIndex(2)

    def exit_button_clicked(self):
        '''
            exit_button_clicked() - termination function to finish program.
        '''
        sys.exit()

class SettingsTab(QtWidgets.QWidget):
    '''
        SettingsTab class is designed to hold the program parameters that user wants to see.
    '''
    def __init__(self, global_tabs_list):
        super().__init__()
        self.global_tabs_list = global_tabs_list    # The tabs list.

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
            self.global_tabs_list.showFullScreen()
        else:
            # self.global_tabs_list.resize(1280, 720)
            self.global_tabs_list.showNormal()

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(0)

class CharactersMenuTab(QtWidgets.QWidget):
    '''
        CharactersMenuTab class is designed to hold the characters widgets that user has at the moment.
    '''
    def __init__(self, global_tabs_list):
        super().__init__()
        self.global_tabs_list = global_tabs_list    # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Characters Menu", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Create character button.
        self.create_character_button = QtWidgets.QPushButton("ADD")
        self.create_character_button.setStyleSheet(universal_stylesheet)
        self.create_character_button.clicked.connect(self.create_character_button_clicked)

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)    # Create layout.
        layout.addWidget(self.menu_name)    # Add the tab name to the layout.
        if len(characters_list) < 1:
            layout.addWidget(self.create_character_button)  # Add create character button to the layout.
        else:   # If there are any characters: add them on the layout.
            for i in range(len(characters_list)):
                layout.addWidget(self.characters_list[i])   # Add character chat button to the layout.
            layout.addWidget(self.create_character_button)  # Add create character button to the layout.
        layout.addWidget(self.back_button)  # Add the back button to the layout.

    def create_character_button_clicked(self):
        '''
            create_character_button_clicked() - opens character creation tab.
        '''
        self.global_tabs_list.setCurrentIndex(1)
        print("Create character button was clicked, but have not been implemented yet.")

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(0)

class CharactersCreationTab(QtWidgets.QWidget):
    '''
        CharactersCreationTab class is designed to create a character.
    '''
    def __init__(self, global_tabs_list):
        super().__init__()
        self.global_tabs_list = global_tabs_list    # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Characters Menu", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # TODO: implement the parameters to create characters.

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(0)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create a QStackedWidget - a list that will hold all the tabs we have.
    global_tabs_list = QtWidgets.QStackedWidget()

    # Add the main tab to the list.
    main_tab = MainTab(global_tabs_list)
    global_tabs_list.addWidget(main_tab)

    # Add the characters tab to the list.
    characters_tab = CharactersMenuTab(global_tabs_list)
    global_tabs_list.addWidget(characters_tab)

    # Add the settings tab to the list.
    settings_tab = SettingsTab(global_tabs_list)
    global_tabs_list.addWidget(settings_tab)

    # Add the character creation tab to the list.
    character_creation_tab = CharactersCreationTab(global_tabs_list)
    global_tabs_list.addWidget(character_creation_tab)
    
    # Show in normal (window) mode.
    global_tabs_list.resize(800, 600)
    global_tabs_list.showNormal()

    sys.exit(app.exec())