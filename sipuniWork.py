from sipuni_api import Sipuni
from yandexSpeach import *
from dotenv import load_dotenv
load_dotenv()

client_id = os.environ.get('SIPUNU_CLIENT_ID')
secret_id = os.environ.get('SIPUNU_SECRET_ID')
client = Sipuni(client_id, secret_id)


# call statistic
from datetime import datetime, timedelta
a = client.get_call_stats(from_date=(datetime.now() - timedelta(days=1)), to_date=datetime.now())   # return csv data
print(a)

# import csv

# text_data = a

# csv_file = 'output.csv'

# # Splitting the text data by semicolon (;)
# data_list = text_data.split(';')

# with open(csv_file, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(data_list)
import requests

# # get call record
def get_url_record(fileID:str):
    import requests
    downloadURL = client.get_record(fileID)   
    # bytes = client.get_record(fileID)   
    response = requests.get(downloadURL)
    # response.raise_for_status() # вызывает исключение, если возникла ошибка при загрузке файла
    fileName=f'{fileID}.mp3'
    with open(fileName, "wb") as file:
        file.write(response.content)


    upload_file(fileName, bytes)
    print("Файл успешно загружен") 
    text = get_text_record(fileName)
    
    with open(f'{fileID}.txt', "w") as file:
        file.write(text) 
# 
get_url_record('1696324590.113123')
