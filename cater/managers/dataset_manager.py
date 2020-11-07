from datetime import datetime
import os
from pathlib import Path
import shutil

import pandas as pd


class DatasetManager:

    _DEFAULT_SAVE_DIR = "datasets"

    def __init__(self):

        self._datasets = {}

        # TODO .sql files?
        self.file_ext_read_funcs = {
            ".feather": pd.read_feather,
            ".csv": pd.read_csv,
            ".json": pd.read_json,
            ".html": pd.read_html,
            ".xls": pd.read_excel,
            ".xlsx": pd.read_excel,
            ".hdf": pd.read_hdf,
            ".parquet": pd.read_parquet,
            ".dta": pd.read_stata,
            ".pkl": pd.read_pickle,
            ".pickle": pd.read_pickle,
        }

    def get_datasets(self, dataset_keys=None):

        # If they didn't specify, then give them everything.
        if dataset_keys is None:

            return self._datasets

        else:

            return dict(
                filter(
                    lambda dataset_entry: dataset_entry[0] in dataset_keys,
                    self._datasets.items(),
                )
            )

    def load_datasets(self, workspace_path, *dataset_paths):

        for dataset_path in dataset_paths:

            dataset_name = self._determine_dataset_name(dataset_path)

            # If the dataset is already in the workspace, no need to load it.
            if dataset_path.parent != workspace_path:

                read_func = self.file_ext_read_funcs(dataset.suffix)

                # TODO try/except
                # TODO Address different params each read method allows.

                df = read_func(dataset_path)

                # E.g. /path/data.csv --> /workspace/data.feather
                new_file_path = workspace_path.joinpath(
                    dataset_path.withsuffix(".feather")
                )

                df.to_feather(new_file_path)

            self._datasets[dataset_name] = dataset_path

    def _determine_dataset_name(self, dataset_path):

        dataset_name = dataset_path.stem

        # If there's already a dataset saved with the target name,
        # we'll want to add a suffix to it so we can tell them apart
        # when querying.
        if dataset_name in self._datasets.keys():

            suffix = 2

            while f"{dataset_name}{suffix}" in self._datasets.keys():

                suffix += 1

            dataset_name = f"{dataset_name}{suffix}"

        return dataset_name

    def remove_datasets(self, selected_datasets):

        for dataset_name in selected_datasets:

            # TODO cater.py should be checking this. Is this even possible?
            if dataset_name in self._datasets.keys():

                dataset_path = self._datasets[dataset_name]

                # Not sure how the dataset would go missing
                # (barring the user manually deleting it,)
                # but airing on the side of caution.
                dataset_path.unlink(missing_ok=True)

                del self._datasets[dataset]

    def get_dataset_names(self):

        return list(self._datasets.keys())

    def export_datasets(self, datasets):

        dir_name = self._DEFAULT_SAVE_DIR

        if Path(dir_name).exists():

            timestamp = datetime.now().timestamp().__str__()

            dir_name = f"{dir_name}_{timestamp}"

        save_dir = Path(dir_name)

        save_dir.mkdir()

        # TODO cater.py should probably ensure all these still exist
        # before trying to interact with them,
        # just to be safe.
        for dataset_name in datasets:

            dataset_path = self._datasets[dataset_name]

            # TODO cater.py should determine how the user wants to save the files.
            # E.g. if they want .feather files they should be able to specify that,
            # rather than defaulting to .csv.

            dataset_save_path = save_dir.joinpath(dataset_path.withsuffix(".csv"))

            shutil.copy(dataset_path, dataset_save_path)
