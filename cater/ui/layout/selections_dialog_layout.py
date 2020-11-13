import PySimpleGUI as psg


class SelectionsDialogLayout(list):
    """The Selections Dialog layout.
    """

    def __init__(self, *choices):
        """Constructor
        """

        self._checkboxes = {choice: psg.Checkbox(choice) for choice in self._choices}

        return [
            list(self._checkboxes.values()),
            [psg.Button(self.OK), psg.Button(self.BTN_CANCEL)],
        ]
