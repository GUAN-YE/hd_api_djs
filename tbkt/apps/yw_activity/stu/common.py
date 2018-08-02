# coding:utf-8
import time
from libs.utils import db
from com import com_user
from apps.active.common import update_score
import requests
from bs4 import BeautifulSoup

def index(request,user_id,is_open,t_id,class_id,city):
    """
    获取首页的排名和积分
    :param request:
    :param user_id:  用户id
    :return:
    """

    add_time=time.time()
    t = time.localtime(add_time)
    zero_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
    activity_record = db.tbkt_active_slave.yw_activity_record_hd.get(user_id=user_id,add_time__gte=zero_time)
    if not activity_record:
        #首次进入老师加积分，调用增加积分的接口
        db.tbkt_active.yw_activity_record_hd.create(user_id=user_id,
                                                    add_time=add_time
                                                   )
        if t_id and city !=411200:
            update_score(t_id,5,'attend', user_id, 0, 0, is_open)
    if is_open==1:
        is_open_db = db.tbkt_active_slave.yw_activity_record_hd.get(user_id=user_id, is_open=1)
        if not is_open_db:
            db.tbkt_active.yw_activity_record_hd.create(user_id=user_id,
                                                        is_open=1
                                                       )
            if city !=411200:
                update_score(user_id, 4, 'isfrist', user_id, 0, class_id, is_open)
                return "开通成功！获得 1000积分"




def article_details(article_name,ch_Code,state):
    """

    :param article_name:  文章名称
    :param ch_Code: 文章code
    :param state: 状态
    :return:
    """
    sql="select ti_Contents from yw_textinfo where ch_Code=%s" % ch_Code
    data = db.tbkt_yw_slave.fetchone_dict(sql)
    if data:
        data['article_name']=article_name
        data['state'] = state
        return data



def article_recom(recom_p,user_id,t_id):
    """
    学生端文章列表
    :param request:
    :param user_id: 用户id
    :param p: 范文朗读的页数
    :param recom_p: 老师推荐的文章页数
    :param t_id: 老师id
    :return:
    """
    # p_begin=(p-1)*5
    # p_end = p * 5

    recom_p_begin = (recom_p - 1) * 5

    sql_recording_hd="select * from yw_recording_hd where user_id=%s" % user_id
    recording_hd = db.tbkt_active_slave.fetchall_dict(sql_recording_hd)
    recording_dict={recording.ch_Code: recording for recording in recording_hd}

    #范文朗读 文章列表
    sql="select ch_Name,ch_Code from yw_chapter where ct_ID=35 and ch_IsContent=1 and enable_flag=0"
    chapter_data = db.tbkt_yw_slave.fetchall_dict(sql)
    chapter_dict={}
    for chapter in chapter_data:
        chapter_dict[int(chapter.ch_Code)]=chapter.ch_Name


    user_sql="select ch_Code,add_time from yw_article_recommend_hd where user_id=%s limit %s,5" % (t_id,recom_p_begin)
    user_data = db.tbkt_active_slave.fetchall_dict(user_sql)
    for user in user_data:
        ch_Name = chapter_dict.get(user.ch_Code, '')
        user.ch_Name=ch_Name
        recording = recording_dict.get(user.ch_Code,0)
        user.recording = recording
        user.add_time=date_format(user.add_time)

    return user_data


def article_all(p,user_id):
    """
    学生端文章列表
    :param request:
    :param user_id: 用户id
    :param p: 范文朗读的页数
    :param t_id: 老师id
    :return:
    """
    p_begin=(p-1)*5
    p_end = p * 5

    # recom_p_begin = (recom_p - 1) * 5
    # recom_p_end = recom_p * 5

    sql_recording_hd="select * from yw_recording_hd where user_id=%s" % user_id
    recording_hd = db.tbkt_active_slave.fetchall_dict(sql_recording_hd)
    recording_dict={recording.ch_Code: recording for recording in recording_hd}

    #范文朗读 文章列表
    sql="select ch_Name,ch_Code from yw_chapter where ct_ID=35 and ch_IsContent=1 and enable_flag=0"
    chapter_data = db.tbkt_yw_slave.fetchall_dict(sql)
    chapter_dict={}
    for chapter in chapter_data:
        recording = recording_dict.get(int(chapter.ch_Code), 0)
        chapter['recording']=recording
        chapter_dict[int(chapter.ch_Code)]=chapter.ch_Name
    return chapter_data[p_begin:p_end]





def date_format(temp):
    """
    格式化时间
    :param temp: 毫秒值
    :return:
    """
    return time.strftime("%Y-%m-%d", time.localtime(temp))

def recommend_article(user_id,ch_Code):
    """
    老师推荐文章入库
    :param request:
    :param user_id: 用户id
    :param ch_ID: 章节id
    :return:
    """
    add_time=time.time()
    t = time.localtime(add_time)
    zero_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))

    detail = db.tbkt_active_slave.yw_article_recommend_hd.get(user_id=user_id,add_time__gte=zero_time)
    if not detail:
        db.tbkt_active.yw_article_recommend_hd.create(user_id=user_id,
                                                      ch_Code=ch_Code,
                                                    add_time=add_time
                                                   )
        #调用加积分接口
        return 1

def article_details(state,ch_Code,user_id,ch_Name):
    """
    #文章详情
    :param status: #0未录制，1，已录制，2已分享
    :param ch_Code: #文章code
    :param user_id: 学生id
    :return:
    """
    sql="select ti_Contents from yw_textinfo where ch_Code=%s" % ch_Code
    data = db.tbkt_yw_slave.fetchone_dict(sql)
    if data:

        data['ch_Name'] = ch_Name
        data['user_id'] = user_id
        data['status'] = state
        return data

def post_recording(json_info,ch_Code,user_id):
    """
    录音入库
    :param json_info: 录音路径
    :param ch_Code: 文章code
    :param user_id: 用户id
    :return:
    """

    add_time=time.time()
    tbkt_active=db.tbkt_active_slave.yw_recording_hd.get(user_id=user_id,ch_Code=ch_Code)
    if not tbkt_active:
        recording=db.tbkt_active.yw_recording_hd.create(user_id=user_id,
                                              ch_Code=ch_Code,
                                              json_info=json_info,
                                              add_time=add_time,
                                              state=1,
                                              ballot_num=0
                                                   )
        return 1



def recording_integral(recording_id, share_time,state,user_id,is_open,class_id,city):
    """
    每天最新一次分享加分
    :param recording_id:  录音id
    :param share_time: 最新一次分享时间
    :param state: 状态
    :param user_id: 用户id
    :return:
    """

    add_time=time.time()
    t = time.localtime(add_time)
    zero_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00',t), '%Y-%m-%d %H:%M:%S'))
    if state==1 or (zero_time>share_time and state==2):
        #当天首次分享
        recording_hd = db.tbkt_active.yw_recording_hd.filter(user_id=user_id, id=recording_id).update(state=2,add_time=add_time)
        # 首次分享学生加分
        if city != 411200:
            update_score(user_id,4,'share',user_id,0,class_id, is_open)
        return 1


def get_open(user_id):
    """
    判断是否开通
    :return:
    """
    recording = db.tbkt_active_slave.yw_activity_record_hd.get(user_id=user_id,add_time=0)
    is_open=0
    if recording:
        is_open=recording.is_open
        return is_open

def ballot_integral(user_id,class_id,ch_Code,city_id):
    """

    :param recording_id:  录音id
    :param is_open: #是否开通
    :return:
    """

    recording = db.tbkt_active.yw_recording_hd.filter(ch_Code=ch_Code, user_id=user_id)
    if not recording[0]:
        return 0

    recording_ballot = recording[0].ballot_num
    recording.update(ballot_num=recording_ballot + 1)
    is_open = get_open(user_id)
    if city_id != 411200:
        update_score(user_id, 4, 'ticket', user_id, 0, class_id, is_open)
    return 1



# def ballot_integral(recording_id,is_open,user_id,class_id,ch_Code):
#     """
#
#     :param recording_id:  录音id
#     :param is_open: #是否开通
#     :return:
#     """
#
#     ip=get_ip()
#     add_time = time.time()
#     t = time.localtime(add_time)
#
#     zero_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
#     ballot_record = db.tbkt_active.yw_ballot_record_hd.filter(ip=ip)
#     if recording_id:
#         recording = db.tbkt_active.yw_recording_hd.filter(id=recording_id,user_id=user_id)
#     elif ch_Code:
#         recording = db.tbkt_active.yw_recording_hd.filter(ch_Code=ch_Code,user_id=user_id)
#     else:
#         return 0
#     if not recording[0]:
#         return 0
#
#     recording_ballot=recording[0].ballot_num
#
#     if ballot_record and ballot_record[0].add_time ==zero_time:
#         ballot_num=ballot_record[0].ballot_num
#
#         if ballot_num<500:
#             ballot_record.update(ballot_num=ballot_num+1)
#             recording.update(ballot_num=recording_ballot+1)
#             if is_open==-1:
#                 is_open=get_open(user_id)
#             update_score(user_id, 4, 'ticket', ip, 0, class_id, is_open)
#             return 1
#             #投票成功，加分
#     elif not ballot_record:
#         db.tbkt_active.yw_ballot_record_hd.create(ip=ip,
#                                                   ballot_num=1,
#                                                   add_time=zero_time
#                                                    )
#         # 投票成功，根據是否開通加分
#         recording.update(ballot_num=recording_ballot + 1)
#         if is_open == -1:
#             is_open = get_open(user_id)
#         update_score(user_id, 4, 'ticket', ip, 0, class_id, is_open)
#         return 1
#     elif ballot_record and ballot_record[0].add_time <zero_time:
#         ballot_record.update(ballot_num=1,add_time=zero_time)
#         # 投票成功，根據是否開通加分
#         recording.update(ballot_num=recording_ballot + 1)
#         if is_open == -1:
#             is_open = get_open(user_id)
#         update_score(user_id, 4, 'ticket', ip, 0, class_id, is_open)
#         return 1
#     return 0





def get_ip():
    # url = r'http://1212.ip138.com/ic.asp'
    # r = requests.get(url)
    # txt = r.text
    # ip = txt[txt.find("[") + 1: txt.find("]")]
    # return ip
    ip=get_out_ip(get_real_url())
    return ip



# 获取外网IP
def get_out_ip(url):
    r = requests.get(url)
    txt = r.text
    ip = txt[txt.find("[") + 1: txt.find("]")]
    return ip


def get_real_url(url=r'http://www.ip138.com/'):
    r = requests.get(url)
    txt = r.text
    soup = BeautifulSoup(txt,"html.parser").iframe
    return soup["src"]




def all_recording(p, user_id):
    """
    學生端全省積分作品排名
    :param p: 分頁
    :param user_id: 用戶id
    :return:
    """
    #gt > ; gte >=;lt <;lte <=

    p_begin=(p-1)*10
    p_end = p * 10

    now_time=time.time()
    active=db.tbkt_active_slave.active.get(subject_id=51,user_type=1,begin_time__lte=now_time,end_time__gte=now_time)
    if active:
        id=active.id

        sql="select user_id from active_score_user where active_id= %s ORDER BY score desc  limit %s,%s" % (id,p_begin,p_end)
        active=db.tbkt_active_slave.fetchall_dict(sql)
        if active:
            user_ids=[data.user_id for data in active]
            user_str=(",".join(str(i) for i in user_ids))

            sql = "SELECT user_id, ch_Code,json_info, max(ballot_num) ballot_num FROM yw_recording_hd where user_id in (%s) GROUP BY user_id" % user_str
            recording = db.tbkt_active_slave.fetchall_dict(sql)
            recording_dict={}
            ch_code_list=[]
            for is_data in recording:
                recording_dict[is_data.user_id]=is_data
                ch_code_list.append(is_data.ch_Code)
            ch_name = db.tbkt_yw_slave.yw_chapter.filter(ch_Code__in=ch_code_list, ch_IsContent=1, enable_flag=0).select("ch_Code","ch_Name")
            ch_name_dict ={int(is_data.ch_Code): is_data.ch_Name for is_data in ch_name}
            recording_dict = {is_data.user_id: is_data for is_data in recording}
            school_dict=com_user.users_info(user_ids)

            for is_data in active:
                is_recording_dict=recording_dict.get(is_data.user_id,"")
                ch_Code=is_recording_dict.get("ch_Code", "")

                is_data['ch_name']=  ch_name_dict.get(ch_Code, "")
                is_data['school_dict'] = school_dict.get(is_data.user_id,"")
                is_data['recording_dict']=is_recording_dict
            return active





def share_activity(user_id,class_id,is_open,city):
    """
    学生端分享活动页加分
    :param user_id: 用户id
    :return:
    """

    t = time.localtime(time.time())
    zero_time = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
    ballot_record = db.tbkt_active.yw_ballot_record_hd.filter(ip=user_id)
    if ballot_record:
        add_time=ballot_record[0].add_time
        if add_time !=zero_time:
            ballot_record.update(add_time=zero_time)
            if city !=411200:
                a=update_score(user_id, 4, 'activity_share', user_id, 0, class_id, is_open)
                return 1

    else:
        db.tbkt_active.yw_ballot_record_hd.create(ip=user_id,
                                                add_time=zero_time
                                                   )
        if city !=411200:
            a=update_score(user_id, 4, 'activity_share', user_id, 0, class_id, is_open)
            return  1
    return 0















