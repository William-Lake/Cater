from pathlib import Path
from threading import Thread

import pandas as pd
import PySimpleGUI as psg
from tabulate import tabulate
import sqlparse
from pandasql import sqldf

from ui.app_ui import AppUI
from ui.layout.app_ui_layout import AppUILayout
from managers.dataset_manager import DatasetManager
from managers.workspace_manager import WorkspaceManager
from managers.input_manager import InputManager
from ui.reporting_dialog import ReportingDialog
from managers.config_manager import ConfigManager
from report_generator import ReportGenerator


class Cater:
    """Directs traffic between backend and frontend."""

    def __init__(self):
        """Constructor"""

        # TODO Before exiting, if the user has datasets in their workspace
        # warn they'll be lost and ask if they'd like to save them first.

        # TODO Right click menu option in the dataset listbox to get a
        # dataset summary.

        self._create_resources()

        self._callback_dict = {
            AppUILayout.BTN_EXECUTE: self._execute_query,
            AppUILayout.MNU_SAVE_WORKSPACE: self._save_workspace,
            AppUILayout.MNU_LOAD_WORKSPACE: self._load_workspace,
            AppUILayout.BTN_ADD_DATASET: self._add_dataset,
            AppUILayout.BTN_ADD_RESULTS_TO_DATASETS: self._add_results_as_dataset,
            AppUILayout.BTN_REMOVE_DATASET: self._remove_dataset,
            AppUILayout.BTN_EXPORT_DATASET: self._export_dataset,
            AppUILayout.BTN_REPORTING: self._generate_report,
        }

        self._app_ui = AppUI(self._callback_dict)

        self._current_results_df = None

    def _generate_report(self):
        """Generates dataset reports.
        """

        report_data = ReportingDialog(self._dataset_manager).start()

        self._report_generator.generate_reports(**report_data)

    def _execute_query(self):
        """Executes the query provided by the user against the datasets specified in their query.
        """

        query = self._app_ui[AppUILayout.ML_SQL].Get()

        if query:

            self._app_ui[AppUILayout.ML_SQL].Update(
                sqlparse.format(query, reindent=True)
            )

            dfs = {
                df_name: pd.read_feather(df_path)
                for df_name, df_path in self._dataset_manager.items()
                if df_name in query
            }

            result = sqldf(query, dfs)

            self._app_ui[AppUILayout.ML_RSLT].Update(
                tabulate(result, headers="keys", tablefmt="fancy_grid", showindex=False)
            )

            self._current_results_df = result

    def _save_workspace(self):
        """Saves the current workspace.
        """

        if not self._workspace_manager.is_empty():

            filepath = InputManager.get_filepath_input(
                message="Select Workspace", save_as=True
            )

            if filepath:

                self._workspace_manager.save_workspace(filepath)

    def _load_workspace(self):
        """Replaces the current workspace with another.
        """

        workspace_path = InputManager.get_filepath_input(message="Select Workspace",file_types=(('Cater Workspaces','*.cater'),))

        if workspace_path:

            if not self._workspace_manager.is_empty():

                if (
                    InputManager.get_user_confirmation(
                        prompt="It looks like there's already a workspace- would you like to save it before continuing?"
                    )
                    == InputManager.YES
                ):

                    self._save_workspace()

            self._create_resources()

            self._app_ui.reset()

            self._workspace_manager.load_workspace(workspace_path)

            # Is there any reason to believe rglob would be necessary here?
            # I would only think it was if the user manually went in and changed the workspace
            # while cater was running, but how likely is that?
            self._load_datasets(*list(self._workspace_manager.get_workspace_path().glob("*.feather")))

    def _add_dataset(self):
        """Adds a dataset.
        """

        file_paths = InputManager.get_filepath_input(
            message="Select dataset(s)", multiple_files=True
        )

        # if not empty and not None
        if file_paths:

            self._load_datasets(*file_paths)

    def _add_results_as_dataset(self):
        """Adds the current sql results as a dataset.
        """

        if self._current_results_df is not None:

            dataset_name = InputManager.get_user_text_input("Dataset Name?")

            while dataset_name in self._dataset_manager.keys():

                dataset_name = InputManager.get_user_text_input(
                    "That dataset name is already being used. Please use another."
                )

            if dataset_name is not None:

                dataset_path = self._workspace_manager.get_workspace_path().joinpath(f"{dataset_name}.feather")

                self._current_results_df.to_feather(dataset_path)

                self._dataset_manager[dataset_name] = dataset_path

                self._app_ui[AppUILayout.LB_DATASETS].Update(
                    self._dataset_manager.keys()
                )

    def _load_datasets(self, *dataset_paths):
        """Loads the provided dataset paths to the datasets.
        """

        # This all seems very messy.

        dataset_validation = self._dataset_manager.validate_dataset_paths(*dataset_paths)

        if all(dataset_validation.values()):

            datasets_to_load = dataset_paths

        elif any(dataset_validation.values()):

            if InputManager.get_user_confirmation('It looks like some of the datasets aren\'t valid formats. Would you like to continue with just the valid ones?') == InputManager.YES:

                datasets_to_load = [
                    dataset_path
                    for dataset_path,is_valid
                    in dataset_validation.items()
                    if is_valid
                ]

            else:

                datasets_to_load = None

        else:

            datasets_to_load = None

        if datasets_to_load is not None:

            self._dataset_manager.load_datasets(
                self._workspace_manager.get_workspace_path(), *datasets_to_load
            )

            self._app_ui.update_datasets(self._dataset_manager.keys())

    def _remove_dataset(self):
        """Removes selected datasets.
        """

        selection_indexes = self._app_ui[AppUILayout.LB_DATASETS].GetIndexes()

        if selection_indexes:

            dataset_names = list(self._app_ui[AppUILayout.LB_DATASETS].GetListValues())

            selected_datasets = [
                dataset_names[dataset_index] for dataset_index in selection_indexes
            ]

            if (
                InputManager.get_user_confirmation(
                    f'Really remove the following {len(selected_datasets)} datasets? {", ".join(selected_datasets)}'
                )
                == InputManager.YES
            ):

                self._dataset_manager.remove_datasets(selected_datasets)

                self._app_ui.update_datasets(self._dataset_manager.keys())

    def _export_dataset(self):
        """Exports selected datasets.
        """

        """
        give user popup with list of options
        get file type from user
        get save path from user
        save dataset
        """
        selection_indexes = self._app_ui[AppUILayout.LB_DATASETS].GetIndexes()

        if selection_indexes:

            dataset_names = list(self._app_ui[AppUILayout.LB_DATASETS].GetListValues())

            selected_datasets = [
                dataset_names[dataset_index] for dataset_index in selection_indexes
            ]

            if len(selected_datasets) == len(self._dataset_manager.keys()):

                self._save_workspace()

            else:

                self._dataset_manager.export_datasets(*selected_datasets)

    def _generate_datacompy_report(self):
        """Generates a Datacompy report.

        :return: The path to the report data directory.
        :rtype: pathlib.Path
        """

        """
        if number of datasets < 2
            tell the user this isn't possible
        else
            use popup to get a selection of 2 datasets from user
            generate the datacompy report
            return the dir the report is located in
        """

        selected_datasets = InputManager.get_user_selections(
            self._dataset_manager.keys(), limit=2
        )

        if selected_datasets:

            selected_datasets = dict(
                filter(
                    lambda dataset_entry: dataset_entry[0] in selected_datasets,
                    self._dataset_manager.items(),
                )
            )

            return self._report_generator.generate_datacompy_report(selected_datasets)

    def _generate_pandas_profiling_report(self):
        """Generates a Pandas-Profiling report.

        :return: The path to the generated report.
        :rtype: pathlib.Path
        """

        """
        if number of datasets < 1
            tell the user this isn't possible
        else
            use popup to get a selection of 2 datasets from user
            gather the file save path from the user
            generate the pandas profiling report
            return the name of the report
        """

        selected_dataset = InputManager.get_user_selections(
            self._dataset_manager.keys()
        )

        if selected_dataset:

            save_path = InputManager.get_filepath_input(
                message="Save Pandas Profiling Report as...", save_as=True
            )

            # TODO Should the user be alerted that their report wont be generated if they dont provide a save path?
            if save_path:

                return self._report_generator.generate_pandas_profiling_report(
                    save_path, self._dataset_manager.get_datesets(selected_dataset)
                )

    def _create_resources(self):
        """Creates the Cater resources.
        """

        self._dataset_manager = DatasetManager()

        self._workspace_manager = WorkspaceManager()

        self._report_generator = ReportGenerator()

        ConfigManager().clear_config()

    def start(self):
        """Starts the app."""

        self._app_ui.start()

        if not self._workspace_manager.is_empty() and InputManager.get_user_confirmation(
                        prompt="It looks like your workspace isn't empty- would you like to save it before exiting?"
                    ) == InputManager.YES:

            self._save_workspace()
