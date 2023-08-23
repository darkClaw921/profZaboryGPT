#!/bin/bash

# Запускаем Redis-сервер
redis-server /etc/redis/redis.conf &

# Запускаем файл workTelegram.py
python /app/workTelegram.py