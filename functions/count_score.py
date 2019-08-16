import math


def count_jcr(paper_type, top, esi):
    """

    :param paper_type: string, JCR-1,2,3,4. CCF-A-B-C
    :param top: bool, is top
    :param esi: bool, is ESI high citation
    :return: float, JCR index
    """
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
    elif paper_type == 1:  # JCR-1
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
    elif paper_type == 2:  # JCR-2
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
    elif paper_type == 3:  # JCR-3
        if esi:
            return 3
        else:
            return 2
    elif paper_type == 4:  # JCR-4
        if esi:
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

    return float('%.2f' % total_score)


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
