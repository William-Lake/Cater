import PySimpleGUI as psg

from ui.layout.selections_dialog_layout import SelectionsDialogLayout


class SelectionsDialog(psg.Window):
    """A custom dialog for gathering user selections.

    :param psg: The parent Window.
    :type psg: PySimpleGUI.Window
    """

    OK = "OK"
    BTN_CANCEL = "BTN_CANCEL"

    def __init__(self, *choices):
        """Constructor
        """

        self._choices = choices

        self._layout = SelectionsDialogLayout(*choices)

        super().__init__("Choose at least one option...", self._layout)

    def start(self, limit=1):
        """Starts the UI event loop.

        :param limit: The default number of expected choices, defaults to 1
        :type limit: int, optional
        :return: The user selections, or None if the hit "Cancel"/closed the dialog.
        :rtype: list
        """

        selections = None

        while True:

            event, values = self.read()

            if event == psg.WIN_CLOSED or event == self.BTN_CANCEL:

                break

            elif event == self.OK:

                selections = [
                    selection
                    for selection, chk in self._layout.checkboxes.items()
                    if chk.Get()
                ]

                break

        self.close()

        # May not want to *force* the user to pick something.
        # What if they change their mind?
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
