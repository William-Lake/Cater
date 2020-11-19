import PySimpleGUI as psg

from cater.ui.controls.summary_dialog_controls import *


class SummaryDialogLayout(list):
    """The layout for the SummaryDialog.
    """

    def __init__(self, dataset_name, summary_data):

        summary_items = []

        max_width = None

        total_height = 0

        for title, data in summary_data.items():

            width = len(data.splitlines()[0])

            height = len(data.splitlines())

            total_height += height

            if max_width is None or width > max_width:
                max_width = width

            summary_items.append([DataFrame(title, DataMultiLine(data, width, height))])

            summary_items.append([psg.HorizontalSeparator(pad=(5, 5))])

        self.extend(
            [
                [psg.Text(f"Summary for {dataset_name}")],
                [
                    psg.Column(
                        layout=[*summary_items],
                        scrollable=True,
                        size=(
                            max_width * 6.25,
                            (total_height + len(summary_items) * 5) * 7,
                        ),
                    )
                ],
                [scrollable_column],
                [psg.Button("Ok")],
            ]
        )
