import xlrd
import time
from django.shortcuts import render
from functions.count_score import *
from functions.paper_search import *


def home(request):
    return render(request, 'home.html')


def upload(request):
    if request.method == 'POST':
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

            list_record = list()
            unsearched_list = list()  # To contain papers that have not been searched
            for info in exist_papers_infos:
                dict_record = dict()
                pa_name = info[0].rstrip('\r\n')
                jn_name = info[1].replace('&', 'and')

                pa_info = get_paper_info(pa_name)
                jn_info = get_journal_info(jn_name)
                if jn_info is None:
                    unsearched_list.append({'paper_name': pa_name, 'journal_name': jn_name})
                # time.sleep(3)
                else:
                    dict_record['paper_name'] = pa_name
                    dict_record['journal_name'] = jn_name
                    dict_record['fenqu'] = jn_info['ZKY'][0]['Section']
                    dict_record['top'] = jn_info['ZKY'][0]['Top']
                    dict_record['if_avg'] = jn_info['Indicator']['IFavg']
                    dict_record['cites'] = int(pa_info)
                    dict_record['esi'] = False  # Default false
                    list_record.append(dict_record)
            ''' Paper Search Finished '''

            # Count comprehensive indicators(suppose all paper infos have been filled)
            com_ind = assess_score(list_record, patents)
            sum_esi, sum_jcr12, sum_cites = 0, 0, 0
            for record in list_record:
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

            return render(request, 'search.html', {'state': recommonded_title})

            # Create a form to show all the infos which have already been searched, also the papers not searched.
        else:
            # raise Exception('导入文件不是xlsx文件，请重新导入正确文件！')
            return render(request, 'filefail.html')
