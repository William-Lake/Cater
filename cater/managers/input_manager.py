from pathlib import Path

import PySimpleGUI as psg

from ui.selections_dialog import SelectionsDialog
from ui.cater_palette import BUTTON, BACKGROUND, TEXT


class InputManager:
    """Manages collecting user inputs.
    """

    YES = "Yes"
    NO = "No"

    @staticmethod
    def get_filepath_input(**kwargs):
        """Collects one or more filepaths from the user.

        :return: A list of filepaths.
        :rtype: list
        """

        if "no_window" not in kwargs.keys() or not kwargs["no_window"]:

            kwargs["no_window"] = True

        selected_paths = psg.PopupGetFile(
            button_color=BUTTON, background_color=BACKGROUND, text_color=TEXT, **kwargs
        )

        # If selection(s) made,
        if selected_paths:

            if isinstance(selected_paths, tuple):

                selected_paths = [
                    Path(selected_path) for selected_path in selected_paths
                ]

        return selected_paths

    @staticmethod
    def get_directory_input(**kwargs):
        """Collects a directory path from the user.

        :return: The collected path.
        :rtype: pathlib.Path
        """

        if "no_window" not in kwargs.keys() or not kwargs["no_window"]:

            kwargs["no_window"] = True

        selected_directory = psg.PopupGetFolder(
            button_color=BUTTON, background_color=BACKGROUND, text_color=TEXT, **kwargs
        )

        if selected_directory:

            selected_directory = Path(selected_directory)

        return selected_directory

    @staticmethod
    def get_user_confirmation(prompt):
        """Gets a yes/no response from the user.

        :param prompt: The prompt to provide the user.
        :type prompt: str
        :return: The user's selection, either YES or NO.
        :rtype: str
        """

        # TODO This should return a boolean.

        return psg.PopupYesNo(
            prompt, button_color=BUTTON, background_color=BACKGROUND, text_color=TEXT
        )

    @staticmethod
    def get_user_selections(*choices, limit=1):
        """Collects user choics from a given selection.

        :param limit: The minimum number of choices, defaults to 1
        :type limit: int, optional
        :return: The selections made by the user.
        :rtype: list
        """

        return SelectionsDialog(*choices).start(limit=limit)

    @staticmethod
    def get_user_text_input(prompt):
        """Collects text input from the user.

        :param prompt: The prompt to show the user.
        :type prompt: str
        :return: The provided user text.
        :rtype: str
        """

        return psg.PopupGetText(
            prompt, button_color=BUTTON, background_color=BACKGROUND, text_color=TEXT
        )
