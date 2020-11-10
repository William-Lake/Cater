from pathlib import Path

import PySimpleGUI as psg

from ui.selections_dialog import SelectionsDialog


class InputManager:

    YES = "Yes"
    NO = "No"

    @staticmethod
    def get_filepath_input(**kwargs):

        if "no_window" not in kwargs.keys() or not kwargs["no_window"]:

            kwargs["no_window"] = True

        selected_paths = psg.PopupGetFile(**kwargs)

        # If selection(s) made,
        if selected_paths:

            if isinstance(selected_paths, tuple):

                selected_paths = [
                    Path(selected_path) for selected_path in selected_paths
                ]

        return selected_paths

    @staticmethod
    def get_directory_input(**kwargs):

        if "no_window" not in kwargs.keys() or not kwargs["no_window"]:

            kwargs["no_window"] = True

        selected_directory = psg.PopupGetFolder(**kwargs)

        print(selected_directory)

        if selected_directory:

            selected_directory = Path(selected_directory)

        return selected_directory

    @staticmethod
    def get_user_confirmation(prompt):

        return psg.PopupYesNo(prompt, button_color=("#E0FBFC", "#1982C4"))

    @staticmethod
    def get_user_selections(*choices, limit=1):

        return SelectionsDialog(*choices).start(limit=limit)

    @staticmethod
    def get_user_text_input(prompt):

        return psg.PopupGetText(prompt, button_color=("#E0FBFC", "#DE1A1A"))
