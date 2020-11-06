from datetime import datetime
import os
from pathlib import Path
import shutil

class DatasetManager:

    def __init__(self):

        self._datasets = {}

    def get_datasets(self,dataset_keys=None):

        if dataset_keys is None:

            return self._datasets
        
        else:

            return {
                key:dataset
                for key, dataset
                in self._datasets.items()
                if key in dataset_keys
            }

    def load_datasets(self,workspace_path,*dataset_paths):

        # TODO Determine how to load the dataset based on the filetype

        for dataset_path in dataset_paths:

            if Path(dataset_path).parent == Path(workspace_path).parent and 

            dataset_name = Path(dataset_path).stem

            count = 0

            while dataset_name in self._datasets.keys():

                count += 1

                if count == 1:

                    dataset_name = '.'.join(dataset_name.split('.')[:-1])

                dataset_name = f'{dataset_name}.{count}'

            df = pd.read_csv(dataset_path)

            

            self._datasets[dataset_name] = dataset_path

    def remove_datasets(self,selected_datasets):

        for dataset in selected_datasets:

            if dataset in self._datasets.keys():

                del self._datasets[dataset]

    def get_dataset_names(self):

        return list(self._datasets.keys())

    def export_datasets(self,datasets):

        dir_name = 'datasets'

        if os.path.exists(dir_name):

            timestamp = datetime.now().timestamp()

            dir_name = f'datasets_{timestamp}'

        os.mkdir(dir_name)

        for dataset in datasets:

            shutil.copy(self._datasets[dataset],os.path.join(dir_name,Path(self._datasets[dataset]).name))