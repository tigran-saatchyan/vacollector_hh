from abc import abstractmethod, ABC


class DBEngine(ABC):

    @abstractmethod
    def get_companies_and_vacancies_count(self):
        pass

    @abstractmethod
    def get_all_vacancies(self):
        pass

    @abstractmethod
    def get_avg_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_higher_salary(self):
        pass

    @abstractmethod
    def get_vacancies_with_keyword(self):
        pass

    @abstractmethod
    def set_employers(self, cur, employers_list):
        pass

    @abstractmethod
    def set_vacancy(self, vacancy):
        pass

    @abstractmethod
    def update_vacancy(self, vacancy_id):
        pass

    @abstractmethod
    def get_employers(self, cur, employer_id=None):
        pass

    @abstractmethod
    def delete_employer(self, cur, employer_id=None):
        pass
