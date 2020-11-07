from pathlib import Path

import PySimpleGUI as psg

from ui.selections_dialog import SelectionsDialog


class InputManager:
    def get_filepath_input(self, **kwargs):

        selected_paths = psg.PopupGetFile("Pick File", **kwargs)

        # If selection(s) made,
        if selected_paths:

            # Convert the paths to Path objects.
            # If multiple files selected, they are returned
            # as a ';' delimited string.
            selected_paths = [
                Path(selected_path) for selected_path in selected_paths.split(";")
            ]

        return selected_paths

    def get_user_confirmation(self, prompt):

        return psg.PopupYesNo(prompt)

    def get_user_selections(self, choices, limit=None):

        return SelectionsDialog(choices, limit)
