-- Создать базу данных  vacollector
CREATE DATABASE vacollector;

-- Сброс всех таблиц
DROP TABLE IF EXISTS employer CASCADE;
DROP TABLE IF EXISTS vacancies CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS vacancy_types CASCADE;

-- Таблица employer (Компания / Работадатель)
CREATE TABLE IF NOT EXISTS employers (
    id                INTEGER PRIMARY KEY NOT NULL,
    name              VARCHAR NOT NULL,
    alternate_url     TEXT NOT NULL,
    logo_url_90       TEXT,
    logo_url_240      TEXT,
    logo_url_original TEXT
);

-- Таблица experiences (Опыт работы)
CREATE TABLE IF NOT EXISTS experiences (
    id            SERIAL NOT NULL PRIMARY KEY,
    experience    VARCHAR NOT NULL,
    ru_experience VARCHAR
);

-- Таблица vacancy_types (Тип вакансии: Открытая/Закрытая)
CREATE TABLE IF NOT EXISTS vacancy_types (
    id           SERIAL NOT NULL PRIMARY KEY,
    vacancy_type VARCHAR NOT NULL,
    ru_type      VARCHAR
);

-- Таблица vacancy (Вакансии)
CREATE TABLE IF NOT EXISTS vacancies (
    id             INTEGER PRIMARY KEY NOT NULL,
    name           TEXT,
    salary_from    INTEGER,
    salary_to      INTEGER,
    type_id        INTEGER NOT NULL REFERENCES vacancy_types (id),
    published_at   DATE,
    created_at     DATE,
    archived       BOOLEAN,
    alternate_url  TEXT,
    requirement    TEXT,
    responsibility TEXT,
    experience_id  INTEGER NOT NULL REFERENCES experiences (id),
    employment     VARCHAR,
    employer_id    INTEGER NOT NULL REFERENCES employers (id)
);

