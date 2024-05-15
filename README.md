# Сбор статистики из Яндекс.Метрики, Яндекс.Промостраниц и Callibri

![Static Badge](https://img.shields.io/badge/python-3.11-blue)
![Static Badge](https://img.shields.io/badge/gspread-5.4.0-red)
![Static Badge](https://img.shields.io/badge/pandas-1.4.2-orange)
![Static Badge](https://img.shields.io/badge/requests-2.27.1-yellow)
![Static Badge](https://img.shields.io/badge/termcolor-1.1.0-purple)

# Документация
1. Все зависимости описаны в файле __requirements.txt__
2. В файле __instruction.txt__ прописана инструкция для получения json ключа для доступа к Google таблицам
3. Необходимо прописать настройки в файле ___setup.py__. После заполнения необходимо убрать нижнее подчеркивание в названии файла
```python
# Токен API Яндекса. Получаем здесь: https://yandex.ru/dev/id/doc/ru/how-to
yandex_token = ""

# Почта в сервисе callibri, она же является логином
callibri_email = ""
# Токен калибри. Инструкция по получению токена: https://callibri.ru/help/sinhronizatsii_i_api/kak_vospolzovatsya_api
callibri_token = ""

# !!!Не менять!!! Кусок url для подключения к API Callibri
connect_token = f'&user_email={callibri_email}&user_token={callibri_token}'

# Имя json ключа для подключения к Google таблицам. Ключ должен лежать в той же папке, что и все файлы.
# Получаем ключ по инструкции из файла instruction.txt
# Пример: callibri-statistics-6599e4bb45602.json
google_json = ''

# Токен для подключения к Яндекс.Промостраницам
yaTokenPromopages = ""

# Главная рабочая таблица, откуда берутся данные и куда складывается собранная статистика
# Пример: https://docs.google.com/spreadsheets/d/1NsL_AI0sapHoAt1Wtsd3447dxmtcFqOUNq25w3e_8/edit#gid=134123123052
url_sheet = ''

# Название листа, куда будет складываться полученная статистика из Callibri.
# Пример: "Получение данных Callibri"
name_worksheet = ''

# Название листа, где обновляется количество звонков по каждому клиенту
name_worksheet_for_calls = 'Calls'

# Название листа со списком клиентов, для которых необходимо собирать статистику из Яндекс.Метрики.
# Пример: "Клиенты для метрики"
name_worksheet_for_clients_metrika = ''

# Название листа, куда будет складываться полученная статистика из Яндекс.Метрики.
# Пример: "Получение данных метрики"
name_worksheet_for_metrika = ''

# Название листа со списком клиентов по Промостраницам, для которых необходимо собирать статистику.
# Пример: "Список клиентов по Promopages"
worksheet_for_promopages_with_a_list_of_clients = ''

# Название листа, куда будут складываться полученные данных по промостраницам.
# Пример: "Полученные данные Promopages"
worksheet_for_promopages = ''
```
4. Предоставляем доступ на редактирование в рабочие Google таблицы для почты сервисного аккаунта гугла, который создали по инструкции. Пример такой почты: parser@parser377917.iam.gserviceaccount.com

# Скрипты
1. Для сбора статистики по звонкам по каждому клиенту за определенный период запускаем файл [get_statistics_callibri.py](get_statistics_callibri.py)
2. Для сбора текущего количества звонков по клиенту на текущий момент запускаем [get_statistics_callibri_calls.py](get_statistics_callibri_calls.py)
3. Для сбора статистики по клиентам из метрики за определенный период запускаем [get_statistics_metrika.py](get_statistics_metrika.py)
4. Для сбора статистики по клиентам в промостраницах запускаем [get_statistics_promopages.py](get_statistics_promopages.py)
