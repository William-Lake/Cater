from pathlib import Path

import PySimpleGUI as psg

from ui.selections_dialog import SelectionsDialog


class InputManager:
    def get_filepath_input(self, **kwargs):

        if 'no_window' not in kwargs.keys() or not kwargs['no_window']:

            kwargs['no_window'] = True

        selected_paths = psg.PopupGetFile(**kwargs)

        # If selection(s) made,
        if selected_paths:

            if isinstance(selected_paths,tuple):

                selected_paths = [
                    Path(selected_path) for selected_path in selected_paths
                ]                

        return selected_paths

    def get_directory_input(self, **kwargs):

        if 'no_window' not in kwargs.keys() or not kwargs['no_window']:

            kwargs['no_window'] = True        

        selected_directory = psg.PopupGetFolder(**kwargs)

        if selected_directory:

            selected_diretory = Path(selected_directory)

        return selected_directory

    def get_user_confirmation(self, prompt):

        return psg.PopupYesNo(prompt,button_color=("#E0FBFC",'#1982C4'))

    def get_user_selections(self, choices, limit=None):

        return SelectionsDialog(choices, limit)
