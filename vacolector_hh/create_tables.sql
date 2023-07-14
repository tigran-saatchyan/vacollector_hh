-- Сброс всех таблиц
DROP TABLE IF EXISTS employers CASCADE;
DROP TABLE IF EXISTS vacancies CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS vacancy_types CASCADE;

-- Таблица employers (Компания / Работодатель)
CREATE TABLE IF NOT EXISTS employers (
    id             INTEGER PRIMARY KEY NOT NULL,
    name           VARCHAR,
    open_vacancies INTEGER,
    alternate_url  TEXT
);

-- Таблица vacancies (Вакансии)
CREATE TABLE IF NOT EXISTS vacancies (
    id             INTEGER PRIMARY KEY NOT NULL,
    name           TEXT,
    salary_from    INTEGER,
    salary_to      INTEGER,
    currency       VARCHAR,
    published_at   DATE,
    alternate_url  TEXT,
    employer_id    INTEGER NOT NULL REFERENCES employers (id),
    requirement    TEXT,
    responsibility TEXT
);
