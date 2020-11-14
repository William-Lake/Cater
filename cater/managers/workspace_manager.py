import os
import shutil
from pathlib import Path
from zipfile import ZipFile

from tempfile import TemporaryDirectory


class WorkspaceManager:
    """Manages workspaces.
    """

    def __init__(self):
        """Constructor
        """

        self._tmp_dir = TemporaryDirectory()

    def save_workspace(self, save_location):
        """Saves the current workspace to the given location as an archive.

        :param save_location: The location to save the workspace to.
        :type save_location: pathlib.Path
        """

        zip_path = save_location.with_suffix(".cater")

        with ZipFile(zip_path, "w") as out_zip:

            for file_path in self.get_workspace_path().iterdir():

                out_zip.write(file_path, arcname=file_path.name)

    def is_empty(self):
        """Determines whether the current workspace is empty.

        :return: True if the workspace is empty.
        :rtype: bool
        """

        dir_is_empty = True

        for item in Path(self._tmp_dir.name).iterdir():

            dir_is_empty = False

            break

        return dir_is_empty

    def load_workspace(self, workspace_path):
        """Replaces the current workspace with the one at the target location.

        :param workspace_path: The workspace to load.
        :type workspace_path: pathlib.Path
        """

        # Replacing the previous workspace with a new one.
        self._tmp_dir = TemporaryDirectory()

        with ZipFile(workspace_path, "r") as in_zip:

            in_zip.extractall(path=Path(self._tmp_dir.name))

        print(list(Path(self._tmp_dir.name).glob("*")))

    def get_workspace_path(self):
        """Returns the current workspace path.

        :return: The current workspace path.
        :rtype: pathlib.Path
        """

        return Path(self._tmp_dir.name)
