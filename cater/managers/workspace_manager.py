import os
import shutil
from pathlib import Path

from tempfile import TemporaryDirectory


class WorkspaceManager:
    """Manages workspaces.
    """

    def __init__(self):
        """Constructor
        """

        self._tmp_dir = TemporaryDirectory()

    def save_workspace(self, save_location):
        """Saves the current workspace to the given location.

        :param save_location: The location to save the workspace to.
        :type save_location: pathlib.Path
        """

        shutil.copytree(self._tmp_dir, save_location)

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

        # TODO In the future the workspace should be a .cater file
        # so change the extension to .zip, unzip, remove the .zip file,
        # then load.

        shutil.copytree(workspace_path, self._tmp_dir.name, dirs_exist_ok=True)

    def get_workspace_path(self):
        """Returns the current workspace path.

        :return: The current workspace path.
        :rtype: pathlib.Path
        """

        return self._tmp_dir

    def save_workspace(self, workspace_path):
        """Exports the current workspace.

        :param workspace_path: The path the workspace should be exported to.
        :type workspace_path: pathlib.Path
        """

        # TODO .zip this up after copying, then change the extension to .cater

        shutil.copytree(self._tmp_dir.name, workspace_path)
