import yadisk 
import os
#запрос через приложение https://oauth.yandex.ru/authorize?response_type=token&client_id= айди приложения
token = 'y0_AgAAAAAhxYgkAAhiegAAAADN_6WND-7Hk8pGQGi2H453O_ihG89sYQY'
disk = yadisk.YaDisk(token=token)
folder_path = '/test'
files = disk.listdir(folder_path)
print(files)
for file in files:
    file_path = os.path.join(folder_path, file.name)
    output_path = os.path.join('/Users/igorgerasimov/Python/Bitrix/test-chatGPT/downloadsProject', file.name)
    disk.download(file_path, output_path)

