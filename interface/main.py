'''
        To install pyside6 run: pip install pyside6
'''
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from settings_manager import load_user_settings, save_user_settings
from characters_manager import load_user_characters, save_user_characters

# User's characters.
user_characters = load_user_characters()

# Load user's settings.
user_settings = load_user_settings()
fullscreen_mode = user_settings.get("fullscreen", False)

# Universal stylesheet - uses CSS syntax.
universal_stylesheet =  """font-size: 32px;
                           font-family: Times New Roman;
                        """

class MainTab(QtWidgets.QWidget):
    '''
        MainTab class is designed to contain the main menu of the program, that consists of:
            - "CHARACTERS" button, which leads to the characters' page;
            - "SETTINGS" button, which leads to the settings menu;
            - "EXIT" button, which closes the program.
    '''
    def __init__(self, global_tabs_list):
        super().__init__()
        self.global_tabs_list = global_tabs_list # The tabs list.

        # Program name (to be discussed). 
        self.program_name = QtWidgets.QLabel("D&D AI CHATBOTS", # Create a text label.
                                             alignment=QtCore.Qt.AlignCenter) # Text alignment.
        self.program_name.setStyleSheet(universal_stylesheet) # Add style to text.

        # Characters button.
        self.characters_menu_button = QtWidgets.QPushButton("CHARACTERS") # Create a button.
        self.characters_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.characters_menu_button.clicked.connect(self.characters_menu_button_clicked) # Go to characters menu.

        # Settings button.
        self.settings_menu_button = QtWidgets.QPushButton("SETTINGS") # Create a button.
        self.settings_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.settings_menu_button.clicked.connect(self.settings_menu_button_clicked) # Go to settings menu.

        # Exit button.
        self.exit_button = QtWidgets.QPushButton("EXIT") # Create a button.
        self.exit_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.exit_button.clicked.connect(self.exit_button_clicked) # Call exit function.

        # Layout.
        self.layout = QtWidgets.QVBoxLayout(self) # Create layout.
        self.layout.addWidget(self.program_name) # Add text label to the layout.
        self.layout.addWidget(self.characters_menu_button) # Add characters button to the layout.
        self.layout.addWidget(self.settings_menu_button) # Add settings button to the layout.
        self.layout.addWidget(self.exit_button) # Add exit button to the layout.

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
        self.global_tabs_list = global_tabs_list # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Settings", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Screen mode settings.
        self.fullscreen_checkbox = QtWidgets.QCheckBox("Fullscreen mode")
        self.fullscreen_checkbox.setStyleSheet(universal_stylesheet)
        self.fullscreen_checkbox.setChecked(fullscreen_mode)
        self.fullscreen_checkbox.stateChanged.connect(self.toggle_fullscreen_checkbox)

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.menu_name)
        layout.addWidget(self.fullscreen_checkbox)
        layout.addWidget(self.back_button)
    
    def toggle_fullscreen_checkbox(self, state):
        '''
            toggle_fullscreen_checkbox() - changes the screen mode:
                - Fullscreen if checkbox is checked.
                - Window mode if checkbox is not checked.
        '''
        self.fullscreen_mode = bool(state)
        user_settings["fullscreen"] = self.fullscreen_mode
        save_user_settings(user_settings)

        if self.fullscreen_checkbox.isChecked():
            self.global_tabs_list.showFullScreen()
        else:
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
        self.global_tabs_list = global_tabs_list # The tabs list.

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
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.menu_name)

        if not user_characters: # User does not have any characters - the set is empty
            layout.addWidget(self.create_character_button) # Add create character button to the layout.
        else: # If there are any characters: add them on the layout.
            for character in user_characters:
                name_button = character.name
                self.name_button = QtWidgets.QPushButton(f"{name_button}")
                self.name_button.setStyleSheet(universal_stylesheet)
                layout.addWidget(self.name_button) # Add character chat button to the layout.

            layout.addWidget(self.create_character_button) # Add create character button to the layout.
        
        layout.addWidget(self.back_button) # Add the back button to the layout.

    def update_characters(self):
        '''
            update_characters() - updates the displayed list of characters on the Characters page.
        '''
        # Load updated characters from the file.
        user_characters = load_user_characters()

        # Clear the layout or widget containing the characters.
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
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
        
        self.layout().addWidget(self.menu_name)

        # Add characters to the layout.
        for character in user_characters:
            name_button = character.name
            self.name_button = QtWidgets.QPushButton(f"{name_button}")
            self.name_button.setStyleSheet(universal_stylesheet)
            self.layout().addWidget(self.name_button) # Add character chat button to the layout.

        self.layout().addWidget(self.create_character_button) # Add create character button to the layout.
        self.layout().addWidget(self.back_button) # Add the back button to the layout.

    def create_character_button_clicked(self):
        '''
            create_character_button_clicked() - opens character creation tab.
        '''
        self.global_tabs_list.setCurrentIndex(3)

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
        self.global_tabs_list = global_tabs_list # The tabs list.

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel("Create a character", alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # TODO: implement the parameters to create characters.
        # Character name input.
        self.name_label = QtWidgets.QLabel("Character Name:")
        self.name_input = QtWidgets.QLineEdit()

        # Character age input.
        self.age_label = QtWidgets.QLabel("Character Age:")
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(0, 150)

        # Positive traits input.
        self.positive_label = QtWidgets.QLabel("Positive Traits (comma-separated):")
        self.positive_input = QtWidgets.QLineEdit()

        # Negative traits input.
        self.negative_label = QtWidgets.QLabel("Negative Traits (comma-separated):")
        self.negative_input = QtWidgets.QLineEdit()

        # Character lore input.
        self.lore_label = QtWidgets.QLabel("Character Lore:")
        self.lore_input = QtWidgets.QTextEdit()

        # Save button.
        self.save_button = QtWidgets.QPushButton("SAVE")
        self.save_button.setStyleSheet(universal_stylesheet)
        self.save_button.clicked.connect(self.save_character)

        # Back button.
        self.back_button = QtWidgets.QPushButton("BACK")
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.menu_name)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)
        layout.addWidget(self.positive_label)
        layout.addWidget(self.positive_input)
        layout.addWidget(self.negative_label)
        layout.addWidget(self.negative_input)
        layout.addWidget(self.lore_label)
        layout.addWidget(self.lore_input)
        layout.addWidget(self.save_button)
        layout.addWidget(self.back_button)

    def save_character(self):
        '''
            save_character() - saves the character data to the file and redirects to the characters menu.
        '''
        # Collect character data.
        name = self.name_input.text()
        age = self.age_input.value()
        positive_traits = [trait.strip() for trait in self.positive_input.text().split(",") if trait.strip()]
        negative_traits = [trait.strip() for trait in self.negative_input.text().split(",") if trait.strip()]
        lore = self.lore_input.toPlainText()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Character name cannot be empty.")
            return

        # Load existing characters and add the new one.
        characters = load_user_characters()
        new_character = {
            "name": name,
            "age": age,
            "positive_traits": positive_traits,
            "negative_traits": negative_traits,
            "lore": lore
        }
        characters.append(new_character)
        save_user_characters(characters)

        # Update the characters list in the CharactersMenuTab.
        characters_menu_tab = self.global_tabs_list.widget(1)
        if hasattr(characters_menu_tab, "update_characters"):
            characters_menu_tab.update_characters()

        # Redirect to the characters menu.
        self.global_tabs_list.setCurrentIndex(1)
    
    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the characters menu under 1 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(1)

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

    # Check settings for the fullscreen mode.
    if fullscreen_mode:
        global_tabs_list.showFullScreen()
    else:
        global_tabs_list.showNormal()
        global_tabs_list.resize(800, 600)

    sys.exit(app.exec())