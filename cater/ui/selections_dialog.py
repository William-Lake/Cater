import PySimpleGUI as psg


class SelectionsDialog(psg.Window):

    OK = "OK"
    CANCEL = "CANCEL"

    def __init__(self, *choices):

        self._choices = choices

        super().__init__("Choose at least one option...", self._create_layout())

    def _create_layout(self):

        self._checkboxes = {choice: psg.Checkbox(choice) for choice in self._choices}

        return [
            list(self._checkboxes.values()),
            [psg.Button(self.OK), psg.Button(self.CANCEL)],
        ]

    def start(self, limit=1):

        selections = None

        while True:

            event, values = self.read()

            if event == psg.WIN_CLOSED or event == self.CANCEL:

                break

            elif event == self.OK:

                selections = [
                    selection
                    for selection, chk in self._checkboxes.items()
                    if chk.Get()
                ]

                break

        self.close()

        if selections is not None and len(selections) != limit:

            if len(selections) != limit:

                message = (
                    f"You must select {limit} options."
                    if limit > 1
                    else "You must select at least one option."
                )

                psg.PopupError(message)

                return SelectionsDialog(*self._choices).start(limit=limit)

        return selections
