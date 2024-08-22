from abc import ABC, abstractmethod

import requests

from data.list_of_companies import companies


class Parser(ABC):
    """Абстрактный класс определяющий методы класса ApiConnect"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def parsing(self):
        pass


class ApiConnect(Parser):
    """Класс для подключения к стороннему API сайта HH.ru"""

    def __init__(self, employer_id):
        self.employer_id = employer_id
        self.__url = f"https://api.hh.ru/vacancies?employer_id={self.employer_id}"
        self.__headers = {"User-Agent": "HH-User-Agent"}

    def parsing(self):
        result = requests.get(self.__url)
        if result.status_code == 200:
            return result.json()
        else:
            print("Ошибка подключения к стороннему API")
            return []


companies = companies


class VacanciesInfo:
    """Класс получающий информацию о вакансиях компаний из списка компаний"""

    def __init__(self, companies_list):
        self.companies_dict = {}
        self.companies = companies_list

    def list_vacancies(self):
        for a, i in self.companies.items():
            vacancies_list = []
            results = ApiConnect(i)
            par = results.parsing()
            for vacancy in par["items"]:
                vacancies_list.append(vacancy)
            self.companies_dict.update({a: vacancies_list})
        return self.companies_dict
