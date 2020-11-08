import PySimpleGUI as psg


class AppUILayout(list):

    BTN_GO = "BTN_GO"

    LB_DATASETS = "LB_DATASETS"

    ML_SQL = "ML_SQL"
    ML_RSLT = "ML_RSLT"

    COL = "COL"

    EXIT = "EXIT"

    SAVE_WORKSPACE = "Save..."
    LOAD_WORKSPACE = "Load..."
    ADD_DATASET = "Add..."
    REMOVE_DATASET = "Remove..."
    EXPORT_DATASET = "Export..."

    DATACOMPY_REPORT = "Datacompy..."
    PANDAS_PROFILING_REPORT = "Pandas Profiling..."

    def __init__(self):

        """
        bottom
            frame
                multiline - results
        """

        menu = psg.MenuBar(
            background_color="#CCCCCC",
            menu_definition=[
                ["File", [self.EXIT]],
                ["Workspace", [self.SAVE_WORKSPACE, self.LOAD_WORKSPACE]],
                [
                    "Dataset",
                    [
                        self.ADD_DATASET,
                        self.EXPORT_DATASET,
                        self.REMOVE_DATASET,
                        "Reporting",
                        [self.DATACOMPY_REPORT, self.PANDAS_PROFILING_REPORT],
                    ],
                ],
            ],
        )

        self.append([menu])

        dataset_container = psg.Listbox(
            [],
            key=self.LB_DATASETS,
            size=(62, 10),
            background_color="#FCC7EB",
            text_color="#96433B",
        )

        dataset_frame = psg.Frame(
            "Datasets",
            layout=[[dataset_container]],
        )

        sql_entry = psg.Multiline(
            key=self.ML_SQL,
            size=(62, 10),
            background_color="#E0FBFC",
            text_color="#4A6C96",
        )

        sql_submit = psg.Button(
            "EXECUTE",
            key=self.BTN_GO,
            button_color=("#404040", "#8AC926"),
        )

        query_frame = psg.Frame(
            "SQL Query",
            layout=[
                [sql_entry],
                [sql_submit],
            ],
        )

        self.append([psg.vtop(dataset_frame), query_frame])

        results_container = psg.Multiline(
            background_color="#FCF5C7",
            text_color="#7168B0",
            font=["Courier New", 10],
            key=self.ML_RSLT,
            auto_refresh=True,
            size=(750, 350),
            auto_size_text=True,
        )

        scrollable_column = psg.Column(
            layout=[[results_container]],
            scrollable=True,
            size=(900, 350),
            key=self.COL,
        )

        self.append([scrollable_column])
