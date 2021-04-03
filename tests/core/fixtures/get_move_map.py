import os

import yaml

from core.types import FileDescriptor
from utils import full_path


def get_move_map():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'move_map.yml')
    with open(file_path, 'r') as file_:
        move_map = yaml.full_load(file_)

    for year_values in move_map.values():
        for preiod_name, period_values in year_values.items():
            year_values[preiod_name] = [
                FileDescriptor(
                    full_path(value['path']),
                    value['name']
                ) for value in period_values
            ]

    return move_map
