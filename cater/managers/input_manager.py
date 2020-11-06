import PySimpleGUI as psg

from ui.selections_dialog import SelectionsDialog


class InputManager:

    def get_filepath_input(self,**kwargs):

        return psg.PopupGetFile('Pick File',**kwargs)

    def get_user_confirmation(self,prompt):

        return psg.PopupYesNo(prompt)

    def get_user_selections(self,choices,limit=None):

        return SelectionsDialog(choices,limit)