import time

from termcolor import cprint

import promopages as pp
import setup
from google_sheets import GooglesheetPromopages

cprint('Укажите диапазон, за который получить статистику. Формат даты: гггг-мм-дд', color='yellow')
start_date = input('Введите начальную дату (гггг-мм-дд): ')
end_date = input('Введите конечную дату (гггг-мм-дд): ')

print('Обращаемся к гугл таблице и получаем информацию о клиентах')
# Получение основных данных для последующего получения статистики по звонкам

# определяем лист с клиентами для промостраниц
worksheet_with_clients = setup.worksheet_for_promopages_with_a_list_of_clients
# определяем лист, куда будем складывать статистику
worksheet_for_update_statistic_promopages = setup.worksheet_for_promopages
promopages = GooglesheetPromopages(worksheet=worksheet_with_clients)
google_sheet = GooglesheetPromopages(worksheet=worksheet_for_update_statistic_promopages)
clients = promopages.get_clients()  # получаем список клиентов из google таблицы

row = 2  # строка, с которой будем начинать заносить статистику в гугл таблицу

for client in clients:
    # запрос на создание отчета
    client_name = client[0]  # имя клиента
    client_id = client[1]  # id клиента
    campaigns = client[2]  # id рекламных кампаний

    print(f'Создаем отчет для клиента {client_name}')

    report_id = pp.create_report(client_id, campaigns, start_date, end_date)
    # report_id = '656f39bb835fb165ab4f3685'  # пример отчета для тестирования 2023-12-03 Лесной мир
    print(client[0], report_id)

    print('Спим 30 секунд')
    time.sleep(30)

    # Получаем статистику по id отчета за все дни и за все РК
    print("Получаем статистику по id отчета")
    response = pp.get_report(report_id)

    # Разбиваем статистику по дням
    statistics_by_day = pp.statistics_handler(client_name, response)

    print(f'Статистика по {client_name} получена')
    print(statistics_by_day)
    if not statistics_by_day:
        cprint('Статистика пустая', color='red')
        continue

    # Заносим полученную статистику в гугл таблицу
    print('Начинаем обновление Гугл таблицы')
    row = google_sheet.update_promopages_statistic(data=statistics_by_day, row=row)
    print('Спим 10 секунд')
    time.sleep(10)

cprint(f'Статистика за период с {start_date} по {end_date} успешно обновлена', color='green')
