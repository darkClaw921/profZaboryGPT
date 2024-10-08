from sipuni_api import Sipuni
from yandexSpeach import *
from dotenv import load_dotenv
from helper import voice_processing
from workGS import Sheet
from dataclasses import dataclass
from chat import GPT
from amocrmWork import get_leadID_from_contact
from testLogg import logg
from translation import transcript_audio
from postgreWork import add_table
load_dotenv()
# /Users/igorgerasimov/Python/Bitrix/profZaboryGPT
# logger=logg('profZaboryGPT','sipuniWork')

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
    # print(downloadURL)
    # print('начинаем загрузку файла')
    # try:
    #     response = requests.get(downloadURL.encode())
    # except:
    #     print('ошибка загрузки файла')
    #     # downloadURL.replace('0xff','')
    #     response = requests.get(downloadURL)
        
    # response.raise_for_status() # вызывает исключение, если возникла ошибка при загрузке файла
    # fileName=f'{fileID}'
    # fileName = '/Users/igorgerasimov/Downloads/audio1492119703.mp3'
    fileName=f'{fileID}.mp3'
    # fileName=f'{fileID}.ogg'
    # text = voice_processing(filename=fileName, response=response)
    # # logger.debug(f'{text}')
    with open(fileName, "wb") as file:
        # file.write(response.content)
        file.write(downloadURL)
    
    # fileName = 'audio1492119703.mp3'
        
    # upload_file(fileName, bytes) #YSC 
    print("Файл успешно загружен") 
    text=transcript_audio(fileName) # GPT
    print('Получли текст')
    # text = get_text_record(fileName) #YSC
    print(text)
    with open('textPrepare.txt', "w") as file:
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
badPhones = [
'+79652050875',
'+79652050861',
'+79652050854',
'+79660326963',
'+79660326967',
'+79660320058',
]
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
            phoneBad=call['Куда']
            if call['\ufeffТип'] == 'Исходящий':
                phone = call['Куда']
                phoneBad=call['Откуда']

            if phoneBad in badPhones or phone in badPhones:
                continue
            date = call['Время']
            date = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
            assignedCRM = call['Ответственный из CRM']
            
            
            duration = call['Длительность звонка'] 
            # isNew =True if call['Новый клиент']=='1' else False
            # if not isNew:
            #     continue
            try:
                urlDeal = get_leadID_from_contact(phone)    
            except StopIteration:
                print('urlDeal не найден')
                continue

            urlDeal = f'https://profzabor.amocrm.ru/leads/detail/{urlDeal}'
            logger.debug(urlDeal)


            try:
                #TODO переделать на async
                text = get_url_record(call['ID записи']) 
            except Exception as e:
                print('id записи не неайден', e)
                logger.error(e)
                continue
            if text is None : continue
            logger.debug(f'{text=}')
            #иногда нужно повторить
            logger.debug('отправляем в gpt')
            try:
                if call['\ufeffТип'] == 'Исходящий':
                    promt1='напиши по строчкам кто горорил Клиент: или Оператор: учитывай что первый говорил Клиент:'
                else:    
                    promt1='напиши по строчкам кто горорил Клиент: или Оператор: учитывай что первый говорил Оператор:'
                    
                answerGPTPrepare = gpt.answer(promt1,[{"role": "user", "content": text}])[0]
                print(f'{answerGPTPrepare=}')
                answerGPT = gpt.answer(promt,[{"role": "user", "content": answerGPTPrepare}])[0]
            except Exception as e:
                print('ошибка gpt')
                print(e.__traceback__)
                logger.error(e)
                continue
                # answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
            
            logger.debug('получили ответ от gpt')
            ball, rez, good, bad, recomend = prepare_answer_gpt(answerGPT=answerGPT)
            print(answerGPT)
            promtBall='Преобразуйте текст в баллы если балы написаны в тексте то переведи их в цифру если 4/9 то просто 4 если 5 баллов то 5 если 3/9 В результате, менеджер выполнил только 3 пункта из 9, перечисленных в чек-листе контроля качества то 3 и так далее. В ответ ты должен отправить только цифру'
            ball= gpt.answer(promtBall,[{"role": "user", "content": ball}])[0] 
            
            lst=[date, assignedCRM, urlDeal, duration, ball, rez, good, bad, recomend, answerGPT, phone, answerGPTPrepare, call['\ufeffТип']]

            tab={
                'date_call':date,
                'assigned':assignedCRM,
                'url_deal':urlDeal,
                'duration':duration,
                'ball':ball,
                'rez':rez,
                'good':good,
                'bad':bad,
                'recomend':recomend,
                'answer_gpt':answerGPT,
                'phone':phone,
                'answer_gpt_prepare':answerGPTPrepare,
                'type':call['\ufeffТип']
            } 
            add_table(tab)
            # sheet.insert_cell(data=lst)



        # except Exception as e:
        #     logger.error(e)
        #     continue
            # get_url_record(call['ID записи'])
        #TODO
            
    pass
if __name__ == '__main__':
    # a = sheet.get_cell(6,3)
    # get_url_record_local('1701158977.29346')
    # 1/0
    text='ты кто?'
    answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
    logger.debug(answerGPT) 
    # print(a)
    main()

    
# 
# get_url_record('1696324590.113123')
