import requests
from lxml import etree


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


def get_paper_info(paper_name):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh;q=0.8,zh-TW;q=0.7,zh-CN;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'UM_distinctid=16bdbd547349c-0f56d61f2860fa-e343166-13c680-16bdbd547359b7; NID=188=SCq9JGQVG3wiRlc_kKrORp09p8rIS9JycX2tHbyUvjSUXG6pU-wYKtr-BYiNoOXEKue1XHzMwniDXUEaoJ8B_kmtjc4gWoavKjufmCgl-vvWl_LFH9LzXQ1EtTN8DKPcP4JLmVqCD_Env4O_i6zyICbJ0QBBV0IbYNBdDC6Q2No; GSP=NW=1:LM=1564621868:S=dTZn-sXwLNdzuMde; security_session_verify=7a4e20eb5ed52d55422bf2bbdc285d0e; security_session_mid_verify=aedd772e2a81a8ae4929d42b75f48ab9; CNZZDATA1273252441=695695754-1564578705-https%253A%252F%252Fgfsoso.99lb.net%252F%7C1565914513',
        'Host': 'c.glgoo.top',
        'Referer': 'https://c.glgoo.top/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }

    parameters = {
        'hl': 'zh-CN',
        'as_sdt': '0,5',
        'q': paper_name,
        'btnG': '',
    }

    url = 'https://c.glgoo.top/scholar?'
    r1 = requests.get(url, headers=headers, params=parameters)
    html = etree.HTML(r1.text)
    # html_data2 = html.xpath('/html/head/title/text()')
    html_data = html.xpath('//*[@id="gs_res_ccl_mid"]/div/div[2]/div[3]/a[3]/text()')[0]
    if '被引用次数：' in html_data:
        return html_data.replace('被引用次数：', '')
    else:
        return 0
