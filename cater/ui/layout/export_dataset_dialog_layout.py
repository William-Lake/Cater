import PySimpleGUI as psg


class ExportDatasetDialogLayout(list):
    """The layout for the ExportDatasetDialog.
    """

    CMB_OPTIONS = "CMB_OPTIONS"
    CHK_ALL = "Use for all datasets"
    FRM_DATASETS = "Datasets"
    BTN_OK = "Ok"

    def __init__(self, dataset_names, export_options):

        cmb_options = psg.Combo(export_options, key=self.CMB_OPTIONS)

        chk_all = psg.Check(self.CHK_ALL, key=self.CHK_ALL, default=True)

        self.dataset_options = {
            dataset_name: [
                psg.Text(dataset_name),
                psg.Combo(export_options, key=dataset_name),
            ]
            for dataset_name in dataset_names
        }

        frm_datasets = psg.pin(
            psg.Frame(
                self.FRM_DATASETS,
                key=self.FRM_DATASETS,
                layout=list(self.dataset_options.values()),
                visible=False,
            )
        )

        btn_ok = psg.Button(self.BTN_OK)

        self.extend([[cmb_options, chk_all], [frm_datasets], [btn_ok]])
