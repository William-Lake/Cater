import PySimpleGUI as psg
import pandas as pd

from cater.ui.layout.summary_dialog_layout import SummaryDialogLayout
from cater.managers.input_manager import InputManager


class SummaryDialog(psg.Window):
    """A dialog for providing a dataset summary.

    :param psg: The parent Window.
    :type psg: PySimpleGUI.Window
    """

    def __init__(self, dataset_name, summary_data):
        """Constructor

        :param datasets: The current datasets.
        :type datasets: list
        """

        super().__init__("Summary", SummaryDialogLayout(dataset_name, summary_data))

    def start(self):
        """Starts the UI event loop.

        :return: The mapping of report types and associated data for report generation.
        :rtype: dict
        """

        while True:

            event, values = self.read()

            if event in [
                psg.WIN_CLOSED,
                "Ok",
            ]:

                break

        self.close()
