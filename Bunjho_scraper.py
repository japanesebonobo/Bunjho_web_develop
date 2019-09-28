import re
import time
from typing import Iterator
import requests
import pandas as pd
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def main():
    """
    クローラーのメイン処理
    """
    urls = scrape_search_page_url()
    #print(list(urls))

    batting_data = []
    batting_data = pd.DataFrame(batting_data)

    for url in list(urls):
        time.sleep(1)
        session = requests.Session()
        response = session.get(url)
        batting_data = batting_data.append(scrape_detail_page(response))
        batting_data = batting_data.reset_index(drop=True)
        print(batting_data)

    feature = ['選手名','年度','チーム','試合','打席','打数','得点','安打','二塁打','三塁打','本塁打','塁打','打点','盗塁','盗塁刺','犠打','犠飛','四球','死球','三振','併殺打','打率','長打率','出塁率']
    batting_data.columns = feature
    batting_data = batting_data.reset_index(drop=True)
    print(batting_data)
    batting_data.to_csv('/Users/yoshitomiyuuta/scraping/scraping_virtual/NPB_外国人野手通算成績.csv')

def scrape_search_page_url() -> Iterator[str]:
    """
    外国人野手選手名から選手検索結果ページのURLを抜き出し、詳細ページのURLを取得する関数。
    """

    csv_input = pd.read_csv(filepath_or_buffer="/Users/yoshitomiyuuta/scraping/scraping_virtual/外国人野手選手名.csv", encoding="utf-8", sep=",")
    print(csv_input.size)
    print(csv_input[["選手名"]])

    for row in csv_input['選手名']:
        url = 'http://npb.jp/bis/players/search/result?search_keyword=' + row + '&active_flg='
        print(url)
        time.sleep(1)
        session = requests.Session()
        response = session.get(url)
        soup = BeautifulSoup(response.text,'html.parser')

        for a in soup.select('#pl_result_list > div[class="three_column_player"] > a[class="player_unit_1"]'):
            url = urljoin(response.url,a.get('href'))
            print(url)
            yield url

        for a in soup.select('#pl_result_list > div[class="three_column_player"] > a[class="player_unit_1 old_player"]'):
            url = urljoin(response.url,a.get('href'))
            print(url)
            yield url

def scrape_detail_page(response:requests.Response):
    """
    詳細ページのResponseから打撃成績の情報をdictで取得する
    """
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text,'html.parser')

    score = []
    for td in soup.select('.registerStats > td'):
        score.append(td.text.strip())


    name = []
    for li in soup.select('li#pc_v_name'):
        name.append(li.text.strip())

    print(name)
    print(score)
    score2 = pd.DataFrame(score)
    name2 = pd.DataFrame(name)
    print(name2)
    #score2 = name2.join(score2)
    length = len(score2)//23

    final_score = []
    final_score = pd.DataFrame(final_score)

    for i in range(int(length)):
        a = int(0+23*i)
        b = int(23+23*i)
        score3 = score2[a:b].reset_index(drop=True)
        score4 = score3.T
        score4 = pd.DataFrame(score4)
        score5 = pd.concat([name2,score4],axis=1)
        final_score = final_score.append(score5)

    return final_score

if __name__=='__main__':
    main()
