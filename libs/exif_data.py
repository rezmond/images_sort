from typing import Optional

from typeguard import typechecked
import exifread


@typechecked
def get_exif_data(path: str) -> Optional[str]:
    with open(path, 'rb') as current_file:
        tags = exifread.process_file(current_file)

    exif_data = tags.get('EXIF DateTimeOriginal', None)

    if exif_data is None:
        return None

    return exif_data.values
