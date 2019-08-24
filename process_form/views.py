import xlrd
from django.shortcuts import render, redirect
from functions.count_score import *
from functions.paper_search import *


list_searched = list()
list_unsearched = list()
dict_basicinfo = dict()
my_cookies = dict()


def home(request):
    return render(request, 'process_form/home.html')


def about(request):
    return render(request, 'process_form/about.html')


def search(request):
    global list_searched, list_unsearched, dict_basicinfo, my_cookies
    if request.method == 'POST':
        if request.FILES.get('表格') is None:
            return render(request, 'process_form/nofile.html')
            # return redirect('processform:nofile_html')
        else:
            excel_file = request.FILES.get('表格')
            excel_type = excel_file.name.split('.')[1]
            if excel_type in ['xlsx']:
                workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
                # Read excel
                basic_info = workbook.sheet_by_name('基本信息')
                title_name = basic_info.cell_value(2, 2)
                nsfc_funding_name = basic_info.cell_value(3, 2)
                patent_sheet = workbook.sheet_by_name('专利')
                patents = patent_sheet.col_values(2)[2:]
                project_sheet = workbook.sheet_by_name('项目')
                projects_fund = project_sheet.col_values(2)[2:]

                dict_basicinfo['title'] = title_name
                dict_basicinfo['nsfc'] = nsfc_funding_name
                dict_basicinfo['patents'] = patents
                dict_basicinfo['funding'] = projects_fund

                ''' Paper Search '''
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

                list_searched = list()
                list_unsearched = list()  # To contain papers that have not been searched
                my_cookies = get_cookies()

                for info in exist_papers_infos:
                    dict_record = dict()
                    pa_name = info[0].rstrip('\r\n')
                    jn_name = info[1].replace('&', 'and')

                    pa_info = get_paper_info(pa_name, my_cookies)
                    jn_info = get_journal_info(jn_name)
                    if jn_info is None:  # If journal is not researched
                        list_unsearched.append({'paper_name': pa_name, 'journal_name': jn_name})
                    else:
                        dict_record['paper_name'] = pa_name
                        dict_record['journal_name'] = jn_name
                        dict_record['fenqu'] = jn_info['ZKY'][0]['Section']
                        dict_record['top'] = jn_info['ZKY'][0]['Top']
                        dict_record['if_avg'] = jn_info['Indicator']['IFavg']
                        dict_record['cites'] = int(pa_info)
                        dict_record['esi'] = False  # Default false
                        list_searched.append(dict_record)
                ''' Paper Search Finished '''

                content = {'searched': list_searched, 'unsearched': list_unsearched}
                return render(request, 'process_form/paperinfo.html', content)

            else:
                return render(request, 'process_form/filefail.html')


def result(request):
    global dict_basicinfo
    print(dict_basicinfo)
    patents = dict_basicinfo['patents']
    nsfc_funding_name = dict_basicinfo['nsfc']
    title_name = dict_basicinfo['title']
    projects_fund = dict_basicinfo['funding']

    com_ind = assess_score(list_searched, patents)
    sum_esi, sum_jcr12, sum_cites = 0, 0, 0
    for record in list_searched:
        if record['esi']:
            sum_esi += 1
        if record['fenqu'] <= 2:
            sum_jcr12 += 1
        sum_cites += record['cites']
    nsfc_funding_name = nsfc_funding_name.split('/')
    nsfc_key, nsfc_face, nsfc_youth = False, False, False
    for nsfc in nsfc_funding_name:
        if nsfc == 'NSFC青年基金':
            nsfc_youth = True
        if nsfc == 'NSFC面上基金':
            nsfc_face = True
        if nsfc == 'NSFC重点基金':
            nsfc_key = True
    title_name = title_name.split('/')
    four_youth_title = False
    for title in title_name:
        if title in ['院士', '千人', '杰青', '优青']:
            four_youth_title = True
    projects_fund = sum([str(x) for x in projects_fund if x != ''])

    recommonded_title = title_recommend(four_youth_title, sum_esi, projects_fund, sum_jcr12,
                                        com_ind, sum_cites, nsfc_key, nsfc_face, nsfc_youth)
    content = {
        'recommonded_title': recommonded_title,
        'com_indi': com_ind,
        'jcr12': sum_jcr12,
        'total_cites': sum_cites,
        'nsfc_key': nsfc_key,
        'nsfc_face': nsfc_face,
        'nsfc_youth': nsfc_youth,
        'four_youth': four_youth_title,
        'esi_num': sum_esi,
        'total_funding': projects_fund,
    }

    return render(request, 'process_form/result.html', content)


def edit(request, forloop_counter):
    global list_searched
    if request.method == 'GET':
        content = {'searched': list_searched[int(forloop_counter) - 1]}

        return render(request, 'process_form/edit.html', content)

    elif request.method == 'POST':
        list_searched[int(forloop_counter) - 1]['paper_name'] = request.POST.get('paper_name')
        list_searched[int(forloop_counter) - 1]['journal_name'] = request.POST.get('journal_name')
        list_searched[int(forloop_counter) - 1]['fenqu'] = int(request.POST.get('fenqu'))
        list_searched[int(forloop_counter) - 1]['top'] = bool(request.POST.get('top'))
        list_searched[int(forloop_counter) - 1]['if_avg'] = float(request.POST.get('if_avg'))
        list_searched[int(forloop_counter) - 1]['cites'] = int(request.POST.get('cites'))
        list_searched[int(forloop_counter) - 1]['esi'] = bool(request.POST.get('esi'))

        return redirect("processform:paperinfo_html")


def edit_unsearched(request, forloop_counter):
    global list_unsearched
    if request.method == 'GET':
        content = {'searched': list_unsearched[int(forloop_counter) - 1]}

        return render(request, 'process_form/edit_unsearched.html', content)

    elif request.method == 'POST':
        list_unsearched[int(forloop_counter) - 1]['paper_name'] = request.POST.get('paper_name')
        list_unsearched[int(forloop_counter) - 1]['journal_name'] = request.POST.get('journal_name')
        # list_unsearched[int(forloop_counter) - 1]['fenqu'] = request.POST.get('fenqu')
        # list_unsearched[int(forloop_counter) - 1]['top'] = request.POST.get('top')
        # list_unsearched[int(forloop_counter) - 1]['if_avg'] = request.POST.get('if_avg')
        # list_unsearched[int(forloop_counter) - 1]['cites'] = request.POST.get('cites')
        # list_unsearched[int(forloop_counter) - 1]['esi'] = request.POST.get('esi')

        return redirect("processform:paperinfo_html")


def delete(request, forloop_counter):
    global list_searched
    list_searched.pop(int(forloop_counter) - 1)
    return redirect("processform:paperinfo_html")


def delete_unsearched(request, forloop_counter):
    global list_unsearched
    list_unsearched.pop(int(forloop_counter) - 1)
    return redirect("processform:paperinfo_html")


def paperinfo(request):
    content = {'searched': list_searched, 'unsearched': list_unsearched}
    return render(request, 'process_form/paperinfo.html', content)


def add(request):
    global list_searched
    if request.method == 'GET':

        return render(request, 'process_form/add.html')

    elif request.method == 'POST':
        dict_tmp = dict()
        dict_tmp['paper_name'] = request.POST.get('paper_name')
        dict_tmp['journal_name'] = request.POST.get('journal_name')
        dict_tmp['fenqu'] = request.POST.get('fenqu')
        dict_tmp['top'] = request.POST.get('top')
        dict_tmp['if_avg'] = request.POST.get('if_avg')
        dict_tmp['cites'] = request.POST.get('cites')
        dict_tmp['esi'] = request.POST.get('esi')
        list_searched.append(dict_tmp)

        return redirect("processform:paperinfo_html")


def research(request, forloop_counter):
    global my_cookies
    pa_name = list_unsearched[int(forloop_counter) - 1]['paper_name']
    jn_name = list_unsearched[int(forloop_counter) - 1]['journal_name']

    pa_info = get_paper_info(pa_name, my_cookies)
    jn_info = get_journal_info(jn_name)
    if jn_info is not None:
        list_unsearched.pop(int(forloop_counter) - 1)
        dict_record = dict()
        dict_record['paper_name'] = pa_name
        dict_record['journal_name'] = jn_name
        dict_record['fenqu'] = jn_info['ZKY'][0]['Section']
        dict_record['top'] = jn_info['ZKY'][0]['Top']
        dict_record['if_avg'] = jn_info['Indicator']['IFavg']
        dict_record['cites'] = int(pa_info)
        dict_record['esi'] = False  # Default false
        list_searched.append(dict_record)

    content = {'searched': list_searched, 'unsearched': list_unsearched}

    return render(request, 'process_form/paperinfo.html', content)


def nofile(request):
    if request.method == 'POST':
        return redirect('processform:home_html')
