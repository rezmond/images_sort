# -*- coding: utf-8 -*-

from datetime import datetime
import exifread
import filecmp
import os
import shutil


class ImagesCopier(object):
    """Объект копирования файлов"""
    ALLOWED_EXTENSIONS = (
        '.jpg',
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

    def __init__(self):
        super(ImagesCopier, self).__init__()
        self._sorted_by_year = {}
        self._structed_files_data = {
            'already_exists': [],
            'moved': [],
            'no_exif': []
        }

    def __cmp_files(self, dst_dir, file_dict):
        """
        Смотрит, нет ли в целевой папке файла с таким же именем.

        Если есть и файл идентичен существующему, то возвращает
        полный путь к целевой папке с типом результата "already_exists"

        Если не идентичен, то переименовывет целевой файл путём добавления
        целового значение через подчёркивание.

        :return: (<тип результата>, <полный путь к файлу>)
        """
        num = 1
        curr_file_name = file_dict['name']
        dst_file_path = os.path.join(dst_dir, curr_file_name)
        while os.path.isfile(dst_file_path):
            if filecmp.cmp(file_dict['path'], dst_file_path):
                return 'already_exists', dst_file_path
            curr_file_name = '{0}_{1}'.format(file_dict['name'], num)
            dst_file_path = os.path.join(dst_dir, curr_file_name)
            num += 1
        return 'moved', dst_file_path

    def _get_block_name(self, month):
        """
        Возвращает название месяца в человекочитаемом формате.
        :param month: номер месяца (От 1 до 12)
        """
        if month not in range(1, 13):
            raise ValueError(
                'Month number must be from 1 to 12. Not "{0}"'.format(month))

        for key, value in self.BLOCKS.items():
            if value[0] <= month <= value[1]:
                return key
        raise IndexError('Not found blocks name for month "{0}"'.format(month))

    @staticmethod
    def _get_datetime(src):
        return datetime.strptime(src, '%Y:%m:%d %H:%M:%S')

    def _get_images_list(self, current_dir_path=None):
        """
        Получение списка всех подходящих по разширению файлов,
        с учётом вложенности.
        """
        if current_dir_path is None:
            current_dir_path = self.IMAGES_PATH
        result = []
        for node_name in os.listdir(current_dir_path):
            node_path = os.path.join(current_dir_path, node_name)
            if not os.path.isfile(node_path):
                result.extend(self._get_images_list(node_path))
                continue
            if self._is_allowed_extension(node_path):
                result.append({
                    'path': node_path,
                    'name': node_name
                })
        return result

    def _is_allowed_extension(self, file_path):
        """Разрешённое ли расширение файла"""
        return os.path.splitext(file_path)[1] in self.ALLOWED_EXTENSIONS

    @staticmethod
    def __make_dir_if_not_exists(path):
        """Если целевой папки не было создано"""
        if not os.path.exists(path):
            os.makedirs(path)

    def scan(self):
        # формирование структуры по exif
        for file_dict in self._get_images_list():
            with open(file_dict['path'], 'rb') as current_file:
                tags = exifread.process_file(current_file)
            exif_data = tags.get('EXIF DateTimeOriginal', None)
            if not exif_data:
                self._structed_files_data['no_exif'].append(file_dict['path'])
                continue
            date = self._get_datetime(exif_data.values)
            # years
            year_in_string = str(date.year)
            if year_in_string not in set(self._sorted_by_year.keys()):
                self._sorted_by_year[year_in_string] = {}
            # month
            month_in_string = self._get_block_name(date.month)
            if month_in_string not in set(self._sorted_by_year[year_in_string].keys()):
                self._sorted_by_year[year_in_string][month_in_string] = []
            self._sorted_by_year[year_in_string][month_in_string]\
                .append(file_dict)

    def _move_by_month(self, year_name, month_items):
        for m_name, m_value in month_items:
            dst_dir_path = (
                os.path.join(self.RESULT_FOLDER_PATH, year_name, m_name))
            self.__make_dir_if_not_exists(dst_dir_path)
            for file_dict in m_value:
                result_type, result_path = (
                    self.__cmp_files(dst_dir_path, file_dict))
                if result_type == 'moved':
                    shutil.copy2(file_dict['path'], result_path)
                elif result_type != 'already_exists':
                    raise Exception('No result')
                self._structed_files_data[result_type]\
                    .append(file_dict['path'])

    def move(self):
        # перемещение файлов
        year_items = self._sorted_by_year.items()
        for y_name, y_value in year_items:
            month_items = self._sorted_by_year[y_name].items()
            self._move_by_month(y_value, month_items)
