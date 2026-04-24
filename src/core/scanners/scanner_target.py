import os

from typeguard import typechecked

from libs.monads import Success
from src.core.fs import FolderExtractorBase, FsManipulatorBase
from src.core.scanners.base import TargetFolderScannerBase

MEDIA_EXTENSIONS = {
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
    '.bmp',
    '.tiff',
    '.webp',
    '.mp4',
    '.avi',
    '.mov',
    '.wmv',
    '.flv',
    '.webm',
    '.mkv',
    '.mpg',
}


class TargetFolderScanner(TargetFolderScannerBase):
    """
    Service to scan the target folder before file moving/copying operations
    to detect existing media files and prevent duplication.
    """

    _CHUNK_SIZE = 8192  # 8KB chunks for reading files (default)

    @typechecked
    def __init__(
        self, folder_extractor: FolderExtractorBase, fs_manipulator: FsManipulatorBase
    ):
        self._folder_extractor = folder_extractor
        self._fs_manipulator = fs_manipulator
        self._hash_cache = {}
        self._size_index = {}

    @typechecked
    def scan(self, folder: str) -> None:
        """
        Scan the target folder recursively for existing media files.
        For each media file found, add it to the size index for conflict detection.

        Args:
            folder (str): Target folder path to scan
        """
        media_file_paths = filter(
            self._is_media_file,
            self._folder_extractor.folder_to_file_pathes(folder),
        )

        for media_file_path in media_file_paths:
            self._add_file_size_index(media_file_path)

    @typechecked
    def _add_file_size_index(self, file_path: str) -> None:
        """
        Adds media file size to paths map for efficient size-based filtering.
        The index includes only files from the target folder.
        Files that cannot be accessed are skipped (handled in detect_conflicts).
        """
        size_result = self._fs_manipulator.getsize(file_path)
        match size_result:
            case Success(value):
                if value not in self._size_index:
                    self._size_index[value] = set()
                self._size_index[value].add(file_path)
            case _:
                # Skip files we cannot access to. Because we just can't obtain the size and can't work with that
                pass

    @typechecked
    def _is_media_file(self, file_path: str) -> bool:
        """
        Check if a file is a media file (image or video) based on extension.
        """

        _, ext = os.path.splitext(file_path.lower())
        return ext in MEDIA_EXTENSIONS

    @typechecked
    def detect_duplicates(self, src_file: str) -> bool:
        def detect_by_size(src_size: int) -> bool:
            same_size_files = self._size_index.get(src_size, None)
            if same_size_files is None:
                return False

            for same_size_file in same_size_files:
                if same_size_file != src_file and self._compare_files(
                    src_file, same_size_file
                ):
                    return True
            return False

        size_result = self._fs_manipulator.getsize(src_file)
        match size_result:
            case Success(value):
                return detect_by_size(value)
            case _:
                # If we cannot get file size (error, file inaccessible, etc.),
                # return True to create a duplicate with a new name instead of losing the file.
                # This follows the principle: "we don't want to lose any media file".
                return True

    @typechecked
    def _get_file_hash(self, file_path: str) -> str:
        """
        Get SHA1 hash of a file content for conflict detection.
        """
        if file_path in self._hash_cache:
            return self._hash_cache[file_path]

        import hashlib

        sha1_hash = hashlib.sha1()

        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(self._CHUNK_SIZE), b''):
                    sha1_hash.update(chunk)

            hash_result = sha1_hash.hexdigest()
            self._hash_cache[file_path] = hash_result
            return hash_result
        except Exception:
            # If we cannot read the file, return a hash based on file metadata
            # This ensures we don't crash the application
            file_size_result = self._fs_manipulator.getsize(file_path)
            file_name = os.path.basename(file_path)
            match file_size_result:
                case Success(file_size):
                    hash_base = f'{file_size}_{file_name}'.encode()
                case _:
                    # we can't rely on file size is not available for both comparing files
                    # so we rather use file name to compare them in next steps
                    hash_base = file_name.encode()

            hash_result = hashlib.sha1(hash_base).hexdigest()
            self._hash_cache[file_path] = hash_result
            return hash_result

    @typechecked
    def _compare_files(self, src_file: str, dst_file: str) -> bool:
        """
        Compare two files to determine if they're identical.
        We suppose that the size of these files has already been checked and it is the same.
        """

        if src_file == dst_file:
            return True

        try:
            # TODO: check if files are equal by them content if this test is true
            return self._get_file_hash(src_file) == self._get_file_hash(dst_file)
        except Exception:
            # If we cannot compare files properly, check their name
            # This prevents the application from crashing on file access issues
            # And it is critical to preserve every unique media file even if we create a copy
            return os.path.basename(src_file) == os.path.basename(dst_file)
