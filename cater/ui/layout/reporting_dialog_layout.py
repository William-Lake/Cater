import PySimpleGUI as psg


class ReportingDialogLayout(list):

    LB_DATASETS = "LB_DATASETS"
    LB_PLANNED_REPORTS = "LB_PLANNED_REPORTS"
    DATACOMPY_REPORT = "Datacompy"
    PANDAS_PROFILING_REPORT = "Pandas Profiling"
    REMOVE_REPORT = "Remove"

    GENERATE_REPORTS = "Generate Reports"
    CANCEL = "Cancel"

    def __init__(self, datasets):

        """
        frame - report types
            dataset_container
            column
                report buttons
        frame - planned reports
            planned reports
            vtop
                button - remove

        """

        dataset_container = psg.Listbox(
            list(datasets.keys()),
            key=self.LB_DATASETS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
        )

        dataset_buttons = [
            [
                psg.Button(
                    self.PANDAS_PROFILING_REPORT
                )
            ],
            [psg.Button(self.DATACOMPY_REPORT)],
        ]

        dataset_buttons_column = psg.vtop(psg.Column(layout=dataset_buttons))

        report_type_frame = psg.Frame(
            "Report Types", layout=[[dataset_container, dataset_buttons_column]]
        )

        self.append([report_type_frame])

        planned_reports = psg.Listbox(
            [],
            key=self.LB_PLANNED_REPORTS,
            size=(35, 10),
            select_mode=psg.LISTBOX_SELECT_MODE_EXTENDED,
        )

        remove_report = psg.vtop(psg.Button(self.REMOVE_REPORT))

        planned_reports_frame = psg.Frame(
            "Planned Reports", layout=[[planned_reports, remove_report]]
        )

        self.append([planned_reports_frame])

        self.append([psg.Button(self.GENERATE_REPORTS), psg.Button(self.CANCEL)])
