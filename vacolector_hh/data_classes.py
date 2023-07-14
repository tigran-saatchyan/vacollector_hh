from dataclasses import dataclass
from datetime import datetime


@dataclass
class Employer:
    id: int
    name: str
    alternate_url: str
    open_vacancies: int

    def __str__(self) -> str:
        """
        Return a string representation of the employer.

        Returns:
            str: String representation of the employer.
        """
        return f"Name: {self.name},\n" \
               f"ID: {self.id}, \n" \
               f"Open Vacancies: {self.open_vacancies}, \n" \
               f"URL: {self.alternate_url}\n"


@dataclass
class Vacancy:
    id: int
    name: str
    salary_from: int
    salary_to: int
    currency: str
    published_at: datetime
    alternate_url: str
    employer_id: int
    requirement: str
    responsibility: str

    def __str__(self) -> str:
        """
        Return a string representation of the vacancy.

        Returns:
            str: String representation of the vacancy.
        """
        return (
            f'ID: {self.id}\n'
            f'Title: {self.name}\n'
            f'Salary: {self.salary_from} {self.currency} - '
            f'{self.salary_to} {self.currency} \n'
            f'requirement: {self.requirement}\n'
            f'Link: {self.alternate_url}\n'
            f'___________________________________________________________\n'
        )

    def __repr__(self) -> str:
        """
        Return a string representation of the vacancy for debugging purposes.

        Returns:
            str: String representation of the vacancy.
        """
        return (
            f'Vacancy(vacancy_id={self.id}, \n'
            f'\ttitle={self.name}, \n'
            f'\turl={self.alternate_url}, \n'
            f'\tsalary_from={self.salary_from} {self.currency}, \n'
            f'\tsalary_to={self.salary_to} {self.currency}, \n'
            f'\trequirement={self.requirement})\n'
        )
