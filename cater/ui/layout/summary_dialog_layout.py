import PySimpleGUI as psg


class SummaryDialogLayout(list):
    """The layout for the SummaryDialog.
    """

    BTN_OK = "Ok"

    def __init__(self, dataset_name, summary_data):

        self.append([psg.Text(f'Summary for {dataset_name}')])

        summary_items = []
        
        max_width = None

        total_height = 0

        for title, data in summary_data.items():

            width = len(data.splitlines()[0])

            height = len(data.splitlines())

            total_height += height

            if max_width is None or width > max_width: max_width = width

            summary_items.append([psg.Frame(
                title,
                layout=[
                    [
                        psg.Multiline(
                            data,
                            font=["Courier New", 8],
                            auto_refresh=True,
                            size=(width, height),
                            auto_size_text=True,
                            disabled=True,
                        )
                    ]
                ],
            )        ])    

            summary_items.append([psg.HorizontalSeparator(pad=(5,5))])

        scrollable_column = psg.Column(
            layout=[*summary_items], scrollable=True, size=(max_width * 6.25, (total_height + len(summary_items) * 5) * 7),
        )

        self.append([scrollable_column])

        self.append([psg.Button(self.BTN_OK)])