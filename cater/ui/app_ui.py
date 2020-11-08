import PySimpleGUI as psg

from ui.layout.app_ui_layout import AppUILayout


class AppUI(psg.Window):
    def __init__(self, cater_callback_dict):

        psg.ChangeLookAndFeel("Dark")

        psg.SetOptions(
            element_padding=(0, 0), button_element_size=(15, 1), auto_size_buttons=False
        )

        super().__init__(title="Cater", layout=AppUILayout())

        self._control_action_dict = cater_callback_dict

    def start(self):

        while True:

            (event, values) = self.read(timeout=100)

            if event == AppUILayout.EXIT or event == psg.WIN_CLOSED:

                break  # exit button clicked

            elif event in self._control_action_dict.keys():

                self._control_action_dict[event]()

            self._review_control_state()

        self.close()

    def _review_control_state(self):

        # Is there a better way to do this?
        is_empty = lambda val: val is None or len(val) == 0 or (isinstance(val,str) and len(val.strip()) == 0)

        theres_no_datasets = is_empty(self[AppUILayout.LB_DATASETS].GetIndexes())

        theres_no_results = is_empty(self[AppUILayout.ML_RSLT].Get())

        target_button_is_disabled_dict = {
            AppUILayout.REMOVE_DATASET : theres_no_datasets,
            AppUILayout.EXPORT_DATASET : theres_no_datasets,
            AppUILayout.REPORTING : theres_no_datasets,
            AppUILayout.ADD_RESULTS_TO_DATASETS : theres_no_results
        }

        for button_key, is_disabled in target_button_is_disabled_dict.items():

            self[button_key].Update(disabled=is_disabled)

    def reset(self):

        self[AppUILayout.LB_DATASETS].Update([])

        self[AppUILayout.ML_SQL].Update()

        self[AppUILayout.ML_RSLT].Update()

    def update_datasets(self, dataset_names):

        self[AppUILayout.LB_DATASETS].Update(dataset_names)
