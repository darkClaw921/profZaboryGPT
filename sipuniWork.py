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
        
    # upload_file(fileName, bytes) #YSC 
    print("Файл успешно загружен") 
    text=transcript_audio(fileName) # GPT
    # text = get_text_record(fileName) #YSC
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
    calls = client.get_call_stats(from_date=(datetime.now() - timedelta(days=2)), to_date=(datetime.now() - timedelta(days=2)), first_time=1)   # return csv data
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
            lst=[date, assignedCRM, urlDeal, duration, ball, rez, good, bad, recomend, answerGPT, phone, text]
            
            sheet.insert_cell(data=lst)



        # except Exception as e:
        #     logger.error(e)
        #     continue
            # get_url_record(call['ID записи'])
        #TODO
            
    pass
if __name__ == '__main__':
    # a = sheet.get_cell(6,3)
#     text="""Алло
# Да удобно
# Точнее у вас параметры меня зовут николай как могу к вам обращаться
# Меня зовут марина но мы пока делаем предварительный расчет то есть
# Хорошо считаем 100 погонных метров включая одни ворота 1 калитку
# Я не могу сказать параметры
# Да да да
# Высота забора нестандартная за 20
# А стандартная какая 2
# Да
# Нет стандартную значит двухметровую
# 2 м считаем и профнастил двухстороннее напыление
# Да да
# Установку планируете в ближайшее время
# Ну не весной нет через какое то время
# Понял рассчитаюсь с ценами на данный момент они актуальны примерно до 11 февраля если по бюджету понравится можно будет оформить договор с сохранением цены повышение цен на металл у вас не коснется
# Ага
# Угу спасибо
# Так по бюджету установка займет 2 дня бригада приезжает и уезжает с материалом на день при этой высоте используем 2 лаги
# Самореза кровельный цвет листа
# Прорезиненной шайбой профнастил новолипецкий металлокомбинат 0 4 толщиной в договоре толщины прописываем и если потребуется мы проверим при вас по участию
# Столбы используем квадратные 60 на 60 толщина 2 мм заглубляем метр 20
# Бурения до забивания и утрамбов и гравий под ворота калитку столбы усиленные 80 на 80 и заглубляем на полтора метра
# Фурнитура входит в одноместные рамки весь каркас будет загрунтован гарантия 2 года по договору и выезд замерщика бесплатный при оформлении
# Все вместе с доставкой материалы работа получится на 260000 р ровно
# Угу
# Хорошо а скажите пожалуйста то есть вы работаете это ваша фирма правильно юридическое лицо то есть договор все как положено оформляем
# Да мы работаем по договору по белому на рынке 11 год но мы работаем от ип
# Угу а в чеховском районе вы работаете
# Конечно у нас производство в подольске
# А придется попадать все поняла а вот ваш номер вот этот я могу сохранить чтобы потом вам позвонить когда мы сориентируемся по времени и так далее
# Да конечно вам еще на ватсап придет визитка там будут указаны контакты
# Ага отлично
# Да обращайтесь буду рад помочь
# Спасибо большое
# Да всего доброго до свидания"""
    # get_url_record_local('1701158977.29346')
    # 1/0
    text='ты кто?'
    answerGPT = gpt.answer(promt,[{"role": "user", "content": text}])[0]
    logger.debug(answerGPT) 
    # print(a)
    main()

    
# 
# get_url_record('1696324590.113123')
