from datetime import datetime
from typing import Any, List


class DataValidation:
    def __init__(self, response: Any) -> None:
        self.response = response

    def load_vacancy_sj(self) -> List[dict]:
        """
        Создание списка вакансий с нужными данными из SuperJob.ru.
        """
        vacancies = []
        try:
            for vacancy in self.response.get("objects", []):
                published_at = datetime.fromtimestamp(vacancy.get("date_published", ""))
                super_job = {
                    "id": vacancy.get("id", ""),
                    "name": vacancy.get("profession", ""),
                    "salary_ot": vacancy.get("payment_from", None),
                    "salary_do": vacancy.get("payment_to", None),
                    "responsibility": vacancy.get("candidat", "").replace("\n", "").replace("•", ""),
                    "data": published_at.strftime("%d.%m.%Y"),
                    "link": vacancy.get("link", None),
                }
                vacancies.append(super_job)
            return vacancies
        except Exception as error:
            print(f"Ошибка при загрузке вакансий с SuperJob: {error}")
            return []

    def load_vacancy_hh(self) -> List[dict]:
        """
        Создание списка вакансий с нужными данными из hh.ru.
        """
        vacancies = []
        try:
            for vacancy in self.response.get("items", []):
                published_at = datetime.strptime(vacancy.get("published_at", ""), "%Y-%m-%dT%H:%M:%S%z")
                vacancy_info = {
                    "id": vacancy.get("id", ""),
                    "name": vacancy.get("name", ""),
                    "salary_ot": vacancy["salary"].get("from", None) if vacancy.get("salary") else None,
                    "salary_do": vacancy["salary"].get("to", None) if vacancy.get("salary") else None,
                    "responsibility": vacancy["snippet"].get("responsibility", ""),
                    "data": published_at.strftime("%d.%m.%Y"),
                    "link": vacancy.get("alternate_url", None),
                }
                vacancies.append(vacancy_info)
            return vacancies
        except Exception as error:
            print(f"Ошибка при загрузке вакансий с HeadHunter: {error}")
            return []

    @staticmethod
    def get_top_vacancies(vacancies: list) -> list:
        top_5_vacancies = sorted(vacancies, key=lambda x: x.get("salary", {}).get("from", 0), reverse=True)[:5]
        return top_5_vacancies
