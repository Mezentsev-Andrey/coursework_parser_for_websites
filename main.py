import json
from pprint import pprint
from typing import Any

from src.api import HeadHunterAPI, SuperJobAPI
from src.working_with_data import ReadWriteFile
from src.working_with_vacancies import DataValidation


def select_platform() -> str:
    """
    Выбор платформы для поиска вакансий.
    """
    while True:
        platform = input(
            """Выберете цифру для поиска:
        1 - HeadHunter
        2 - SuperJob
        """
        )
        if platform in ("1", "2"):
            return platform
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2.")


def select_sorting() -> str:
    """
    Выбор сортировки для поиска вакансий.
    """
    while True:
        sorting = input(
            """Укажите сортировку: Дата/Зарплата
        """
        ).lower()
        if sorting in ("дата", "зарплата"):
            return "publication_time" if sorting == "дата" else "salary_desc"
        else:
            print("Неверный выбор. Пожалуйста, введите 'Дата' или 'Зарплата'.")


def get_activation_class(platform: str, sorting: str, vacancy_name: str, payment_from: int) -> Any:
    """
    Получение экземпляра класса в зависимости от выбранной платформы.
    """
    if platform == "1":
        if sorting == "дата":
            sorting = "publication_time"
        else:
            sorting = "salary_desc"
        return HeadHunterAPI(vacancy_name, sorting, payment_from)
    else:
        if sorting == "дата":
            sorting = "date"
        else:
            sorting = "payment"
        return SuperJobAPI(vacancy_name, sorting, payment_from)


def get_data_status() -> str:
    """
    Выбор статуса данных (создать новый файл / дополнить прежний)
    """
    while True:
        data_status = input(
            """Выберите действие:
        1. Создать новый файл
        2. Дополнить прежний (при условии уже выполненного ранее 1 пункта)
        """
        )
        if data_status in ("1", "2"):
            return data_status
        else:
            print("Неверный выбор. Пожалуйста, введите 1 или 2.")


def main() -> None:
    """
    Основная функция программы для взаимодействия с пользователем, поиска вакансий и работы с данными.
    """
    while True:
        platform = select_platform()
        vacancy_name = input(
            """Укажите профессию
        """
        )
        payment_from = int(
            input(
                """Укажите минимальную желаемую сумму зарплаты
        """
            )
        )

        sorting = select_sorting()

        activation_class = get_activation_class(platform, sorting, vacancy_name, payment_from)
        sending_request = activation_class.connect_get_vacancies()
        creation_of_vacancies = DataValidation(sending_request)
        vacancy_data = (
            creation_of_vacancies.load_vacancy_hh() if platform == "1" else creation_of_vacancies.load_vacancy_sj()
        )

        activating_class_for_record = ReadWriteFile(vacancy_data)

        data_status = get_data_status()
        if data_status == "1":
            activating_class_for_record.save_vacancies()
            print("Файл создан успешно")
        else:
            activating_class_for_record.adding_data()
            print("Файл дополнен успешно")

        while True:
            choice_to_delete = input(
                """Хотите удалить какую-либо вакансию из файла? Да/Нет
            """
            ).lower()
            if choice_to_delete == "да":
                vacancy_for_removal = input(
                    """Введите id вакансии для удаления
                """
                )
                activating_class_for_record.delete_vacancies(vacancy_for_removal)
                print("Успешно удалено")
            else:
                break

        continuation_of_the_cycle = input(
            """Хотите повторно сформировать список подходящих вакансий? Да/Нет
        """
        ).lower()
        if continuation_of_the_cycle == "нет":
            break

    selecting_console_output = input(
        """Вывести топ-5 вакансий по заработной плате в консоль? Да/Нет
    """
    ).lower()
    if selecting_console_output == "да":
        with open("Vacancies_for_you.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            pprint(DataValidation(data).get_top_vacancies(data))


if __name__ == "__main__":
    main()
