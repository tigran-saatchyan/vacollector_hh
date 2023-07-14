import os

CODE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE_CONFIG = os.path.join(CODE_DIR, 'database.ini')
TABLE_CREATION_SCRIPT = os.path.join(CODE_DIR, 'create_tables.sql')
EMPLOYERS_LIST = os.path.join(CODE_DIR, 'employer.txt')