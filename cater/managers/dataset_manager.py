from datetime import datetime
import os
from pathlib import Path
import shutil
import traceback

import pandas as pd
from pyarrow.lib import ArrowIOError


class DatasetManager(dict):
    """Manages datasets.
    """

    _DEFAULT_SAVE_DIR = "datasets"

    def __init__(self):
        """Constructor
        """

        # TODO .sql files?
        self._file_ext_read_funcs = {
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

    def load_datasets(self, workspace_path, *dataset_paths):
        """Loads the given datasets from the target workspace.
        """

        for dataset_path in dataset_paths:

            dataset_name = self._determine_dataset_name(dataset_path)

            # If the dataset is already in the workspace, no need to load it.
            if dataset_path.parent != workspace_path:

                read_func = self._file_ext_read_funcs[dataset_path.suffix]

                # TODO try/except
                # TODO Address different params each read method allows.

                try:

                    df = read_func(dataset_path.as_posix())

                except Exception as e:

                    # TODO The user should be made aware of this.
                    traceback.print_exc()

                    continue

                # workspace_path is tempfile.Temporary_Directory which is why we have to turn it into a Path object before using .joinpath.
                # E.g. /path/data.csv --> /workspace/data.feather
                new_file_path = Path(workspace_path.name).joinpath(
                    dataset_path.with_suffix(".feather").name
                )

                df.to_feather(new_file_path)

                dataset_path = new_file_path

            self[dataset_name] = dataset_path

    def _determine_dataset_name(self, dataset_path):
        """Determines the best dataset name for the given dataset.

        :param dataset_path: The path the dataset exists at.
        :type dataset_path: pathlib.Path
        :return: The best name for the given dataset.
        :rtype: str
        """

        dataset_name = dataset_path.stem.upper()

        # If there's already a dataset saved with the target name,
        # we'll want to add a suffix to it so we can tell them apart
        # when querying.
        if dataset_name in self.keys():

            suffix = 2

            while f"{dataset_name}{suffix}" in self.keys():

                suffix += 1

            dataset_name = f"{dataset_name}{suffix}"

        return dataset_name

    def validate_dataset_paths(self,*dataset_paths):

        return {
            dataset_path:dataset_path.suffix in self._file_ext_read_funcs.keys()
            for dataset_path
            in dataset_paths
        }

    def remove_datasets(self, selected_datasets):
        """Removes the given datasets from the manager.

        :param selected_datasets: The datasets to remove.
        :type selected_datasets: list
        """

        for dataset_name in selected_datasets:

            dataset_path = self[dataset_name]

            # Not sure how the dataset would go missing
            # (barring the user manually deleting it,)
            # but airing on the side of caution.
            dataset_path.unlink(missing_ok=True)

            del self[dataset_name]

    def export_datasets(self, *datasets):
        """Saves the given datasets to a custom dataset directory.

        This differs from exporting a workspace because an exported
        workspace includes all the datasets, while this exports a
        subset.
        """

        dir_name = self._DEFAULT_SAVE_DIR

        if Path(dir_name).exists():

            timestamp = datetime.now().timestamp().__str__()

            dir_name = f"{dir_name}_{timestamp}"

        save_dir = Path(dir_name)

        save_dir.mkdir()

        for dataset_name in datasets:

            dataset_path = self[dataset_name]

            # TODO cater.py should determine how the user wants to save the files.
            # E.g. if they want .feather files they should be able to specify that,
            # rather than defaulting to .csv.

            dataset_save_path = save_dir.joinpath(dataset_path.with_suffix(".csv").name)

            try:

                pd.read_feather(dataset_path).to_csv(dataset_save_path, index=False)

            except ArrowIOError as e:

                # TODO log this.
                traceback.print_exc()

