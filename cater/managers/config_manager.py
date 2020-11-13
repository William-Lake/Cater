import dataset
import json
import pandas as pd

from managers.singleton import Singleton

class ConfigManager(metaclass=Singleton):
    """Manages Cater Configuration.
    """

    def __init__(self):
        """Constructor
        """

        self._db = dataset.connect('sqlite:///:memory:')

    def save_data(self,table_name,**kwargs):
        """Saves the given data to the given table.

        :param table_name: The table to save the data to.
        :type table_name: str
        """

        table = self._db[table_name]

        table.insert(kwargs)

        self._db.commit()

    def get_data(self,table_name,**kwargs):
        """Gathers some data from the given table.

        :param table_name: The table to gather the data from.
        :type table_name: str
        :return: The gathered data.
        :rtype: dict
        """

        table = self._db[table_name]

        return table.find(**kwargs)

    def delete_data(self,table_name,**kwargs):
        """Deletes some or all of the data from the target table.

        :param table_name: The table to delete the data from.
        :type table_name: str
        """

        table = self._db[table_name]

        table.delete(**kwargs)

    def get_all_data(self,table_name):
        """Returns all data in the target table.

        :param table_name: The table to gather data from.
        :type table_name: str
        :return: The table data.
        :rtype: dict
        """

        return self._db[table_name].all()

    def export_config(self,export_loc):
        """Exports the current configuration to the target location as .json files.

        :param export_loc: The location to export the data to.
        :type export_loc: pathlib.Path
        """

        for table_name in self._db.tables:

            table = list(self._db[table_name].all())

            with open(export_loc.joinpath(f'{table_name}.json'),'w+') as out_file:

                out_file.write(json.dumps(table,indent=4))

    def import_config(self,import_loc):
        """Clears the current configuration and imports the configuration in the target location.

        :param import_loc: The location of the configuration files.
        :type import_loc: pathlib.Path
        """

        self.clear_config()

        for config_file in import_loc.glob('*.json'):

            json_data = json.loads(open(config_file).read())

            table_name = config_file.stem

            for row in json_data:

                del row['id']

                self.save_data(table_name,**row)

    def clear_config(self):
        """Clears out the in-memory configuration database.
        """

        for table_name in self._db.tables:

            self._db[table_name].drop()       
