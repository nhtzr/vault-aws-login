import os
import sys
from configparser import ConfigParser


def merge_sections_into(output_path, input_paths):
    config = ConfigParser()
    for input_path in input_paths:
        for overriding_section in sections_of(input_path):
            config.remove_section(overriding_section)
        config.read(input_path)
    with open_output(output_path) as out_file:
        config.write(out_file)


def sections_of(input_path):
    next_overriding_config = ConfigParser()
    next_overriding_config.read(input_path)
    return next_overriding_config.sections()


def open_output(path):
    if path is None:
        return sys.stdout
    path_ = os.path.expanduser(path)
    return open(path_, 'w')
