import PySimpleGUI as psg

###########################

BTN_DATACOMPY_REPORT = "Datacompy"
BTN_PANDAS_PROFILING_REPORT = "Pandas Profiling"
BTN_REMOVE_REPORT = "Remove"
BTN_GENERATE_REPORTS = "Generate Reports"
BTN_CANCEL = "Cancel"

###########################


LB_DATASETS = "LB_DATASETS"


class DatasetListbox(psg.Listbox):
    def __init__(self, dataset_names):

        super().__init__(
            dataset_names,
            key=LB_DATASETS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
        )


LB_PLANNED_REPORTS = "LB_PLANNED_REPORTS"


class PlannedReportsListbox(psg.Listbox):
    def __init__(self):

        super().__init__(
            [],
            key=LB_PLANNED_REPORTS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
        )
