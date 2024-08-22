import os

import psycopg2
from dotenv import load_dotenv

from src.api_connect import VacanciesInfo

load_dotenv()

password = os.getenv("PASSWORD")


class DBCreater:
    """Класс осуществляющий создание и наполнение таблиц в DataBase"""

    def __init__(self, data_base_name, data):
        self.data_base = data_base_name
        self.data = data
        self.cur = self.connection().cursor()

    def connection(self):
        try:
            conn = psycopg2.connect(
                host="localhost",
                database=f"{self.data_base}",
                user="postgres",
                password=f"{password}",
            )
            return conn
        except Exception as ex:
            print(ex)
            return None

    def companies_table(self):
        self.cur.execute(
            "CREATE TABLE companies("
            "employer_id int PRIMARY KEY,"
            " company_name varchar(100) NOT NULL,"
            " vacancies_quantity int NOT NULL);"
        )
        companies_info = VacanciesInfo(self.data)
        list_vacancies = companies_info.list_vacancies()
        for key, value in self.data.items():
            self.cur.execute(
                f"INSERT INTO companies VALUES ({value}, '{key}', {len(list_vacancies[key])})"
            )
        self.cur.execute("SELECT * FROM companies;")
        return self.cur

    def vacancies_table(self):
        self.cur.execute(
            "CREATE TABLE vacancies("
            "vacancy_id int PRIMARY KEY,"
            " vacancy_title varchar(100) NOT NULL,"
            " vacancy_url varchar(100) NOT NULL,"
            " salary int NOT NULL,"
            " type varchar(50) NOT NULL, "
            " employer_id int NOT NULL);"
        )
        vacancies_info = VacanciesInfo(self.data)
        list_vacancies = vacancies_info.list_vacancies()
        for key, value in list_vacancies.items():
            for i in value:
                if i["salary"] is not None:
                    if i["salary"]["from"] is None:
                        self.cur.execute(
                            f"INSERT INTO vacancies VALUES("
                            f"{i['id']},"
                            f" '{i['name']}',"
                            f" '{i['alternate_url']}',"
                            f" {i['salary']['to']},"
                            f" '{i['type']['name']}',"
                            f" {i['employer']['id']});"
                        )
                    else:
                        self.cur.execute(
                            f"INSERT INTO vacancies VALUES({i['id']},"
                            f" '{i['name']}',"
                            f" '{i['alternate_url']}',"
                            f" {i['salary']['from']},"
                            f" '{i['type']['name']}',"
                            f" {i['employer']['id']});"
                        )
        self.cur.execute("SELECT * FROM vacancies;")
        return self.cur


class DBManager:
    """Класс осуществляющий работу с таблицами данных DataBase"""

    def __init__(self, cur):
        self.cur = cur

    @staticmethod
    def connect():
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="Course_5_work",
                user="postgres",
                password=f"{password}",
            )
            return conn
        except Exception as ex:
            print(ex)
            return None

    def get_companies_and_vacancies_count(self):
        self.cur.execute("SELECT company_name, vacancies_quantity FROM companies")
        rows = self.cur.fetchall()
        return rows

    def get_all_vacancies(self):
        self.cur.execute(
            "SELECT vacancy_title, company_name, salary, vacancy_url"
            " FROM companies INNER JOIN vacancies USING(employer_id)"
        )
        rows = self.cur.fetchall()
        return rows

    def get_avg_salary(self):
        self.cur.execute("SELECT AVG(salary) FROM vacancies;")
        result = self.cur.fetchone()
        return round(result[0], 2)

    def get_vacancies_with_higher_salary(self):
        self.cur.execute(
            f"SELECT * FROM vacancies WHERE salary > {self.get_avg_salary()}"
        )
        rows = self.cur.fetchall()
        return rows

    def get_vacancies_with_keyword(self, keyword):
        self.cur.execute(
            f"SELECT * FROM vacancies WHERE vacancy_title LIKE '%{keyword[1:]}%'"
        )
        rows = self.cur.fetchall()
        return rows
