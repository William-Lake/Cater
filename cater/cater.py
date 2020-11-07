from pathlib import Path
from threading import Thread

import pandas as pd
import PySimpleGUI as psg
import fleep

from ui.app_ui import AppUI
from ui.layout.app_ui_layout import AppUILayout
from doers.report_generator import ReportGenerator
from doers.query_executor import QueryExecutor
from managers.dataset_manager import DatasetManager
from managers.workspace_manager import WorkspaceManager
from managers.input_manager import InputManager


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
            AppUILayout.BTN_GO:self._execute_query,
            AppUILayout.SAVE_WORKSPACE:self._save_workspace,
            AppUILayout.LOAD_WORKSPACE:self._load_workspace,
            AppUILayout.ADD_DATASET:self._add_dataset,
            AppUILayout.REMOVE_DATASET:self._remove_dataset,
            AppUILayout.EXPORT_DATASET:self._export_dataset,
            AppUILayout.DATACOMPY_REPORT:self._generate_datacompy_report,
            AppUILayout.PANDAS_PROFILING_REPORT:self._generate_pandas_profiling_report
        }

        self._app_ui = AppUI(self._callback_dict)

    def _execute_query(self):

        query = self._app_ui[AppUILayout.ML_SQL].Get()

        dfs = {
            df_name:pd.read_feather(df_path)
            for df_name,df_path
            in self._dataset_manager.get_datasets().items()
            if df_name in query
        }

        return self._query_executor.execute_query_against_dfs(query=query,dfs=dfs)

    def _save_workspace(self):

        if not self._workspace_manager.is_empty():

            filepath = self._input_manager.get_filepath_input()

            # TODO Validation

            if filepath:
                
                self._workspace_manager.save_workspace(filepath)

    def _load_workspace(self):

        # TODO In the future workspace files wont be dirs.
        workspace_path = self._input_manager.get_filepath_input(is_directory=True)

        if workspace_path:

            if not self._workspace_manager.is_empty():

                if self._input_manager.get_user_confirmation(prompt='It looks like there\'s already a workspace- would you like to save it before continuing?'):

                    self._save_workspace()

            self._create_resources()

            self._app_ui.reset()

            self._workspace_manager.load_workspace(workspace_path)

            # Is there any reason to believe rglob would be necessary here?
            # I would only think it was if the user manually went in and changed the workspace
            # while cater was running, but how likely is that?
            self._load_datasets(workspace_path.glob('*.feather'))

            

    def _add_dataset(self):

        '''
        Gather file paths from user
        determine file type
        determine method for loading df
        if method can be determined
            load file into df
            save df to tmp dir
            add df to local dict
            add df name to ui listbox
        else
            alert the user they can't use that thing as a datasource
        '''

        file_paths = self._input_manager.get_filepath_input(multiple_files=True)

        # if not empty and not None
        if file_paths:

            self._load_datasets(*file_paths)

    def _load_datasets(self,*dataset_paths):

        '''
        TODO
        Determine whether the dataset paths are supported file types.
        If any aren't, ask the user if they want to continue.
        If only some aren't and the user wants to continue-
            go on without the problematic ones.
        If all aren't and the user wants to continue-
            alert the user and abandon.

        dataset_manager.file_ext_read_funcs is public, and its keys are the supported file extensions.
        '''

        self._dataset_manager.load_datasets(self._workspace_manager.get_workspace_path(),*dataset_paths)

        self._app_ui.update_datasets(self._dataset_manager.get_dataset_names())        

    def _remove_dataset(self):

        '''
        give user pop up with list of options
        get user selections for which to remove
        for each selection
            remove from local dict
            remove from tmp dir
        '''
        selected_datasets = self._input_manager.get_user_selections(self._dataset_manager.get_dataset_names())

        if selected_datasets:

            self._dataset_manager.remove_datasets(selected_datasets)

            self._app_ui.update_datasets(self._dataset_manager.get_dataset_names()) 

    def _export_dataset(self):

        '''
        give user popup with list of options
        get file type from user
        get save path from user
        save dataset
        '''
        selected_datasets = self._input_manager.get_user_selections(self._dataset_manager.get_dataset_names())

        if selected_datasets:

            self._dataset_manager.export_datasets(selected_datasets)
                    

    def _generate_datacompy_report(self):

        '''
        if number of datasets < 2
            tell the user this isn't possible
        else
            use popup to get a selection of 2 datasets from user
            generate the datacompy report
            return the dir the report is located in
        '''

        selected_datasets = self._input_manager.get_user_selections(self._dataset_manager.get_dataset_names(),limit=2)

        if selected_datasets:

            return self._report_generator.generate_datacompy_report(self._dataset_manager.get_datasets(selected_datasets))

    def _generate_pandas_profiling_report(self):

        '''
        if number of datasets < 1
            tell the user this isn't possible
        else
            use popup to get a selection of 2 datasets from user
            gather the file save path from the user
            generate the pandas profiling report
            return the name of the report
        '''

        selected_dataset = self._input_manager.get_user_selections(self._dataset_manager.get_dataset_names(),limit=1)

        if selected_dataset:

            save_path = self._input_manager.get_filepath_input(save_as=True)

            # TODO Should the user be alerted that their report wont be generated if they dont provide a save path?
            if save_path:

                return self._report_generator.generate_pandas_profiling_report(save_path,self._dataset_manager.get_datesets(selected_dataset))

    def _create_resources(self):

        self._dataset_manager = DatasetManager()

        self._workspace_manager = WorkspaceManager()

        self._input_manager = InputManager()

        self._report_generator = ReportGenerator()

        self._query_executor = QueryExecutor()          

    def start(self):
        """Starts the app."""

        self._app_ui.start()

    def process_request(self, event, values):

        try:

            return self._callback_dict[event]()

        except Exception as e:

            return e