import dataset
import pandas as pd

from managers.singleton import Singleton

class ConfigManager(metaclass=Singleton):

    def __init__(self):

        self._db = dataset.connect('sqlite:///:memory:')

    def save_info(self,table_name,**kwargs):

        table = self._db[table_name]

        table.insert(kwargs)

    def get_info(self,table_name):

        # TODO
        return list(self._db[table_name].all())

    def save(self,save_loc):

        for table in self._db.tables:

            table = self._db[table]

            df_data = {column:[] for column in table.columns}

            for record in table:

                for column in table.columns:

                    df_data[column].append(record[column])

            pd.DataFrame(df_data).to_feather(save_loc.joinpath(f'{table}.config'))

    def load(self,load_loc):

        for config_df in load_loc.glob('*.config'):

            df = pd.read_feather(config_df)

            table_name = config_df.stem

            for idx,row in df.iterrows():

                self.save_info(table_name,**row.to_dict())