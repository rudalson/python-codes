FROM python:3

WORKDIR /app
ADD    ./requirements.txt   /app/
RUN    pip install -r requirements.txt

ADD    ./bot       /app/bot/
ADD    ./conf      /app/conf/

CMD ["python", "bot/naver-weather-bot.py"]