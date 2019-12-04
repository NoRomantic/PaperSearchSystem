import math


def count_jcr(paper_type, top, esi):
    """

    :param paper_type: string, JCR-1,2,3,4. CCF-A-B-C
    :param top: str, '是' or '否'
    :param esi: bool, is ESI high citation
    :return: float, JCR index
    """
    if paper_type == 'CCF-A':
        if esi == '是':
            return 16
        else:
            return 6
    elif paper_type == 'CCF-B':
        if esi == '是':
            return 11
        else:
            return 4
    elif paper_type == 'CCF-C':
        if esi == '是':
            return 3
        else:
            return 2
    elif paper_type == 1:  # JCR-1
        if top == '是':
            if esi == '是':
                return 17
            else:
                return 7
        else:
            if esi == '是':
                return 15
            else:
                return 5
    elif paper_type == 2:  # JCR-2
        if top == '是':
            if esi == '是':
                return 11
            else:
                return 4
        else:
            if esi == '是':
                return 10
            else:
                return 3
    elif paper_type == 3:  # JCR-3
        if esi == '是':
            return 3
        else:
            return 2
    elif paper_type == 4:  # JCR-4
        if esi == '是':
            return 2
        else:
            return 1
    else:  # If paper_type is not in CCF or JCR
        return 0


def assess_score(list_record, patents):
    jcr_score = 0
    total_if, total_cites = 0.0, 0
    for patent in patents:
        if patent == '国内':
            jcr_score += 1
        if patent == '国际':
            jcr_score += 5

    for record in list_record:
        jcr_score += count_jcr(record['fenqu'], record['top'], record['esi'])
        total_if += record['if_avg']
        total_cites += record['cites']

    total_score = jcr_score + math.log(total_if + 1) * math.log(total_cites + 1)

    return total_score, jcr_score, total_if, total_cites


def title_recommend(four_youth_title, sum_esi, project_funding, sum_jcr12,
                    comprehensive_indicator, sum_cites, nsfc_key, nsfc_face, nsfc_youth):

    if four_youth_title or sum_esi or project_funding >= 300:
        return '教授'

    flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 5:
        flag_jcr = 1
    if comprehensive_indicator >= 50:
        flag_score = 1
    if sum_cites >= 50:
        flag_if = 1
    if nsfc_key:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 4:
        flag_jcr = 1
    if comprehensive_indicator >= 40:
        flag_score = 1
    if sum_cites >= 40:
        flag_if = 1
    if nsfc_key:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '见习教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 3:
        flag_jcr = 1
    if comprehensive_indicator >= 30:
        flag_score = 1
    if sum_cites >= 30:
        flag_if = 1
    if nsfc_key or nsfc_face:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '副教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if, flag_nsfc = 0, 0, 0, 0

    if sum_jcr12 >= 2:
        flag_jcr = 1
    if comprehensive_indicator >= 20:
        flag_score = 1
    if sum_cites >= 20:
        flag_if = 1
    if nsfc_key or nsfc_face or nsfc_youth:
        flag_nsfc = 1
    if (flag_jcr + flag_score + flag_if + flag_nsfc) >= 2:
        return '见习副教授'
    else:  # Reset flags
        flag_jcr, flag_score, flag_if = 0, 0, 0

    if sum_jcr12 >= 1:
        flag_jcr = 1
    if comprehensive_indicator >= 5:
        flag_score = 1
    if sum_cites >= 7:
        flag_if = 1
    if (flag_jcr + flag_score + flag_if) >= 2:
        return '讲师'
    else:
        return '无'


def get_details(info):
    content = dict()
    content['professor'] = ''
    content['trainee_prof'] = ''
    content['asso_prof'] = ''
    content['trainee_asso_prof'] = ''
    content['lecturer'] = ''
    content['prof_jcr12'] = ''
    content['trainee_prof_jcr12'] = ''
    content['asso_prof_jcr12'] = ''
    content['trainee_asso_prof_jcr12'] = ''
    content['lecturer_jcr12'] = ''
    content['prof_four_youth'] = ''
    content['prof_esi_num'] = ''
    content['prof_total_funding'] = ''
    content['prof_com_indi'] = ''
    content['trainee_prof_com_indi'] = ''
    content['asso_prof_com_indi'] = ''
    content['trainee_asso_prof_com_indi'] = ''
    content['lecturer_com_indi'] = ''
    content['prof_total_cites'] = ''
    content['trainee_prof_total_cites'] = ''
    content['asso_prof_total_cites'] = ''
    content['trainee_asso_prof_total_cites'] = ''
    content['lecturer_total_cites'] = ''
    content['trainee_asso_prof_nsfc_key'] = ''
    content['asso_prof_nsfc_key'] = ''
    content['trainee_prof_nsfc_key'] = ''
    content['prof_nsfc_key'] = ''

    if info['recom_title'] == '教授':
        content['professor'] = '√'
        content['prof_four_youth'] = '√' if info['four_youth'] else ''
        content['prof_esi_num'] = '√' if info['esi_num'] >= 1 else ''
        content['prof_total_funding'] = '√' if info['total_funding'] >= 300 else ''
        if info['jcr12'] >= 5:
            content['prof_jcr12'] = '√'
        if info['com_indi'] >= 50:
            content['prof_com_indi'] = '√'
        if info['total_cites'] >= 50:
            content['prof_total_cites'] = '√'
    elif info['recom_title'] == '见习教授':
        content['trainee_prof'] = '√'
        if info['jcr12'] >= 4:
            content['trainee_prof_jcr12'] = '√'
        if info['com_indi'] >= 40:
            content['trainee_prof_com_indi'] = '√'
        if info['total_cites'] >= 40:
            content['trainee_prof_total_cites'] = '√'
    elif info['recom_title'] == '副教授':
        content['asso_prof'] = '√'
        if info['jcr12'] >= 3:
            content['asso_prof_jcr12'] = '√'
        if info['com_indi'] >= 30:
            content['asso_prof_com_indi'] = '√'
        if info['total_cites'] >= 30:
            content['asso_prof_total_cites'] = '√'
    elif info['recom_title'] == '见习副教授':
        content['trainee_asso_prof'] = '√'
        if info['jcr12'] >= 2:
            content['trainee_asso_prof_jcr12'] = '√'
        if info['com_indi'] >= 20:
            content['trainee_asso_prof_com_indi'] = '√'
        if info['total_cites'] >= 20:
            content['trainee_asso_prof_total_cites'] = '√'
    elif info['recom_title'] == '讲师':
        content['lecturer'] = '√'
        if info['jcr12'] >= 1:
            content['lecturer_jcr12'] = '√'
        if info['com_indi'] >= 5:
            content['lecturer_com_indi'] = '√'
        if info['total_cites'] >= 7:
            content['lecturer_total_cites'] = '√'

    if info['jcr12'] >= 5:
        content['prof_jcr12'] = '√'
    elif info['jcr12'] >= 4:
        content['trainee_prof_jcr12'] = '√'
    elif info['jcr12'] >= 3:
        content['asso_prof_jcr12'] = '√'
    elif info['jcr12'] >= 2:
        content['trainee_asso_prof_jcr12'] = '√'
    elif info['jcr12'] >= 1:
        content['lecturer_jcr12'] = '√'

    if info['com_indi'] >= 50:
        content['prof_com_indi'] = '√'
    elif info['com_indi'] >= 40:
        content['trainee_prof_com_indi'] = '√'
    elif info['com_indi'] >= 30:
        content['asso_prof_com_indi'] = '√'
    elif info['com_indi'] >= 20:
        content['trainee_asso_prof_com_indi'] = '√'
    elif info['com_indi'] >= 5:
        content['lecturer_com_indi'] = '√'

    if info['total_cites'] >= 50:
        content['prof_total_cites'] = '√'
    elif info['total_cites'] >= 40:
        content['trainee_prof_total_cites'] = '√'
    elif info['total_cites'] >= 30:
        content['asso_prof_total_cites'] = '√'
    elif info['total_cites'] >= 20:
        content['trainee_asso_prof_total_cites'] = '√'
    elif info['total_cites'] >= 7:
        content['lecturer_total_cites'] = '√'

    content['prof_nsfc_key'] = '√' if info['nsfc_key'] else ''  # True or 是
    if info['nsfc_key']:
        content['prof_nsfc_key'] = '√'
        content['trainee_prof_nsfc_key'] = '√'
    if info['nsfc_face']:
        content['asso_prof_nsfc_key'] = '√'
    if info['nsfc_youth']:
        content['trainee_asso_prof_nsfc_key'] = '√'

    return content
