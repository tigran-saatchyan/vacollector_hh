from configparser import ConfigParser

from vacolector_hh.constants import DATABASE_CONFIG


def config(filename=DATABASE_CONFIG, section="postgresql"):
    """
    Read the database configuration file and return the configuration
    parameters for a specific section.

    Args:
        filename (str, optional): The name of the configuration file.
        Defaults to DATABASE_CONFIG.
        section (str, optional): The section in the configuration file
        to retrieve parameters from. Defaults to "postgresql".

    Returns:
        dict: Dictionary containing the configuration parameters.

    Raises:
        Exception: If the specified section is not found in the
        configuration file.
    """
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
