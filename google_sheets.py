# -*- coding: utf-8 -*-
import gspread
from gspread.cell import Cell

import setup


class GoogleSheets:

    def __init__(self, worksheet):
        self.gc = gspread.service_account(filename=setup.google_json)  # Указываем путь к JSON с ключами
        self.sh = self.gc.open_by_url(setup.url_sheet)  # открывает таблицу
        self.worksheet = self.sh.worksheet(worksheet)  # определяем рабочий лист

    def get_cell_value(self, cell):
        val = self.worksheet.acell(cell).value
        return val


class GoogleSheetsUpdater(GoogleSheets):

    def __init__(self, worksheet):
        super().__init__(worksheet)
        # self.worksheet = self.sh.worksheet(setup.name_worksheet)  # открываем нужный лист

    def update_callibri_statistic(self, data, row):
        cells = []
        row = row
        for row_data in data:
            for i in range(len(row_data)):
                cells.append(Cell(row=row, col=i + 1, value=row_data[i]))
            row += 1
        self.worksheet.update_cells(cells, value_input_option='USER_ENTERED')
        print('Статистика успешно обновлена')


class GoogleSheetsCalls(GoogleSheets):

    def __init__(self, worksheet):
        super().__init__(worksheet)
        # self.worksheet = self.sh.worksheet(setup.name_worksheet_for_calls)  # открываем нужный лист

    def get_list_clients(self):
        client_data = self.worksheet.get('A2:C250')
        clients = []
        for i in range(len(client_data)):
            if len(client_data[i]) == 3 and client_data[i][1] and client_data[i][2]:
                client_name = client_data[i][0]
                client_id = client_data[i][1]
                date_start = client_data[i][2]
                clients.append([client_name, client_id, date_start, i + 2])
                print(client_name)
        return clients

    def update_call_callibri_statistic(self, data):
        cells = []
        for row_data in data:
            cells.append(Cell(row=row_data[1], col=4, value=row_data[2]))
            cells.append(Cell(row=row_data[1], col=5, value=row_data[3]))
        # print(cells)
        self.worksheet.update_cells(cells)
        print('Статистика успешно обновлена')


class GoogleSheetsMetrika(GoogleSheets):
    """
    Работа с google таблицами метрики. Получение списка клиентов, по которым необходимо обновить статистику, и
    выгрузка полученной статистики из метрики в отдельную гугл таблицу.

    Методы:
    get_list_clients - получение списка клиентов
    update_metrika_statistic - выгрузка полученной статистики в гугл таблицу
    """

    def __init__(self, worksheet):
        super().__init__(worksheet)

    def get_list_clients(self):
        clients_data = self.worksheet.get('A2:G300')
        clients = []
        for i in range(len(clients_data)):
            if len(clients_data[i]) > 1 and clients_data[i][1] and clients_data[i][2]:
                client_name = clients_data[i][0].strip()
                metrika_id = clients_data[i][2]
                goals = f'{clients_data[i][5]};{clients_data[i][6]}'
                goals = [] if goals is None else goals.split(';')
                clients.append([client_name, metrika_id, goals])
                print(client_name)
        return clients

    def update_metrika_statistic(self, data):
        row = 2
        cells = []
        for row_data in data:
            for i in range(len(row_data)):
                cells.append(Cell(row=row, col=i + 1, value=row_data[i]))
            row += 1
        self.worksheet.update_cells(cells, value_input_option='USER_ENTERED')
        print('Статистика успешно обновлена')


class GooglesheetPromopages(GoogleSheets):
    """
    Работа с google таблицами промостраниц.
    Методы:
    get_clients - Получение списка клиентов, для которых необходимо собрать статистику.
    update_promopages_statistic - Добавление полученной статистики по промостраницам в гугл таблицу
    """

    def __init__(self, worksheet):
        super().__init__(worksheet=worksheet)

    def get_clients(self):
        clients_data = self.worksheet.get('A2:D60')
        clients_promopages = []
        for client in clients_data:
            if len(client) > 0 and client[0] == 'active':
                name = client[1]
                client_id = client[2]
                campaign_ids = client[3:][0].split(',')
                clients_promopages.append([name, client_id, campaign_ids])
                print(name)
        return clients_promopages

    def update_promopages_statistic(self, data: dict, row):
        current_row = row
        cells = []
        for key, value in data.items():
            row_data: list = value
            row_data.insert(1, key)
            for i in range(len(row_data)):
                cells.append(Cell(row=current_row, col=i + 1, value=row_data[i]))
            current_row += 1
        self.worksheet.update_cells(cells, value_input_option='USER_ENTERED')
        print('Статистика по клиенту успешно обновлена')
        return current_row
