# -*- coding: utf-8 -*-

import getopt
import sys
from typing import Tuple

from .base import ViewBase
from ..constants import COMMAND_LINE_SYNTAX_ERROR, SUCCESSFUL_TERMINATION

MAIN_PROGRAMM = 'sorter.py'


class ConsoleView(ViewBase):

    def handle_image_moved(self, move_pair: Tuple[str, str]):
        from_, to_ = move_pair
        print(f'{from_} --> {to_}')

    def show(self):
        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifolder=", "ofolder="])
        except getopt.GetoptError:
            print('{0} -i <source/folder> -o <dst/folder>'.format(MAIN_PROGRAMM))
            sys.exit(COMMAND_LINE_SYNTAX_ERROR)

        for opt, arg in opts:
            if opt == '-h':
                print('{0} -i <source/folder> -o <dst/folder>'.format(MAIN_PROGRAMM))
                sys.exit(SUCCESSFUL_TERMINATION)
            elif opt in ("-i", "--ifolder"):
                self._controller.set_src_folder(arg)
            elif opt in ("-o", "--ofolder"):
                self._controller.set_dst_folder(arg)
