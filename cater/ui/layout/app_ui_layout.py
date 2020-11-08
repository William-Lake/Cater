import PySimpleGUI as psg


class AppUILayout(list):

    EXECUTE = "EXECUTE"

    LB_DATASETS = "LB_DATASETS"

    ML_SQL = "ML_SQL"
    ML_RSLT = "ML_RSLT"

    COL = "COL"

    EXIT = "EXIT"

    SAVE_WORKSPACE = "Save..."
    LOAD_WORKSPACE = "Load..."
    ADD_DATASET = "Add Dataset(s)"
    REMOVE_DATASET = "Remove Dataset"
    EXPORT_DATASET = "Export Dataset(s)"
    ADD_RESULTS_TO_DATASETS = 'Add Results to Datasets'

    REPORTING = 'Reporting...'
    DATACOMPY_REPORT = "Datacompy..."
    PANDAS_PROFILING_REPORT = "Pandas Profiling..."

    def __init__(self):

        '''
        column
            sql frame
            dataset frame
        column
            results
        '''

        menu = psg.MenuBar(
            background_color="#CCCCCC",
            menu_definition=[
                ["File", [self.EXIT]],
                ["Workspace", [self.SAVE_WORKSPACE, self.LOAD_WORKSPACE]],
            ],
        )

        self.append([menu])


        sql_entry = psg.Multiline(
            key=self.ML_SQL,
            size=(54, 10),
            background_color="#E0FBFC",
            text_color="#4A6C96",
            enable_events=True
        )

        sql_submit = psg.Button(
            "EXECUTE",
            button_color=("#404040", "#8AC926"),
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
            background_color="#FCC7EB",
            text_color="#96433B",
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED
        )

        dataset_buttons = [
            [psg.Button(self.ADD_DATASET,button_color=('#404040','#E0FBFC'))],
            [psg.Button(self.ADD_RESULTS_TO_DATASETS,button_color=('#404040','#FF8552'),disabled=True)],
            [psg.Button(self.REMOVE_DATASET,button_color=('#E0FBFC','#1982C4'),disabled=True)],
            [psg.Button(self.EXPORT_DATASET,button_color=('#404040','#FFCA3A'),disabled=True)],
            [psg.Button(self.REPORTING,button_color=('#E0FBFC','#BD8B9C'),disabled=True)]
        ]

        ds_button_column = psg.Column(layout = dataset_buttons)

        dataset_frame = psg.Frame(
            "Datasets",
            layout=[[dataset_container,ds_button_column]],
        )

        left_column = psg.Column(            
            layout=[[query_frame],[dataset_frame]],
        )

        results_frame = psg.Frame('Results',layout=[[psg.Multiline(
            background_color="#FCF5C7",
            text_color="#7168B0",
            font=["Courier New", 10],
            key=self.ML_RSLT,
            auto_refresh=True,
            size=(500, 302),
            auto_size_text=True,
            disabled=True
        )]])

        right_column = psg.Column(
            layout=[[results_frame]],
            scrollable=True,
            size=(500, 302),
            key=self.COL,
        )

        status_bar = psg.StatusBar('Load a Workspace, or add a Dataset to begin.',text_color='#FFCA3A')

        self.append([left_column, right_column])

        self.append([psg.HorizontalSeparator(pad=(0,5))])

        self.append([status_bar])
