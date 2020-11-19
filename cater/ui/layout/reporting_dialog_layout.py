import PySimpleGUI as psg

from cater.ui.controls.reporting_dialog_controls import *


class ReportingDialogLayout(list):
    """The layout for the ReportingDialog.
    """

    def __init__(self, datasets):
        """Constructor, creates the layout.

        :param datasets: The datasets to use when creating the layout.
        :type datasets: dict
        """

        self.extend(
            [
                [
                    psg.Frame(
                        "Report Types",
                        layout=[
                            [
                                DatasetListbox(list(datasets.keys())),
                                psg.vtop(
                                    psg.Column(
                                        layout=[
                                            [psg.Button(BTN_PANDAS_PROFILING_REPORT)],
                                            [psg.Button(BTN_DATACOMPY_REPORT)],
                                        ]
                                    )
                                ),
                            ]
                        ],
                    )
                ],
                [
                    psg.Frame(
                        "Planned Reports",
                        layout=[
                            [
                                PlannedReportsListbox(),
                                psg.vtop(psg.Button(BTN_REMOVE_REPORT)),
                            ]
                        ],
                    )
                ],
                [psg.Button(BTN_GENERATE_REPORTS), psg.Button(BTN_CANCEL)],
            ]
        )
