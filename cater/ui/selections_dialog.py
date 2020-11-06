import PySimpleGUI as psg


class SelectionsDialog(psg.Window):
    def __init__(self,*choices,limit=None):

        super().__init__("Selections", self._create_layout(*choices))

        return self.start(limit)

    def _create_layout(self, *choices):

        self._checkboxes = {choice: psg.Checkbox(choice) for choice in choices}

        return [list(self._checkboxes.values())]

    def start(self,limit):

        while True:

            event, values = self.read()

            if event == psg.WIN_CLOSED:

                break

        selections = [col for col, chk in self._checkboxes.items() if chk.Get()]

        if len(selections) != limit:

            psg.PopupError(f'You must select {limit} options.')

            return self._start(limit)
