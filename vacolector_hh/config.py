import os
from configparser import ConfigParser

from vacolector_hh.constants import CODE_DIR

file_name = os.path.join(CODE_DIR, 'database.ini')


def config(filename=file_name, section="postgresql"):
    db = {}

    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            f'Section {section} is not found in the {filename} file.'
        )
    return db
