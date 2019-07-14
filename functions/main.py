from .assess_score import *
from .read_excel import *


if __name__ == '__main__':
    file_path = 'D:\\学术水平查询系统\\06-27\\信息学院人才引进综合评价信息采集表.xlsx'
    personnel_info = read_excel(file_path)
    title_name = personnel_info[0]
    nsfc_funding_name = personnel_info[1]
    list_proj_fund = [x for x in personnel_info[2] if x != '']
    list_patent = [x for x in personnel_info[3] if x != '']
    list_paper_type = personnel_info[4]
    list_paper_top = [x for x in personnel_info[5] if x != '']
    list_paper_if = [x for x in personnel_info[6] if x != '']
    list_paper_cite = personnel_info[7]
    list_paper_esi = [x for x in personnel_info[8] if x != '']

    for i in range(len(list_paper_type)):
        if list_paper_type[i] == '':
            list_paper_cite[i] = 0

    list_paper_type = [x for x in list_paper_type if x != '']
    list_paper_cite = [x for x in list_paper_cite if x != '']
    sum_cite = sum(list_paper_cite)

    jcr_list = [count_jcr(list_paper_type[i], list_paper_top[i], list_paper_esi[i])
                for i in range(len(list_paper_type))]
    patent = count_patent(list_patent)
    jcr = sum(jcr_list) + patent
    composite_score = assess_composite_score(jcr, list_paper_if, list_paper_cite)

    title_name = is_four_youth(title_name)
    sum_esi = fun_sum_esi(list_paper_esi)
    project_funding = sum(list_proj_fund)
    sum_jcr12 = fun_sum_jcr12(list_paper_type)
    sum_if = sum(list_paper_if)
    nsfc_key = nsfc_fund(nsfc_funding_name, judge_name='NSFC重点基金')
    nsfc_face = nsfc_fund(nsfc_funding_name, judge_name='NSFC面上基金')
    nsfc_youth = nsfc_fund(nsfc_funding_name, judge_name='NSFC青年基金')

    personnel_level = decide_level(title_name, sum_esi, project_funding, sum_jcr12,
                                   composite_score, sum_if, nsfc_key, nsfc_face, nsfc_youth)
    print("\nJCR：%s\nIF: %s\n他引之和: %s\nJCR1+2: %s\n项目总金额（万元）: %s\n综合分数: %s\n\n定岗推荐: %s"
          % (jcr, sum_if, sum_cite, sum_jcr12, project_funding, composite_score, personnel_level))


