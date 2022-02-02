import logging
import json

class FileUtils:
    """Class handling writing dicts to disk"""
    def __init__(self, path):
        self.path = path

    def read_dict(self):
        """Reads file at self.path, returns dict"""
        try:
            with open(self.path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError as err:
            logging.warning("File not found at %s", self.path)
            raise err

        return data

    def write_dict(self, data):
        """Writes contents of data to file at self.path"""
        try:
            with open(self.path, 'w') as file:
                json.dump(data, file)
        except OSError as err:
            logging.critical("Unable to write to disk:%s", err)
            raise err
