import PySimpleGUI as psg

from ui.controls.app_ui_controls import *


class AppUILayout(list):
    """The layout for the AppUI.
    """

    def __init__(self):
        """Constructor

        Builds the UI.
        """

        self.extend(
            [
                [MainMenuBar()],
                [
                    psg.Column(layout=[[QueryFrame()], [DatasetFrame()]],),
                    psg.Column(
                        layout=[[ResultsFrame()]],
                        scrollable=True,
                        size=(500, 302),
                        key=COL,
                    ),
                ],
                [psg.HorizontalSeparator(pad=(0, 5))],
                [
                    psg.StatusBar(
                        "Load a Workspace, or add a Dataset to begin.", key=STATUS_BAR
                    )
                ],
            ]
        )
