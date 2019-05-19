# -*- coding: utf-8 -*-

from collections import namedtuple

MoveResult = namedtuple('MoveResult', (
    'moved',
    'already_exists',
    'no_exif',
    'not_images',
))
