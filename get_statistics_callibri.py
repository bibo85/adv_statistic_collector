# -*- coding: utf-8 -*-
import time

from termcolor import cprint

import setup
from callibri import (get_active_sites, get_call_statistics,
                      get_mail_statistics, get_site_statistics,
                      get_statistics_on_orders)
from google_sheets import GoogleSheetsUpdater
from input_date_handler import creating_date_range, get_dates_info

cprint('Укажите диапазон, за который получить статистику. Формат даты: дд.мм.гггг', color='yellow')

# получаем начальную и конечную дату и создаем список дат
start_date, end_date = get_dates_info()
dates = creating_date_range(start_date, end_date)  # ['26.11.2021', '27.11.2021', '28.11.2021', '29.11.2021']
row = 2

for date in dates:
    print('Получаем статистику за', date)
    # получение списка активных сайтов
    active_sites = get_active_sites()
    time.sleep(1)

    callibri_statistics = []
    for site in active_sites:
        # получение статистики по конкретным сайтам
        print('Получаем статистику по проекту:', site['sitename'])
        site_statistic = get_site_statistics(site_id=str(site['site_id']), date_from=date, date_to=date)
        time.sleep(1)

        if site_statistic:
            first_calls, adv_calls = get_call_statistics(site_statistic[0]['calls'])
            first_orders, adv_orders = get_statistics_on_orders(site_statistic[0]['feedbacks'])
            first_emails, adv_emails = get_mail_statistics(site_statistic[0]['emails'])

            # добавляем собранную статистику в общий словарь
            callibri_statistics.append(
                [site['domains'], date,
                 first_calls, adv_calls,
                 first_orders, adv_orders,
                 first_emails, adv_emails])
        else:
            callibri_statistics.append([site['domains'], date, 0, 0, 0, 0, 0, 0])

    print(f'Статистика за {date} получена')
    time.sleep(1)
    print('Начинаем обновление Гугл таблицы')

    worksheet = setup.name_worksheet  # определяем рабочий лист
    google_sheet = GoogleSheetsUpdater(worksheet=worksheet)
    google_sheet.update_callibri_statistic(data=callibri_statistics, row=row)
    row += len(active_sites)
cprint(f'Статистика за период с {start_date} по {end_date} успешно обновлена', color='green')
