import math


def count_jcr(paper_type, top, esi):
    """

    :param paper_type: string, JCR-1,2,3,4. CCF-A-B-C
    :param top: bool, is top
    :param esi: bool, is ESI high citation
    :return: float, JCR index
    """
    if top == '是':
        top = True
    else:
        top = False

    if esi == '是':
        esi = True
    else:
        esi = False

    if paper_type == 'CCF-A':
        if esi:
            return 16
        else:
            return 6
    elif paper_type == 'CCF-B':
        if esi:
            return 11
        else:
            return 4
    elif paper_type == 'CCF-C':
        if esi:
            return 3
        else:
            return 2
    elif paper_type == 'JCR-1':
        if top:
            if esi:
                return 17
            else:
                return 7
        else:
            if esi:
                return 15
            else:
                return 5
    elif paper_type == 'JCR-2':
        if top:
            if esi:
                return 11
            else:
                return 4
        else:
            if esi:
                return 10
            else:
                return 3
    elif paper_type == 'JCR-3':
        if esi:
            return 3
        else:
            return 2
    elif paper_type == 'JCR-4':
        if esi:
            return 2
        else:
            return 1
    else:  # If paper_type is not in CCF or JCR
        return 0


def assess_composite_score(jcr, list_if, list_citation):
    '''

    :param jcr: float, JCR score
    :param list_if: list of paper impact factors
    :param list_citation: list of citations
    :return: comprehensive assessment score
    '''
    sum_if = sum(list_if)
    sum_citation = sum(list_citation)
    return jcr + math.log(sum_if + 1) * math.log(sum_citation + 1)


def decide_level(four_youth_title, sum_esi, project_funding, sum_jcr12,
                 composite_score, sum_if, nsfc_key, nsfc_face, nsfc_youth):
    '''

    :param four_youth_title: bool, if one of four youth title
    :param sum_esi: int, total number of esi paper
    :param project_funding: float, total number of project funding
    :param sum_jcr12: int, total number of paper which is published on JCR1 or JCR2
    :param composite_score: float
    :param sum_if: int
    :param nsfc_key: bool, NSFC funding type, similarly hereinafter.
    :param nsfc_face: bool
    :param nsfc_youth: bool
    :return:
    '''
    if four_youth_title or sum_esi or project_funding >= 300:
        return '教授'

    flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 5:
        flag_jcr = 1
    if composite_score >= 50:
        flag_score = 1
    if sum_if >= 50:
        flag_if = 1
    if nsfc_key:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 4:
        flag_jcr = 1
    if composite_score >= 40:
        flag_score = 1
    if sum_if >= 40:
        flag_if = 1
    if nsfc_key:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '见习教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 3:
        flag_jcr = 1
    if composite_score >= 30:
        flag_score = 1
    if sum_if >= 30:
        flag_if = 1
    if nsfc_key or nsfc_face:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '副教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 2:
        flag_jcr = 1
    if composite_score >= 20:
        flag_score = 1
    if sum_if >= 20:
        flag_if = 1
    if nsfc_key or nsfc_face or nsfc_youth:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '见习副教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if = 0, 0, 0

    if sum_jcr12 >= 1:
        flag_jcr = 1
    if composite_score >= 5:
        flag_score = 1
    if sum_if >= 7:
        flag_if = 1
    if (flag_jcr + flag_score + flag_if) >= 2:
        return '讲师'
    else:
        return 'None'


def fun_sum_jcr12(list_type):
    jcr12 = 0
    for i in list_type:
        if i == 'JCR-1' or i == 'JCR-2':
            jcr12 += 1
    return jcr12


def fun_sum_esi(list_esi):
    sum_esi = 0
    for i in list_esi:
        if i == '是':
            sum_esi += 1
    return sum_esi


def is_four_youth(title_name):
    if title_name == '无' or title_name == '':
        return False


def nsfc_fund(nsfc_funding_name, judge_name=None):
    if judge_name in nsfc_funding_name:
        return True
    else:
        return False


def count_patent(patent_list):
    patent = 0
    for i in patent_list:
        if i == '国际':
            patent += 5
        elif i == '国内':
            patent += 1
    return patent
