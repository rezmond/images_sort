# images_sort
Sort images by year and season.

(Temporary) Start project:
from the project folder directory run

`
    python3 start <src> <dst>
`

Run tests:

`
    pytest
`

Run tests with the coverage:

`
    pytest --cov="./core" --cov-report=html
`

Roadmap:
    [] - The moving process
    [] - Promose to create destination folder if it is not existed
    [] - Update the script help
    [] - Case for images withot exif data, but with file name like "20200429_*.jpg"