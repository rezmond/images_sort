# -*- coding: utf-8 -*-
import os


def validate_folder_path(param_value, param_humanize):
    if not param_value:
        raise ValueError(
            'The {0} folder\'s path did not set.'
            ' Please set the {0} folder path and try again.'
            .format(param_humanize))

    if not os.path.isabs(param_value):
        raise ValueError(
            f'The {param_humanize} folder path should be absolute,'
            f' but got "{param_value}"')

    if not os.path.isdir(param_value):
        raise ValueError(
            f'The folder "{param_value}" not found')
