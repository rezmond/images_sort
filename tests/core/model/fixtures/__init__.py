# -*- coding: utf-8 -*-

import json
import os

ROOT_DIR = os.path.abspath(__file__ + '../../../../../../')


def get_move_map():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'move_map.json')
    with open(file_path, 'r') as file_:
        move_map = json.load(file_)

    for year_values in move_map.values():
        for period_values in year_values.values():
            for value in period_values:
                value['path'] = os.path.join(ROOT_DIR, value['path'])

    return move_map
