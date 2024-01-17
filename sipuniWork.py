from sipuni_api import Sipuni
from yandexSpeach import *
from dotenv import load_dotenv
from helper import voice_processing
from workGS import Sheet
from dataclasses import dataclass
from chat import GPT
from amocrmWork import get_leadID_from_contact
from testLogg import logg
load_dotenv()
# /Users/igorgerasimov/Python/Bitrix/profZaboryGPT
logger=logg('profZaboryGPT','sipuniWork')

client_id = os.environ.get('SIPUNU_CLIENT_ID')
secret_id = os.environ.get('SIPUNU_SECRET_ID')
client = Sipuni(client_id, secret_id)

gpt = GPT()

PROMT_URL = 'https://docs.google.com/document/d/1w67skmqY2AXl2WwxnrbSFvx24p_1KCrIFrhsNpa8MeQ/edit?usp=sharing'

promt = gpt.load_prompt(PROMT_URL)

@dataclass
class Table:
    date='A'
    assigned='B'
    urlDeal='C'
    duration = 'D'


sheet = Sheet('profzaboru-5f6f677a3cd8.json','Эффективность_звонков',)
# next_row = len(sheet.get_all_values()) + 1
# call statistic
from datetime import datetime, timedelta
# a = client.get_call_stats(from_date=(datetime.now() - timedelta(days=1)), to_date=datetime.now())   # return csv data

def prepare_calls_stats(calls:str):
    calls = calls.split('\n')
    title = calls[0].split(';')
    # pprint(title)

    lstCall = []
    for call in calls:
        call = call.split(';')
        # print(call)
        callDic = {}
        for nameValue, valueCall in zip(title,call):
            if valueCall == nameValue:
                continue
            callDic[nameValue]=valueCall
            
        # pprint(callDic)
        if callDic != {}:
            lstCall.append(callDic)
    return lstCall

import requests


# # get call record
def get_url_record(fileID:str):
    import requests
    downloadURL = client.get_record(fileID)   
    # bytes = client.get_record(fileID)   
    response = requests.get(downloadURL)
    # response.raise_for_status() # вызывает исключение, если возникла ошибка при загрузке файла
    # fileName=f'{fileID}'
    # fileName = '/Users/igorgerasimov/Downloads/audio1492119703.mp3'
    fileName=f'{fileID}.mp3'
    # fileName=f'{fileID}.ogg'
    # text = voice_processing(filename=fileName, response=response)
    # # logger.debug(f'{text}')
    with open(fileName, "wb") as file:
        file.write(response.content)
    
    # fileName = 'audio1492119703.mp3'
    upload_file(fileName, bytes)
    print("Файл успешно загружен") 
    text = get_text_record(fileName)
    print(text)
    with open('textPrepare', "w") as file:
        file.write(text)
    # with open(f'{fileID}.txt', "w") as file:
    #     file.write(text) 
    os.remove(fileName)
    return text

def get_url_record_local(fileName:str):
    import requests
    
    fileName = 'audio_2023-12-29_13-39-06.mp3'
    
    upload_file(fileName, bytes)
    print("Файл успешно загружен") 
    text = get_text_record(fileName)
    print(text)
    with open('textPrepare.txt', "w") as file:
        file.write(text)
    # with open(f'{fileID}.txt', "w") as file:
    #     file.write(text) 
    # os.remove(fileName)
    return text

def slice_str(s:str,start:str, end:str):
    a = s.find(start)
    if a == -1:
        return ' '
    if end == '.':
        return s[s.find(start)+len(start):len(s)]
    else:
        return s[s.find(start)+len(start):s.find(end)]

def prepare_answer_gpt(answerGPT):
    ball = slice_str(answerGPT,'Баллы:','Результат:')
    rez = slice_str(answerGPT,'Результат:','Хорошо:')
    good = slice_str(answerGPT,'Хорошо:','Плохо:')
    bad = slice_str(answerGPT,'Плохо:','Рекомендации:')
    recomend = slice_str(answerGPT,'Рекомендации:','.')
    return ball, rez, good, bad, recomend

# @logger.catch
def main():
    # calls = client.get_call_stats(from_date=datetime.now(), to_date=datetime.now(), first_time=1)   # return csv data
    calls = client.get_call_stats(from_date=(datetime.now() - timedelta(days=1)), to_date=(datetime.now() - timedelta(days=1)), first_time=1)   # return csv data
    calls  = prepare_calls_stats(calls) 
    # logger.debug(f'{len(calls)}')
    # return 0 
    for call in calls:
        # pprint(call)
        try:
            if call['Длительность звонка'] == '': continue
        except KeyError:
            continue

        # if call['ID записи']== '1701158977.29346':
            # pprint(call)
        if float(call['Длительность звонка']) >= 60:
            print(f"{call['Длительность звонка']=} {call['ID записи']=} {call['Откуда']=} {call['Схема']=} {call['Куда']=}")
            pprint(call)
            phone = call['Откуда']
            if call['\ufeffТип'] == 'Исходящий':
                phone = call['Куда']
            
            date = call['Время']
            assignedCRM = call['Ответственный из CRM']
            
            
            duration = call['Длительность звонка'] 
            # isNew =True if call['Новый клиент']=='1' else False
            # if not isNew:
            #     continue
            try:
                urlDeal = get_leadID_from_contact(phone)    
            except StopIteration:
                continue

            urlDeal = f'https://profzabor.amocrm.ru/leads/detail/{urlDeal}'
            logger.debug(urlDeal)


            try:
                #TODO переделать на async
                text = get_url_record(call['ID записи']) 
            except Exception as e:
                logger.error(e)
                continue
            if text is None : continue
            logger.debug(f'{text=}')
            #иногда нужно повторить
            logger.debug('отправляем в gpt')
            try:
                answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
            except Exception as e:
                logger.error(e)
                continue
                # answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
            
            logger.debug('получили ответ от gpt')
            ball, rez, good, bad, recomend = prepare_answer_gpt(answerGPT=answerGPT)
            print(answerGPT)
            lst=[date, assignedCRM, urlDeal, duration, ball, rez, good, bad, recomend, answerGPT, phone]
            
            sheet.insert_cell(data=lst)



        # except Exception as e:
        #     logger.error(e)
        #     continue
            # get_url_record(call['ID записи'])
        #TODO
            
    pass
if __name__ == '__main__':
    # a = sheet.get_cell(6,3)
    # text='Алло\nЗдравствуйте компания вопрос забора вы заявочку оставляли на расчет удобно пообщаться\nЕсли меня слышно то удобно\nВчера актуальная тема для вас на этот год планируете или на следующий\nНет вот в течение недели 2 планирую\nДавайте примерно сориентирую по ценам вот эти 30 м 1 и 8 высота одностороннее покрытие без ворот без калитки все вместе под ключ обойдется 76 200\nПримерно 30 32 м профнастил\nАвтомобильские или механические страницы\nНе знаю\nСегодня будем переезжать вот ну примерно 3,5 там не было\nВорота откатные механические если с обшивкой из профлиста в районе 85 с автоматикой 120 где то выходит\nВот так более детально замерщик выезжает с образцами с ним уже по месту можно все обсудить если вместе будете заказывать то тогда дешевле сделаю\nЕсли вместе то ошибка профлист нужна или какой материал\nОбшивка профлист нужна или какой материал\nАлло\nАлло вас не слышно\n'
    # get_url_record_local('1701158977.29346')
    # 1/0
    text='ты кто?'
    answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
    logger.debug(answerGPT) 
    # print(a)
    main()

    
# 
# get_url_record('1696324590.113123')
