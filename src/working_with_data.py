import json
from abc import ABC, abstractmethod


class VacancyManager(ABC):
    """
    Абстрактный класс для работы с полученными вакансиями.
    """

    @abstractmethod
    def save_vacancies(self) -> None:
        """
        Запись данных в файл.
        """
        pass

    @abstractmethod
    def delete_vacancies(self, user_id: str) -> None:
        """
        Удаление данных из файла по id.
        """
        pass

    @abstractmethod
    def adding_data(self) -> None:
        """
        Добавление вакансий в существующий файл.
        """
        pass


class ReadWriteFile(VacancyManager):
    """
    Чтение и запись вакансий в json-файл.
    """

    def __init__(self, data: list) -> None:
        self.data = data

    def save_vacancies(self) -> None:
        """
        Запись списка вакансий в файл json.
        """
        with open("vacancies_for_you.json", "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)

    def delete_vacancies(self, user_id: str) -> None:
        """
        Удаление вакансии по id.
        """
        try:
            with open("vacancies_for_you.json", "r", encoding="utf-8") as file:
                initial_data = json.load(file)

            new_list = [vacancy for vacancy in initial_data if vacancy.get("id") != user_id]

            with open("vacancies_for_you.json", "w", encoding="utf-8") as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as error:
            print(f"Ошибка при декодировании JSON: {error}")
        except FileNotFoundError:
            print("Файл не найден.")
        except Exception as error:
            print(f"Необработанная ошибка: {error}")

    def adding_data(self) -> None:
        """
        Добавление вакансий к списку в файле json.
        """
        try:
            with open("vacancies_for_you.json", "r", encoding="utf-8") as file:
                initial_data = json.load(file)

            new_list = initial_data + self.data

            with open("vacancies_for_you.json", "w", encoding="utf-8") as file:
                json.dump(new_list, file, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as error:
            print(f"Ошибка при декодировании JSON: {error}")
        except FileNotFoundError:
            print("Файл не найден.")
        except Exception as error:
            print(f"Необработанная ошибка: {error}")
