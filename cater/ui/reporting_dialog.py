import PySimpleGUI as psg

from ui.layout.reporting_dialog_layout import ReportingDialogLayout


class ReportingDialog(psg.Window):

    def __init__(self,datasets):

        self._planned_reports = {
            ReportingDialogLayout.DATACOMPY_REPORT : {},
            ReportingDialogLayout.PANDAS_PROFILING_REPORT : {}
        }

        super().__init__("Reporting", ReportingDialogLayout(datasets))

    def start(self):

        while True:

            event, values = self.read(timeout=100)

            if event in [psg.WIN_CLOSED, ReportingDialogLayout.CANCEL, ReportingDialogLayout.GENERATE_REPORTS]:

                break

            elif event == ReportingDialogLayout.PANDAS_PROFILING_REPORT:

                selected_datasets = self._get_listbox_values(ReportingDialogLayout.LB_DATASETS)

                current_planned_reports = self._get_listbox_values(ReportingDialogLayout.LB_PLANNED_REPORTS)

                for selected_dataset in selected_datasets:

                    planned_report = f'PP : {selected_dataset}'

                    current_planned_reports.append(planned_report)

                    self._planned_reports[ReportingDialogLayout.PANDAS_PROFILING_REPORT][planned_report] = selected_dataset

                self[ReportingDialogLayout.LB_PLANNED_REPORTS].Update(current_planned_reports)

            elif event == ReportingDialogLayout.DATACOMPY_REPORT:

                selected_datasets = self._get_listbox_values(ReportingDialogLayout.LB_DATASETS)

                current_planned_reports = self[ReportingDialogLayout.LB_PLANNED_REPORTS].GetListValues()

                planned_report = f'DC : {", ".join(selected_datasets)}'

                current_planned_reports.append(planned_report)

                self._planned_reports[ReportingDialogLayout.DATACOMPY_REPORT][planned_report] = selected_datasets

                self[ReportingDialogLayout.LB_PLANNED_REPORTS].Update(current_planned_reports)

            elif event == ReportingDialogLayout.REMOVE_REPORT:

                selected_reports = self._get_listbox_values(ReportingDialogLayout.LB_PLANNED_REPORTS)

                planned_reports = self[ReportingDialogLayout.LB_PLANNED_REPORTS].GetListValues()

                for selected_report in selected_reports:

                    for report_type in [ReportingDialogLayout.PANDAS_PROFILING_REPORT, ReportingDialogLayout.DATACOMPY_REPORT]:

                        if selected_report in self._planned_reports[report_type].keys():

                            del self._planned_reports[report_type][selected_report]

                    planned_reports.remove(selected_report)

                self[ReportingDialogLayout.LB_PLANNED_REPORTS].Update(planned_reports)                

            self._review_control_state()

        self.close()

        return {
            report_type:list(report_data.values())
            for report_type, report_data
            in self._planned_reports.items()
        }

    def _review_control_state(self):

        num_datasets_selected = len(self[ReportingDialogLayout.LB_DATASETS].GetIndexes())

        num_datasets_to_remove = len(self[ReportingDialogLayout.LB_PLANNED_REPORTS].GetIndexes())

        target_button_is_disabled_dict = {
            ReportingDialogLayout.PANDAS_PROFILING_REPORT: num_datasets_selected == 0,
            ReportingDialogLayout.DATACOMPY_REPORT: num_datasets_selected != 2,
            ReportingDialogLayout.REMOVE_REPORT: num_datasets_to_remove == 0
        }

        for button_key, is_disabled in target_button_is_disabled_dict.items():

            self[button_key].Update(disabled=is_disabled)

    def _get_listbox_values(self,listbox_key):

        selection_indexes = self[listbox_key].GetIndexes()

        dataset_names = list(self[listbox_key].GetListValues())

        return [
            dataset_names[dataset_index] for dataset_index in selection_indexes
        ]         
