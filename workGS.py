import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger
from dataclasses import dataclass
from pprint import pprint
import time
from tqdm import tqdm
class Sheet():

    @logger.catch
    def __init__(self, jsonPath: str, sheetName: str,  servisName: str = None):

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            jsonPath, self.scope)  # Секретынй файл json для доступа к API
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open(
            sheetName).sheet1  # get_worksheet(0)  # Имя таблицы

    @logger.catch
    def send_cell(self, cell: str, value, form: bool = False):
        """
            [cell]: str - адрес ячейки 
                Например: "A1" или если [form] == True ([1, 2], 'value')
            [form]: bool = False - обозначение ячейки текстом или цифрами
                Например: True с цифрами ([1, 2], value) False текстом ('A1', value)
        value_input_option='USER_ENTERED' - иногда данные вставляются с ковычкой в начале это решает проблемму
        """
        if form:
            self.sheet.update_cell(
                cell[0], cell[1], value, value_input_option='USER_ENTERED')
        else:
            # update(cell, value)
            # value_input_option='USER_ENTERED')
            self.sheet.update(cell, value)

    def get_cell(self, i, n):
        value = self.sheet.cell(i, n).value
        return value

    def get_rom_value(self, i):
        """
        1 - первая строка
        """
        return self.sheet.row_values(i)
    
    def get_gs_text(self):
        allText = '\n\n<Описание Проектов>'
        urls={}
        b =1
        for i in tqdm(range(2,118)):
            #print(f'{b=}')
            #TODO удалить потом
            #if b == 2: 
            #    return allText, urls
            text = self.get_rom_value(i)
            time.sleep(1.2)
            a, url= prepare_text(text)
            allText += a
            urls.update(url)
            b += 1
        return allText, urls

@dataclass
class table:
    #номер колонки
    numberPP= '1'
    A :int = 0
    B :int = 1
    C :int = 2
    D :int = 3
    E :int = 4
    F :int = 5
    G :int = 6
    H :int = 7
    I :int = 8
    J :int = 9
    K :int = 10
    L :int = 11
    M :int = 12
    
def prepare_text(lst:list):
    text = ''
    urls = {}
    try:
        lst[table.H]=lst[table.H].replace('\xa0', ' ')
        lst[table.I]=lst[table.I].replace('\xa0', ' ')
        lst[table.J]=lst[table.J].replace('\xa0', ' ')
    except Exception as e:
        print('ошибка в GS prepare_text ',e)
        text = f"""
<Проект: {lst[table.C]}>""" 
        return text
    
    text = f"""
<Проект: {lst[table.C]}>

м.кв.: {lst[table.F]}

Количество этажей: {lst[table.D]}
Стиль: {lst[table.E]}

{lst[table.G]}
{lst[table.H]}

Стоимость {lst[table.C]}:
ЗК: {lst[table.J]}
ТК: {lst[table.K]}
ВО: {lst[table.L]}

Фото проекта:{lst[table.C]}
{lst[table.I]}
    """
    print(f'{text=}')
    urls.setdefault(lst[table.C], lst[table.I])
    return text,urls 



if __name__ == '__main__':
    json = 'kgtaprojects-8706cc47a185.json'
    sheet = Sheet(json,'цены на дома 4.0 актуально ')
    a = sheet.get_rom_value(113) 
    a = prepare_text(a)
    pprint(a)