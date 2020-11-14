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
            AppUILayout.F5_KEY: self._execute_query,
            AppUILayout.MNU_SAVE_WORKSPACE: self._save_workspace,
            AppUILayout.MNU_LOAD_WORKSPACE: self._load_workspace,
            AppUILayout.BTN_ADD_DATASET: self._add_dataset,
            AppUILayout.BTN_ADD_RESULTS_TO_DATASETS: self._add_results_as_dataset,
            AppUILayout.BTN_REMOVE_DATASET: self._remove_dataset,
            AppUILayout.BTN_EXPORT_DATASET: self._export_dataset,
            AppUILayout.BTN_REPORTING: self._generate_report,
        }

        self._app_ui = AppUI(self._callback_dict)

        self._update_status_callback = None

        self._current_results_df = None

        self._unsaved_changes = False

    def _update_status(self, message):

        if self._update_status_callback is None:

            self._update_status_callback = self._app_ui[AppUILayout.STATUS_BAR].Update

        self._update_status_callback(message)

    def _generate_report(self):
        """Generates dataset reports.
        """

        self._update_status("Generating reports...")

        report_data = ReportingDialog(self._dataset_manager).start()

        self._report_generator.generate_reports(self._update_status, **report_data)

        self._update_status("Done")

    def _execute_query(self):
        """Executes the query provided by the user against the datasets specified in their query.
        """

        self._update_status("Executing Query...")

        query = self._app_ui[AppUILayout.ML_SQL].Get()

        if query:

            query = sqlparse.format(query, reindent=True, keyword_case="upper")

            self._app_ui[AppUILayout.ML_SQL].Update(query)

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

            self._update_status("Done")

        else:

            self._update_status("No query to execute!")

    def _save_workspace(self):
        """Saves the current workspace.
        """

        self._update_status("Saving Workspace...")

        if not self._workspace_manager.is_empty():

            filepath = InputManager.get_filepath_input(
                message="Select Workspace", save_as=True
            )

            if filepath:

                self._workspace_manager.save_workspace(filepath)

                self._update_status("Workspace Saved.")

                self._unsaved_changes = False

            else:

                self._update_status("No filepath provided to save workspace to!")

        else:

            self._update_status("No files in workspace to save!")

    def _load_workspace(self):
        """Replaces the current workspace with another.
        """

        self._update_status("Loading Workspace...")

        workspace_path = InputManager.get_filepath_input(
            message="Select Workspace", file_types=(("Cater Workspaces", "*.cater"),)
        )

        if workspace_path:

            if not self._workspace_manager.is_empty():

                if InputManager.get_user_confirmation(
                    prompt="It looks like there's already a workspace- would you like to save it before continuing?"
                ):

                    self._save_workspace()

            self._create_resources()

            self._app_ui.reset()

            self._workspace_manager.load_workspace(workspace_path)

            # Is there any reason to believe rglob would be necessary here?
            # I would only think it was if the user manually went in and changed the workspace
            # while cater was running, but how likely is that?
            self._load_datasets(
                *list(self._workspace_manager.get_workspace_path().glob("*.feather"))
            )

            self._unsaved_changes = False

            self._update_status("Done")

        else:

            self._update_status("No workspace path provided to load from!")

    def _add_dataset(self):
        """Adds a dataset.
        """

        self._update_status("Adding dataset...")

        file_paths = InputManager.get_filepath_input(
            message="Select dataset(s)", multiple_files=True
        )

        # if not empty and not None
        if file_paths:

            self._load_datasets(*file_paths)

            self._unsaved_changes = True

            self._update_status("Done")

        else:

            self._update_status("No dataset paths provided to add to workspace!")

    def _add_results_as_dataset(self):
        """Adds the current sql results as a dataset.
        """

        self._update_status("Adding results as dataset...")

        if self._current_results_df is not None:

            dataset_name = InputManager.get_user_text_input("Dataset Name?")

            if dataset_name is not None:

                while dataset_name in self._dataset_manager.keys():

                    dataset_name = InputManager.get_user_text_input(
                        "That dataset name is already being used. Please try another."
                    )

                    if dataset_name is None:

                        self._update_status("Cancelled")

                        return

                dataset_path = self._workspace_manager.get_workspace_path().joinpath(
                    f"{dataset_name}.feather"
                )

                self._current_results_df.to_feather(dataset_path)

                self._dataset_manager[dataset_name] = dataset_path

                self._app_ui[AppUILayout.LB_DATASETS].Update(
                    self._dataset_manager.keys()
                )

                self._unsaved_changes = True

                self._update_status("Done")

            else:

                self._update_status("No dataset name provided, dataset not added!")

        else:

            self._update_status("No query results to add to datasets!")

    def _load_datasets(self, *dataset_paths):
        """Loads the provided dataset paths to the datasets.
        """

        self._update_status("Loading Datasets...")

        # This all seems very messy.

        self._update_status("Validating dataset paths...")

        dataset_validation = self._dataset_manager.validate_dataset_paths(
            *dataset_paths
        )

        if all(dataset_validation.values()):

            datasets_to_load = dataset_paths

            self._update_status("Dataset paths valid.")

        elif any(dataset_validation.values()):

            self._update_status("Some dataset paths invalid!")

            if InputManager.get_user_confirmation(
                "It looks like some of the datasets aren't valid formats. Would you like to continue with just the valid ones?"
            ):

                datasets_to_load = [
                    dataset_path
                    for dataset_path, is_valid in dataset_validation.items()
                    if is_valid
                ]

            else:

                datasets_to_load = None

        else:

            self._update_status("All dataset paths invalid!")

            datasets_to_load = None

        if datasets_to_load is not None:

            self._dataset_manager.load_datasets(
                self._update_status,
                self._workspace_manager.get_workspace_path(),
                *datasets_to_load,
            )

            self._app_ui.update_datasets(self._dataset_manager.keys())

            self._unsaved_changes = True

            self._update_status("Done")

    def _remove_dataset(self):
        """Removes selected datasets.
        """

        self._update_status("Removing Datasets...")

        selection_indexes = self._app_ui[AppUILayout.LB_DATASETS].GetIndexes()

        if selection_indexes:

            dataset_names = list(self._app_ui[AppUILayout.LB_DATASETS].GetListValues())

            selected_datasets = [
                dataset_names[dataset_index] for dataset_index in selection_indexes
            ]

            if InputManager.get_user_confirmation(
                f'Really remove the following {len(selected_datasets)} datasets? {", ".join(selected_datasets)}'
            ):

                self._dataset_manager.remove_datasets(
                    self._update_status, selected_datasets
                )

                self._app_ui.update_datasets(self._dataset_manager.keys())

                self._unsaved_changes = True

            else:

                self._update_status("Cancelled")

        else:

            self._update_status("No datasets selected for removal!")

    def _export_dataset(self):
        """Exports selected datasets.
        """

        """
        give user popup with list of options
        get file type from user
        get save path from user
        save dataset
        """
        self._update_status("Exporting dataset(s)...")

        selection_indexes = self._app_ui[AppUILayout.LB_DATASETS].GetIndexes()

        if selection_indexes:

            dataset_names = list(self._app_ui[AppUILayout.LB_DATASETS].GetListValues())

            selected_datasets = [
                dataset_names[dataset_index] for dataset_index in selection_indexes
            ]

            if len(selected_datasets) == len(self._dataset_manager.keys()):

                self._save_workspace()

            else:

                self._dataset_manager.export_datasets(
                    self._update_status, *selected_datasets
                )

        else:

            self._update_status("No datasets selected for export!")

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

        if not self._workspace_manager.is_empty() and self._unsaved_changes and InputManager.get_user_confirmation(
            prompt="It looks like your workspace isn't empty- would you like to save it before exiting?"
        ):

            self._save_workspace()
