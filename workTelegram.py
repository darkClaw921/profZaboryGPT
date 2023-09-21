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
from workBitrix import *
from helper import *
from workGDrive import *
from telebot.types import InputMediaPhoto
from workRedis import *
import workGS
from questions import *
load_dotenv()
isDEBUG = True

logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("file_1.log", rotation="50 MB")
gpt = GPT()
GPT.set_key(os.getenv('KEY_AI'))
bot = telebot.TeleBot(os.getenv('TELEBOT_TOKEN'))
sheet = workGS.Sheet('kgtaprojects-8706cc47a185.json','Ссылки на изображения')
sql = workYDB.Ydb()

TYPE_QUESTIONS = {'profNastil': questionProfNastil,} 
URL_USERS = {}
QUESTS_USERS = {}

MODEL_URL= 'https://docs.google.com/document/d/1M_i_C7m3TTuKsywi-IOMUN0YD0VRpfotEYNp1l2CROI/edit?usp=sharing'
#gsText, urls_photo = sheet.get_gs_text()
#print(f'{urls_photo=}')
model_index=gpt.load_search_indexes(MODEL_URL)
# model_project = gpt.create_embedding(gsText)
PROMT_URL = 'https://docs.google.com/document/d/10PvyALgUYLKl-PYwwe2RZjfGX5AmoTvfq6ESfemtFGI/edit?usp=sharing'
model= gpt.load_prompt(PROMT_URL)

PROMT_URL_SUMMARY ='https://docs.google.com/document/d/1XhSDXvzNKA9JpF3QusXtgMnpFKY8vVpT9e3ZkivPePE/edit?usp=sharing'
#PROMT_PODBOR_HOUSE = 'https://docs.google.com/document/d/1WTS8SQ2hQSVf8q3trXoQwHuZy5Q-U0fxAof5LYmjYYc/edit?usp=sharing'



CHECK_WORDS = sheet.get_words_and_urls()

@bot.message_handler(commands=['addmodel'])
def add_new_model(message):
    sql.set_payload(message.chat.id, 'addmodel')
    bot.send_message(message.chat.id, 
        "Пришлите ссылку model google document и через пробел название модели (model1). Не используйте уже существующие названия модели\n Внимани! конец ссылки должен вылядить так /edit?usp=sharing",)


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
    username = message.from_user.username
    row = {'id': 'Uint64', 'MODEL_DIALOG': 'String', 'TEXT': 'String'}
    sql.create_table(str(message.chat.id), row)
    #row = {'id': message.chat.id, 'payload': '',}
    row = {'id': message.chat.id, 'model': 'model1', 'promt': 'promt1','nicname':username, 'payload': ''}
    sql.replace_query('user', row)
    
    text = """Здравствуйте, я AI ассистент компании Проф заборы. Я отвечу на Ваши вопросы по поводу строительства заборов 😁. Хотите я Вам расскажу про варианты комплектации ?"""
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
    global URL_USERS, QUESTS_USERS,TYPE_QUESTIONS
    userID = callFull.message.chat.id
    call = callFull.data.split('_')
    logger.debug(f'{call=}')
    if call[0] == 'type':
        bot.send_message(userID, TYPE_QUESTIONS[call[1]]['1']['text'],reply_markup=TYPE_QUESTIONS[call[1]]['1']['keyboard'])
        sql.set_payload(userID, f'quest_2_{call[1]}')
        QUESTS_USERS.setdefault(userID,[call[1]])
        bot.answer_callback_query(callFull.id)
        return 0
    
    if call[0] == 'profNastil':    
        payload = sql.get_payload(userID)
        quest = str(int(payload.split('_')[1]))
        logger.debug(f'{quest=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
         
        
        bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard'])
        QUESTS_USERS[userID].append(call[1])
        sql.set_payload(userID, f'quest_{int(quest)+1}_{typeQuest}')
        bot.answer_callback_query(callFull.id)
        
        return 0
    
    bot.send_message(userID,f'вот {QUESTS_USERS[userID]=}')
    # sql.set_payload(userID, 'exit')
    


@bot.message_handler(content_types=['text'])
@logger.catch
def any_message(message):
    global URL_USERS, QUESTS_USERS,TYPE_QUESTIONS
    #print('это сообщение', message)
    #text = message.text.lower()
    text = message.text
    userID= message.chat.id
    username = message.from_user.username
    payload = sql.get_payload(userID)
    

    if text == 'calc':
        sql.set_payload(userID, 'quest_1')
        bot.send_message(userID,'Из какого материала хотите забор?',reply_markup=keyboard_quest1())
        return 0
    
    if payload.startswith('quest'):
        QUESTS_USERS[userID].append(text)
        quest = payload.split('_')[1]
        logger.debug(f'{quest=}')
        typeQuest = payload.split('_')[2]
        listQuestions = TYPE_QUESTIONS[typeQuest]
        try:
            bot.send_message(userID,listQuestions[quest]['text'],reply_markup=listQuestions[quest]['keyboard'])
        except Exception as e:
            logger.debug(f'{e=}')
            bot.send_message(userID,'Спасибо за ответы, мы просчитаем Ваш проект и свяжемся с вами')
            sql.set_payload(userID, 'exit')
            # bot.send_message(userID, f'{QUESTS_USERS[userID]=}')
            path = send_values_in_sheet(typeQuest, QUESTS_USERS[userID], f'{username} {QUESTS_USERS[userID][0]}',)   
            with open('pdfCalc/'+path+'.pdf', 'rb') as pdf_file:
                bot.send_message(userID,'Вот предворительный расчет, после провери менеджер свяжется с вами и предоставит скидку')
                bot.send_document(userID, pdf_file)#filename='file.pdf')
            return 0
        
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


    
print(f'[OK]')
bot.infinity_polling()
