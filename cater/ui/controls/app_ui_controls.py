import PySimpleGUI as psg

##################################

COL = "COL"
STATUS_BAR = "STATUS_BAR"

#################################


MNU_SAVE_WORKSPACE = "Save..."
MNU_LOAD_WORKSPACE = "Load..."
MNU_EXIT = "EXIT"


class MainMenuBar(psg.MenuBar):
    def __init__(self):

        super().__init__(
            menu_definition=[
                ["File", [MNU_EXIT]],
                ["Workspace", [MNU_SAVE_WORKSPACE, MNU_LOAD_WORKSPACE]],
            ],
        )


ML_SQL = "ML_SQL"
BTN_EXECUTE = "EXECUTE"
F5_KEY = "F5:71"


class QueryFrame(psg.Frame):
    def __init__(self):

        sql_entry = psg.Multiline(key=ML_SQL, size=(54, 10), enable_events=True,)

        sql_submit = psg.Button(BTN_EXECUTE, disabled=True)

        super().__init__(
            "SQL Query", layout=[[sql_entry], [sql_submit],],
        )


LB_DATASETS = "LB_DATASETS"
MNU_SUMMARIZE = "Summarize"
MNU_RENAME = "Rename"
BTN_ADD_DATASET = "Add Dataset(s)"
BTN_REMOVE_DATASET = "Remove Dataset"
BTN_EXPORT_DATASET = "Export Dataset(s)"
BTN_ADD_RESULTS_TO_DATASETS = "Add Results to Datasets"
BTN_REPORTING = "Reporting..."


class DatasetFrame(psg.Frame):
    def __init__(self):

        dataset_container = psg.Listbox(
            [],
            key=LB_DATASETS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
            right_click_menu=["&Right", [MNU_SUMMARIZE, MNU_RENAME]],
        )

        dataset_buttons = [
            [psg.Button(BTN_ADD_DATASET)],
            [psg.Button(BTN_ADD_RESULTS_TO_DATASETS, disabled=True,)],
            [psg.Button(BTN_REMOVE_DATASET, disabled=True,)],
            [psg.Button(BTN_EXPORT_DATASET, disabled=True,)],
            [psg.Button(BTN_REPORTING, disabled=True)],
        ]

        ds_button_column = psg.Column(layout=dataset_buttons)

        super().__init__(
            "Datasets", layout=[[dataset_container, ds_button_column]],
        )


ML_RSLT = "ML_RSLT"


class ResultsFrame(psg.Frame):
    def __init__(self):

        super().__init__(
            "Results",
            layout=[
                [
                    psg.Multiline(
                        font=["Courier New", 8],
                        key=ML_RSLT,
                        auto_refresh=True,
                        size=(500, 302),
                        auto_size_text=True,
                        disabled=True,
                    )
                ]
            ],
        )
