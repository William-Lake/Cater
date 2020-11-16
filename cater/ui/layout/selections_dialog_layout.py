import PySimpleGUI as psg


class SelectionsDialogLayout(list):
    """The Selections Dialog layout.
    """

    def __init__(self, *choices):
        """Constructor
        """

        self.checkboxes = {choice: psg.Checkbox(choice) for choice in choices}

        self.extend(
            [list(self.checkboxes.values()), [psg.Button("Ok"), psg.Button("Cancel")]]
        )
