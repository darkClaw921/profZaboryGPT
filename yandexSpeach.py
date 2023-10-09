import urllib.request
import json
from pprint import pprint
from loguru import logger
from dotenv import load_dotenv
load_dotenv
@logger.catch
def get_text_record(fileName:str):
    FOLDER_ID = "b1g83bovl5hjt7cl583v" # Идентификатор каталога
    API_KEY = os.environ.get('API_KEY_YANDEX_SPEACH')
    # filePath = '/Users/igorgerasimov/Python/Bitrix/test-chatGPT/aa/record.ogg'

    # длинные аудио
    import requests
    import time
    import json

    # Укажите ваш API-ключ и ссылку на аудиофайл в Object Storage.
    #key = '<IAM-токен_сервисного_аккаунта>'
    #filelink = 'https://storage.yandexcloud.net/ai-akademi-zabory-audios/audio_2023-08-03_20-05-07.ogg'
    filelink = f'https://storage.yandexcloud.net/ai-akademi-zabory-audios/{fileName}'

    POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"

    body ={
        "config": {
            "specification": {
                'audioEncoding': 'MP3',
                "languageCode": "ru-RU"
            }
        },
        "audio": {
            "uri": filelink
        }
    }

    header = {'Authorization': 'Api-Key {}'.format(API_KEY)}

    # Отправить запрос на распознавание.
    req = requests.post(POST, headers=header, json=body)
    data = req.json()
    print(data)

    id = data['id']

    # Запрашивать на сервере статус операции, пока распознавание не будет завершено.
    while True:

        time.sleep(1)

        GET = "https://operation.api.cloud.yandex.net/operations/{id}"
        req = requests.get(GET.format(id=id), headers=header)
        req = req.json()

        if req['done']: break
        print("Not ready")

    # Показать полный ответ сервера в формате JSON.
    # print("Response:")
    # print(json.dumps(req, ensure_ascii=False, indent=2))

    # Показать только текст из результатов распознавания.
    print("Text chunks:")
    pprint(req)
    fullText=''
    for chunk in req['response']['chunks']:
        # print(chunk['alternatives'][0]['text'])
        # fullText =+ chunk['alternatives'][0]['text']
        fullText1 = chunk['alternatives'][0]['text']
        print(fullText1)
        fullText+= fullText1+'\n'
    
    return fullText


import os
import boto3
from dotenv import load_dotenv

load_dotenv()

#os.env: Ж
session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    endpoint_url='https://storage.yandexcloud.net',
    aws_access_key_id=os.environ.get('aws_access_key_id'),
    aws_secret_access_key=os.environ.get('aws_secret_access_key'),
)
# Создать новый бакет
# s3.create_bucket(Bucket='bucket-name-123')

# # Загрузить объекты в бакет

# ## Из строки
# s3.put_object(Bucket='bucket-name-123', Key='object_name', Body='TEST', StorageClass='COLD')
# Создать новый бакет
# s3.create_bucket(Bucket='')

# Загрузить объекты в бакет

# Из строки
def upload_file(key, body:str):
    # s3.put_object(Bucket='ai-akademi-zabory-audios', Key=key,
    #           Body=body, StorageClass='COLD')
    s3.upload_file(key, 'ai-akademi-zabory-audios', key)

def get_file(key)->int:
    get_object_response = s3.get_object(Bucket='ai-akademi-zabory-audios', Key=key)['Body'].read()
    return(int(get_object_response))





#короткие до 30 сек
# with open(filePath, "rb") as f:
#     data = f.read()

# params = "&".join([
#     "topic=general",
#     "folderId=%s" % FOLDER_ID,
#     "lang=ru-RU"
# ])

# url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
# #url.add_header("Authorization", "Bearer %s" % IAM_TOKEN)
# url.add_header("Authorization", "Api-Key %s" % API_KEY)

# responseData = urllib.request.urlopen(url).read().decode('UTF-8')
# decodedData = json.loads(responseData)

# if decodedData.get("error_code") is None:
#     print(decodedData.get("result"))