FROM python:3

WORKDIR /app
ADD    ./requirements.txt   /app/
RUN    pip install -r requirements.txt

ADD    ./bot       /app/bot/
ADD    bot/conf      /app/conf/

CMD ["python", "bot/naver-weather-bot.py"]