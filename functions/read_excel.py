import os, shutil
import openpyxl as xl
from copy import copy


# def read_excel(file_path):
#     # Read sheets of excel
#     workbook = xlrd.open_workbook(file_path)
#     basic_info = workbook.sheet_by_name('基本信息')
#     projects = workbook.sheet_by_name('项目')
#     patents = workbook.sheet_by_name('专利')
#     papers = workbook.sheet_by_name('论文')
#
#     # Read necessary data
#     title_name = basic_info.cell_value(2, 2)
#     nsfc_funding_name = basic_info.cell_value(3, 2)
#     list_proj_fund = projects.col_values(2)[2:50]
#     list_patent = patents.col_values(2)[2:50]
#     list_paper_type = papers.col_values(3)[2:50]
#     list_paper_top = papers.col_values(4)[2:50]
#     list_paper_if = papers.col_values(5)[2:50]
#     list_paper_cite = papers.col_values(6)[2:50]
#     list_paper_esi = papers.col_values(7)[2:50]
#
#     return title_name, nsfc_funding_name, list_proj_fund, list_patent, list_paper_type, \
#            list_paper_top, list_paper_if, list_paper_cite, list_paper_esi


def write_excel(path, tg_dir, info, content):
    if os.path.exists(tg_dir):
        shutil.rmtree(tg_dir)
    os.makedirs(tg_dir)

    org_wb = xl.load_workbook(filename=path)
    cp_wb = copy(org_wb)
    cp_ws = cp_wb['综合评价']

    # Basic font style
    font = xl.styles.Font(
        name='等线',
        bold=False,
    )
    alignment = xl.styles.Alignment(
        horizontal='general',
        vertical='bottom',
    )

    b_col = cp_ws.column_dimensions['B']
    b_col.font = font
    b_col.alignment = alignment

    # 综合指标各项
    cp_ws['B2'] = info['com_indi']
    cp_ws['B3'] = info['jcr12']
    cp_ws['B4'] = info['total_cites']
    cp_ws['B5'] = 1 if info['nsfc_key'] else 0
    cp_ws['B6'] = 1 if info['nsfc_face'] else 0
    cp_ws['B7'] = 1 if info['nsfc_youth'] else 0
    cp_ws['B8'] = 1 if info['four_youth'] else 0
    cp_ws['B9'] = info['esi_num']
    cp_ws['B10'] = info['total_funding']
    cp_ws['B11'] = info['recom_title']
    cp_ws['E10'] = info['jcr_score']
    cp_ws['E11'] = info['if']
    cp_ws['E12'] = info['ci']

    # 达标状态
    cp_ws['D7'] = content['professor']
    cp_ws['D6'] = content['trainee_prof']
    cp_ws['D5'] = content['asso_prof']
    cp_ws['D4'] = content['trainee_asso_prof']
    cp_ws['D3'] = content['lecturer']

    # jcr12
    cp_ws['F7'] = content['prof_jcr12']
    cp_ws['F6'] = content['trainee_prof_jcr12']
    cp_ws['F5'] = content['asso_prof_jcr12']
    cp_ws['F4'] = content['trainee_asso_prof_jcr12']
    cp_ws['F3'] = content['lecturer_jcr12']

    # 四青
    cp_ws['F8'] = content['prof_four_youth']
    # esi
    cp_ws['H8'] = content['prof_esi_num']
    # 项目经费
    cp_ws['K8'] = content['prof_total_funding']

    # 综合指标
    cp_ws['K7'] = content['prof_com_indi']
    cp_ws['K6'] = content['trainee_prof_com_indi']
    cp_ws['K5'] = content['asso_prof_com_indi']
    cp_ws['K4'] = content['trainee_asso_prof_com_indi']
    cp_ws['K3'] = content['lecturer_com_indi']

    # cite
    cp_ws['N7'] = content['prof_total_cites']
    cp_ws['N6'] = content['trainee_prof_total_cites']
    cp_ws['N5'] = content['asso_prof_total_cites']
    cp_ws['N4'] = content['trainee_asso_prof_total_cites']
    cp_ws['N3'] = content['lecturer_total_cites']

    # nsfc
    cp_ws['Q4'] = content['trainee_asso_prof_nsfc_key']
    cp_ws['Q5'] = content['asso_prof_nsfc_key']
    cp_ws['Q6'] = content['trainee_prof_nsfc_key']
    cp_ws['Q7'] = content['prof_nsfc_key']

    cp_path = os.path.join(tg_dir, 'result.xlsx')
    cp_wb.save(cp_path)


def export_excel():
    pass


if __name__ == '__main__':
    file_path = 'D:\\学术水平查询系统\\案例-信息学院人才引进综合评价信息采集表.xlsx'
    write_excel(file_path)
    # print('finished')

