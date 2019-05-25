# -*- coding: utf-8 -*-

import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))


def full_path(rel_path):
    return os.path.join(ROOT_DIR, rel_path)
