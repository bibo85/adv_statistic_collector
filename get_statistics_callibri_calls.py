# -*- coding: utf-8 -*-
import time

from termcolor import cprint

import setup
from callibri import get_call_statistics, get_site_statistics
from google_sheets import GoogleSheetsCalls
from input_date_handler import check_entered_dates, creating_date_range_by_week

# Ячейка с конечной датой, для которой получаем звонки
CELL = 'F1'

print('Обращаемся к гугл таблице и получаем информацию о клиентах')
# Получение основных данных для последующего получения статистики по звонкам
worksheet = setup.name_worksheet_for_calls  # определяем рабочий лист
update_callibri_calls = GoogleSheetsCalls(worksheet=worksheet)
end_date = update_callibri_calls.get_cell_value(CELL)  # конечная дата
clients = update_callibri_calls.get_list_clients()  # получаем список клиентов из google таблицы
print('\nИнформация о клиентах успешно получена')

# Получаем статистику по каждому клиенту
call_statistics = []  # общая статистика по всем строкам

for client in clients:
    # Client: ['Имя_клиента', 'id_клиента', 'дата', строка].
    # Пример: ['Модуль дом', '52523', '12.10.2021', 4]
    # Основная информация о клиенте
    client_name = client[0]
    client_id = client[1]
    start_date = client[2]
    client_row = client[3]

    print(f'Получаем статистику по клиенту {client_name}')

    # проверяем даты и формируем диапазоны понедельно для дальнейшего получения статистики
    result_of_checking = check_entered_dates(start_date=start_date, end_date=end_date)
    if result_of_checking:
        cprint('Проверьте корректность введенных данных в ячейках Начало периода и конечной даты', color="red")
        continue

    # получаем список с датами по неделям [['05.02.2024', '11.02.2024'], ['12.02.2024', '18.02.2024']...]
    dates = creating_date_range_by_week(start_date=client[2], end_date=end_date)

    first_calls = 0
    adv_calls = 0
    for date in dates:
        site_statistic = get_site_statistics(site_id=client_id, date_from=date[0], date_to=date[1])

        time.sleep(1)

        if site_statistic:
            # собираем статистику по звонкам
            f_calls, a_calls = get_call_statistics(site_statistic[0]['calls'])
            first_calls += f_calls
            adv_calls += a_calls

    call_statistics.append([client_name, client_row, first_calls, adv_calls])

print('Статистика получена')

time.sleep(1)

print('Начинаем обновление Гугл таблицы')
update_callibri_calls.update_call_callibri_statistic(call_statistics)

cprint('Статистика по общему количеству звонков обновлена', color='green')
