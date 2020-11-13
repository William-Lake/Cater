import dataset
import json
import pandas as pd

from managers.singleton import Singleton

class ConfigManager(metaclass=Singleton):

    def __init__(self):

        self._db = dataset.connect('sqlite:///:memory:')

    def __del__(self):

        del self._db

    def save_data(self,table_name,**kwargs):

        table = self._db[table_name]

        table.insert(kwargs)

        self._db.commit()

    def get_data(self,table_name,**kwargs):

        table = self._db[table_name]

        return table.find(**kwargs)

    def delete_data(self,table_name,**kwargs):

        table = self._db[table_name]

        table.delete(**kwargs)

    def get_all_data(self,table_name):

        return self._db[table_name].all()

    def export_config(self,export_loc):

        for table_name in self._db.tables:

            table = list(self._db[table_name].all())

            with open(export_loc.joinpath(f'{table_name}.json'),'w+') as out_file:

                out_file.write(json.dumps(table,indent=4))

    def import_config(self,import_loc):

        self.clear_config()

        for config_file in import_loc.glob('*.json'):

            json_data = json.loads(open(config_file).read())

            table_name = config_file.stem

            for row in json_data:

                del row['id']

                self.save_data(table_name,**row)

    def clear_config(self):

        for table_name in self._db.tables:

            self._db[table_name].delete()        
