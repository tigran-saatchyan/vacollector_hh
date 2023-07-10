from functools import wraps

import psycopg2
from psycopg2.extras import DictCursor

from vacolector_hh.config import config
from vacolector_hh.db_engine import DBEngine


class DBManager(DBEngine):

    def __init__(self):
        super().__init__()
        self.params = config()
        self.db_name = "vacollector"

    def create_database(self) -> None:
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True

        cur = conn.cursor()
        cur.execute(f"CREATE DATABASE {self.db_name}")

        cur.close()
        conn.close()

    def connect_to_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = None
            if 'dbname' not in self.params.keys():
                self.params.update({'dbname': self.db_name})
            try:
                with psycopg2.connect(**self.params) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cur:
                        result =func(self, cur, *args, **kwargs)
            except psycopg2.DatabaseError as e:
                print(e)
            finally:
                if conn is not None:
                    conn.close()

            return result
        return wrapper

    @connect_to_db
    def set_employers(self, cur, employers_list):
        for employer in employers_list:
            cur.execute(f"INSERT INTO employers (id) VALUES ({employer})")

    def set_vacancy(self, vacancy):
        pass

    def update_vacancy(self, vacancy_id):
        pass

    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass

    @connect_to_db
    def get_employers(self, cur, employer_id=None):
        sql = "SELECT id FROM employers"
        if employer_id is not None:
            sql += f" WHERE employee_id={employer_id}"
        cur.execute(sql + ";")
        result = cur.fetchall()
        result_to_list = [row[0] for row in result]
        return result_to_list

    @connect_to_db
    def delete_employer(self, cur, employer_id=None):
        if employer_id is None:
            sql = "TRUNCATE TABLE employers CASCADE;"
        else:
            sql = f"DELETE FROM employers WHERE id = {employer_id};"
        cur.execute(sql)
