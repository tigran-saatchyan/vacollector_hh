""" Parser implementation for the HH.ru website. """
from typing import List

from vacolector_hh.data_classes import Employer, Vacancy
from vacolector_hh.parser import Parser, RequestMixin


class HHParser(Parser, RequestMixin):
    """
    Parser implementation for the HH.ru website.
    """

    def __init__(self):
        super().__init__()
        self.per_page: int = 100
        self.vacancy_url: str = 'https://api.hh.ru/vacancies'
        self.employer_url: str = 'https://api.hh.ru/employers'

        self.headers: dict = {
            'HHParser-User-Agent': 'Va-collector/1.0 (mr.saatchyan@yandex.com)'
        }

        self.parameters: dict = {
            'page': 0,
            'per_page': self.per_page,
        }

    def parse_vacancies(
            self, employer_id: int, count: int = None
    ) -> List[Vacancy]:
        """
        Parses vacancies from the HH.ru website based on the given
        employer ID and count.

        Args:
            employer_id (int): The ID of the employer to retrieve
            vacancies for.
            count (int, optional): The number of vacancies to retrieve.
            Defaults to None.

        Returns:
            List[Vacancy]: The parsed vacancies.
        """
        parameters = self.parameters.copy()
        parameters['employer_id'] = employer_id or ''
        vacancies_list = []

        if count is not None:
            pages = (
                            count // self.per_page
                    ) + 1 if count % self.per_page else count // self.per_page
        else:
            pages = 1

        vacancies = self.request_all_pages(pages, parameters, self.vacancy_url)

        for vacancy in vacancies:
            salary_from = vacancy['salary'].get('from', 0) if vacancy[
                'salary'] else 0
            salary_to = vacancy['salary'].get('to', 0) if vacancy[
                'salary'] else 0
            currency = vacancy['salary'].get('currency', '') if vacancy[
                'salary'] else ''

            vacancies_list.append(
                Vacancy(
                    id=vacancy['id'],
                    name=vacancy['name'],
                    salary_from=salary_from,
                    salary_to=salary_to,
                    currency=currency,
                    alternate_url=vacancy['alternate_url'],
                    published_at=vacancy['published_at'],
                    requirement=vacancy['snippet'].get('requirement', ''),
                    responsibility=vacancy['snippet'].get(
                        'responsibility', ''
                    ),
                    employer_id=vacancy['employer']['id'],
                )
            )

        return vacancies_list

    def parse_employers(self, employers_name: str) -> List[Employer]:
        """
        Parses employers from the HH.ru website based on the given name.

        Args:
            employers_name (str): The name of the employers to search for.

        Returns:
            List[Employer]: The parsed employers.
        """
        pages = 1
        similar_name_employers = []
        parameters = self.parameters.copy()
        parameters['text'] = employers_name or ''
        parameters['only_with_vacancies'] = True

        employers = self.request_all_pages(
            pages, parameters, self.employer_url
        )

        for employer in employers:
            similar_name_employers.append(
                Employer(
                    id=int(employer['id']),
                    name=employer['name'],
                    alternate_url=employer['alternate_url'],
                    open_vacancies=int(employer['open_vacancies']),
                )
            )

        return similar_name_employers

    def request_all_pages(
            self, pages: int, parameters: dict, url: str
    ) -> List[dict]:
        """
        Requests all pages of data from the API.

        Args:
            pages (int): The number of pages to request.
            parameters (dict): The parameters to include in the request.
            url (str): The URL to make the request to.

        Returns:
            List[dict]: The combined data from all pages.
        """
        page = 0
        result = []

        while page < pages:
            parameters['page'] = page
            response = self.make_request(url, parameters, self.headers)
            page += 1
            pages = response['pages']
            result.extend(response['items'])

        return result
