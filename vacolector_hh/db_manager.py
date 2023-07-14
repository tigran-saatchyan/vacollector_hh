import traceback
from functools import wraps

import psycopg2
from psycopg2 import ProgrammingError
from psycopg2.extras import DictCursor

from vacolector_hh.config import config
from vacolector_hh.constants import TABLE_CREATION_SCRIPT
from vacolector_hh.db_engine import DBEngine


class DBManager(DBEngine):

    def __init__(self):
        super().__init__()
        self.params = config()
        self.db_name = "vacollector"

    def create_database(self) -> None:
        """
        Create the database if it doesn't exist.

        Raises:
            ProgrammingError: If an error occurs during the database
            creation.
        """
        conn = psycopg2.connect(**self.params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"CREATE DATABASE {self.db_name}")
            print(f"Database '{self.db_name}' created successfully.")
        except ProgrammingError as e:
            pass
        cur.close()
        conn.close()

    def create_tables(self):
        """
        Create the database tables using the SQL script.

        Raises:
            Exception: If an error occurs during table creation.
        """
        self.params.update({'dbname': self.db_name})
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    with open(TABLE_CREATION_SCRIPT, 'r') as script:
                        cur.execute(script.read())
            print(f"{self.db_name} tables successfully created")
        except (Exception, psycopg2.DatabaseError):
            traceback.print_exc()

    def connect_to_db(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            conn = None
            if 'dbname' not in self.params.keys():
                self.params.update({'dbname': self.db_name})
            result = None
            try:
                with psycopg2.connect(**self.params) as conn:
                    with conn.cursor(cursor_factory=DictCursor) as cur:
                        result = func(self, cur, *args, **kwargs)
            except psycopg2.DatabaseError:
                traceback.print_exc()
            finally:
                if conn is not None:
                    conn.close()
            return result

        return wrapper

    @connect_to_db
    def is_tables_existing(self, cur):
        """
        Check if the tables exist in the database.

        Args:
            cur: Database cursor.

        Returns:
            bool: True if tables exist, False otherwise.
        """
        cur.execute(
            f"""SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            """
        )
        result = cur.fetchone()[0]
        return result > 0

    @connect_to_db
    def set_vacancies(self, cur, vacancy_list):
        """
        Insert vacancies into the database.

        Args:
            cur: Database cursor.
            vacancy_list (list): List of Vacancy objects.
        """
        for vacancy in vacancy_list:
            cur.execute(
                f"""
                INSERT INTO vacancies (id, name, salary_from, salary_to, currency, published_at, alternate_url, employer_id, requirement, responsibility) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    vacancy.id,
                    vacancy.name,
                    vacancy.salary_from,
                    vacancy.salary_to,
                    vacancy.currency,
                    vacancy.published_at,
                    vacancy.alternate_url,
                    vacancy.employer_id,
                    vacancy.requirement,
                    vacancy.responsibility
                )
            )

    @connect_to_db
    def get_companies_and_vacancies_count(self, cur):
        """
        Retrieve all companies and their open vacancies count from the
        database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of tuples containing company names and their
            open vacancies count.
        """
        cur.execute(
            """
            SELECT name, open_vacancies
            FROM employers;
            """
        )
        return cur.fetchall()

    @connect_to_db
    def get_all_vacancies(self, cur):
        """
        Retrieve all vacancies from the database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of tuples containing vacancy details.
        """
        cur.execute(
            """
            SELECT e.name AS employer_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.currency, v.alternate_url
            FROM vacancies v
            INNER JOIN employers e ON v.employer_id = e.id;
            """
        )
        return cur.fetchall()

    @connect_to_db
    def get_avg_salary(self, cur):
        """
        Retrieve the average salary from the database.

        Args:
            cur: Database cursor.

        Returns:
            float: Average salary.
        """
        cur.execute(
            """
                SELECT ROUND(
                    AVG(
                        CASE
                            WHEN salary_from > 0 AND salary_to > 0
                                THEN (salary_from + salary_to) / 2.0
                            ELSE GREATEST(salary_from, salary_to)
                        END
                        )
                    )
                FROM vacancies;
            """
        )
        return cur.fetchone()[0]

    @connect_to_db
    def get_vacancies_with_higher_salary(self, cur):
        """
        Retrieve vacancies with salary above average from the database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of tuples containing vacancy details.
        """
        cur.execute(
            """
            SELECT e.name AS employer_name, v.name AS vacancy_name, salary_from, salary_to, currency, v.alternate_url
            FROM vacancies v
            INNER JOIN employers e ON e.id = v.employer_id
            WHERE (
                CASE
                    WHEN salary_from > 0 AND salary_to > 0
                        THEN (salary_from + salary_to) / 2.0
                    ELSE GREATEST(salary_from, salary_to)
                END
                ) > (
                    SELECT ROUND(
                        AVG(
                            CASE
                                WHEN salary_from > 0 AND salary_to > 0
                                    THEN (salary_from + salary_to) / 2.0
                                ELSE GREATEST(salary_from, salary_to)
                            END
                            )
                        )
                    FROM vacancies
                );
            """
        )
        return cur.fetchall()

    @connect_to_db
    def get_vacancies_with_keyword(self, cur, keyword):
        """
        Retrieve vacancies containing a specific keyword from the
        database.

        Args:
            cur: Database cursor.
            keyword (str): Keyword to search for.

        Returns:
            list: List of tuples containing vacancy details.
        """
        cur.execute(
            f"""
            SELECT e.name as employer_name, v.name as vacancy_name, salary_from, salary_to, currency, v.alternate_url
            FROM vacancies v
            INNER JOIN employers e ON e.id = v.employer_id
            WHERE v.name ILIKE ('%{keyword}%')
                OR requirement ILIKE ('%{keyword}%')
                OR responsibility ILIKE ('%{keyword}%');
            """
        )
        return cur.fetchall()

    @connect_to_db
    def get_employers(self, cur, employer_id=None):
        """
        Retrieve employers from the database.

        Args:
            cur: Database cursor.
            employer_id (int, optional): Employer ID. If provided,
            retrieve a specific employer. Defaults to None.

        Returns:
            list: List of employer IDs or a single employer ID if
            employer_id is provided.
        """
        sql = "SELECT id FROM employers"
        if employer_id is not None:
            sql += f" WHERE employee_id={employer_id}"

        cur.execute(sql + ";")

        result_to_list = [row[0] for row in cur.fetchall()]
        return result_to_list

    @connect_to_db
    def set_employers(self, cur, employers_list):
        """
        Insert employers into the database.

        Args:
            cur: Database cursor.
            employers_list (list): List of Employer objects.
        """
        for employer in employers_list:
            cur.execute(
                f"""
                INSERT INTO employers (id, name, open_vacancies, alternate_url) 
                VALUES (%s, %s, %s, %s);""",
                (
                    employer.id,
                    employer.name,
                    employer.open_vacancies,
                    employer.alternate_url
                )

            )

    @connect_to_db
    def delete_employer(self, cur, employer_id=None):
        """
        Delete an employer from the database.

        Args:
            cur: Database cursor.
            employer_id (int, optional): Employer ID. If provided,
            delete a specific employer. Defaults to None.
        """
        if employer_id is None:
            sql = "TRUNCATE TABLE employers CASCADE;"
        else:
            sql = f"DELETE FROM employers WHERE id = {employer_id};"
        cur.execute(sql)
