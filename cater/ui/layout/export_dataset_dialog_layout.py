import PySimpleGUI as psg

from ui.controls.export_dataset_dialog_controls import *


class ExportDatasetDialogLayout(list):
    """The layout for the ExportDatasetDialog.
    """

    def __init__(self, dataset_names, export_options):

        frm_datasets = psg.pin(DatasetFrame(dataset_names, export_options))

        self.extend(
            [
                [OptionsCombo(export_options), ApplyToAllCheckbox()],
                [frm_datasets],
                [psg.Button("Ok")],
            ]
        )
