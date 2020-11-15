import PySimpleGUI as psg
import pandas as pd

from ui.layout.export_dataset_dialog_layout import ExportDatasetDialogLayout
from managers.input_manager import InputManager


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
                ExportDatasetDialogLayout.BTN_OK,
            ]:

                selections = values

                break

            self._review_control_state()

        self.close()

        selected_options = None

        if self[ExportDatasetDialogLayout.CHK_ALL]:

            selected_option = selections[ExportDatasetDialogLayout.CMB_OPTIONS]

            selected_options = {
                dataset_name: selected_option for dataset_name in self._dataset_names
            }

        else:

            selected_options = {
                dataset_name: selections[dataset_name]
                for dataset_name in self._dataset_names
            }

        print(selected_options)

        if all(selected_options.values()):

            return selected_options

    def _review_control_state(self):
        """Enables/Disables controls based on current user input.
        """

        frame_visible = not self[ExportDatasetDialogLayout.CHK_ALL].Get()

        self[ExportDatasetDialogLayout.FRM_DATASETS].Update(visible=frame_visible)
