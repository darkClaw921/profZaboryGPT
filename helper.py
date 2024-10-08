import re
import telebot
from loguru import logger
#import datetime 
from datetime import datetime, timedelta
from workGDrive import *
from workGS import *
from telebot.types import InputMediaPhoto
from workRedis import *
# from questions import pokrytie, porydok,
import uuid
import speech_recognition as sr
language='ru_RU'
r = sr.Recognizer()

month_translations = {
    "January": "январь",
    "February": "февраль",
    "March": "март",
    "April": "апрель",
    "May": "май",
    "June": "июнь",
    "July": "июль",
    "August": "август",
    "September": "сентябрь",
    "October": "октябрь",
    "November": "ноябрь",
    "December": "декабрь"
}

# from questions import * 
from questionsNoKeyboard import *
# any
def get_dates(day, patern = '%Y-%m-%dT%H:%M:%SZ'):
    # Текущая дата
    #patern = '2023-07-18T20:26:32Z'
    # patern = '%Y-%m-%dT%H:%M:%SZ'
    current_date = datetime.now().strftime(patern)

    # Дата, отстоящая на 30 дней
    delta = timedelta(days=day)
    future_date = (datetime.now() + delta).strftime(patern)

    return current_date, future_date

def timestamp_to_date(timestap, pattern = '%Y-%m-%dT%H:%M:%SZ'):
   
    """timestamp

    Returns:
        str: %Y-%m-%dT%H:%M:%SZ
    """
    a = time.gmtime(timestap)
    date_time = datetime(*a[:6])
    date_string = date_time.strftime(pattern)
    
    return date_string

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
    st = '\n'
    for key, value in dic.items():
        st += f'{key}. {value}\n'
    return st

def list_to_str(lst:dict)->str:
    if quests != None:   
        quests = quests.keys() 
        text = '\n'
        for rang,i in enumerate(quests):
            text +=f'{rang} -> '+ i + '\n'
        quests= text
    else:
        quests = ''
    return quests


def find_phone_numbers(text):
    pattern = r'(\+?\d{1,2}\s?[-(]?\d{3}[-)]?\s?\d{3}\s?[-]?\s?\d{2}\s?[-]?\s?\d{2})'
    phone_numbers = re.findall(pattern, text)
    result = []
    for num in phone_numbers:
        number = num.replace("-", "").replace(' ','').replace('(','').replace(')','')
        if len(number) == 11 and num[0] != '8':
            number = '+' + number
        elif len(number) == 10:
            number = '+7' + number
        result.append(number)
        
    return result
        
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

def send_values_in_sheet(typeMaterial:str, values:list, sheetName:str, first:bool=False, mkad=0):
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
        sheet.send_cell('B3', str(values[2]).replace('.',',').replace('m',''))
        sheet.send_cell('B6', str(values[3]).replace('.',',').replace('mm',''))
        sheet.send_cell('B8', pokrytie[str(values[4])])
        # sheet.send_cell('B8', str(values[4]))
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
        # sheet.send_cell('Z6', str(values[3]))
        # sheet.send_cell('Z8', str(values[4]))
        sheet.send_cell('Z10', values[5])# зазор
        sheet.send_cell('Z16', values[6])
        sheet.send_cell('Z23', values[7])
        try:
            sheet.send_cell('C170', values[8])
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
        sheet.send_cell('AH10', values[5])# зазор
        sheet.send_cell('AH16', values[6])
        sheet.send_cell('AH23', values[7])

    if typeMaterial == 'evroShtak3':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('AP2', str(values[1]).replace('.',','))
        sheet.send_cell('AP3', str(values[2]).replace('.',','))
        sheet.send_cell('AP6', porydok(str(values[3])))
        sheet.send_cell('AP8', pokrytie[str(values[4])])
        sheet.send_cell('AP10', values[5])# зазор
        sheet.send_cell('AP16', values[6])
        sheet.send_cell('AP23', values[7])
    
    if typeMaterial == 'GridRabit1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('AX2', str(values[1]).replace('.',','))
        sheet.send_cell('AX3', str(values[2]).replace('.',','))
        sheet.send_cell('AX4', values[3])
        sheet.send_cell('AX15', values[4])
        sheet.send_cell('AX22', values[5])
    
    if typeMaterial == 'GridRabit2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('BF2', str(values[1]).replace('.',','))
        sheet.send_cell('BF3', str(values[2]).replace('.',','))
        sheet.send_cell('BF4', values[3])
        sheet.send_cell('BF15', values[4])
        sheet.send_cell('BF22', values[5])
    
    if typeMaterial == '3d1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('BN2', str(values[1]).replace('.',','))
        sheet.send_cell('BN3', str(values[2]).replace('.',','))
        sheet.send_cell('BN16', values[3])
        sheet.send_cell('BN23', values[4])
    
    if typeMaterial == '3d2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('BV2', str(values[1]).replace('.',','))
        sheet.send_cell('BV3', str(values[2]).replace('.',','))
        sheet.send_cell('BV16', values[3])
        sheet.send_cell('BV23', values[4])
    
    if typeMaterial == 'Zaluzi1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('CT2', str(values[1]).replace('.',','))
        sheet.send_cell('CT3', str(values[2]).replace('.',','))
        sheet.send_cell('CT16', values[3])
        sheet.send_cell('CT23', values[4])
    sheet.send_cell('C170', mkad)

    # sheet.export_pdf(sheetName)
    return sheetName


def send_values_in_sheet_no_keyboard(typeMaterial:str, values:list, sheetName:str, first:bool=False, mkad=0):
    if first:
        copy_file('1c3cz_6RvneBEitvgtTxL5lxVfBdKb4kmyG9f8QqoUp0', sheetName)
    sheet = Sheet('GDtxt.json',sheetName,get_worksheet=1)
    # sheet.export_pdf(sheetName) 
    # 1/0
    # keyProfNastil = questionProfNastil.keys()
    # keyGridRabit = questionGridRabit.keys()
    # key3d = question3d.keys()
    # keyZaluzi = questionZaluzi.keys()
    if len(values) == 1:
        return sheetName
    #клавиатуры
    upValuesProfNastil = list(questionProfNastil['2']['keyboard'].keys())
    widthValuesProfNastil = list(questionProfNastil['3']['keyboard'].keys())
    coverageValuesProfNastil = list(questionProfNastil['4']['keyboard'].keys())
    

    upValuesGridRabit = list(questionGridRabit['2']['keyboard'].keys())
    armatyraValuesGridRabit = list(questionGridRabit['3']['keyboard'].keys())


    upValues3d = list(question3d['2']['keyboard'].keys())

    upValuesZaluzi = list(questionZaluzi['2']['keyboard'].keys())

    upValuesEvroShtak = list(questionEvroShtak['2']['keyboard'].keys())
    stepEvroShtak = list(questionEvroShtak['3']['keyboard'].keys())
    coverageValuesEvroShtak = list(questionEvroShtak['4']['keyboard'].keys())
    zazorValuesEvroShtak = list(questionEvroShtak['5']['keyboard'].keys())



    


    if typeMaterial == 'profNastil1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('B2', str(values[1]).replace('.',','))
        sheet.send_cell('B3', upValuesProfNastil[int(values[2])].replace('.',','))
        sheet.send_cell('B6', widthValuesProfNastil[int(values[3])].replace('.',','))
        sheet.send_cell('B8', coverageValuesProfNastil[int(values[4])])
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
        sheet.send_cell('J3', upValuesProfNastil[int(values[2])].replace('.',','))
        sheet.send_cell('J6', widthValuesProfNastil[int(values[3])].replace('.',','))
        sheet.send_cell('J8', coverageValuesProfNastil[int(values[4])])
        sheet.send_cell('J16', values[5])
        sheet.send_cell('J23', values[6])
        # sheet.send_cell('C170', values[7])
    if typeMaterial == 'profNastil3':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('R2', str(values[1]).replace('.',','))
        sheet.send_cell('R3', upValuesProfNastil[int(values[2])].replace('.',','))
        sheet.send_cell('R6', widthValuesProfNastil[int(values[3])].replace('.',','))
        sheet.send_cell('R8', coverageValuesProfNastil[int(values[4])])
        sheet.send_cell('R16', values[5])
        sheet.send_cell('R23', values[6])
    
    if typeMaterial == 'evroShtak1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('Z2', str(values[1]).replace('.',','))
        sheet.send_cell('Z3', upValuesEvroShtak[int(values[2])].replace('.',','))
        sheet.send_cell('Z6', stepEvroShtak[int(values[3])])
        sheet.send_cell('Z8', coverageValuesEvroShtak[int(values[4])])
        # sheet.send_cell('Z6', str(values[3]))
        # sheet.send_cell('Z8', str(values[4]))
        # sheet.send_cell('Z10', zazorValuesEvroShtak[int(values[5])])# зазор
        sheet.send_cell('Z10', int(values[5]))# зазор
        sheet.send_cell('Z16', values[6])
        sheet.send_cell('Z23', values[7])
        try:
            sheet.send_cell('C170', values[8])
        except:
            1+0

    if typeMaterial == 'evroShtak2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('AH2', str(values[1]).replace('.',','))
        sheet.send_cell('AH3',upValuesEvroShtak[int(values[2])].replace('.',','))
        sheet.send_cell('AH6', stepEvroShtak[int(values[3])])
        sheet.send_cell('AH8', coverageValuesEvroShtak[int(values[4])])
        sheet.send_cell('AH10', zazorValuesEvroShtak[int(values[5])])# зазор
        sheet.send_cell('AH16', values[6])
        sheet.send_cell('AH23', values[7])

    if typeMaterial == 'evroShtak3':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('AP2', str(values[1]).replace('.',','))
        sheet.send_cell('AP3', upValuesEvroShtak[int(values[2])].replace('.',','))
        sheet.send_cell('AP6',stepEvroShtak[int(values[3])])
        sheet.send_cell('AP8', coverageValuesEvroShtak[int(values[4])])
        sheet.send_cell('AP10', zazorValuesEvroShtak[int(values[5])])# зазор
        sheet.send_cell('AP16', values[6])
        sheet.send_cell('AP23', values[7])
    
    if typeMaterial == 'GridRabit1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('AX2', str(values[1]).replace('.',','))
        sheet.send_cell('AX3', upValuesGridRabit[int(values[2])].replace('.',','))
        sheet.send_cell('AX4', armatyraValuesGridRabit[int(values[3])])
        sheet.send_cell('AX15', values[4])
        sheet.send_cell('AX22', values[5])
    
    if typeMaterial == 'GridRabit2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('BF2', str(values[1]).replace('.',','))
        sheet.send_cell('BF3', upValuesGridRabit[int(values[2])].replace('.',','))
        sheet.send_cell('BF4', armatyraValuesGridRabit[int(values[3])])
        sheet.send_cell('BF15', values[4])
        sheet.send_cell('BF22', values[5])
    
    if typeMaterial == '3d1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)

        sheet.send_cell('BN2', str(values[1]).replace('.',','))
        sheet.send_cell('BN3',  upValues3d[int(values[2])].replace('.',','))
        sheet.send_cell('BN16', values[3])
        sheet.send_cell('BN23', values[4])
    
    if typeMaterial == '3d2':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('BV2', str(values[1]).replace('.',','))
        sheet.send_cell('BV3', upValues3d[int(values[2])].replace('.',','))
        sheet.send_cell('BV16', values[3])
        sheet.send_cell('BV23', values[4])
    
    if typeMaterial == 'Zaluzi1':
        print('отправка значений ' + typeMaterial)
        a = sheet.get_cell(1,1)
        print(a)
        sheet.send_cell('CT2', str(values[1]).replace('.',','))
        sheet.send_cell('CT3', upValuesZaluzi[int(values[2])].replace('.',','))
        sheet.send_cell('CT16', values[3])
        sheet.send_cell('CT23', values[4])
    sheet.send_cell('C170', mkad)

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
                return URL_USERS,0,0
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
        if photo.split('.')[1].lower() == 'mp4': continue
        #path = '/Users/igorgerasimov/Python/Bitrix/test-chatGPT'
        try:
            media_group.append(InputMediaPhoto(open(f'downloads/{photo}', 'rb'),
                                caption = photo))
        except Exception as e:
            logger.error(e)
            continue
    #mediaGroup = create_media_gorup(download_files)
    #bot.send_media_group(message.chat.id, mediaGroup)
    #bot.send_media_group(message.chat.id, media_group,)
    #print('отправка сообщегия')
    #answer = answer
    #answer = re.sub(r'\[.*?\]\(.*?\)', '', message_content).replace(' ссылка на', '')
    #answer = remove_empty_lines(message_content)
    # nameProject = downloadFiles[0].split(' ')[0]
    nameProject = downloadFiles[0].split('-')[0]
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

r = sr.Recognizer()

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            print('Converting audio transcripts into text ...')
            print(text)
            return text
        except:
            print('Sorry.. run again...')
            return "Sorry.. run again..."


def voice_processing(filename:str, response):
    filename = str(uuid.uuid4())
    file_name_full="voice/"+filename+".ogg"
    file_name_full_converted="ready/"+filename+".wav"
    # file_info = bot.get_file(message.voice.file_id)
    # downloaded_file = bot.download_file(file_info.file_path)
    # with open(file_name_full, 'wb') as new_file:
        # new_file.write(downloaded_file)
    with open(file_name_full, "wb") as file:
        file.write(response.content)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    text=recognise(file_name_full_converted)
    # bot.reply_to(message, text)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    return text


#chatRoom

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