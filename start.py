# -*- coding: utf-8 -*-

from datetime import datetime
from functools import reduce
from operator import methodcaller
import exifread
import os
import filecmp
import getopt
import shutil
import sys


class Console(object):
    NOT_TRUE_ANSWER_MSG = 'пожалуйста введите одно из следующих значений'

    def __init__(self, allowed_commands):
        super(Console, self).__init__()
        self._allowed_commands = allowed_commands

    @property
    def allowed_commands(self):
        return self._allowed_commands

    @property
    def quoted_allowed_commands(self):
        return map('"{}"'.format, self._allowed_commands)

    def ask_user(self, message):
        user_answer = input(message).lower()

        not_true_answer_msg = '{0}: {1}\n'.format(
            self.NOT_TRUE_ANSWER_MSG.capitalize(), ', '.join(self.quoted_allowed_commands))\
            .encode('utf-8')

        while user_answer not in self.allowed_commands:
            user_answer = input(not_true_answer_msg).lower()

        return user_answer


class ResolverConsole(Console):

    def __init__(self, true_commands, false_commands):
        super(ResolverConsole, self).__init__(true_commands + false_commands)
        self._true_commands = true_commands
        self._false_commands = false_commands

    def ask_user(self, message):
        result = super(ResolverConsole, self).ask_user(message)
        return result in self._true_commands


class Sorter(object):

    ALLOWED_EXTENSIONS = (
        '.jpg',
        '.JPG',
        '.jpeg',
        '.png'
    )

    IMAGES_FOLDER_NAME = 'src_images'
    RESULT_FOLDER_NAME = 'result'

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGES_PATH = os.path.join(ROOT_PATH, IMAGES_FOLDER_NAME)
    RESULT_FOLDER_PATH = os.path.join(ROOT_PATH, RESULT_FOLDER_NAME)

    BLOCKS = {
        'Зима (начало)': (1, 2),
        'Весна': (3, 5),
        'Лето': (6, 8),
        'Осень': (9, 11),
        'Зима (конец)': (12, 12),
    }

    def __init__(self, source_folder, dst_folder):
        super(Sorter, self).__init__()
        self._source_folder = source_folder
        self._dst_folder = dst_folder.decode('utf-8')
        self._check_folders_exists()

        self.resolution_getter = ResolverConsole(
            true_commands=('yes',), false_commands=('no',))

    def _check_folders_exists(self):
        folder_paths = (self._source_folder, self._dst_folder)
        if not self._source_folder:
            raise ValueError(
                'Не задана папка источник'.encode('utf-8'))
        if not self._dst_folder:
            raise ValueError(
                'Не задана папка приёмник'.encode('utf-8'))
        for path in folder_paths:
            if not os.path.isdir(path):
                raise ValueError(
                    'Папка "{0}" не найдена'.format(path).encode('utf-8'))

    @staticmethod
    def cmp_files(dst_dir, file_dict):
        num = 1
        curr_file_name = file_dict['name']
        try:
            dst_file_path = os.path.join(dst_dir, curr_file_name)
        except UnicodeDecodeError:
            return 'errors', curr_file_name
        while os.path.isfile(dst_file_path):
            if filecmp.cmp(file_dict['path'], dst_file_path):
                return 'already_exists', dst_file_path
            curr_file_name = '{0}_{1}'.format(file_dict['name'], num)
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1
        return 'moved', dst_file_path

    def get_block_name(self, month):
        for key, value in self.BLOCKS.items():
            if value[0] <= month <= value[1]:
                return key
        raise IndexError('Not found blocks name for month "{0}"'.format(month))

    @staticmethod
    def get_datetime(src):
        return datetime.strptime(src, '%Y:%m:%d %H:%M:%S')

    def get_images_list(self, current_dir_path):
        """
        Получение списка всех подходящих по разширению файлов, с учётом вложенности.
        """
        def _reduce_dirs_nodes(res, node_name):
            node_path = os.path.join(current_dir_path, node_name)
            if not os.path.isfile(node_path):
                return res + self.get_images_list(node_path)

            if not self._self_is_allowed_file_type(node_path):
                return res
            return res + [{
                'path': node_path,
                'name': node_name
            }]

        return reduce(_reduce_dirs_nodes, os.listdir(current_dir_path), [])

    def _self_is_allowed_file_type(self, node_path):
        return os.path.splitext(node_path)[1] in self.ALLOWED_EXTENSIONS

    def sort(self):
        # print u'\n'.join(get_images_list(IMAGES_PATH)).encode('utf-8')

        sorted_by_year = {}

        result = {
            'already_exists': [],
            'moved': [],
            'no_exif': [],
            'errors': [],
        }

        result_messages_map = {
            'already_exists': 'Уже есть в соответвующей папке',
            'moved': 'Успешно перемещено в соответвующую папку',
            'no_exif': 'Не иммеют exif',
            'errors': 'Файлов при обработке которых были ошибки',
        }

        # формирование структуры по exif
        for file_dict in self.get_images_list(self._source_folder):
            with open(file_dict['path'], 'rb') as current_file:
                tags = exifread.process_file(current_file)
            exif_data = tags.get('EXIF DateTimeOriginal', None)
            if not exif_data:
                # print file_dict['name'], file_dict['path']
                result['no_exif'].append(file_dict['path'])
                continue
            date = self.get_datetime(exif_data.values)
            year_in_string = str(date.year)
            if year_in_string not in set(sorted_by_year.keys()):
                sorted_by_year[year_in_string] = {}
            month_in_string = self.get_block_name(date.month)
            if month_in_string not in set(sorted_by_year[year_in_string].keys()):
                sorted_by_year[year_in_string][month_in_string] = []
            sorted_by_year[year_in_string][month_in_string].append(file_dict)

        # перемещение файлов
        for y_name, y_value in sorted_by_year.items():
            for m_name, m_value in sorted_by_year[y_name].items():
                path_chain = map(
                    methodcaller('encode', 'utf-8'), (self._dst_folder, y_name, m_name))
                dst_dir_path = os.path.join(*path_chain)
                # если целвой папки не было создано
                if not os.path.exists(dst_dir_path):
                    os.makedirs(dst_dir_path)
                for file_dict in m_value:
                    result_type, result_path = (
                        self.cmp_files(dst_dir_path, file_dict))
                    if result_type == 'moved':
                        shutil.copy2(file_dict['path'], result_path)
                    elif result_type not in ('already_exists', 'errors'):
                        raise Exception('No result')
                    result[result_type].append(file_dict['path'])

        moved_len = len(result['moved'])
        already_exists_len = len(result['already_exists'])

        if (moved_len + already_exists_len) == 0:
            return

        are_images_need_delete = (
            'Удалить {0} перемещённых и {1} уже существующих файлов? (yes|no):\n'
            .format(moved_len, already_exists_len)
            .encode('utf-8'))

        images_need_delete = (
            self.resolution_getter.ask_user(are_images_need_delete))

        if images_need_delete:
            print('Удаляем:\n'.encode('utf-8'))
        else:
            print('Перемещено:'.encode('utf-8'))

        for i in result['moved']:
            if isinstance(i, str):
                print(i.encode('utf-8'))
            else:
                print(i)

        if images_need_delete:
            print()
        else:
            print('Уже сущенствует:'.encode('utf-8'))

        for i in result['already_exists']:
            if isinstance(i, str):
                print(i.encode('utf-8'))
            else:
                print(i)

        if not images_need_delete:
            return

        for moved in result['moved']:
            os.remove(moved)

        for exists in result['already_exists']:
            os.remove(exists)

        def _make_result_message(item):
            return '{0:>40}: {1}'.format(
                result_messages_map[item], len(result[item]))

        result_msg = (
            map(_make_result_message, ('moved', 'already_exists', 'no_exif', 'errors')))
        print(('{0}\n{1}\n{2}'.format(*result_msg)).encode('utf-8'))


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
            print('{0} -i <sourcefolder> -o <dstfolder>'.format(MAIN_PROGRAMM))
            sys.exit()
        elif opt in ("-i", "--ifolder"):
            source_folder = arg
        elif opt in ("-o", "--ofolder"):
            dst_folder = arg

    sorter = Sorter(source_folder, dst_folder)
    sorter.sort()

if __name__ == "__main__":
    main(sys.argv[1:])
