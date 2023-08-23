# Используем базовый образ Ubuntu 20.04
FROM python:3.10


ENV TZ=Europe/Moscow
RUN apt-get update && apt-get install -y nano vim redis-server

# Устанавливаем пакеты системы 
# RUN apt-get update && apt-get install -y \
#     python3.10 \
#     python3-pip \
#     && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы helper.py, chat.py, workFlask.py и workBinance.py в директорию /app контейнера
COPY chat.py helper.py index.py workBitrix.py workGDrive.py workGS.py workRedis.py workTelegram.py yandexDiskWork.py workYDB.py createKeyboard.py run.sh /app/

# Копируем файл requirements.txt в директорию /app контейнера
COPY requirements.txt /app/

# Устанавливаем зависимости из requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Открываем порт 5000 (или любой другой необходимый порт)
EXPOSE 5002

# Копируем файл .env внутрь контейнера
COPY .env txt.json GDtxt.json kgtaprojects-8706cc47a185.json /app/
RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]
#CMD ["python", "workFlask.py"]
