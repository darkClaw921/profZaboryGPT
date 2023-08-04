import os
import io
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload
from dotenv import load_dotenv

load_dotenv()
# Установка облачного хранилища
api_key = os.getenv('api_key_google_drive')
service_account_file = 'GDtxt.json'
#service_account_file = '/Users/igorgerasimov/Python/Bitrix/test-chatGPT/GDtxt.json'
credentials = service_account.Credentials.from_service_account_file(service_account_file)
drive = build('drive', 'v3', credentials=credentials)

# ID папки в Google Drive
#folder_id = '1H7rj0sO_jNtd1NbsHhxJDh5VYBuxyHjj'

# Получение списка файлов в папке
def download_files(FOLDER_ID:str, maxFile:int = 5)-> list:
    """Скачивает файлы из папки в google drive

    Args:
        FOLDER_ID (str): id папки из которой качать
        maxFile (int, optional): сколько нужно скачать файлов Defaults to 5.

    Returns:
        list: список имен скаченных файлов
    """

    results = drive.files().list(q=f"'{FOLDER_ID}' in parents", pageSize=20).execute()
    folder_info = drive.files().get(fileId=FOLDER_ID, fields='name').execute()
    items = results.get('files', [])
    print(items)
    print(f'{folder_info}')
    # Создание папки для скачивания файлов
    download_folder = 'downloads/'
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Скачивание файлов
    file_list = []

    for i, item in enumerate(items):
        file_id = item['id']
        #file_name = os.path.join(download_folder, item['name'])
        file_name = f"{folder_info['name']} - {i}.png"

        request = drive.files().get_media(fileId=file_id)
        fh = io.FileIO(download_folder+file_name, mode='wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False

        while not done:
            status, done = downloader.next_chunk()

        print(f'Successfully downloaded file: {file_name}')
        file_list.append(file_name)
        if i == maxFile-1:
            return file_list

    print('All files downloaded successfully.')
    return file_list

if __name__ == '__main__':
    pass
    #download_files('1H7rj0sO_jNtd1NbsHhxJDh5VYBuxyHjj')