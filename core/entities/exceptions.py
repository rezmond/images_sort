class SorterError(Exception):
    ''''''


class FolderValidationError(SorterError):
    def __init__(self, name, path=None):
        super().__init__()
        self._name = name
        self._path = path


class NoArgumentPassedError(FolderValidationError):

    def __str__(self):
        return (
            'The "{0}" folder\'s path has not been set.'
            ' Please set the "{0}" folder path and try again.'
            .format(self._name))


class RelativeFolderPathError(FolderValidationError):
    def __str__(self):
        return (
            f'The "{self._name}" folder path should be absolute,'
            f' but got "{self._path}"')


class FolderNotFoundError(FolderValidationError):
    def __str__(self):
        return f'The "{self._path}" folder does not exist'
