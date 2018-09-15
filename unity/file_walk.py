# -*- coding: utf-8 -*-

import os
import tempfile

class FileOPerator(object):
    """

    """
    def __init__(self, src_dir):
        self.__source_dir = src_dir

    def open_file(self, file_path):
        try:
            fp = open(file_path)
        except PermissionError:
            print("some default data")
            return None
        else:
            with fp:
                return fp.read()

    def write_to_file(self):
        pass

    def copy_file(self, src_path, des_path):
        pass

    def create_tmp_file(self, des_dir, func):
        tempfile.tempdir = des_dir
        with tempfile.TemporaryFile() as fp:
            """
            fp.write(b'Hello world!')
            fp.seek(0)
            fp.read()
            """

            pass

    def traverse_dir(self):
        for root,dirs,filenames in os.walk():
            for dir_ in dirs:
                print(root, dir_)
                for 




