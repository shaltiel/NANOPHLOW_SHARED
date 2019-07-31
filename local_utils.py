#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import glob
import sys
import os
import shutil
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


class paths:

    PROJECT = r"/Users/se399/PycharmProjects/DFSimone";
    restart_files = PROJECT + '/Inputs/particle/*';
    template = PROJECT + '/Inputs/Template'
    outputs = PROJECT + '/Outputs'  # SE: called previously home dir.
    sim_outputs = PROJECT + '/Simulations'

    @classmethod
    def clean(cls,path):
        shutil.rmtree(path, ignore_errors=True)  # clean recursively.

    @classmethod
    def get_restart_files(cls):
        return glob.glob(cls.restart_files)


    # @classmethod
    # def create_unique_name(cls,list_names,list_val):

def replace(file_path, origin_line, new_line):
    # Create temp file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(origin_line, new_line))
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)
