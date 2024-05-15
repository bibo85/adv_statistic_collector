# -*- coding: utf-8 -*-

import requests
from termcolor import cprint
import setup

ACCESS_TOKEN = setup.yandex_token

url = 'https://api-metrika.yandex.net/stat/v1/data'

header_params = {
    'GET': '/management/v1/counters HTTP/1.1',
    'Host': 'api-metrika.yandex.net',
    'Authorization': 'OAuth ' + ACCESS_TOKEN,
    'Content-Type': 'application/x-yametrika+json',
    'Content-Length': '123'
}


def get_statistics_on_goals(metrika_id, goals, date_from, date_to):
    if goals:
        count_attempt = 0
        data = None
        while True:
            metrics = [f'ym:s:goal{goal}visits' for goal in goals]
            metrics = ', '.join(metrics)
            if count_attempt == 3:
                cprint('Скрипт не смог получить статистику, проверьте настройки в таблице с клиентами метрики',
                       color='red')
                break
            try:
                response = requests.get(url +
                                        "?" +
                                        f"ids={metrika_id}&metrics={metrics}" +
                                        "&dimensions=ym:s:date" +
                                        f"&date1={date_from}&date2={date_to}",
                                        headers=header_params, timeout=90)
            except Exception:
                cprint('Метрика не ответила. Пробуем снова', color='red')
                count_attempt += 1
                continue
            if response.status_code == 200:
                print('Получили ответ')
                data = response.json()['data']
                break
            cprint(f'Ответ не получен {response}', color='red')
            count_attempt += 1
        if data:
            return data
        else:
            return 0
