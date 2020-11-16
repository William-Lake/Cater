import PySimpleGUI as psg


FRM_DATASETS = "Datasets"


class DatasetFrame(psg.Frame):
    def __init__(self, dataset_names, export_options):

        dataset_options = [
            [psg.Text(dataset_name), psg.Combo(export_options, key=dataset_name),]
            for dataset_name in dataset_names
        ]

        super().__init__(
            FRM_DATASETS,
            key=FRM_DATASETS,
            layout=dataset_options,
            visible=False,
        )


CMB_OPTIONS = "CMB_OPTIONS"


class OptionsCombo(psg.Combo):
    def __init__(self, export_options):

        super().__init__(export_options, key=CMB_OPTIONS)


CHK_ALL = "Apply to all datasets"


class ApplyToAllCheckbox(psg.Check):
    def __init__(self):

        super().__init__(CHK_ALL, key=CHK_ALL, default=True)
