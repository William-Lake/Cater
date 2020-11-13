import PySimpleGUI as psg


class SelectionsDialogLayout(list):
    """The Selections Dialog layout.
    """

    OK = 'OK'
    BTN_CANCEL = 'CANCEL'

    def __init__(self, *choices):
        """Constructor
        """

        self.checkboxes = {choice: psg.Checkbox(choice) for choice in choices}

        self.append(list(self.checkboxes.values()))

        self.append([psg.Button(self.OK), psg.Button(self.BTN_CANCEL)])
