import re
import telebot
from loguru import logger
#import datetime 
from datetime import datetime
from workGDrive import *
from workGS import *
from telebot.types import InputMediaPhoto
from workRedis import *
from questions import pokrytie, porydok
# any
def time_epoch():
    from time import mktime
    dt = datetime.now()
    sec_since_epoch = mktime(dt.timetuple()) + dt.microsecond/1000000.0

    millis_since_epoch = sec_since_epoch * 1000
    return int(millis_since_epoch)

def get_model_url(modelName: str):
    modelUrl = sql.select_query('model', f'model = "{modelName}"')[0]['url']
    logger.info(f'get_model_url {modelUrl}')
    #print('a', modelUrl)
    return modelUrl.decode('utf-8')

def remove_empty_lines(text):
    lines = text.splitlines()  # Разделение текста на отдельные строки
    stripped_lines = (line.strip() for line in lines)  # Удаление начальных и конечных пробелов
    non_empty_lines = (line for line in stripped_lines if line)  # Отбор только непустых строк
    return "\n".join(non_empty_lines) 

def slice_str(s:str,start:str, end:str):
    a = s.find(start)
    print(a)
    if a == -1:
        return ' '
    return s[s.find(start)+len(start):s.find(end)]

def slice_str_phone(message:str,):
    
    #return s[s.find(start)+len(start):s.find(start)+len(start)+18]
    #a = """Client's name: \nCustomer's phone number: 79777345754\n\nConfiguration at the customer's choice (closed circuit, warm circuit, exterior finish): \nThe amount that the client expects to pay: \nDoes the client have a home design: No\nArchitectural style that the client likes: Modern\nDoes the client need a house for permanent residence or for a weekend vacation: Permanent residence\nThe number of beds and the size of the client's family: Big family\nThe parameters of the house desired by the client: 3 floors, 2 bedrooms\nWhen the client plans to move:\nDoes the client need a mortgage:\nProjects that the client liked (project names only):"""
#b = slice_str(a, '\n','Configuration')
    logger.info(f'{message=}')
    #b = slice_str(message, 'phone number:','Configuration').strip()
    b = slice_str(message, 'Номер телефона клиента:','Конфигурация').strip()
    logger.info(f'вырезаный телефон ', b)
    return b

def sum_dict_values(dict1, dict2):
    result = {}

    for key in dict1:
        if key in dict2:
            result[key] = dict1[key] + dict2[key]
        else:
            result[key] = dict1[key]

    for key in dict2:
        if key not in dict1:
            result[key] = dict2[key]

    return result

def extract_id_from_url(url):
    id_start_index = url.rfind('/') + 1
    id_end_index = url.find('?') if '?' in url else len(url)
    return url[id_start_index:id_end_index]

def extract_url(text):
    pattern = re.compile(r'(https?://\S+)')
    match = pattern.search(text)
    if match:
        return match.group(1).replace(')','')
    else:
        return None
    
def create_media_gorup(lst:list):
    media_group = telebot.types.MediaGroup()
    for i in lst:
        photo = open(i, 'rb')
        media_group.attach_photo(photo)
        
    return media_group

def prepare_dict_keyboadr(dic)->str:
    st = ''
    for key, value in dic.items():
        st += f'{key}. {value}\n'
    return st

        
#Google Sheet
@logger.catch
def check_need_words(data:list, text:str):
    ursl=[]
    for item in data:
        if any(word in text for word in item['words']):
            if item['words2'] != ['']:
                if any(word in text for word in item['words2']):
                    ursl.append(item['url'])
                    #return item['url']
            else:
                ursl.append(item['url'])
                #return item['url']
    return ursl
    #return False


   

def send_values_in_sheet(typeMaterial:str, values:list, sheetName:str, first:bool=False):
    if first:
        copy_file('1c3cz_6RvneBEitvgtTxL5lxVfBdKb4kmyG9f8QqoUp0', sheetName)
    sheet = Sheet('GDtxt.json',sheetName,get_worksheet=1)
    # sheet.export_pdf(sheetName) 
    # 1/0
    if typeMaterial == 'profNastil1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('B2', str(values[1]).replace('.',','))
        sheet.send_cell('B3', str(values[2]).replace('.',','))
        sheet.send_cell('B6', str(values[3]).replace('.',','))
        sheet.send_cell('B8', pokrytie[str(values[4])])
        sheet.send_cell('B16', values[5])
        sheet.send_cell('B23', values[6])
        try:
            sheet.send_cell('C170', values[7])
        except:
            1+0
    if typeMaterial == 'profNastil2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('J2', str(values[1]).replace('.',','))
        sheet.send_cell('J3', str(values[2]).replace('.',','))
        sheet.send_cell('J6', str(values[3]).replace('.',','))
        sheet.send_cell('J8', pokrytie[str(values[4])])
        sheet.send_cell('J16', values[5])
        sheet.send_cell('J23', values[6])
        # sheet.send_cell('C170', values[7])
    if typeMaterial == 'profNastil3':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('R2', str(values[1]).replace('.',','))
        sheet.send_cell('R3', str(values[2]).replace('.',','))
        sheet.send_cell('R6', str(values[3]).replace('.',','))
        sheet.send_cell('R8', pokrytie[str(values[4])])
        sheet.send_cell('R16', values[5])
        sheet.send_cell('R23', values[6])
    
    if typeMaterial == 'evroShtak1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('Z2', str(values[1]).replace('.',','))
        sheet.send_cell('Z3', str(values[2]).replace('.',','))
        sheet.send_cell('Z6', porydok[str(values[3])])
        sheet.send_cell('Z8', pokrytie[str(values[4])])
        sheet.send_cell('Z16', values[5])
        sheet.send_cell('Z23', values[6])
        try:
            sheet.send_cell('C170', values[7])
        except:
            1+0

    if typeMaterial == 'evroShtak2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('AH2', str(values[1]).replace('.',','))
        sheet.send_cell('AH3', str(values[2]).replace('.',','))
        sheet.send_cell('AH6', porydok(str(values[3])))
        sheet.send_cell('AH8', pokrytie[str(values[4])])
        sheet.send_cell('AH16', values[5])
        sheet.send_cell('AH23', values[6])

    if typeMaterial == 'evroShtak3':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('AP2', str(values[1]).replace('.',','))
        sheet.send_cell('AP3', str(values[2]).replace('.',','))
        sheet.send_cell('AP6', porydok(str(values[3])))
        sheet.send_cell('AP8', pokrytie[str(values[4])])
        sheet.send_cell('AP16', values[5])
        sheet.send_cell('AP23', values[6])
    # sheet.export_pdf(sheetName)
    return sheetName


#Google Drive 
import base64
import urllib.request

def read_file_as_base64(file_path):
    
    with open(file_path, 'rb') as file:
        file_data = file.read()
        if file_data:
            file_base64 = base64.b64encode(file_data).decode('utf-8')
            return file_base64
        else:
            print("Файл пуст.")
            return None
        
def download_file(url):
    directory = 'downloadsProject/'
    os.makedirs(directory, exist_ok=True) # Создаем папку, если её не существует
    filename = url.split('/')[-1]  # Извлекаем имя файла из ссылки
    full_path = os.path.join(directory, filename)  # Формируем полный путь для сохранения файла
    urllib.request.urlretrieve(url, full_path)  # Скачиваем файл по ссылке и сохраняем его по указанному пути
    return full_path

@logger.catch
def download_photo(urlExtract, URL_USERS, userID,):

    #urlExtract = message_content
    #if urlExtract is None:
    #    return URL_USERS, [], 0
    #logger.info(f'{urlExtract=}')
    #logger.info(f'{URL_USERS[userID]=}')

    media_group = [] 
    try:
        if URL_USERS == {}:
        
            URL_USERS.setdefault(userID,[urlExtract])
        else: 
            if urlExtract in URL_USERS[userID]:
                return 0
            else:
                URL_USERS[userID].append(urlExtract) 
    except Exception as e:
        logger.info(f'{e=}')
        URL_USERS.setdefault(userID,[urlExtract])
        #URL_USERS.setdefault(userID,[urlExtract])
    logger.info(f'{URL_USERS=}')
    nameProject=' '
    #try:

    #TODO    

    idExtract = extract_id_from_url(urlExtract)
    logger.info(f'{extract_id_from_url=}')
    #сколько файлов загружать
    downloadFiles = download_files(idExtract, 5)
    logger.info(f'{downloadFiles=}')
    #media_group = []
    for photo in downloadFiles:
        #path = '/Users/igorgerasimov/Python/Bitrix/test-chatGPT'
        media_group.append(InputMediaPhoto(open(f'downloads/{photo}', 'rb'),
        #media_group.append(InputMediaPhoto(open(f'{path}/{photo}', 'rb'),
                                caption = photo))
    #mediaGroup = create_media_gorup(download_files)
    #bot.send_media_group(message.chat.id, mediaGroup)
    #bot.send_media_group(message.chat.id, media_group,)
    #print('отправка сообщегия')
    #answer = answer
    #answer = re.sub(r'\[.*?\]\(.*?\)', '', message_content).replace(' ссылка на', '')
    #answer = remove_empty_lines(message_content)
    nameProject = downloadFiles[0].split(' ')[0]
    #except Exception as e:
    #    logger.error(e)
        #answer = 'Извините сейчас не могу найти актуальную ссылку'
    return URL_USERS, media_group, nameProject

#telegram 
def summary(userID, error, isDEBUG):
    if isDEBUG : bot.send_message(userID, error)
        #bot.send_message(userID, 'начинаю sammury: ответ может занять больше времени, но не более 3х минут')
    history = get_history(str(userID))
    summaryHistory = gpt.summarize_questions(history)
    logger.info(f'summary истории {summaryHistory}')

    history = [summaryHistory]
    history.extend([{'role':'user', 'content': text}])
    add_old_history(userID,history)
    history = get_history(str(userID))
    logger.info(f'история после summary {history}')
    
    answer, allToken, allTokenPrice, message_content = gpt.answer_index(model, text, history, model_index,temp=0.5, verbose=0)
    bot.send_message(message.chat.id, answer)
    add_message_to_history(userID, 'assistant', answer)


if __name__ == '__main__':
#     data = [{'url': 'https://drive.google.com/drive/folders/18MGvuit-R5PJFyJ902M_DpyQTC6VFzCH',
#   'words': ['из евроштакетника', 'евроштакетник'],
#   'words2': ['шахматка', 'шахматный порядок']},
#  {'url': 'https://drive.google.com/drive/folders/1Vj6JMswjZlnuoEidOmQyl9ZzZ6uv7JIl',
#   'words': ['жалюзи'],
#   'words2': ['']}]
#     text = "Привет это помощник по заборам у нас есть евроштакетник из жалюзи "
#     rez = check_words(data,text)
#     print(rez)
    typeQuest = 'profNastil'

    send_values_in_sheet(typeQuest, ['profNastil', '120', '130', '0.2', '4', '5', '220'], f'darkClaw921_{typeQuest}') 