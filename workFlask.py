import os

from datetime import datetime, timedelta
from dotenv import load_dotenv
from pprint import pprint
from chat import GPT
from datetime import datetime
import workYDB
import json
from loguru import logger
import sys
from createKeyboard import *
from createKeyboard import *

from helper import *
from workGDrive import *
from telebot.types import InputMediaPhoto
from workRedis import *
import workGS
from questions import *
from questionsNoKeyboard import *
from flask import Flask, request, render_template

#TODO
# from amocrmWork import *


load_dotenv()
app = Flask(__name__)
isDEBUG = True

logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("file_1.log", rotation="50 MB")
# gpt = GPT()
# GPT.set_key(os.getenv('KEY_AI'))
# bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))
# sheet = workGS.Sheet('kgtaprojects-8706cc47a185.json','Ссылки на изображения')
sql = workYDB.Ydb()

TYPE_QUESTIONS = {'profNastil': questionProfNastil,
                  'evroShtak':questionEvroShtak} 
# TYPE_QUESTIONS = {'Профнастил': questionProfNastil,
#                   'Евроштакетник':questionEvroShtak} 
URL_USERS = {}
QUESTS_USERS = {}
COUNT_ZABOR_USER={}
ALL_QUESTS_USERS ={}
SECTION_QUESTS_USERS ={}
# MODEL_URL= 'https://docs.google.com/document/d/1M_i_C7m3TTuKsywi-IOMUN0YD0VRpfotEYNp1l2CROI/edit?usp=sharing'
# #gsText, urls_photo = sheet.get_gs_text()
# #print(f'{urls_photo=}')
# model_index=gpt.load_search_indexes(MODEL_URL)
# # model_project = gpt.create_embedding(gsText)
# PROMT_URL = 'https://docs.google.com/document/d/10PvyALgUYLKl-PYwwe2RZjfGX5AmoTvfq6ESfemtFGI/edit?usp=sharing'
# model= gpt.load_prompt(PROMT_URL)

# PROMT_URL_SUMMARY ='https://docs.google.com/document/d/1XhSDXvzNKA9JpF3QusXtgMnpFKY8vVpT9e3ZkivPePE/edit?usp=sharing'
# #PROMT_PODBOR_HOUSE = 'https://docs.google.com/document/d/1WTS8SQ2hQSVf8q3trXoQwHuZy5Q-U0fxAof5LYmjYYc/edit?usp=sharing'



# CHECK_WORDS = sheet.get_words_and_urls()

# @bot.message_handler(commands=['help', 'start'])
@app.route('/reg/<int:userID>/<string:message>')
def say_welcome(userID, message):

    #TODO
    # leadID = get_leadID_from(string=message)
    # row = {'id': userID,  'payload': '', 'leadID':leadID}
    
    row = {'id': userID,  'payload': '', 'leadID':1}
    sql.replace_query('SaleBot', row)
    
    text = """Здравствуйте, я AI ассистент компании Проф заборы. Я отвечу на Ваши вопросы по поводу строительства заборов 😁. Хотите я Вам расскажу про варианты комплектации ?"""
    return {'abs':text}
#expert_promt = gpt.load_prompt('https://docs.google.com/document/d/181Q-jJpSpV0PGnGnx45zQTHlHSQxXvkpuqlKmVlHDvU/')



def callback_inline(callFull):
    global URL_USERS, QUESTS_USERS,TYPE_QUESTIONS,COUNT_ZABOR_USER
    userID = callFull.message.chat.id
    call = callFull.data.split('_')
    logger.debug(f'{call=}')
    # if call[0] == 'type':


    if call[0] == 'type':
        bot.send_message(userID, TYPE_QUESTIONS[call[1]]['1']['text'],reply_markup=TYPE_QUESTIONS[call[1]]['1']['keyboard'])
        sql.set_payload(userID, f'quest_2_{call[1]}')

        try:
            QUESTS_USERS[userID].append([call[1]])
        except:
            QUESTS_USERS.setdefault(userID,[[call[1]]])

        bot.answer_callback_query(callFull.id)
        return 0
    
    if call[0] == 'profNastil' or call[0] == 'evroShtak':    
        payload = sql.get_payload(userID)
        quest = str(int(payload.split('_')[1]))
        logger.debug(f'{quest=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
         
        
        bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard'])
        QUESTS_USERS[userID][COUNT_ZABOR_USER[userID]['real']-1].append(call[1])
        sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')
        bot.answer_callback_query(callFull.id)
        
        return 0
    
    bot.send_message(userID,f'вот {QUESTS_USERS[userID]=}')
    # sql.set_payload(userID, 'exit')
    

def get_leadID_from(string:str)-> int:
    string= string.replace('\r','')
    rows = string.split('\n')
    for row in rows:
        if row.startswith('amo_lead_id:'):
            return int(row.split(' ')[1])
        
@app.route('/<int:userID>/<string:message>')
@logger.catch
def any_message(userID,message):
    global URL_USERS, QUESTS_USERS,TYPE_QUESTIONS,COUNT_ZABOR_USER
    # print('da')

    
    
    #TODO
    # leadID = sql.get_leadID(userID)
    # if leadID is not None:
    #     isSendAnswer = check_need_answered_for(leadID=leadID)
    #     logger.debug(f'{isSendAnswer=}')
    #     logger.debug(f'{leadID=}')
    
    
    # data = request.get_json() 
    # logger.debug(f'{data=}') 
    

    
    
    # return {'asd':'test text'}

    #print('это сообщение', message)
    # text = message.text.lower()
    text = message
    userID= userID
   
    username = userID
    # try: 
    payload = sql.get_payload(userID)
    # except:
    #     say_welcome

    
    #TODO добавить в конец вопрос хотите добавить еще секцию? и нет спасибо 
    if text == 'calc': 
        text = "Из скольки видов материала хотите забор? (максимум по 3 секции одного материала)(введите число от 1..3)"
        # bot.send_message(userID,'Из скольки видов материала хотите забор? (максимум по 3 секции одного материала)(введите число от 1..3)',)
        sql.set_payload(userID, 'quest_0')
        # ALL_QUESTS_USERS[userID]={
        #     'profNastil':[],
        #     'evroShtak':[],
        # }
        QUESTS_USERS[userID]=[] 
        return {'asd':text}

    #Выбор продолжить или нет добавлять новые секции
    if payload == 'select':
        if text == '1': #ДА
            sql.set_payload(userID,'quest_0')
        elif text == '2':#НЕТ
            # sql.set_payload(userID,'exit')
            sql.set_payload(userID,'generate')
        payload = 'generate'
        
        # typeMaterial =questionTypeMaterialEN[int(SECTION_QUESTS_USERS[userID][0])]
        typeMaterial =SECTION_QUESTS_USERS[userID][0][:-1]
        # ALL_QUESTS_USERS[userID][typeMaterial].append(SECTION_QUESTS_USERS[userID])
        QUESTS_USERS[userID].append(SECTION_QUESTS_USERS[userID])
    
    if payload == 'quest_0':
        
        try:
            COUNT_ZABOR_USER[userID]['real'] += 1  
        except:
            COUNT_ZABOR_USER.setdefault(userID, {'max':int(text),
                                                 'real': 1,
                                                 'profNastil': 1,
                                                 'evroShtak':1})
        numberZabor = COUNT_ZABOR_USER[userID]['real'] 
        textSendMessage = f'Из какого материала будет секция?\n'
        keyboardText = questionTypeMaterial
        keyboardText = prepare_dict_keyboadr(keyboardText)
        textSendMessage += keyboardText

        SECTION_QUESTS_USERS[userID] = []
        sql.set_payload(userID, 'quest_1') 
        # bot.send_message(userID,f'Из какого материала будет {numberZabor}я секция?',reply_markup=keyboard_quest1())
        
        return {'asd':textSendMessage}


    if payload.startswith('quest'):
        numberQuest = int(payload.split('_')[1])
        
        logger.debug(f'{payload}')
        if payload == 'quest_1':
            typeQuest = questionTypeMaterialEN[int(text)]
            typeMaterialQuest = questionTypeMaterial[int(text)]
             
        else:
            typeQuest = payload.split('_')[2] 
            # typeMaterialQuest = payload.split('_')[2] 

        listQuestions = TYPE_QUESTIONS[typeQuest]
        
        if numberQuest == len(listQuestions):
            textSendMessage = 'Хотите выбрать еще секцию?\n1. Да\n2. Нет'
            sql.set_payload(userID,'select')
            logger.critical('запрос на выборку секции')
            return {'asd':textSendMessage}
        try:
            textAnsewer = text if listQuestions[numberQuest]['keyboard'] is None else listQuestions[numberQuest]['keyboard'][int(text)] 
        except:
            textAnsewer = text 

        if payload != 'quest_1':
            SECTION_QUESTS_USERS[userID].append(textAnsewer)
        else:
            #Евроштакетник
            typeMaterial = questionTypeMaterialEN[int(text)]
            # SECTION_QUESTS_USERS[userID].append(questionTypeMaterialEN[int(text)]+ )
            SECTION_QUESTS_USERS[userID].append(typeMaterial+f"{COUNT_ZABOR_USER[userID][typeMaterial]}")
            SECTION_QUESTS_USERS[userID].append(textAnsewer)
            # SECTION_QUESTS_USERS[userID].append(int(text))
    
        logger.debug(f'Ответ на {numberQuest} вопрос {textAnsewer} для {typeQuest}')

         
        if listQuestions[numberQuest]['keyboard'] is None: 
            textSendMessage = listQuestions[numberQuest]['text']
        else:
            keyboard = prepare_dict_keyboadr(listQuestions[numberQuest]['keyboard'])
            textSendMessage = listQuestions[numberQuest]['text'] + keyboard  
        logger.debug(f'Ответ на {numberQuest} {textSendMessage} вопрос {textAnsewer} для {typeQuest}')

        payload = f'quest_{int(numberQuest)+1}_{typeQuest}'
        sql.set_payload(userID,payload)
        return {'asd':textSendMessage}

    if payload.startswith('generate'): 

        print(f"{COUNT_ZABOR_USER[userID]['real']=} {COUNT_ZABOR_USER[userID]['max']=}")
        # print(f'{int(quest)=} {len(listQuestions)=}')
        
        # if int(quest) == len(listQuestions)+1 and COUNT_ZABOR_USER[userID]['real'] < COUNT_ZABOR_USER[userID]['max']:
        #         sql.set_payload(userID, 'quest_0') 
        #         return 0
        # elif int(quest) == len(listQuestions) and COUNT_ZABOR_USER[userID]['real'] == COUNT_ZABOR_USER[userID]['max']:
            
        sql.set_payload(userID, 'exit')
        # bot.send_message(userID, f'{QUESTS_USERS[userID]=}')
        
        path = ''
        copyTable = True
        # for answers in QUESTS_USERS[userID]:
        print(f'{QUESTS_USERS=}') 
        for answers in QUESTS_USERS[userID]:
            pprint(QUESTS_USERS[userID])
            # answersOneSection = answersAll[answersAll]
            # for answers in answersOneSection:

            print(f'{answers=}')
            print(f'{COUNT_ZABOR_USER[userID]=}')
            # print(f'{COUNT_ZABOR_USER[userID][answers[0]]=}')
            # typeQuest1 = f"{answers[0]}{COUNT_ZABOR_USER[userID][answers[0]][:-1]}"
            typeQuest1 = answers[0]
            print(f'{typeQuest1=}')
            # path = send_values_in_sheet(typeQuest1, answers, f'{username}_{QUESTS_USERS[userID][0][0]}', first=copyTable)   
            path = send_values_in_sheet(typeQuest1, answers, f'{username}_{typeQuest1}', first=copyTable)   
            # COUNT_ZABOR_USER[userID][answers[0]] += 1
            copyTable = False
            #path = send_values_in_sheet(typeQuest, QUESTS_USERS[userID], f'{username} {QUESTS_USERS[userID][0]}',)   
        
        sheet = Sheet('GDtxt.json',path,get_worksheet=1)
        url = sheet.export_pdf(path)
        #отправка файла
        # with open('pdfCalc/'+path+'.pdf', 'rb') as pdf_file:
        #     bot.send_message(userID,'Вот предворительный расчет, после провери менеджер свяжется с вами и предоставит скидку')
        #     bot.send_document(userID, pdf_file)#filename='file.pdf')
        # else:    
        #     sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')
        textAnsewer = f'Спасибо за ответы, мы просчитаем Ваш проект и свяжемся с вами \n\n вот предворительный расчет {url}'
        return {'asd':textAnsewer}


    #TODO выбросить
    if payload.startswith('quest'):
        QUESTS_USERS[userID][COUNT_ZABOR_USER[userID]['real']-1].append(text)
        quest = payload.split('_')[1]
        logger.debug(f'{quest=}')
        logger.debug(f'{text=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
        try:
            #TODO 
            #добавить клавиатуру как текст с кнопками 
            textMessage = listQuestions[quest]['text'] 
            keyboard = listQuestions[quest]['keyboard'] 
            bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard']) 
        except Exception as e:

            sql.set_payload(userID, 'quest_1') 
            try:
                COUNT_ZABOR_USER[userID]['real'] += 1  
            except:
                COUNT_ZABOR_USER.setdefault(userID, {'max':int(text),
                                                    'real': 1,
                                                    'profNastil': 1,
                                                    'evroShtak':1})
            numberZabor = COUNT_ZABOR_USER[userID]['real'] 
            bot.send_message(userID,f'Из какого материала будет {numberZabor}я секция?',reply_markup=keyboard_quest1())
            return 0
        
        # if COUNT_ZABOR_USER[userID]['real'] == COUNT_ZABOR_USER[userID]['max']+1: 
        #         sql.set_payload(userID, 'quest_20') 
        #         return 0

        print(f"{COUNT_ZABOR_USER[userID]['real']=} {COUNT_ZABOR_USER[userID]['max']=}")
        print(f'{int(quest)=} {len(listQuestions)=}')
        
        if int(quest) == len(listQuestions)+1 and COUNT_ZABOR_USER[userID]['real'] < COUNT_ZABOR_USER[userID]['max']:
                sql.set_payload(userID, 'quest_0') 
                return 0
        elif int(quest) == len(listQuestions) and COUNT_ZABOR_USER[userID]['real'] == COUNT_ZABOR_USER[userID]['max']:
            bot.send_message(userID,'Спасибо за ответы, мы просчитаем Ваш проект и свяжемся с вами')
            sql.set_payload(userID, 'exit')
            bot.send_message(userID, f'{QUESTS_USERS[userID]=}')
            
            path = ''
            copyTable = True
            for answers in QUESTS_USERS[userID]:
                pprint(QUESTS_USERS[userID])
                typeQuest1 = f"{answers[0]}{COUNT_ZABOR_USER[userID][answers[0]]}"
                print(f'{typeQuest1=}')
                path = send_values_in_sheet(typeQuest1, answers, f'{username}_{QUESTS_USERS[userID][0][0]}', first=copyTable)   
                COUNT_ZABOR_USER[userID][answers[0]] += 1
                copyTable = False
                #path = send_values_in_sheet(typeQuest, QUESTS_USERS[userID], f'{username} {QUESTS_USERS[userID][0]}',)   
            sheet = Sheet('GDtxt.json',path,get_worksheet=1)
            sheet.export_pdf(path)
            with open('pdfCalc/'+path+'.pdf', 'rb') as pdf_file:
                bot.send_message(userID,'Вот предворительный расчет, после провери менеджер свяжется с вами и предоставит скидку')
                bot.send_document(userID, pdf_file)#filename='file.pdf')
        else:    
            sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')

        return 0 



    if payload == 'addmodel':
        text = text.split(' ')
        rows = {'model': text[1], 'url': text[0] }
        sql.replace_query('model',rows)
        return 0
    
    if payload == 'addpromt':
        text = text.split(' ')
        rows = {'promt': text[1], 'url': text[0] }
        sql.replace_query('prompt',rows)
        return 0
    
    
    add_message_to_history(userID, 'user', text)
    history = get_history(str(userID))
    logger.info(f'история {history}')

    #для теста почему-то иногда бывыет битая ссылка
    try:
        logger.info(f'{PROMT_URL}')
        model= gpt.load_prompt(PROMT_URL) 
    except:
        model= gpt.load_prompt(PROMT_URL) 

    lastMessage = history[-1]['content'] 
        
    try:
        if text == 'aabb':
            #принудительная саммари диалога
            1/0
        answer, allToken, allTokenPrice, message_content = gpt.answer_index(model, lastMessage+text, history, model_index,temp=0.5, verbose=0)
    
        logger.info(f'ответ сети если нет ощибок: {answer}')
    except Exception as e:
        #саммари если превышено колтчество токенов
        if isDEBUG : bot.send_message(userID, e)
        history = summary(userID, e) 
        
        answer, allToken, allTokenPrice, message_content = gpt.answer_index(model, text, history, model_index,temp=0.5, verbose=0)
        bot.send_message(message.chat.id, answer)
        add_message_to_history(userID, 'assistant', answer)

        return 0 
    
   
    add_message_to_history(userID, 'assistant', answer)

    prepareAnswer= answer.lower()
 
    b = prepareAnswer.find('спасибо за предоставленный номер') 
    print(f'{b=}')

    logger.info(f'{message_content=}')
        
    # photoFolder = message_content[0].page_content.find('https://drive') 
    # logger.info(f'{photoFolder=}')
    bot.send_message(message.chat.id, answer,  parse_mode='markdown')
    media_group = []

    photoFolder = -1
    urls = check_need_words(CHECK_WORDS,prepareAnswer)
    if urls != [] :
        photoFolder = 1

    if photoFolder >= 0:
        logger.info(f'{URL_USERS=}')
        # pattern = r"КД-\d+"

        # matches = re.findall(pattern, answer)
        # matches = list(set(matches))
        #TODO удалить если нужно чтобы фото отправлялись по 1 разу
        #URL_USERS={}
        bot.send_message(message.chat.id, 'Подождите, ищу фото проектов...',  parse_mode='markdown')
        for url in urls:
            try:
                URL_USERS, media_group,nameProject = download_photo(url,URL_USERS,userID,)
                if media_group == []:
                    continue
                bot.send_message(message.chat.id, f'Отправляю фото проекта {nameProject}...',  parse_mode='markdown')
                bot.send_media_group(message.chat.id, media_group,)
            except Exception as e:
                bot.send_message(message.chat.id, 'Извините, не могу найти актуальные фото',  parse_mode='markdown') 
                #bot.send_message(message.chat.id, e,  parse_mode='markdown')
    if b >= 0:
        print(f"{prepareAnswer.find('cпасибо за предоставленный номер')=}")
        PROMT_SUMMARY = gpt.load_prompt(PROMT_URL_SUMMARY)
        history = get_history(str(userID))
        history_answer = gpt.answer(PROMT_SUMMARY,history)[0]
        print(f'{history_answer=}')
        print(f'{answer=}')
        #bot.send_message(message.chat.id, answer)
        phone = slice_str_phone(history_answer)
        pprint(f"{phone=}")
        
        print('запиь в битрикс')
        update_deal(phone, history_answer)

    
    now = datetime.now()+timedelta(hours=3)

    formatted_date = now.strftime("%Y-%m-%dT%H:%M:%S")
    
    #answer, allToken, allTokenPrice= gpt.answer(' ',mess,)
    row = {'all_price': float(allTokenPrice), 'all_token': int(allToken), 'all_messages': 1}
    sql.plus_query_user('user', row, f"id={userID}")
    
    
    rows = {'time_epoch': time_epoch(),
            'MODEL_DIALOG': payload,
            'date': formatted_date,
            'id': userID,
            'nicname': username,
            #'token': username,
            #'token_price': username,
            'TEXT': f'Клиент: {text}'}
    sql.insert_query('all_user_dialog',  rows)
    
    rows = {'time_epoch': time_epoch(),
            'MODEL_DIALOG': payload,
            'date': formatted_date,
            'id': userID,
            'nicname': username,
            'token': allToken,
            'token_price': allTokenPrice,
            'TEXT': f'Менеджер: {answer}'}
    sql.insert_query('all_user_dialog',  rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5004')    
    # mesList = ['calc','2','1','2','3','4','5','6','7','8','9']
    # # mesList = ['calc','1','2','3','4','5','6','7','8','9','10']
    # for i in mesList:
    #     any_message(1,i)
    # print(f'[OK]')
    # bot.infinity_polling()
