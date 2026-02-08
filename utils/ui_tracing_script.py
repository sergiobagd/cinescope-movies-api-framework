from pathlib import Path
from datetime import datetime


class Tools:
    @staticmethod
    def project_dir():
        """
        Returns root dir of the project
        Let's imagine that current file is in inner directory 'common
        """
        return Path(__file__).parent.parent

    @staticmethod
    def files_dir(nested_directory: str = None, filename: str = None):
        """
        Returns path to dir 'files' (or its inner dir).
        If dir doesn't exist, it will be created
        If 'filename' is specified, returns full path to file
        """
        files_path = Tools.project_dir() / "files"
        if nested_directory:
            files_path = files_path / nested_directory
        files_path.mkdir(parents=True, exist_ok=True)

        if filename:
            return files_path / filename
        return files_path

    @staticmethod
    def get_timestamp():
        """
        Returns current time mark in format YYYY-MM-DD_HH-MM-SS
        """
        return datetime.now().strftime("%Y-%m-%d_%H-%M-$S")
