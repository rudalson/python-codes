# python-codes

## bot

### crawling
```shell script
pip install requests BeautifulSoup4
```

#### python telegram bot 제작
```shell script
pip install python-telegram-bot --upgrade
```

### docker 실행
```shell script
$ docker build -t naver-weather-bot .
$ docker run --restart=on-failure:10 --name dust-weather --detach naver-weather-bot
```

```
docker run --restart=always --name rudalson-weather --detach rudalson-weather
```

## Reference
* [파이썬 레시피 - 웹 활용 입문편](https://wikidocs.net/book/2965)
