import json
import time

import requests
from termcolor import cprint

import setup

HEADERS = {
    'Content-Type': 'application/json; charset=utf-8',
    'Authorization': f'OAuth {setup.yaTokenPromopages}'
}


def create_report(client_id: str, campaigns: list, date_from: str, date_to: str) -> str:
    """
    Запрос на создание отчета за определенную дату.
    Функция принимает данные по клиенту (id клиента, id рекламных кампаний
    и даты, за которые получить отчет) и создает запрос на создание отчета. В отчет получает id отчета, который
    в дальнейшем может быть получен отдельным запросом.

    @param client_id: str, id клиента
    @param campaigns: list[str], список id рекламных кампаний
    @param date_from: str, начальная дата
    @param date_to: str, конечная дата

    @return report_id: str, id подготовленного отчета от Яндекса
    """
    request_parameters = {
        "publisherId": client_id,
        "campaignIds": campaigns,
        "mskDateFrom": date_from,
        "mskDateTo": date_to
    }

    response_data = requests.post(
        "https://promopages.yandex.ru/api/promo/v1/reports/campaigns-daily-stats",
        headers=HEADERS,
        data=json.dumps(request_parameters),
    )
    return response_data.json()["reportId"]


def get_report(reportid: str):
    """
    Функция, принимающая на вход id отчета промостраниц и возвращающая подготовленный отчет в виде списка словарей,
    разбитых по рекламным кампаниям и датам.

    @param reportid: str, id отчета яндекс промостраниц

    @return список словарей.
    Пример:
        [
          {'campaignId': '655bc606985e8d44fb3f3fa7', 'mskDate': '2023-12-03',...},
          {'campaignId': '655bc606985e8d44fb3f3fa7', 'mskDate': '2023-12-04',...},
          {'campaignId': '65670cb673668f53ead342d6', 'mskDate': '2023-12-03',...},
          ...
        ]
    """
    run_cycle = True
    while run_cycle:
        response_data = requests.get(f"https://promopages.yandex.ru/api/promo/v1/reports/{reportid}?format=json",
                                     headers=HEADERS)
        if response_data.status_code == 200:
            print(response_data.text)
            return response_data.json()["statistics"]
        else:
            print(response_data.status_code)
            cprint('Отчет еще не готов, спим 15 секунд и пробуем снова', color='red')
            time.sleep(15)


def statistics_handler(client_name, stat_data):
    """
    Функция разбивает статистику по дням
    """
    stat = {}

    for i in stat_data:
        # [показы(impressions),клики(clicks),просмотры(views),дочитывания(full_reads),переходы(clickouts),бюджет(budget)]
        stat.setdefault(i["mskDate"], [client_name] + [0] * 6)
        stat[i["mskDate"]][1] += i["impressions"]  # показы
        stat[i["mskDate"]][2] += i["clicks"]  # клики
        stat[i["mskDate"]][3] += i["views"]  # просмотры статьи
        stat[i["mskDate"]][4] += i["fullReads"]  # дочитывания
        stat[i["mskDate"]][5] += i["clickouts"]  # переходы на сайт
        stat[i["mskDate"]][6] += i["budget"]  # бюджет
    return stat
