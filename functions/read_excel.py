import xlrd


def read_excel(file_path):
    # Read sheets of excel
    workbook = xlrd.open_workbook(file_path)
    basic_info = workbook.sheet_by_name('基本信息')
    projects = workbook.sheet_by_name('项目')
    patents = workbook.sheet_by_name('专利')
    papers = workbook.sheet_by_name('论文')

    # Read necessary data
    title_name = basic_info.cell_value(2, 2)
    nsfc_funding_name = basic_info.cell_value(3, 2)
    list_proj_fund = projects.col_values(2)[2:50]
    list_patent = patents.col_values(2)[2:50]
    list_paper_type = papers.col_values(3)[2:50]
    list_paper_top = papers.col_values(4)[2:50]
    list_paper_if = papers.col_values(5)[2:50]
    list_paper_cite = papers.col_values(6)[2:50]
    list_paper_esi = papers.col_values(7)[2:50]

    return title_name, nsfc_funding_name, list_proj_fund, list_patent, list_paper_type, \
           list_paper_top, list_paper_if, list_paper_cite, list_paper_esi


if __name__ == '__main__':
    file_path = 'D:\\学术水平查询系统\\案例-信息学院人才引进综合评价信息采集表.xlsx'
    tmp = read_excel(file_path)
    # print('finished')

