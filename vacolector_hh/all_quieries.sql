-- Создать базу данных  vacollector
CREATE DATABASE vacollector;

-- Сброс всех таблиц
DROP TABLE IF EXISTS employers CASCADE;
DROP TABLE IF EXISTS vacancies CASCADE;
DROP TABLE IF EXISTS experiences CASCADE;
DROP TABLE IF EXISTS vacancy_types CASCADE;

-- Таблица employers (Компания / Работодатель)
CREATE TABLE IF NOT EXISTS employers (
    id                INTEGER PRIMARY KEY NOT NULL,
    name              VARCHAR,
    alternate_url     TEXT,
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

-- Таблица platforms (Платформы)
CREATE TABLE IF NOT EXISTS platforms (
    id           SERIAL NOT NULL PRIMARY KEY,
    vacancy_type VARCHAR NOT NULL,
    ru_type      VARCHAR
);

-- Таблица vacancies (Вакансии)
CREATE TABLE IF NOT EXISTS vacancies (
    id             INTEGER PRIMARY KEY NOT NULL,
    name           TEXT,
    salary_from    INTEGER,
    salary_to      INTEGER,
    currency       VARCHAR,
    type_id        INTEGER NOT NULL REFERENCES vacancy_types (id),
    published_at   DATE,
    created_at     DATE,
    archived       BOOLEAN,
    alternate_url  TEXT,
    employer_id    INTEGER NOT NULL REFERENCES employers (id),
    requirement    TEXT,
    responsibility TEXT,
    experience_id  INTEGER NOT NULL REFERENCES experiences (id),
    employment     VARCHAR,
    platform_id    INTEGER NOT NULL REFERENCES platforms (id)
);

-- Очистка таблицы employers
TRUNCATE TABLE employers CASCADE;

-- Удаление employer по employer ID
DELETE FROM employers WHERE id = 851604;

-- Добавление employer id в базу
INSERT INTO employers (id) VALUES (851604);