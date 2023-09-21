import gspread
from oauth2client.service_account import ServiceAccountCredentials
from loguru import logger
from dataclasses import dataclass
from pprint import pprint
import time
from tqdm import tqdm
import requests
class Sheet():
    
    @logger.catch
    def __init__(self, jsonPath: str, sheetName: str,  servisName: str = None, get_worksheet: int = 0):

        self.scope = ['https://spreadsheets.google.com/feeds',
                      'https://www.googleapis.com/auth/drive']
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            jsonPath, self.scope)  # Секретынй файл json для доступа к API
        self.client = gspread.authorize(self.creds)
        self.sheetAll = self.client.open(
            #sheetName).sheet1  # get_worksheet(0)  # Имя таблицы
            sheetName)
        self.sheet = self.client.open(
            #sheetName).sheet1  # get_worksheet(0)  # Имя таблицы
            sheetName).get_worksheet(get_worksheet)  # get_worksheet(0)  # Имя таблицы

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
            self.sheet.update(cell, value, value_input_option='USER_ENTERED')

    def get_cell(self, i, n):
        value = self.sheet.cell(i, n).value
        return value

    def get_rom_value(self, i):
        """
        1 - первая строка
        """
        return self.sheet.row_values(i)
    def get_words_and_urls(self):
        lst = []
        for i in tqdm(range(2,11)):
            value = self.get_rom_value(i)
            lst.extend(prepare_words(value))
            #print(f'{b=}')

        return lst

    # def get_gs_text(self):
    #     allText = '\n\n<Описание Проектов>'
    #     urls={}
    #     b =1
    #     for i in tqdm(range(2,118)):
    #         #print(f'{b=}')
    #         #TODO удалить потом
    #         #if b == 2: 
    #         #    return allText, urls
    #         text = self.get_rom_value(i)
    #         time.sleep(1.2)
    #         a, url= prepare_text(text)
    #         allText += a
    #         urls.update(url)
    #         b += 1
        return allText, urls

    def copy_sheet(self, name:str):
        # self.sheet.duplicate(insert_sheet_index=1, new_sheet_name=name) копия листа
        # self.client.copy('1Q5YXUfKD8-KV9hOWfagvv9dtGxGIGagmKeGnhQBRzmQ', title=name, copy_permissions=True)
        # worksheet = self.client.open(name)
        # worksheet.share("gerasimov.98.igor@gmail.com", perm_type='user', role='writer')
        # worksheet.share("kgta-34@kgtaprojects.iam.gserviceaccount.com", perm_type='user', role='writer')
        pass
    
    def export_pdf(self, namePdf):
        url = f'https://docs.google.com/spreadsheets/d/{self.sheetAll.id}/export?format=pdf&gid=829589704'
        print(f'{url=}')
        headers = {'Authorization': 'Bearer ' + self.creds.create_delegated("").get_access_token().access_token}
        res = requests.get(url, headers=headers)
        with open('pdfCalc/'+namePdf + ".pdf", 'wb') as f:
            f.write(res.content)

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

@logger.catch
def prepare_words(lst:list):
    text = ''
    l = []
    words = lst[table.A].split(',')
    words = [word.lower().strip() for word in words]
    #print(f'{words=}')
    words2 = lst[table.B].split(',')
    words2 = [word.strip() for word in words2]
    l.append({'words':words,
               'words2': words2,
               'url':lst[table.C]})
    
    #print(f'{text=}')
    #urls.setdefault(lst[table.C], lst[table.I])
    return l 




if __name__ == '__main__':
    json = 'kgtaprojects-8706cc47a185.json'
    sheet = Sheet(json,'testCopy')
    #a = sheet.get_rom_value(7) 
    # a = sheet.get_words_and_urls()
    a = sheet.copy_sheet('testCopy5')
    pprint(a)
    #for aa in a:
    #    print(f'{aa=}')
    #a = prepare_text(a)
    #pprint(a)