# -*- coding: utf-8 -*-

import getopt
import sys

from .base import ViewBase


MAIN_PROGRAMM = 'sorter.py'


class ConsoleView(ViewBase):

    def show(self):
        argv = sys.argv[1:]
        try:
            opts, args = getopt.getopt(argv, "hi:o:", ["ifolder=", "ofolder="])
        except getopt.GetoptError:
            print('{0} -i <source/folder> -o <dst/folder>'.format(MAIN_PROGRAMM))
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('{0} -i <source/folder> -o <dst/folder>'.format(MAIN_PROGRAMM))
                sys.exit()
            elif opt in ("-i", "--ifolder"):
                self._controller.set_src_folder(arg)
            elif opt in ("-o", "--ofolder"):
                self._controller.set_dst_folder(arg)

        self._model.move()
