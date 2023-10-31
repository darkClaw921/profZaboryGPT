from sipuni_api import Sipuni
from yandexSpeach import *
from dotenv import load_dotenv
from helper import voice_processing
from workGS import Sheet
from dataclasses import dataclass
from chat import GPT
from amocrmWork import get_leadID_from_contact
load_dotenv()

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
            
        pprint(callDic)
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
    fileName=f'{fileID}.mp3'
    # text = voice_processing(filename=fileName, response=response)
    # # logger.debug(f'{text}')
    with open(fileName, "wb") as file:
        file.write(response.content)
    

    upload_file(fileName, bytes)
    print("Файл успешно загружен") 
    text = get_text_record(fileName)
    
    # with open(f'{fileID}.txt', "w") as file:
    #     file.write(text) 
    os.remove(fileName)
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
@logger.catch
def main():
    calls = client.get_call_stats(from_date=(datetime.now() - timedelta(hours=2)), to_date=datetime.now(), first_time=1)   # return csv data
    calls  = prepare_calls_stats(calls) 
    logger.debug(f'{len(calls)}')
    # return 0 
    for call in calls:
        pprint(call)
        try: 
            if float(call['Длительность звонка']) >= 60:
                print(f"{call['Длительность звонка']=} {call['ID записи']=}")
                phone = call['Откуда']
                date = call['Время']
                assignedCRM = call['Ответственный из CRM']
                
                
                duration = call['Длительность звонка'] 
                isNew =True if call['Новый клиент']=='1' else False
                if not isNew:
                    continue
                urlDeal = get_leadID_from_contact(phone)
                urlDeal = f'https://profzabor.amocrm.ru/leads/detail/{urlDeal}'
                logger.debug(urlDeal)
                try:
                    #TODO переделать на async
                    text = get_url_record(call['ID записи']) 
                except:
                    continue
                
                #иногда нужно повторить
                try:
                    answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
                except:
                    answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]

                ball, rez, good, bad, recomend = prepare_answer_gpt(answerGPT=answerGPT)
                print(answerGPT)
                lst=[date, assignedCRM, urlDeal, duration, ball, rez, good, bad, recomend, answerGPT]
                sheet.insert_cell(data=lst)
                
        except:
            continue
            # get_url_record(call['ID записи'])
        #TODO
            
    pass
if __name__ == '__main__':
    # a = sheet.get_cell(6,3)
    # print(a)
    main()

    
# 
# get_url_record('1696324590.113123')
