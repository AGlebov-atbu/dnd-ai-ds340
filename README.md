# dnd-ai-ds340
txt2txt AI tool for DnD like games.

- project name: dnd-ai-ds340
- actual name: to be assigned

---
  
# TODO
1. Create interface.  
    - Potential libraries: PyQt (read about this one), Flet, Kivy
    - Main menu with: 1) Name of our product, 2) **[CHARACTERS]** and 3) **[EXIT]** buttons.
    - **[CHARACTERS]** menu consists of a list of n characters + **[CREATE]** button which allows a user to create a new character.
    - Characters will not be editable. However, they can be deleted. So, we need to implement the **[DELETE]** button next to the character.
    - Once in the character creation menu - user accesses the number of fields that they can fill to create the features for their character. The fields that are currently accessible are: **[TODO]**.
    - Once character is created, it is stored on the user's local machine and can be accessed anytime.
    - Once character is clicked in the application - the chat opens and user can haveconversation with this character.
    - User's information is supposed to store somewhere in savings files, so figure out how to do that:
        - How to store information? - have no idea yet
        - Which information should be stored? - characters and their features!
2. Train the model.
    - Figure out what data we need to use in here.
    - Figure out how to separate the behavior. (multiple models?)
    - Figure out how to make it more "alive" and less "predictable". (data problems?)
---