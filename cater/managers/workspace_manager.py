import os
import shutil

from tempfile import TemporaryDirectory


class WorkspaceManager:

    def __init__(self):

        self._tmp_dir = TemporaryDirectory()

    def save_workspace(self,save_location):

        shutil.copytree(self._tmp_dir,save_location)

    def is_empty(self):

        dir_is_empty = True

        for item in Path(self._tmp_dir).iterdir():

            dir_is_empty = False

            break

        return dir_is_empty

    def load_workspace(self,workspace_path):

        # Replacing the previous workspace with a new one.
        self._tmp_dir = TemporaryDirectory()

        # TODO In the future the workspace should be a .cater file
        # so change the extension to .zip, unzip, remove the .zip file,
        # then load.

        shutil.copytree(workspace_path,self._tmp_dir)

    def get_workspace_path(self):

        return self._tmp_dir

    def save_workspace(self,workspace_path):

        # TODO .zip this up after copying, then change the extension to .cater

        shutil.copytree(self._tmp_dir,workspace_path)