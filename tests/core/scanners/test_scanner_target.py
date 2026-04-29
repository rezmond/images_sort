from unittest.mock import Mock, patch

from libs.monads import Success
from src.core.fs import FolderExtractorBase, FsManipulatorBase
from src.core.scanners import TargetFolderScanner


class MockFolderExtractor(FolderExtractorBase):
    def folder_to_file_pathes(self, folder):
        # Mock implementation for testing
        return []


class MockFsManipulator(FsManipulatorBase):
    def getsize(self, path):
        # Mock implementation for testing
        return Success(1024)  # Default size

    def move(self, src, dst):
        # Mock implementation for testing
        pass

    def copy(self, src, dst):
        # Mock implementation for testing
        pass

    def delete(self, path):
        # Mock implementation for testing
        pass

    def makedirs(self, path):
        # Mock implementation for testing
        pass

    def isfile(self, path):
        # Mock implementation for testing
        return True

    def isfolder(self, path):
        # Mock implementation for testing
        return True


def test_target_folder_scanner_init():
    """Test TargetFolderScanner initialization"""
    folder_extractor = MockFolderExtractor()
    fs_manipulator = MockFsManipulator()

    scanner = TargetFolderScanner(folder_extractor, fs_manipulator)

    assert scanner._folder_extractor == folder_extractor
    assert scanner._fs_manipulator == fs_manipulator
    assert scanner._hash_cache == {}
    assert scanner._size_index == {}


def test_target_folder_scanner_scan():
    """Test TargetFolderScanner scan method"""
    # Create a mock folder extractor that returns specific file paths
    mock_extractor = Mock(spec=FolderExtractorBase)
    mock_extractor.folder_to_file_pathes.return_value = [
        '/test/image1.jpg',
        '/test/video1.mp4',
        '/test/document.pdf',
    ]

    # Create a mock fs manipulator
    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.side_effect = [Success(1024), Success(2048), Success(512)]

    scanner = TargetFolderScanner(mock_extractor, mock_fs)

    # Test scan method
    scanner.scan('/test/folder')

    # Verify that getsize was called for media files only
    # Note: Only .jpg and .mp4 are media files, so getsize should be called twice
    assert mock_fs.getsize.call_count == 2
    mock_fs.getsize.assert_any_call('/test/image1.jpg')
    mock_fs.getsize.assert_any_call('/test/video1.mp4')


def test_target_folder_scanner_is_media_file():
    """Test TargetFolderScanner _is_media_file method"""
    folder_extractor = MockFolderExtractor()
    fs_manipulator = MockFsManipulator()
    scanner = TargetFolderScanner(folder_extractor, fs_manipulator)

    # Test media file extensions
    assert scanner._is_media_file('/test/image.jpg') is True
    assert scanner._is_media_file('/test/video.mp4') is True
    assert scanner._is_media_file('/test/image.JPEG') is True
    assert scanner._is_media_file('/test/video.MP4') is True

    # Test non-media file extensions
    assert scanner._is_media_file('/test/document.pdf') is False
    assert scanner._is_media_file('/test/script.py') is False
    assert scanner._is_media_file('/test/readme.txt') is False


def test_target_folder_scanner_add_file_size_index():
    """Test TargetFolderScanner _add_file_size_index method"""
    folder_extractor = MockFolderExtractor()
    # Create a real mock for fs_manipulator
    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.return_value = Success(1024)
    scanner = TargetFolderScanner(folder_extractor, mock_fs)

    # Test adding file to size index
    scanner._add_file_size_index('/test/file.jpg')

    # Verify the size index was updated
    assert 1024 in scanner._size_index
    assert '/test/file.jpg' in scanner._size_index[1024]


def test_target_folder_scanner_detect_duplicates_success():
    """Test TargetFolderScanner detect_duplicates method with success case"""
    folder_extractor = MockFolderExtractor()
    # Create a real mock for fs_manipulator
    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.return_value = Success(1024)
    scanner = TargetFolderScanner(folder_extractor, mock_fs)

    # Add a file to the size index
    scanner._add_file_size_index('/test/existing.jpg')

    # Test detection - should return False for non-conflicting file
    result = scanner.detect_duplicates('/test/new.jpg')
    assert result is False


def test_target_folder_scanner_detect_duplicates_error():
    """Test TargetFolderScanner detect_duplicates method with error case"""
    folder_extractor = MockFolderExtractor()
    # Create a real mock for fs_manipulator
    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.return_value = None  # Error case
    scanner = TargetFolderScanner(folder_extractor, mock_fs)

    # Test detection - should return True when we can't determine (error case)
    result = scanner.detect_duplicates('/test/new.jpg')
    assert result is True


def test_target_folder_scanner_get_file_hash():
    """Test TargetFolderScanner _get_file_hash method"""
    folder_extractor = MockFolderExtractor()
    fs_manipulator = MockFsManipulator()
    scanner = TargetFolderScanner(folder_extractor, fs_manipulator)

    # Test that hash is cached
    with patch('builtins.open', return_value=Mock(read=Mock(return_value=b'test'))):
        hash1 = scanner._get_file_hash('/test/file.jpg')
        hash2 = scanner._get_file_hash('/test/file.jpg')

        # Should be the same hash for the same file
        assert hash1 == hash2
        assert hash1 is not None


def test_target_folder_scanner_compare_files():
    """Test TargetFolderScanner _compare_files method"""
    folder_extractor = MockFolderExtractor()
    fs_manipulator = MockFsManipulator()
    scanner = TargetFolderScanner(folder_extractor, fs_manipulator)

    # Test with same files
    assert scanner._compare_files('/test/file1.jpg', '/test/file1.jpg') is True

    # Test with different files (mocked to return True for simplicity)
    with patch.object(scanner, '_get_file_hash') as mock_hash:
        mock_hash.side_effect = ['hash1', 'hash1']
        assert scanner._compare_files('/test/file1.jpg', '/test/file2.jpg') is True


def test_target_folder_scanner_scan_with_no_files():
    """Test TargetFolderScanner scan method with no files"""
    mock_extractor = Mock(spec=FolderExtractorBase)
    mock_extractor.folder_to_file_pathes.return_value = []

    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.return_value = Success(1024)

    scanner = TargetFolderScanner(mock_extractor, mock_fs)

    # Test scan method with no files
    scanner.scan('/test/folder')

    # Should not crash and size index should be empty
    assert scanner._size_index == {}


def test_target_folder_scanner_scan_with_non_media_files():
    """Test TargetFolderScanner scan method with non-media files"""
    mock_extractor = Mock(spec=FolderExtractorBase)
    mock_extractor.folder_to_file_pathes.return_value = [
        '/test/document.pdf',
        '/test/script.py',
    ]

    mock_fs = Mock(spec=FsManipulatorBase)
    mock_fs.getsize.return_value = Success(1024)

    scanner = TargetFolderScanner(mock_extractor, mock_fs)

    # Test scan method with non-media files
    scanner.scan('/test/folder')

    # Should not call getsize since these are not media files
    assert mock_fs.getsize.call_count == 0
    assert scanner._size_index == {}
