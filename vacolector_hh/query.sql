-- get_companies_and_vacancies_count()
SELECT name, open_vacancies
FROM employers;

-- get_all_vacancies()
SELECT e.name AS employer_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.currency, v.alternate_url
FROM vacancies v
INNER JOIN employers e ON v.employer_id = e.id;

-- get_avg_salary()
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

-- get_vacancies_with_higher_salary()
SELECT e.name as employer_name, v.name as vacancy_name, salary_from, salary_to, currency, v.alternate_url
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

-- get_vacancies_with_keyword()
SELECT e.name as employer_name, v.name as vacancy_name, salary_from, salary_to, currency, v.alternate_url
FROM vacancies v
INNER JOIN employers e ON e.id = v.employer_id
WHERE v.name ILIKE ('%python%')
    OR requirement ILIKE ('%python%')
    OR responsibility ILIKE ('%python%');