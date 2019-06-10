from django.shortcuts import render
# from io import StringIO
import requests


def home(request):
    # url1 = 'https://webapi.fenqubiao.com/api/user/search?' \
    #       'year=2015&keyword=IEEE&user=BUCT_admin&password=1204705'
    # r1 = requests.get(url1)
    # dict1 = r1.json()
    #
    # url2 = 'https://webapi.fenqubiao.com/api/user/get?' \
    #        '&year=2015' \
    #        '&keyword=IEEE%20Transactions%20on%20Intelligent' \
    #        '&user=BUCT_admin&password=1204705'
    # r2 = requests.get(url2)
    # dict2 = r2.json()
    return render(request, 'home.html')


def search(request):
    user_text = request.GET['text']
    url1_head = 'https://webapi.fenqubiao.com/api/user/search?'
    url1_tail = '&user=BUCT_admin&password=1204705'
    year1 = user_text[:4]
    url1_keyword = user_text.replace(year1, '').lstrip().replace('\n', '')\
        .replace('\r', '')
    url1_middle = '&year=' + year1 + '&keyword=' + url1_keyword
    url1 = url1_head + url1_middle + url1_tail
    r1 = requests.get(url1)
    dict1 = r1.json()

    if len(dict1) != 0:
        url2_head = 'https://webapi.fenqubiao.com/api/user/get?'
        url2_tail = '&user=BUCT_admin&password=1204705'
        year2 = str(dict1[0]['Year'])
        url2_keyword = dict1[0]['Title']
        url2_middle = '&year=' + year2 + '&keyword=' + url2_keyword
        url2 = url2_head + url2_middle + url2_tail
        r2 = requests.get(url2)
        dict2 = r2.json()
    else:
        raise Exception('查找结果为空')

    # sio = StringIO(url2)
    # sio.seek(0, 2)
    # user_text = user_text.replace(' ', '%')
    # sio.write(user_text)
    # sio.writelines(url2_last)
    # sio.seek(0)
    # url = sio.read()

    return render(request, 'search.html', {"dict2": dict2})

