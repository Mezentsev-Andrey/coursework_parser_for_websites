import os
from abc import ABC, abstractmethod
from typing import Any

import requests  # type: ignore


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сайтов с вакансиями.
    """

    @abstractmethod
    def connect_get_vacancies(self) -> Any:
        pass


class VacancyParams:
    """
    Параметры для поисков вакансий.
    """

    def __init__(self, vacancy_name: str, sorting: Any, payment_from: int):
        self.vacancy_name = vacancy_name
        self.sorting = sorting
        self.payment_from = payment_from

    def __repr__(self) -> str:
        """
        Вывод введенной вакансии.
        """
        return f"{self.vacancy_name}"


class SuperJobAPI(VacancyParams, VacancyAPI):
    """
    Класс для получения вакансий с сайта Superjob по критериям пользователя.
    """

    def __init__(self, vacancy_name: str, sorting: str, payment_from: int) -> None:
        super().__init__(vacancy_name, sorting, payment_from)
        self.headers = {"X-Api-App-Id": os.getenv("SUPER_JOB_API_KEY")}
        self.url = "https://api.superjob.ru/2.0/vacancies"

    def connect_get_vacancies(self) -> Any:
        """
        Реализация подключения к API SuperJob и получение данных в json формате.
        """
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                params={
                    "keywords": self.vacancy_name,
                    "order_field": self.sorting,
                    "payment_from": self.payment_from,
                    "count": 100,
                },
            ).json()
            return response
        except requests.RequestException as error:
            print(f"Ошибка в запросе к SuperJob API: {error}")


class HeadHunterAPI(VacancyParams, VacancyAPI):
    """
    Класс для получения вакансий с сайта HeadHunter по критериям пользователя.
    """

    def __init__(self, vacancy_name: str, sorting: str, payment_from: int) -> None:
        super().__init__(vacancy_name, sorting, payment_from)
        self.base_url = "https://api.hh.ru/vacancies"

    def connect_get_vacancies(self) -> Any:
        """
        Реализация подключения к API HeadHunter и получение данных в json формате.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/58.0.3029.110 Safari/537.3"
            }
            response = requests.get(
                self.base_url,
                headers=headers,
                params={
                    "text": self.vacancy_name,
                    "order_by": self.sorting,
                    "salary": self.payment_from,
                    "per_page": 100,
                },
            ).json()
            return response
        except requests.RequestException as error:
            print(f"Ошибка в запросе к HeadHunter API: {error}")
