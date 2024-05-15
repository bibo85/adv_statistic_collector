# -*- coding: utf-8 -*-
import datetime
import time

from termcolor import cprint

import setup
from google_sheets import GoogleSheetsMetrika
from metrika import get_statistics_on_goals

cprint('Укажите диапазон, за который получить статистику. Формат даты: гггг-мм-дд)', color='yellow')
start_date = input('Введите начальную дату (гггг-мм-дд): ')
end_date = input('Введите конечную дату (гггг-мм-дд): ')

print('Обращаемся к гугл таблице и получаем информацию о клиентах')
# Получение основных данных для последующего получения статистики по звонкам
worksheet = setup.name_worksheet_for_clients_metrika  # определяем рабочий лист
update_metrika = GoogleSheetsMetrika(worksheet=worksheet)
clients = update_metrika.get_list_clients()  # получаем список клиентов из гугл таблицы
# pprint(clients)

time.sleep(1)
metrika_statistics = []

for client in clients:
    time.sleep(3)
    statistic_for_goals = None
    print(f'\nПолучаем статистику по клиенту {client[0]}')
    try:
        metrika_id = client[1]
        goals = client[2]
        statistic_for_goals = get_statistics_on_goals(metrika_id, goals, start_date, end_date)
        time.sleep(1)
    except Exception as exc:
        print(f'Статистика по клиенту {client[0]} не получена. Ошибка: {exc}')
    print(f'Статистика по клиенту {client[0]} получена')
    print(statistic_for_goals)
    if statistic_for_goals:
        for goal_stat in statistic_for_goals:
            date = goal_stat['dimensions'][0]['name']
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            date = datetime.datetime.strftime(date, '%d.%m.%Y')
            metrika_statistics.append([client[0],
                                       client[1],
                                       date,
                                       int(sum(goal_stat['metrics'][:2])),
                                       int(sum(goal_stat['metrics'][2:-1])),
                                       int(goal_stat['metrics'][-1])])

print('Статистика получена')
# pprint(metrika_statistics)
print('Начинаем обновление Гугл таблицы')

worksheet = setup.name_worksheet_for_metrika  # определяем рабочий лист
google_sheet = GoogleSheetsMetrika(worksheet=worksheet)
google_sheet.update_metrika_statistic(data=metrika_statistics)
cprint(f'Статистика за период с {start_date} по {end_date} успешно обновлена', color='green')
