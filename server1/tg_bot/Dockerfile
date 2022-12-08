FROM python:3.8.16-slim

RUN python3 -m pip install -U --no-cache-dir pip && \
    python3 -m pip install --no-cache-dir pillow pyTelegramBotAPI numpy kafka-python

WORKDIR /app
ENV PYTHONPATH=/app:$PYTHONPATH
COPY tg_bot/ /app

ENTRYPOINT python3 bot_polling.py
