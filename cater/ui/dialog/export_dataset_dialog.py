import PySimpleGUI as psg
import pandas as pd

from cater.ui.layout.export_dataset_dialog_layout import ExportDatasetDialogLayout
from cater.ui.controls.export_dataset_dialog_controls import (
    FRM_DATASETS,
    CMB_OPTIONS,
    CMB_OPTIONS,
    CHK_ALL,
)
from cater.managers.input_manager import InputManager


class ExportDatasetDialog(psg.Window):
    def __init__(self, dataset_names, export_options):

        self._dataset_names = dataset_names

        self._layout = ExportDatasetDialogLayout(dataset_names, export_options)

        super().__init__("Export Datasets", self._layout)

    def start(self):

        selections = None

        while True:

            event, values = self.read(timeout=100)

            if event in [
                psg.WIN_CLOSED,
                "Ok",
            ]:

                selections = values

                break

            self._review_control_state()

        self.close()

        selected_options = None

        if selections:

            if self[CHK_ALL].Get():

                selected_option = selections[CMB_OPTIONS]

                selected_options = {
                    dataset_name: selected_option
                    for dataset_name in self._dataset_names
                }

            else:

                selected_options = {
                    dataset_name: selections[dataset_name]
                    for dataset_name in self._dataset_names
                }

            if any([option is not None for option in selected_options.values()]):

                return selected_options

    def _review_control_state(self):
        """Enables/Disables controls based on current user input.
        """

        frame_visible = not self[CHK_ALL].Get()

        self[FRM_DATASETS].Update(visible=frame_visible)
