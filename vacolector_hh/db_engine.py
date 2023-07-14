from abc import abstractmethod, ABC


class DBEngine(ABC):

    @abstractmethod
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
        pass

    @abstractmethod
    def get_all_vacancies(self, cur):
        """
        Retrieve all vacancies from the database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of Vacancy objects.
        """
        pass

    @abstractmethod
    def get_avg_salary(self, cur):
        """
        Retrieve the average salary from the database.

        Args:
            cur: Database cursor.

        Returns:
            int: Average salary.
        """
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self, cur):
        """
        Retrieve vacancies with salary above average from the database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of Vacancy objects.
        """
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self, cur):
        """
        Retrieve vacancies containing a specific keyword from
        the database.

        Args:
            cur: Database cursor.

        Returns:
            list: List of Vacancy objects.
        """
        pass

    @abstractmethod
    def set_employers(self, cur, employers_list):
        """
        Set employers in the database.

        Args:
            cur: Database cursor.
            employers_list: List of Employer objects.
        """
        pass

    @abstractmethod
    def set_vacancies(self, cur, vacancy_list):
        """
        Set vacancies in the database.

        Args:
            cur: Database cursor.
            vacancy_list: List of Vacancy objects.
        """
        pass

    @abstractmethod
    def get_employers(self, cur, employer_id=None):
        """
        Retrieve employers from the database.

        Args:
            cur: Database cursor.
            employer_id (int, optional): Employer ID. If provided,
            retrieve a specific employer. Defaults to None.

        Returns:
            list: List of Employer objects or a single Employer
            object if employer_id is provided.
        """
        pass

    @abstractmethod
    def delete_employer(self, cur, employer_id=None):
        """
        Delete an employer from the database.

        Args:
            cur: Database cursor.
            employer_id (int, optional): Employer ID. If provided,
            delete a specific employer. Defaults to None.
        """
        pass
