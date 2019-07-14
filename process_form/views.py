from django.shortcuts import render
from django.conf import settings
import requests
import os
import xlrd


def home(request):
    return render(request, 'home.html')


def get_journal_info(journal_name):
    url1_head = 'https://webapi.fenqubiao.com/api/user/search?'
    url1_tail = '&user=BUCT_admin&password=1204705'
    year1 = '2017'  # Attention: the API only supports to year 2017.
    url1_keyword = journal_name.lstrip().replace('\n', '').replace('\r', '')
    url1_middle = '&year=' + year1 + '&keyword=' + url1_keyword
    url1 = url1_head + url1_middle + url1_tail
    r1 = requests.get(url1)
    dict1 = r1.json()

    if dict1:
        url2_head = 'https://webapi.fenqubiao.com/api/user/get?'
        url2_tail = '&user=BUCT_admin&password=1204705'
        year2 = str(dict1[0]['Year'])
        url2_keyword = dict1[0]['Title'].replace('&', 'and')
        url2_middle = '&year=' + year2 + '&keyword=' + url2_keyword
        url2 = url2_head + url2_middle + url2_tail
        r2 = requests.get(url2)
        dict2 = r2.json()
        return dict2
    else:
        raise Exception('查找结果为空')


def upload(request):
    if request.method == 'POST':
        excel_file = request.FILES.get('表格')
        excel_type = excel_file.name.split('.')[1]
        if excel_type in ['xlsx']:
            workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
            paper_sheet = workbook.sheet_by_name('论文')
            row_length = len(paper_sheet.col_values(1))
            all_papers = []
            # Append all paper infos
            for i in range(2, row_length):
                info = paper_sheet.row_values(i)[1: 8]
                all_papers.append(info)

            # Remove blank rows
            exist_papers = [x for x in all_papers if (x[0] != '' and x[1] != '')]
            exist_papers_infos = [x[0: 2] for x in exist_papers]
            # Get JCR,top,impact factor
            journal_names = [x[1].replace('&', 'and') for x in exist_papers_infos]
            dict_record = []
            for journal in journal_names:
                dict_record.append(get_journal_info(journal))

            # Get citation frequence. (ESI index is still not available, default value is '否')
            paper_names = [x[0] for x in exist_papers_infos]

        return render(request, 'search.html', {'state': dict_record})

