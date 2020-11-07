import PySimpleGUI as psg

from ui.layout.app_ui_layout import AppUILayout


class AppUI(psg.Window):
    def __init__(self, cater_callback_dict):

        psg.ChangeLookAndFeel("Dark")

        psg.SetOptions(
            element_padding=(0, 0), button_element_size=(20, 1), auto_size_buttons=False
        )

        super().__init__(title="Cater", layout=AppUILayout())

        self._control_action_dict = cater_callback_dict

    def start(self):

        while True:

            (event, value) = self.read()

            if event == AppUILayout.EXIT or event == psg.WIN_CLOSED:

                break  # exit button clicked

            elif event != "__TIMEOUT__" and event in self._control_action_dict.keys():

                self._control_action_dict[event]()

        self.close()

    def set_control_visibility(self, is_visible, *control_keys):

        for control_key in control_keys:

            self[control_key].Update(visible=is_visible)

    def set_control_disability(self, is_disabled, *control_keys):

        for control_key in control_keys:

            self[control_key].Update(disabled=is_disabled)

    def reset(self):

        self[AppUILayout.LB_DATASETS].Update([])

        self[AppUILayout.ML_SQL].Update()

        self[AppUILayout.ML_RSLT].Update()

    def update_datasets(self, dataset_names):

        self[AppUILayout.LB_DATASETS].Update(dataset_names)
