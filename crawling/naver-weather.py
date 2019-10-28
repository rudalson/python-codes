import os

from bs4 import BeautifulSoup as bs
from pprint import pprint
import requests


def get_naver_weather():
    html = requests.get('https://search.naver.com/search.naver?query=날씨')
    # pprint(html.text)

    soup = bs(html.text, 'html.parser')

    # data1 = soup.find('div', {'class': 'detail_box'})
    # pprint(data1)

    # data2 = data1.findAll('dd')
    # pprint(data2)

    # fine_dust = data2[0].find('span', {'class': 'num'}).text
    # print(fine_dust)
    #
    # ultra_fine_dust = data2[1].find('span', {'class': 'num'}).text
    # print(ultra_fine_dust)

    dust_data = soup.find('div', {'class': 'detail_box'}).findAll('dd')

    fine_dust = dust_data[0].find('span', {'class': 'num'}).text
    ultra_fine_dust = dust_data[1].find('span', {'class': 'num'}).text

    location_data = soup.find('div', {'class': 'select_box'}).find('em').text

    reply_text = f'{location_data} - 미세먼지:{fine_dust}, 초미세먼지:{ultra_fine_dust}'
    print(reply_text)


def get_naver_dust(location=""):
    html = requests.get(f'https://search.naver.com/search.naver?query={location} 미세먼지')

    soup = bs(html.text, 'html.parser')

    content_box = soup.findAll('div', {'class': 'content_box'})

    dust = content_box[1].find('div', {'class': 'state_info'}).find("em", {'class': 'main_figure'}).text

    ultra_dust = content_box[1].find('div', {'class': 'all_state'}).find('span', {'class': 'state'}).text

    update_time = content_box[1].find('div', {'class': 'guide_bx'}).find('span', {'class': 'update'}).find('em').text

    reply_text = f'{dust}, {ultra_dust}(미세, 초미세) - {update_time}'
    print(reply_text)


def main():
    # get_naver_dust(location="천호동")
    get_naver_weather()


if __name__ == '__main__':
    main()
