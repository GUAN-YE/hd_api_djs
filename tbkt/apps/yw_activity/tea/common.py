# coding:utf-8
import time
from libs.utils import db
from com import com_user
from apps.active.common import update_score


def article_details(ch_Code,state,ch_Name):
    """
    :param ch_Code: 文章code
    :param state: 状态
    :return:
    """
    sql="select ti_Contents from yw_textinfo where ch_Code=%s" % ch_Code
    data = db.tbkt_yw_slave.fetchone_dict(sql)
    if data:
        data['ch_Name'] = ch_Name
        data['state'] = state
        return data



def article_list(user_id,p):
    """
    老师端推荐学生列表
    :param request:
    :param user_id: 用户id
    :param p: 页数
    :return:
    """
    page_begin=(p-1)*10



    sql_count="select count(*) from yw_chapter where ct_ID=35 and ch_IsContent=1 and enable_flag=0"
    sql="select ch_Name,ch_Code from yw_chapter where ct_ID=35 and ch_IsContent=1 and enable_flag=0 limit  %s,10" % page_begin
    data = db.tbkt_yw_slave.fetchall_dict(sql)
    data_count = db.tbkt_yw_slave.fetchone(sql_count)
    user_sql="select ch_Code from yw_article_recommend_hd where user_id=%s" % user_id
    user_data = db.tbkt_active_slave.fetchall_dict(user_sql)
    ch_codes = [i.ch_Code for i in user_data]
    for chapter_data in data:
        if int(chapter_data['ch_Code']) in ch_codes:
            chapter_data['state']=1
        else:
            chapter_data['state'] = 0
    page_count = divmod(data_count[0], 10)
    page_count = page_count[0] if page_count[1] == 0 else page_count[0] + 1
    return {"data":data, "page_count":page_count}



def recommend_article(user_id,ch_Code,city):
    """
    老师推荐文章入库
    :param request:
    :param user_id: 用户id
    :param ch_ID: 章节id
    :return:
    """
    add_time=time.time()

    detail = db.tbkt_active_slave.yw_article_recommend_hd.get(user_id=user_id,ch_Code=ch_Code)
    if not detail:
        article_recommend=db.tbkt_active.yw_article_recommend_hd.create(user_id=user_id,
                                                      ch_Code=ch_Code,
                                                    add_time=add_time
                                                   )
        if city != 411200:
            update_score(user_id, 5, 'recomt', user_id, 0, 0, 0)
        #调用加积分接口
        return article_recommend
    return 0

def teacher_ranking(p):
    """
    教师端，老师排名
    :param p: 页数
    :return:
    """

    p_begin = (p - 1) * 10
    sql_count = "select count(*) from active_score_user where active_id= 5"
    # "SELECT a.user_id,a.score FROM active_score_user as a join active_score_user as b on a.id = b.id WHERE a.active_id= 5 ORDER BY a.score desc LIMIT %s,10" % p_begin
    sql = "SELECT a.user_id,a.score FROM active_score_user as a join active_score_user as b on a.id = b.id WHERE a.active_id= 5 ORDER BY a.score desc LIMIT %s,10" % p_begin
    active = db.tbkt_active_slave.fetchall_dict(sql)
    if active:
        active_count = db.tbkt_active_slave.fetchone(sql_count)
        user_ids = [data.user_id for data in active]
        if user_ids:
            school_dict = com_user.users_info(user_ids)
            for is_data in active:
                is_data['school_dict'] = school_dict.get(is_data.user_id, "")
            page_count = divmod(active_count[0], 10)
            page_count = page_count[0] if page_count[1] == 0 else page_count[0] + 1
            return {'active': active, 'page_count': page_count}

