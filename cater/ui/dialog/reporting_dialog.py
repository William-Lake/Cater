import PySimpleGUI as psg
import pandas as pd

from cater.ui.layout.reporting_dialog_layout import ReportingDialogLayout
from cater.managers.input_manager import InputManager
from cater.ui.controls.reporting_dialog_controls import (
    LB_DATASETS,
    BTN_DATACOMPY_REPORT,
    BTN_PANDAS_PROFILING_REPORT,
    LB_PLANNED_REPORTS,
    BTN_REMOVE_REPORT,
    BTN_GENERATE_REPORTS,
    BTN_CANCEL,
)


class ReportingDialog(psg.Window):
    """A dialog for generating reports.

    :param psg: The parent Window.
    :type psg: PySimpleGUI.Window
    """

    def __init__(self, datasets):
        """Constructor

        :param datasets: The current datasets.
        :type datasets: list
        """

        self._datasets = datasets

        self._planned_reports = {
            BTN_DATACOMPY_REPORT: {},
            BTN_PANDAS_PROFILING_REPORT: {},
        }

        super().__init__("Reporting", ReportingDialogLayout(datasets))

    def start(self):
        """Starts the UI event loop.

        :return: The mapping of report types and associated data for report generation.
        :rtype: dict
        """

        while True:

            event, values = self.read(timeout=100)

            if event in [
                psg.WIN_CLOSED,
                BTN_CANCEL,
                BTN_GENERATE_REPORTS,
            ]:

                break

            elif event == BTN_PANDAS_PROFILING_REPORT:

                selected_datasets = self._get_listbox_values(LB_DATASETS)

                current_planned_reports = self._get_listbox_values(LB_PLANNED_REPORTS)

                for selected_dataset in selected_datasets:

                    planned_report = f"PP : {selected_dataset}"

                    current_planned_reports.append(planned_report)

                    self._planned_reports[BTN_PANDAS_PROFILING_REPORT][
                        planned_report
                    ] = {"df": self._datasets[selected_dataset]}

                self[LB_PLANNED_REPORTS].Update(current_planned_reports)

            elif event == BTN_DATACOMPY_REPORT:

                selected_datasets = self._get_listbox_values(LB_DATASETS)

                current_planned_reports = self[LB_PLANNED_REPORTS].GetListValues()

                df_paths = list(
                    dict(
                        filter(
                            lambda dataset_entry: dataset_entry[0] in selected_datasets,
                            self._datasets.items(),
                        )
                    ).values()
                )

                common_columns = list(
                    set(pd.read_feather(df_paths[0]).columns)
                    & set(pd.read_feather(df_paths[1]))
                )

                join_columns = InputManager.get_user_selections(*common_columns)

                if not join_columns:

                    join_columns = common_columns

                planned_report = f'DC : {", ".join(selected_datasets)}'

                current_planned_reports.append(planned_report)

                self._planned_reports[BTN_DATACOMPY_REPORT][planned_report] = {
                    "dfs": [
                        self._datasets[selected_dataset]
                        for selected_dataset in selected_datasets
                    ],
                    "join_columns": join_columns,
                }

                self[LB_PLANNED_REPORTS].Update(current_planned_reports)

            elif event == BTN_REMOVE_REPORT:

                selected_reports = self._get_listbox_values(LB_PLANNED_REPORTS)

                planned_reports = self[LB_PLANNED_REPORTS].GetListValues()

                for selected_report in selected_reports:

                    for report_type in [
                        BTN_PANDAS_PROFILING_REPORT,
                        BTN_DATACOMPY_REPORT,
                    ]:

                        if selected_report in self._planned_reports[report_type].keys():

                            del self._planned_reports[report_type][selected_report]

                    planned_reports.remove(selected_report)

                self[LB_PLANNED_REPORTS].Update(planned_reports)

            self._review_control_state()

        self.close()

        return {
            report_type: list(report_data.values())
            for report_type, report_data in self._planned_reports.items()
        }

    def _review_control_state(self):
        """Enables/Disables controls based on current user input.
        """

        num_datasets_selected = len(self[LB_DATASETS].GetIndexes())

        num_datasets_to_remove = len(self[LB_PLANNED_REPORTS].GetIndexes())

        target_button_is_disabled_dict = {
            BTN_PANDAS_PROFILING_REPORT: num_datasets_selected == 0,
            BTN_DATACOMPY_REPORT: num_datasets_selected != 2,
            BTN_REMOVE_REPORT: num_datasets_to_remove == 0,
        }

        for button_key, is_disabled in target_button_is_disabled_dict.items():

            self[button_key].Update(disabled=is_disabled)

    def _get_listbox_values(self, listbox_key):
        """Returns the current data in the listbox with the given key.

        :param listbox_key: The key to use when gathering the listbox.
        :type listbox_key: str
        :return: The selected values in the listbox.
        :rtype: list
        """

        selection_indexes = self[listbox_key].GetIndexes()

        dataset_names = list(self[listbox_key].GetListValues())

        return [dataset_names[dataset_index] for dataset_index in selection_indexes]
