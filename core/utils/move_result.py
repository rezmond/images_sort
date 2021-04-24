from collections import namedtuple

MoveResult = namedtuple('MoveResult', (
    'moved',
    'already_exists',
    'no_data',
    'not_media',
))
