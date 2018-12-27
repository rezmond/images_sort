# -*- coding: utf-8 -*-

import getopt
import sys

from .model.sorter import Sorter


def main(argv):
    MAIN_PROGRAMM = 'start.py'
    source_folder = ''
    dst_folder = ''

    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('{0} -i <sourcefolder> -o <dstfolder>'.format(MAIN_PROGRAMM))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('{0} -i <source/folder> -o <dst/folder>'.format(MAIN_PROGRAMM))
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            source_folder = arg
        elif opt in ("-o", "--ofolder"):
            dst_folder = arg

    sorter = Sorter(source_folder, dst_folder)
    sorter.sort()


if __name__ == "__main__":
    main(sys.argv[1:])
