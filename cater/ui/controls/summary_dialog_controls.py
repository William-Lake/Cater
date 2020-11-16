import PySimpleGUI as psg


class DataMultiLine(psg.Multiline):
    def __init__(self, data, width, height):

        super().__init__(
            data,
            font=["Courier New", 8],
            auto_refresh=True,
            size=(width, height),
            auto_size_text=True,
            disabled=True,
        )


class DataFrame(psg.Frame):
    def __init__(self, title, ml_data):

        super().__init__(
            title, layout=[[ml_data]],
        )
