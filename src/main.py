from data.list_of_companies import companies
from src.DataBase import DBCreater, DBManager

# Получение списка выбранных компаний
companies = companies


def main():
    """Основная функция взаимодействия с пользователем"""

    # Создание и заполнение таблиц в базе данных

    data_base = DBCreater("Course_5_work", companies)
    data_base.companies_table()
    cur_tables_vac = data_base.vacancies_table()
    my_manager = DBManager(cur_tables_vac)

    # Получение данных из таблиц базы данных

    result_0 = my_manager.get_all_vacancies()
    result_1 = my_manager.get_companies_and_vacancies_count()
    result_2 = my_manager.get_avg_salary()
    result_4 = my_manager.get_vacancies_with_higher_salary()

    starter = 1
    print("Здравствуйте!")
    while starter == 1:
        try:
            info_to_show = int(
                input(
                    """
            Выберите команду:
            1. Получить список всех компаний и количество вакансий у каждой компании.
            2. Получить список всех вакансий.
            3. Получить среднюю зарплату по вакансиям.
            4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
            5. Получить список всех вакансий, в названии которых содержатся ключевое слово. \n"""
                )
            )
        except ValueError:
            print("Некорректный ввод команды. Попробуйте еще раз.")
            continue

        if info_to_show == 1:
            for row in result_1:
                print(f"Компания - {row[0]}, {row[1]} вакансий")
            starter -= 1
        elif info_to_show == 2:
            for row in result_0:
                print(
                    f"Вакансия:\n{row[0]}\nКомпания:\n{row[1]}\nЗарплата:\n{row[2]} руб.\nСсылка:\n{row[3]}\n"
                )
            starter -= 1
        elif info_to_show == 3:
            print(f"Средняя зарплата по вакансиям: \n{result_2} руб.")
            starter -= 1
        elif info_to_show == 4:
            for row in result_4:
                print(
                    f"Вакансия:\n{row[1]}\nЗарплата:\n{row[3]} руб.\nСсылка:\n{row[2]}\nСтатус:\n{row[4]}\n"
                )
            starter -= 1
        elif info_to_show == 5:
            keyword = input("Введите ключевое слово для поиска вакансий: \n")
            result_3 = my_manager.get_vacancies_with_keyword(keyword)
            for row in result_3:
                print(
                    f"Вакансия:\n{row[1]}\nЗарплата:\n{row[3]} руб.\nСсылка:\n{row[2]}\nСтатус:\n{row[4]}\n"
                )
            if len(result_3) == 0:
                print("По Вашему запросу не найдено ни одной вакансии.")
            starter -= 1
        else:
            print("Некорректный ввод команды. Попробуйте еще раз.")
            continue


if __name__ == "__main__":
    main()
