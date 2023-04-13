import os
import time

import pandas as pd
from datetime import datetime
from itertools import count

from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


# 모듈이 실행되고 있는 디렉토리 구하기
BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = '/home/webmaster/crawling-results/'


def crawling_nene():
    results = []

    # 마지막 페이지 확인을 위한 임시 변수
    check_page_string = ''

    # range를 지정하지 않고 count를 지정해서 첫 값만 지정해주기
    for page in range(1, 5):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page={0}'.format(page)

        html = crawler.crawling(url, encoding='utf-8')

        bs = BeautifulSoup(html, 'html.parser')

        # 데이터 변환
        tag_shop_tables = bs.findAll('table', attrs={'class': 'shopTable'})
        # print(tag_shop_tables)
        tag_shop_names = bs.findAll('div', attrs={'class': 'shopName'})
        # print(tag_table)
        tag_shop_addr = bs.findAll('div', attrs={'class': 'shopAdd'})
        shop_lists = zip(tag_shop_names, tag_shop_addr)
        shop_lists = (list(shop_lists))

        # # 마지막 페이지 번호 확인하기
        # if shop_lists[0] == check_page_string:
        #     break
        # else:
        #     check_page_string = shop_lists[0]

        for name, addr in shop_lists:
            # tag들 모두 제외시키고 스트링만 반환시키기, 그 후 리스트로 변경
            name = list(name.strings)[0]
            address = list(addr.strings)[0]
            # address에서 시, 도, 구 를 뽑아내서 변수로 저장 추후 사용될 수 있으므로 예시
            sidogu = address.split()[:2]
            results.append((name, address) + tuple(sidogu))

        # # 마지막 페이지 번호 확인하기(참조함)
        tag_pagination = bs.find('div', attrs={'class', 'pagination'})
        tags_ahref = tag_pagination.findAll('a')
        # 페이지 마지막에 도달한 경우 마지막 <a> 태그의 리스트에는 #으로 처리된 href 값이 들어온다.
        if tags_ahref[-1]['href'] == '#':
            print('break----')
            break

    # 파일로 저장하기
    # Data frame으로 만들어주기, columns = header
    df = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gu'])

    # 모듈이 실행되고 있는 절대 위치 구하기
    print(os.path.abspath(__file__))

    # # 모듈이 실행되고 있는 디렉토리 구하기
    BASE_DIR = (os.path.dirname(os.path.abspath(__file__)))

    # 저장위치를 현재 모듈이 실행되는 디렉토리에 만들기
    RESULT_DIR = os.path.join(BASE_DIR, '__results__')

    # 저장위치를 변경
    df.to_csv(f'{RESULT_DIR}/nene.csv', encoding='utf-8', mode='w', index=True)
    # # for t in results:
    #     print(t)


def store_naver_movie_rank(data):
    for index, div in enumerate(data):
        print(index + 1, div.a.text, sep=":")


def main():
    crawling_nene()

    
if __name__ == '__main__':
    main()