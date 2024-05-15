import time

import requests
from termcolor import cprint

import setup


def get_site_statistics(site_id, date_from, date_to):
    count_attempt = 0
    data = None
    while True:
        time.sleep(count_attempt * 5)
        if count_attempt > 2:
            break
        try:
            response_site_statistics = requests.get(
                'https://api.callibri.ru/site_get_statistics'
                + '?'
                + f'site_id={site_id}&date1={date_from}&date2={date_to}'
                + setup.connect_token, timeout=60)
            if response_site_statistics.status_code == 200:
                data = response_site_statistics.json()['channels_statistics']
                break
        except requests.exceptions.RequestException as exc:
            cprint('Callibri не ответил, пробуем снова', color='red')
            print('Текст ошибки:', exc)
            count_attempt += 1
            continue
    return data


def get_active_sites():
    """
    Получение списка активных сайтов
    :return: список словарей с активными сайтами
    [{'active': 'true',
      'domains': 'okna-online116.ru',
      'site_id': 31640,
      'sitename': 'ЭкоДом Окна'}, ...]
    """
    response_sites = requests.get(
        'https://api.callibri.ru/get_sites'
        + '?'
        + setup.connect_token)
    sites_data = response_sites.json()['sites']
    active_sites_data = [site for site in sites_data if site['active'] == 'true']
    return active_sites_data


def get_call_statistics(call_data):
    # получаем общее количество звонков и количество звонков по рекламе
    primary = [call for call in call_data if call['is_lid']
               and call['status'] not in ('тест', 'Тест', 'ТЕСТ')]
    advertising = [call for call in call_data
                   if call['is_lid'] is True
                   and call['status'] not in ('тест', 'Тест', 'ТЕСТ')
                   and (call['traffic_type'] == 'Переходы по рекламе'
                        or call['source'] == 'Yandex Direct')]
    without_source = [call for call in call_data if call['is_lid']
                      and call['source'] is None
                      and call['status'] not in ('тест', 'Тест', 'ТЕСТ')]

    return len(primary), len(advertising) + len(without_source)


def get_statistics_on_orders(orders_data):
    # получаем общее количество заявок и количество заявок по рекламе
    primary = [order for order in orders_data if order['is_lid'] is True
               and order['status'] not in ('тест', 'Тест', 'ТЕСТ')]
    advertising = [order for order in orders_data
                   if order['is_lid'] is True
                   and order['status'] not in ('тест', 'Тест', 'ТЕСТ')
                   and (order['traffic_type'] == 'Переходы по рекламе'
                        or order['source'] == 'Yandex Direct')]
    without_source = [order for order in orders_data if order['is_lid']
                      and order['source'] is None
                      and order['status'] not in ('тест', 'Тест', 'ТЕСТ')]

    return len(primary), len(advertising + without_source)


def get_mail_statistics(emails_data):
    # получаем общее количество отправленных email и количество email по рекламе
    primary = [email for email in emails_data if email['is_lid'] is True
               and email['status'] not in ('тест', 'Тест', 'ТЕСТ')]
    advertising = [email for email in emails_data
                   if email['is_lid'] is True
                   and email['status'] not in ('тест', 'Тест', 'ТЕСТ')
                   and (email['traffic_type'] == 'Переходы по рекламе'
                        or email['source'] == 'Yandex Direct')]
    without_source = [email for email in emails_data if email['is_lid']
                      and email['source'] is None
                      and email['status'] not in ('тест', 'Тест', 'ТЕСТ')]

    return len(primary), len(advertising + without_source)
