import PySimpleGUI as psg


class AppUILayout(list):

    MNU_SAVE_WORKSPACE = "Save..."
    MNU_LOAD_WORKSPACE = "Load..."
    MNU_EXIT = "EXIT"
    LB_DATASETS = "LB_DATASETS"
    ML_SQL = "ML_SQL"
    ML_RSLT = "ML_RSLT"
    COL = "COL"
    BTN_EXECUTE = "EXECUTE"
    BTN_ADD_DATASET = "Add Dataset(s)"
    BTN_REMOVE_DATASET = "Remove Dataset"
    BTN_EXPORT_DATASET = "Export Dataset(s)"
    BTN_ADD_RESULTS_TO_DATASETS = "Add Results to Datasets"
    BTN_REPORTING = "Reporting..."
    STATUS_BAR = 'STATUS_BAR'

    def __init__(self):

        menu = psg.MenuBar(
            menu_definition=[
                ["File", [self.MNU_EXIT]],
                ["Workspace", [self.MNU_SAVE_WORKSPACE, self.MNU_LOAD_WORKSPACE]],
            ],
        )

        self.append([menu])

        sql_entry = psg.Multiline(
            key=self.ML_SQL,
            size=(54, 10),
            enable_events=True,
        )

        sql_submit = psg.Button(
            self.BTN_EXECUTE,
        )

        query_frame = psg.Frame(
            "SQL Query",
            layout=[
                [sql_entry],
                [sql_submit],
            ],
        )

        dataset_container = psg.Listbox(
            [],
            key=self.LB_DATASETS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
        )

        dataset_buttons = [
            [psg.Button(self.BTN_ADD_DATASET)],
            [
                psg.Button(
                    self.BTN_ADD_RESULTS_TO_DATASETS,
                    disabled=True,
                )
            ],
            [
                psg.Button(
                    self.BTN_REMOVE_DATASET,
                    disabled=True,
                )
            ],
            [
                psg.Button(
                    self.BTN_EXPORT_DATASET,
                    disabled=True,
                )
            ],
            [
                psg.Button(
                    self.BTN_REPORTING, disabled=True
                )
            ],
        ]

        ds_button_column = psg.Column(layout=dataset_buttons)

        dataset_frame = psg.Frame(
            "Datasets",
            layout=[[dataset_container, ds_button_column]],
        )

        left_column = psg.Column(
            layout=[[query_frame], [dataset_frame]],
        )

        results_frame = psg.Frame(
            "Results",
            layout=[
                [
                    psg.Multiline(
                        font=["Courier New", 10],
                        key=self.ML_RSLT,
                        auto_refresh=True,
                        size=(500, 302),
                        auto_size_text=True,
                        disabled=True,
                    )
                ]
            ],
        )

        right_column = psg.Column(
            layout=[[results_frame]],
            scrollable=True,
            size=(500, 302),
            key=self.COL,
        )

        # TODO Updating StatusBar
        status_bar = psg.StatusBar(
            "Load a Workspace, or add a Dataset to begin.",
            key = self.STATUS_BAR
        )

        self.append([left_column, right_column])

        self.append([psg.HorizontalSeparator(pad=(0, 5))])

        self.append([status_bar])
