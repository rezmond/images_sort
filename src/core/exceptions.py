class SorterError(Exception):
    ''''''


class FolderValidationError(SorterError):
    def __init__(self, name, path=None):
        super().__init__()
        self._name = name
        self._path = path


class RelativeFolderPathError(FolderValidationError):
    def __str__(self):
        return (
            f'The "{self._name}" folder path should be absolute,'
            f' but got "{self._path}"')


class FolderNotFoundError(FolderValidationError):
    def __str__(self):
        return f'The "{self._path}" {self._name} folder does not exist'
