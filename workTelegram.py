import os
import telebot
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
# from workBitrix import *
from helper import *
from workGDrive import *
from telebot.types import InputMediaPhoto
from workRedis import *
import workGS
from questions import *
import requests
from amocrmWork import create_lead

load_dotenv()
isDEBUG = True
isSend = True
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("file_1.log", rotation="50 MB")
gpt = GPT()
GPT.set_key(os.getenv('KEY_AI'))
bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))


# sheet = workGS.Sheet('profzaboru-5f6f677a3cd8.json','Ссылки на изображения')s
sql = workYDB.Ydb()

CHAT_ROOM_URL = os.environ.get('CHAT_ROOM_URL')


TYPE_QUESTIONS = {'profNastil': questionProfNastil,
                  'evroShtak':questionEvroShtak,
                  'GridRabit':questionGridRabit,
                  '3d':question3d,
                  'Zaluzi':questionZaluzi} 
URL_USERS = {}
QUESTS_USERS = {}
COUNT_ZABOR_USER={}
MODEL_URL= 'https://docs.google.com/document/d/1M_i_C7m3TTuKsywi-IOMUN0YD0VRpfotEYNp1l2CROI/edit?usp=sharing'
#gsText, urls_photo = sheet.get_gs_text()
#print(f'{urls_photo=}')

def set_isSend():
    global isSend
    isSend = False

@bot.message_handler(commands=['addmodel'])
def add_new_model(message):
    sql.set_payload(message.chat.id, 'addmodel')
    bot.send_message(message.chat.id, 
        "Пришлите ссылку model google document и через пробел название модели (model1). Не используйте уже существующие названия модели\n Внимани! конец ссылки должен вылядить так /edit?usp=sharing",)

def check_time_last_message(userID):
    try:
        time_last_mess = sql.select_query('user',f'id = {userID}')[0]['time_last_mess']
    except Exception as e:
        logger.debug(f'{e=}')
        return True
    
    time_last_mess = timestamp_to_date(time_last_mess)
    time_last_mess = datetime.strptime(time_last_mess, '%Y-%m-%dT%H:%M:%SZ')
    time_now = datetime.now()
    delta = time_now - time_last_mess
    logger.debug(f'{delta=}')
    logger.debug(f'{delta < timedelta(hours=1)=}')

    if delta < timedelta(hours=1):
        return False
    else:
        return True
    

def send_message_to_telegram(userID, message):
    row = {
        'time_last_mess': get_dates(0)[0],
    }
    sql.update_query('user', row, f'id = {userID}')
    bot.send_message(userID, message)

@bot.message_handler(commands=['calc'])
def add_new_model(message):
    #sql.set_payload(message.chat.id, 'addmodel')
    try:
        path = create_pdf()
    except:
        path = 'file.pdf'
    with open(path, 'rb') as pdf_file:
        # Отправьте PDF-файл пользователю, указав параметр filename
        bot.send_document(message.chat.id, pdf_file, )#filename='file.pdf')
    bot.send_message(message.chat.id, 
        "Вот пример расчета",)

@bot.message_handler(commands=['addpromt'])
def add_new_model(message):
    sql.set_payload(message.chat.id, 'addpromt')
    bot.send_message(message.chat.id, 
        "Пришлите ссылку promt google document и через пробел название промта (promt1). Не используйте уже существующие названия модели\n Внимани! конец ссылки должен вылядить так /edit?usp=sharing",)
    

@bot.message_handler(commands=['help', 'start'])
def say_welcome(message):
    global isSend
    username = message.from_user.username
    userID =  message.chat.id 
    a = requests.post(f'{CHAT_ROOM_URL}/create/room/{userID}',timeout=1)
    logger.debug(a)
    isSend = True

    row = {
        ''
    }
    lead_id = create_lead(userName=username, userID=userID)
    
    lead_id =0
    row = {'id': 'Uint64', 'MODEL_DIALOG': 'String', 'TEXT': 'String'}
    sql.create_table(str(message.chat.id), row)
    #row = {'id': message.chat.id, 'payload': '',}
    row = {'id': message.chat.id, 'model': 'model1', 'promt': 'promt1','nicname':username, 'payload': '','lead_id':lead_id}
    sql.replace_query('user', row)
    
    text = """Здравствуйте, я AI ассистент компании ПрофЗаборы. Я отвечу на Ваши вопросы по поводу строительства заборов 😁. 
Если Вы хотите, что бы я Вам рассказал про варианты комплектации, то нажмите на кнопку "Консультация". Если у Вас есть все параметры вашего забора и вы хотите посчитать стоимость, то выберите "Калькулятор"""
    a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {text}',timeout=1)
    clear_history(message.chat.id)
    add_message_to_history(userID, 'assistant', text)
    bot.send_message(message.chat.id, text, 
                     parse_mode='markdown',
                     reply_markup= create_menu_keyboard())
#expert_promt = gpt.load_prompt('https://docs.google.com/document/d/181Q-jJpSpV0PGnGnx45zQTHlHSQxXvkpuqlKmVlHDvU/')

@bot.message_handler(commands=['restart'])
def restart_modal_index(message):
    global model_index, model 
    model_index=gpt.load_search_indexes(MODEL_URL)
    #url = 'https://docs.google.com/document/d/1f4GMt2utNHsrSjqwE9tZ7R632_ceSdgK6k-_QwyioZA/edit?usp=sharing'
    #model= gpt.load_prompt(url)
    model= gpt.load_prompt(PROMT_URL)
    bot.send_message(message.chat.id, 'Обновлено', 
                     parse_mode='markdown',
                     reply_markup= create_menu_keyboard())

@bot.message_handler(commands=['context'])
def send_button(message):
    global URL_USERS
    URL_USERS={}
    payload = sql.get_payload(message.chat.id)
    

    #answer = gpt.answer(validation_promt, context, temp = 0.1)
    sql.delete_query(message.chat.id, f'MODEL_DIALOG = "{payload}"')
    sql.set_payload(message.chat.id, ' ')
    #bot.send_message(message.chat.id, answer)
    clear_history(message.chat.id)
    bot.send_message(message.chat.id, 
        "Контекст сброшен",reply_markup=create_menu_keyboard(),)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
     # Получаем информацию о фото
    username = message.from_user.username
    photo_info = message.photo[-1]
    file_id = photo_info.file_id

    # Скачиваем фото
    file_info = bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEBOT_TOKEN')}/{file_info.file_path}" 
    fileName = download_file(file_url)
    #create_lead_and_attach_file([fileName], username)
    bot.reply_to(message, f'Спасибо, мы просчитаем Ваш проект и свяжемся с вами')

@bot.message_handler(content_types=['document'])
def handle_document(message):
    userID= message.chat.id
    username = message.from_user.username
    logger.info(f'{message.document=}')#
    #for document in message.document:
    file_info = bot.get_file(message.document.file_id)
    pprint(file_info)
    file_url = f"https://api.telegram.org/file/bot{os.getenv('TELEBOT_TOKEN')}/{file_info.file_path}"
        # Отправляем ответное сообщение
    fileName = download_file(file_url)
    #create_lead_and_attach_file([fileName], username)
    bot.reply_to(message, f'Спасибо, мы просчитаем Ваш проект и свяжемся с вами')
    

    #create_lead_and_attach_file([],userID)


@bot.callback_query_handler(func=lambda call: True)
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
    if call[0] in ['profNastil','evroShtak', 'GridRabit', '3d', 'Zaluzi']: 
    # if call[0] == 'profNastil' or call[0] == 'evroShtak':    
        payload = sql.get_payload(userID)
        quest = str(int(payload.split('_')[1]))
        logger.debug(f'{quest=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Клиент: {call[1]}',timeout=1)

        textAnswer=listQuestions[quest]['text']
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1) 
        
        bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard'])
        QUESTS_USERS[userID][COUNT_ZABOR_USER[userID]['real']-1].append(call[1])
        sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')
        bot.answer_callback_query(callFull.id)
        
        return 0
    
    bot.send_message(userID,f'вот {QUESTS_USERS[userID]=}')
    # sql.set_payload(userID, 'exit')
    


@bot.message_handler(content_types=['text'])
@logger.catch
def any_message(message):
    global URL_USERS, QUESTS_USERS,TYPE_QUESTIONS,COUNT_ZABOR_USER, isSend
    #print('это сообщение', message)
    #text = message.text.lower()
    text = message.text
    userID= message.chat.id
    username = message.from_user.username
    payload = sql.get_payload(userID)
    logger.debug(payload)
    logger.debug(text)
    
    
    a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Клиент:{text}',timeout=1)
    
    
        
    phone = find_phone_numbers(text)
    if phone != []:
        textAnswer = 'Спасибо, передал менеджеру'
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        bot.send_message(userID,textAnswer)
        return 0

    if text == 'Калькулятор':
        textAnswer = """Сколько разных видов материалов будет использоваться в заборе? Введите число от 1 до 3. \n
- указывайте длину забора с учетом ширины ворот и калиток
- если во время или после расчета у вас останутся вопросы по комплектации забора, оставляйте свой номер телефона, менеджер свяжется, проконсультирует и посчитает более точно"""
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        sql.set_payload(userID, 'quest_0')

        bot.send_message(userID,textAnswer,)
        COUNT_ZABOR_USER[userID]=0
        # a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}')
        return 0
    
    if text == 'Консультация':
        textAnswer = 'Я считаю себя экспертом в заборостроении и готов помочь вам ответить на вопросы в этой сфере! Задавайте)'
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        # sql.set_payload(userID, 'quest_0')
        bot.send_message(userID,textAnswer,)
        add_message_to_history(userID, 'assistant', textAnswer)
        return 0 

    if payload == 'quest_0':
        sql.set_payload(userID, 'quest_1') 
        try:
            COUNT_ZABOR_USER[userID]['real'] += 1 

        except Exception as e :
            logger.debug(f'{e=}')
            COUNT_ZABOR_USER.setdefault(userID, {'max':int(text),
                                                 'real': 1,
                                                 'profNastil': 1,
                                                 'evroShtak':1,
                                                 'GridRabit':1,
                                                 '3d':1,
                                                 'Zaluzi':1})
            COUNT_ZABOR_USER[userID] = {'max':int(text),
                                        'real': 1,
                                        'profNastil': 1,
                                        'evroShtak':1,
                                        'GridRabit':1,
                                        '3d':1,
                                        'Zaluzi':1}
            
        numberZabor = COUNT_ZABOR_USER[userID]['real'] 

        textAnswer=f'Из какого материала будет {numberZabor}я часть?'
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        bot.send_message(userID,textAnswer,reply_markup=keyboard_quest1())
        return 0
    
    if payload == 'quest_last':
        textAnswer = 'Растояние от МКАД (км)'
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        sql.set_payload(userID, 'quest_end')
        bot.send_message(userID,textAnswer)
        return 0
    
    if payload == 'quest_end':
        textAnswer='Делаем расчет стоимости забора...'
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
        # bot.send_message(userID,QUESTS_USERS[userID])
        bot.send_message(userID,textAnswer)
        sql.set_payload(userID, 'exit')
        # bot.send_message(userID, f'{QUESTS_USERS[userID]=}')
        path = ''
        copyTable = True
        for answers in QUESTS_USERS[userID]:
            pprint(QUESTS_USERS[userID])
            typeQuest1 = f"{answers[0]}{COUNT_ZABOR_USER[userID][answers[0]]}"
            print(f'{typeQuest1=}')
            path = send_values_in_sheet(typeQuest1, answers, f'{username}_{QUESTS_USERS[userID][0][0]}', first=copyTable, mkad=text)   
            COUNT_ZABOR_USER[userID][answers[0]] += 1
            copyTable = False
            #path = send_values_in_sheet(typeQuest, QUESTS_USERS[userID], f'{username} {QUESTS_USERS[userID][0]}',)   
        sheet = Sheet('GDtxt.json',path,get_worksheet=1)
        sheet.export_pdf(path)
        with open('pdfCalc/'+path+'.pdf', 'rb') as pdf_file:
            # textAnswer='Вот предворительный расчет, после проверки менеджер свяжется с вами и предоставит скидку'
            textAnswer='Стоимость со СКИДКОЙ в этом расчете действительна в течении 1 недели. Оставьте свой номер телефона, менеджер свяжется с Вами и согласует дату и время замера'
            a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}',timeout=1)
            
            bot.send_message(userID,textAnswer)
            bot.send_document(userID, pdf_file)#filename='file.pdf')
            a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: отправил файл {path}', timeout=1)
            add_message_to_history(userID,'assistant','КЛИЕНТ УЖЕ СДЕЛАЛ РАСЧЕТ В КАЛЬКУЛЯТОРЕ, больше не предлагать')
            COUNT_ZABOR_USER[userID] = {'max':int(text),
                                        'real': 1,
                                        'profNastil': 1,
                                        'evroShtak':1,
                                        'GridRabit':1,
                                        '3d':1,
                                        'Zaluzi':1}
            QUESTS_USERS[userID] = {}
        return 0

    if payload.startswith('quest'):
        QUESTS_USERS[userID][COUNT_ZABOR_USER[userID]['real']-1].append(text)
        quest = payload.split('_')[1]
        logger.debug(f'{quest=}')
        logger.debug(f'{text=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
        try:
            textAnswer=listQuestions[quest]['text']
            a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}', timeout=1)
            if textAnswer != 'Это конец вопросов секции':
                bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard'])
            else:
                if COUNT_ZABOR_USER[userID]['max'] > 1:
                    # sql.set_payload(userID, 'quest_last')
                    quest = str(int(quest)+1)

        except Exception as e:

            # logger.debug(f'{e=}')
            # bot.send_message(userID,'Спасибо за ответ1ы, мы просчитаем Ваш проект и свяжемся с вами')
            # sql.set_payload(userID, 'exit')
            # # bot.send_message(userID, f'{QUESTS_USERS[userID]=}')
            # path = ''
            # for answers in QUESTS_USERS[userID]:
            #     typeQuest = f"{typeQuest}{COUNT_ZABOR_USER[userID][answers[0]]}"
            #     path = send_values_in_sheet(typeQuest, answers, f'{username}_{QUESTS_USERS[userID][0][0]}',)   
            #     COUNT_ZABOR_USER[userID][answers[0]]+1
            #     #path = send_values_in_sheet(typeQuest, QUESTS_USERS[userID], f'{username}_{QUESTS_USERS[userID][0]}',)   
            # sheet.export_pdf(path)
            # with open('pdfCalc/'+path+'.pdf', 'rb') as pdf_file:
            #     bot.send_message(userID,'Вот предворительный расчет, после провери менеджер свяжется с вами и предоставит скидку')
            #     bot.send_document(userID, pdf_file)#filename='file.pdf')
            # return 0
            sql.set_payload(userID, 'quest_1') 
            try:
                COUNT_ZABOR_USER[userID]['real'] += 1  
            except:
                COUNT_ZABOR_USER.setdefault(userID, {'max':int(text),
                                                 'real': 1,
                                                 'profNastil': 1,
                                                 'evroShtak':1,
                                                 'GridRabit':1,
                                                 '3d':1,
                                                 'Zaluzi':1})
                
            numberZabor = COUNT_ZABOR_USER[userID]['real'] 
            textAnswer=f'Из какого материала будет {numberZabor}я часть?' 
            a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}', timeout=1)
            bot.send_message(userID,textAnswer,reply_markup=keyboard_quest1())
            
            
            return 0
        
        # if COUNT_ZABOR_USER[userID]['real'] == COUNT_ZABOR_USER[userID]['max']+1: 
        #         sql.set_payload(userID, 'quest_20') 
        #         return 0

        print(f"{COUNT_ZABOR_USER[userID]['real']=} {COUNT_ZABOR_USER[userID]['max']=}")
        print(f'{int(quest)=} {len(listQuestions)=}')
        


        if int(quest) >= len(listQuestions)+1 and COUNT_ZABOR_USER[userID]['real'] < COUNT_ZABOR_USER[userID]['max']:
                sql.set_payload(userID, 'quest_0') 
                any_message(message)
                return 0
        
        elif int(quest) >= len(listQuestions) and COUNT_ZABOR_USER[userID]['real'] == COUNT_ZABOR_USER[userID]['max']:
            sql.set_payload(userID, 'quest_last')
            any_message(message)
            return 0

        else:    
            sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')

        return 0 

    # if check_time_last_message(userID) == False: return 0
    # if not isSend: return 0
    
    
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
        # else:
            
        logger.info(f'ответ сети если нет ощибок: {answer}')
    except Exception as e:
        #саммари если превышено колтчество токенов
        if isDEBUG : bot.send_message(userID, e)
        history = summary(userID, e) 
        
        answer, allToken, allTokenPrice, message_content = gpt.answer_index(model, text, history, model_index,temp=0.5, verbose=0)
        
        textAnswer=answer
        
        if isSend:
            a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}', timeout=1)
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
    textAnswer=answer
    
    if isSend:
        a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}', timeout=1)
        bot.send_message(message.chat.id, answer,  parse_mode='markdown')
    else: return 0

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
        isFirst = True
        
        for url in urls:
            try:
                URL_USERS, media_group,nameProject = download_photo(url,URL_USERS,userID,)
                if media_group == [] or media_group == 0:
                    continue
                if isFirst:
                    isFirst = False
                    bot.send_message(message.chat.id, 'Подождите, ищу фото проектов...',  parse_mode='markdown')
                
                textAnswer=f'Отправляю фото {nameProject}...'
                

                bot.send_message(message.chat.id, textAnswer,  parse_mode='markdown')
                bot.send_media_group(message.chat.id, media_group,)

            except Exception as e:
                textAnswer=f'Извините, не могу найти актуальные фото'
                bot.send_message(message.chat.id, textAnswer,  parse_mode='markdown') 
                bot.send_message(message.chat.id, e,  parse_mode='markdown')
                a = requests.post(f'{CHAT_ROOM_URL}/message/{userID}/Бот: {textAnswer}') 
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
        
    #TODO
    model_index=gpt.load_search_indexes(MODEL_URL)

    # model_project = gpt.create_embedding(gsText)
    PROMT_URL = 'https://docs.google.com/document/d/10PvyALgUYLKl-PYwwe2RZjfGX5AmoTvfq6ESfemtFGI/edit?usp=sharing'
    model= gpt.load_prompt(PROMT_URL)
    logger.debug('model загружена')
    
    PROMT_URL_SUMMARY ='https://docs.google.com/document/d/1XhSDXvzNKA9JpF3QusXtgMnpFKY8vVpT9e3ZkivPePE/edit?usp=sharing'
    #PROMT_PODBOR_HOUSE = 'https://docs.google.com/document/d/1WTS8SQ2hQSVf8q3trXoQwHuZy5Q-U0fxAof5LYmjYYc/edit?usp=sharing'
    
    #TODO
    # sheet = workGS.Sheet('profzaboru-5f6f677a3cd8.json','Ссылки на изображения')
    # # sheet = workGS.Sheet('kgtaprojects-8706cc47a185.json','Ссылки на изображения')
    # logger.debug('sheet загружена')
    # a = sheet.get_rom_value(1)
    # logger.debug('a загружена')
    #TODO
    # CHECK_WORDS = sheet.get_words_and_urls()
    # logger.debug('CHECK_WORDS загружена')
    # # # check_time_last_message(400923372)

    print(f'[OK]')
    bot.infinity_polling()
