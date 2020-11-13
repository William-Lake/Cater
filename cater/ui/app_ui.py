import PySimpleGUI as psg

from ui.layout.app_ui_layout import AppUILayout
from ui.cater_palette import THEME


class AppUI(psg.Window):
    """The primary UI for Cater.

    :param psg: The parent Window class.
    :type psg: PySimpleGUI.Window
    """

    def __init__(self, cater_callback_dict):
        """Constructor

        :param cater_callback_dict: The mapping of control keys to cater callbacks.
        :type cater_callback_dict: dict
        """

        self._set_theme()

        psg.SetOptions(
            element_padding=(0, 0), button_element_size=(15, 1), auto_size_buttons=False
        )

        super().__init__(title="Cater", layout=AppUILayout())

        self._control_action_dict = cater_callback_dict

    def _set_theme(self):
        """Sets the color theme.
        """

        psg.LOOK_AND_FEEL_TABLE["Cater"] = THEME

        psg.theme("Cater")

    def start(self):
        """Start the Cater UI event loop.
        """

        while True:

            (event, values) = self.read(timeout=100)

            if event == AppUILayout.MNU_EXIT or event == psg.WIN_CLOSED:

                break  # exit button clicked

            elif event in self._control_action_dict.keys():

                self._control_action_dict[event]()

            self._review_control_state()

        self.close()

    def _review_control_state(self):
        """Disables/Enables controls based on current user input.
        """

        # Is there a better way to do this?
        is_empty = (
            lambda val: val is None
            or len(val) == 0
            or (isinstance(val, str) and len(val.strip()) == 0)
        )

        theres_no_datasets = is_empty(self[AppUILayout.LB_DATASETS].GetListValues())

        theres_no_datasets_selected = is_empty(
            self[AppUILayout.LB_DATASETS].GetIndexes()
        )

        theres_no_results = is_empty(self[AppUILayout.ML_RSLT].Get())

        target_button_is_disabled_dict = {
            AppUILayout.BTN_REMOVE_DATASET: theres_no_datasets_selected,
            AppUILayout.BTN_EXPORT_DATASET: theres_no_datasets_selected,
            AppUILayout.BTN_REPORTING: theres_no_datasets,
            AppUILayout.BTN_ADD_RESULTS_TO_DATASETS: theres_no_results,
        }

        for button_key, is_disabled in target_button_is_disabled_dict.items():

            self[button_key].Update(disabled=is_disabled)

    def reset(self):
        """Clears all user input and resets the controls to their starting state.
        """

        self[AppUILayout.LB_DATASETS].Update([])

        self[AppUILayout.ML_SQL].Update()

        self[AppUILayout.ML_RSLT].Update()

    def update_datasets(self, dataset_names):
        """Adds the given datasets to the dataset listbox.

        :param dataset_names: The dataset names to add.
        :type dataset_names: list
        """

        self[AppUILayout.LB_DATASETS].Update(dataset_names)
