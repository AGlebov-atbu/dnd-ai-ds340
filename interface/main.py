'''
        To install pyside6 run: pip install pyside6
        To run this app: run main.py file.
'''
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from settings_manager import load_user_settings, load_language, save_user_settings
from PySide6.QtWidgets import QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QLabel
from settings_manager import load_user_settings, save_user_settings
from characters_manager import load_user_characters, save_user_characters, get_last_cid
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# User's characters.
user_characters = load_user_characters()

# Last character's ID.
last_cid = get_last_cid()

# Load user's settings.
user_settings = load_user_settings()
fullscreen_mode = user_settings.get("fullscreen", False)
current_language = user_settings.get("language", "en")
translations = load_language(current_language)

def update_language(language_code):
    global translations
    translations = load_language(language_code)
    settings_tab.update_translations(translations)

# Universal stylesheet - uses CSS syntax.
universal_stylesheet =  """font-size: 32px;
                           font-family: Times New Roman;
                        """



# Initialize the LLM
tokenizer = AutoTokenizer.from_pretrained("Gigax/NPC-LLM-7B")
model = AutoModelForCausalLM.from_pretrained("Gigax/NPC-LLM-7B", load_in_4bit = True, device_map="auto", torch_dtype=torch.float16)

class MainTab(QtWidgets.QWidget):
    '''
        MainTab class is designed to contain the main menu of the program, that consists of:
            - "CHAT" button, which leads to the chatting feature with the npc
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

        # Characters menu button.
        self.characters_menu_button = QtWidgets.QPushButton(translations["button_characters_menu"]) # Create a button.

        # Chat button.
        self.chat_menu_button = QtWidgets.QPushButton("CHAT") # Create a button.
        self.chat_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.chat_menu_button.clicked.connect(self.chat_button_clicked) # Open the chat tab.

        # Characters button.
        self.characters_menu_button = QtWidgets.QPushButton("CHARACTERS") # Create a button.
        self.characters_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.characters_menu_button.clicked.connect(self.characters_menu_button_clicked) # Go to characters menu.

        # Settings menu button.
        self.settings_menu_button = QtWidgets.QPushButton(translations["button_settings_menu"]) # Create a button.
        self.settings_menu_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.settings_menu_button.clicked.connect(self.settings_menu_button_clicked) # Go to settings menu.

        # Exit button.
        self.exit_button = QtWidgets.QPushButton(translations["button_exit"]) # Create a button.
        self.exit_button.setStyleSheet(universal_stylesheet) # Add style to a button.
        self.exit_button.clicked.connect(self.exit_button_clicked) # Call exit function.

        # Layout.
        self.layout = QtWidgets.QVBoxLayout(self) # Create layout.
        self.layout.addWidget(self.program_name) # Add text label to the layout.
        self.layout.addWidget(self.chat_menu_button) # Add chat button to the layout
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

    def chat_button_clicked(self):
        """
            Open character selection dialog and start chat.
        """
        try:
            # Open the character selection dialog.
            dialog = CharacterSelectionDialog(user_characters)
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                # Get the selected character name.
                selected_name = dialog.selected_character

                # Find the character data.
                for character in user_characters:
                    if (selected_name == character.name):
                        selected_character = character
                        break
                
                if selected_character:
                    # Pass the character data to the ChatWindow.
                    chat_tab = ChatWindow(self.global_tabs_list, selected_character)
                    self.global_tabs_list.addWidget(chat_tab)
                    self.global_tabs_list.setCurrentWidget(chat_tab)
                else:
                    QtWidgets.QMessageBox.warning(self, "Error", "Character data not found.")
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Error", "Character file not found.")


    def exit_button_clicked(self):
        '''
            exit_button_clicked() - termination function to finish program.
        '''
        sys.exit()

class SettingsTab(QtWidgets.QWidget):
    '''
        SettingsTab class is designed to hold the program parameters that user wants to see.
    '''
    def __init__(self, global_tabs_list, translations, update_language_callback):
        super().__init__()
        self.global_tabs_list = global_tabs_list # The tabs list.
        self.translations = translations
        self.update_language_callback = update_language_callback

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel(translations["title_settings_menu"], alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Screen mode settings.
        self.fullscreen_checkbox = QtWidgets.QCheckBox(translations["label_settings_fullscreen"])
        self.fullscreen_checkbox.setStyleSheet(universal_stylesheet)
        self.fullscreen_checkbox.setChecked(fullscreen_mode)
        self.fullscreen_checkbox.stateChanged.connect(self.toggle_fullscreen_checkbox)
        
        # Language selection.
        self.language_label = QtWidgets.QLabel(self.translations["label_settings_language"])
        self.language_dropdown = QtWidgets.QComboBox()
        self.language_dropdown.addItems(["English", "Русский"])
        self.language_dropdown.setCurrentIndex(0 if user_settings.get("language", "en") == "en" else 1)
        self.language_dropdown.currentIndexChanged.connect(self.change_language)

        # Back button.
        self.back_button = QtWidgets.QPushButton(translations["button_back"])
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout.
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.menu_name)
        layout.addWidget(self.fullscreen_checkbox)
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_dropdown)
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

    def change_language(self, index):
        '''
            change_language() - asks the user to restart the application to apply the new language.
        '''
        language_code = "en" if index == 0 else "ru"

        # Show the message.
        confirmation = QtWidgets.QMessageBox()
        confirmation.setIcon(QtWidgets.QMessageBox.Question)
        confirmation.setWindowTitle(self.translations.get("title_settings_change_language", "Change Language"))
        confirmation.setText(self.translations.get(
            "text_settings_change_language", 
            "To change the language, you need to restart the application. Do you agree?"
        ))
        confirmation.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # Set button labels.
        yes_button = confirmation.button(QtWidgets.QMessageBox.Yes)
        yes_button.setText(self.translations.get("button_yes", "Yes"))
        no_button = confirmation.button(QtWidgets.QMessageBox.No)
        no_button.setText(self.translations.get("button_no", "No"))

        # Wait for the response.
        response = confirmation.exec()

        if response == QtWidgets.QMessageBox.Yes:
            # Save the language setting.
            user_settings["language"] = language_code
            save_user_settings(user_settings)

            # Restart the app.
            QtCore.QCoreApplication.quit()
            QtCore.QProcess.startDetached(sys.executable, sys.argv)
        else:
            # If user choose "No" - do nothing.
            self.language_dropdown.setCurrentIndex(0 if user_settings.get("language", "en") == "en" else 1)

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

        # Main layout of the page.
        layout = QtWidgets.QVBoxLayout(self)

        # Show the tab name.
        self.menu_name = QtWidgets.QLabel(translations["title_characters_menu"], alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)
        layout.addWidget(self.menu_name)

        # Scroll Area for the list of characters.
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True) # Make it resizable.
        layout.addWidget(self.scroll_area)

        # Container inside the Scroll Area.
        self.scroll_content = QtWidgets.QWidget()
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)

        # Create character button.
        self.create_character_button = QtWidgets.QPushButton(translations["button_create_character"])
        self.create_character_button.setStyleSheet(universal_stylesheet)
        self.create_character_button.clicked.connect(self.create_character_button_clicked)
        layout.addWidget(self.create_character_button)

        # Back button.
        self.back_button = QtWidgets.QPushButton(translations["button_back"])
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)
        layout.addWidget(self.back_button)

        # Add characters to the layout.
        self.update_characters()

    def update_characters(self):
        '''
            update_characters() - updates the displayed list of characters on the Characters page.
        '''
        # Load updated characters from the file.
        global user_characters
        user_characters = load_user_characters()

        # Clear the current scroll layout.
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Add characters to the scroll_layout.
        for character in user_characters:
            character_row = QtWidgets.QHBoxLayout() # Horizontal layout for character's button and delete button.

            # Character's button.
            character_button = QtWidgets.QPushButton(character.name)
            character_button.setStyleSheet(universal_stylesheet)
            character_button.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

            # Delete button.
            delete_button = QtWidgets.QPushButton("❌")
            delete_button.setStyleSheet("color: red; font-weight: bold;")
            delete_button.setFixedWidth(30)
            delete_button.clicked.connect(lambda ch, cid=character.cid: self.delete_character(cid))

            # Add buttons to the horizontal layout.
            character_row.addWidget(character_button)
            character_row.addWidget(delete_button)

            # Add horizontal layout to the vertical layout.
            row_widget = QtWidgets.QWidget()
            row_widget.setLayout(character_row)
            self.scroll_layout.addWidget(row_widget)

    def create_character_button_clicked(self):
        '''
            create_character_button_clicked() - opens character creation tab.
        '''
        self.global_tabs_list.setCurrentIndex(3)
    
    def delete_character(self, character_id):
        '''
            delete_character() - deletes a character from the JSON file and updates the interface based on character's ID.
        '''
        # Load characters from the file.
        user_characters = load_user_characters()

        # Delete the character based on its ID.
        updated_characters = [char for char in user_characters if char.cid != character_id]

        # Save the updated list of characters.
        save_user_characters(updated_characters)

        # Update the interface.
        self.update_characters()

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
        self.menu_name = QtWidgets.QLabel(translations["title_characters_creation_menu"], alignment=QtCore.Qt.AlignCenter)
        self.menu_name.setStyleSheet(universal_stylesheet)

        # Character name input.
        self.name_label = QtWidgets.QLabel(translations["label_character_name"])
        self.name_input = QtWidgets.QLineEdit()

        # Character age input.
        self.age_label = QtWidgets.QLabel(translations["label_character_age"])
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(0, 150)

        # Positive traits input.
        self.positive_label = QtWidgets.QLabel(translations["label_character_positive_traits"])
        self.positive_input = QtWidgets.QLineEdit()

        # Negative traits input.
        self.negative_label = QtWidgets.QLabel(translations["label_character_negative_traits"])
        self.negative_input = QtWidgets.QLineEdit()

        # Character lore input.
        self.lore_label = QtWidgets.QLabel(translations["label_character_lore"])
        self.lore_input = QtWidgets.QTextEdit()

        # Save button.
        self.save_button = QtWidgets.QPushButton(translations["button_save"])
        self.save_button.setStyleSheet(universal_stylesheet)
        self.save_button.clicked.connect(self.save_character)

        # Back button.
        self.back_button = QtWidgets.QPushButton(translations["button_back"])
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
        # Make last_cid be global.
        global last_cid
        
        # Collect character data.
        name = self.name_input.text()
        age = self.age_input.value()
        positive_traits = [trait.strip() for trait in self.positive_input.text().split(",") if trait.strip()]
        negative_traits = [trait.strip() for trait in self.negative_input.text().split(",") if trait.strip()]
        lore = self.lore_input.toPlainText()

        if not name:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Character name cannot be empty.")
            return

        # Generate a new unique cid.
        last_cid += 1

        # Load existing characters and add the new one.
        characters = load_user_characters()
        new_character = {
            "cid": last_cid,
            "name": name,
            "age": age,
            "positive_traits": positive_traits,
            "negative_traits": negative_traits,
            "lore": lore
        }
        
        characters.append(new_character)
        save_user_characters(characters)
        
        # Reset the form.
        self.reset_form()

        # Update the characters list in the CharactersMenuTab.
        characters_menu_tab = self.global_tabs_list.widget(1)
        if hasattr(characters_menu_tab, "update_characters"):
            characters_menu_tab.update_characters()

        # Redirect to the characters menu.
        self.global_tabs_list.setCurrentIndex(1)

    def reset_form(self):
        '''
            reset_form() - resets all input fields to their default values.
        '''
        self.name_input.clear()
        self.age_input.setValue(0)
        self.positive_input.clear()
        self.negative_input.clear()
        self.lore_input.clear()

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the characters menu under 1 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(1)

class CharacterSelectionDialog(QtWidgets.QDialog):
    """Dialog for selecting a character."""
    def __init__(self, characters):
        super().__init__()
        self.setWindowTitle("Select a Character")
        self.setGeometry(200, 200, 400, 300)

        self.selected_character = None

        # Create a list widget to display character names
        self.character_list = QtWidgets.QListWidget(self)
        for character in characters:
            # Adjust to access the `name` attribute of `Character` objects
            self.character_list.addItem(character.name)

        # Create "Select" and "Cancel" buttons
        self.select_button = QtWidgets.QPushButton("Select")
        self.select_button.clicked.connect(self.select_character)

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select a character for the chat:"))
        layout.addWidget(self.character_list)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def select_character(self):
        """
            Handle character selection.
        """
        current_item = self.character_list.currentItem()
        if current_item:
            self.selected_character = current_item.text()
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "No Selection", "Please select a character.")


class ChatWindow(QtWidgets.QWidget):
    """
        Chat interface window with LLM integration.
    """
    def __init__(self, global_tabs_list, character_data):
        super().__init__()
        self.global_tabs_list = global_tabs_list  
        self.character_data = character_data #Store character data

        # Conversation log
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Type your message here...")
        self.user_input.returnPressed.connect(self.handle_user_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.handle_user_input)

        # Back button.
        self.back_button = QtWidgets.QPushButton(translations["button_back"])
        self.back_button.setStyleSheet(universal_stylesheet)
        self.back_button.clicked.connect(self.back_button_clicked)

        # Layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(f"Chat with {character_data.name}:", alignment=QtCore.Qt.AlignCenter))
        layout.addWidget(self.chat_history)
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)
        layout.addWidget(self.back_button)

    def back_button_clicked(self):
        '''
            back_button_clicked() - returns to the main menu under 0 index in tabs list.
        '''
        self.global_tabs_list.setCurrentIndex(0)

    def load_character_data(self):
        """
            Load the character's data from the JSON file.
        """
        try:
            with open("user_characters.json", "r") as file:
                characters = json.load(file)
                for char in characters:
                    if char["cid"] == self.character_id:
                        return char
            raise ValueError("Character not found.")
        except FileNotFoundError:
            QtWidgets.QMessageBox.warning(self, "Error", "Character file not found.")
            return {"name": "Unknown NPC",
                    "lore": "",
                    "positive_traits": [],
                    "negative_traits": []}

    def handle_user_input(self):
        """
            Handle user input and display it in the chat history.
        """
        user_text = self.user_input.text().strip()
        if user_text:
            # Add user's message to the chat history.
            self.chat_history.append(f"User: {user_text}")
            self.user_input.clear()

            # Generate NPC response.
            npc_response = self.generate_npc_response(user_text)

            # Add NPC's response to the chat history.
            self.chat_history.append(f"NPC: {npc_response}")

    def generate_npc_response(self, user_text):
        """
            Generate a response using the LLM.
        """
        character_context = (
            f"NPC Name: {self.character_data.name}\n"
            f"Lore: {self.character_data.lore}\n"
            f"Positive Traits: {', '.join(self.character_data.positive_traits)}\n"
            f"Negative Traits: {', '.join(self.character_data.negative_traits)}\n\n"
            f"User: {user_text}\n"
            f"NPC:"
        )

        inputs = tokenizer(character_context, return_tensors="pt", padding=True, truncation=True).to("cuda")
        outputs = model.generate(inputs["input_ids"], attention_mask=inputs["attention_mask"], max_length=100, do_sample=True, temperature=0.7)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Extract only the NPC's response.
        return response.split("NPC:")[-1].strip()



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
    settings_tab = SettingsTab(global_tabs_list, translations, update_language)
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
