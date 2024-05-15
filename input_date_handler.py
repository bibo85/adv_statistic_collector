# -*- coding: utf-8 -*-
import datetime as dt

import pandas as pd


class CustomException(Exception):
    pass


def creating_date_range_by_week(start_date: str, end_date: str):
    """
    Создание диапазона дат по неделям

    @return dates - список списков с датами по неделям
    [['05.02.2024', '11.02.2024'], ['12.02.2024', '18.02.2024'], ['19.02.2024', '25.02.2024']]
    """
    dates = []
    # преобразуем даты в формате строк
    start_date = dt.datetime.strptime(start_date, "%d.%m.%Y")
    end_date = dt.datetime.strptime(end_date, "%d.%m.%Y")
    # создаем периоды длиной в 7 дней, пока не появится промежуток короче
    while (start_date + dt.timedelta(days=6)) <= end_date:
        intermediate_date = start_date + dt.timedelta(days=6)  # создаем промежуточную дату +6 дней
        # переводим даты обратно в строки и записываем в словарь с промежутками
        date1 = dt.datetime.strftime(start_date, "%d.%m.%Y")
        date2 = dt.datetime.strftime(intermediate_date, "%d.%m.%Y")
        dates.append([date1, date2])
        # сдвигаем стартовую и промежуточную дату
        start_date = intermediate_date + dt.timedelta(days=1)
    # записываем последний промежуток, если в нем остался минимум 1 день
    if start_date <= end_date:
        start_date = dt.datetime.strftime(start_date, "%d.%m.%Y")
        end_date = dt.datetime.strftime(end_date, "%d.%m.%Y")
        dates.append([start_date, end_date])
    return dates


def creating_date_range(date_from, date_to):
    """
    Создание диапазона дат за период с date_from по date_to

    @return date_range: list - список дат в формате "dd.mm.yyyy".
    ['26.11.2021', '27.11.2021', '28.11.2021', '29.11.2021']
    """
    res = pd.date_range(
        min(date_from, date_to),
        max(date_from, date_to)
    ).strftime('%d.%m.%Y').tolist()
    return res


def check_entered_dates(start_date, end_date):
    """
    Проверка дат на корректность
    """
    try:
        start_date = dt.datetime.strptime(str(start_date), "%d.%m.%Y")
        end_date = dt.datetime.strptime(str(end_date), "%d.%m.%Y")
        if end_date < start_date:
            raise CustomException('Конечная дата не может быть раньше начальной. Повторите ввод')
    except ValueError:
        return 'Формат даты дд.мм.гггг. Повторите ввод'
    except CustomException as exc:
        return exc.args[0]


def get_dates_info():
    """
    Функция получает начальную и конечную дату от пользователя.

    @return start_date, end_date: <class 'datetime.datetime'> - возвращается начальная и конечная дата
    Пример: 2024-02-05 00:00:00, 2024-02-11 00:00:00
    """
    while True:
        start_date = input('Введите начальную дату (дд.мм.гггг): ')
        end_date = input('Введите конечную дату (дд.мм.гггг): ')

        result_check = check_entered_dates(start_date, end_date)
        if result_check:
            print(result_check)
            continue
        break
    print('Даты проверены и корректны')
    start_date = dt.datetime.strptime(start_date, "%d.%m.%Y")
    end_date = dt.datetime.strptime(end_date, "%d.%m.%Y")
    return start_date, end_date
