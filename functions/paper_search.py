import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def get_journal_info(journal_name):
    url1 = 'https://webapi.fenqubiao.com/api/user/search?'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    parameters1 = {
        'year': '2017',
        'keyword': journal_name,
        'user': 'BUCT_admin',
        'password': '1204705'
    }
    response1 = requests.get(url1, headers=headers, params=parameters1)
    if len(response1.json()) > 0:
        true_name = response1.json()[0]['Title']
    else:
        # Push this paper into a list(where papers can't be searched)
        return None

    url2 = 'https://webapi.fenqubiao.com/api/user/get?'
    parameters2 = {
        'year': '2017',
        'keyword': true_name,
        'user': 'BUCT_admin',
        'password': '1204705'
    }
    response2 = requests.get(url2, headers=headers, params=parameters2)
    dict_info = response2.json()

    return dict_info


def get_paper_info(paper_name, my_cookies):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'c.glgoo.top',
        'Referer': 'https://c.glgoo.top/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }

    parameters = {
        'hl': 'zh - CN',
        'q': paper_name,
        'as_sdt': '0, 5',
    }

    url = 'https://c.glgoo.top/scholar?'
    response = requests.get(url, headers=headers, params=parameters, cookies=my_cookies)
    html = etree.HTML(response.text)
    html_data = html.xpath('//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]/text()')
    if len(html_data) != 0:
        if len(html_data) == 1:
            if '被引用次数：' in html_data[0]:
                return html_data[0].replace('被引用次数：', '')
            else:
                return 0
        else:
            return -1  # A sign for paper unsearched
    else:
        return 0


def get_cookies():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://c.glgoo.top/scholar?')
    time.sleep(0.1)
    # browser.implicitly_wait(5)

    cookies = browser.get_cookies()
    browser.quit()

    my_cookies = dict()
    for cookie in cookies:
        my_cookies[cookie['name']] = cookie['value']

    # print(my_cookies)

    return my_cookies
