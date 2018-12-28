# -*- coding: utf-8 -*-

import json
import os


def get_move_map():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'move_map.json')
    with open(file_path, 'r') as file_:
        move_map = json.load(file_)
    return move_map
