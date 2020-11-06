import os
import shutil

from tempfile import TemporaryDirectory


class WorkspaceManager:

    def __init__(self):

        self._tmp_dir = TemporaryDirectory()

    def save_workspace(self,save_location):

        shutil.copytree(self._tmp_dir,save_location)

    def is_empty(self):

        return len(os.listdir(self._tmp_dir)) == 0

    def load_workspace(self,workspace_path):

        self._tmp_dir = Path(TemporaryDirectory())

        shutil.copytree(workspace_path,self._tmp_dir)

    def get_workspace_path(self):

        return self._tmp_dir

    def save_workspace(self,workspace_path):

        shutil.copytree(self._tmp_dir,workspace_path)