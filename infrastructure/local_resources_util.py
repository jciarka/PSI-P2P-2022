from os import listdir
from os.path import isfile, join, getmtime


class LocalResourcesUtil:
    @staticmethod
    def get(path):
        resources = [{"name": file,
                      "modified": getmtime(path + '/' + file)}
                     for file in listdir(path)
                     if isfile(join(path, file))]

        return resources
