# coding:utf-8
import time
from libs.utils import db,tbktapi,Struct
from com import com_user
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def integral_list(request,p,user_type,is_class):
    """
    學生端全省積分作品排名
    :param p: 分頁
    :param user_id: 用戶id
    :param user_type: 用戶类型参与用户类型 0 全部 1 学生 3 教师
    :param is_class: 0 全省列表，其他，班级id，
    :return:
    """
    if p == 0:
        p = 1
    p_begin=(p-1)*5
    if user_type==1:
        id = 4
    elif user_type==3:
        id = 5
    else:
        return
    if is_class==0:
        sql="select ch_Code,b.user_id,b.json_info,b.ballot_num from active_score_user a inner join (select c.user_id,c.id as record_id, c.ch_Code,c.json_info, c.ballot_num,count(distinct c.user_id) from yw_recording_hd as c where ballot_num = (select max(ballot_num) from yw_recording_hd where c.user_id=user_id) group by c.user_id) b on a.user_id =b.user_id  where a.active_id=%s ORDER BY a.score desc ,a.user_id limit %s,5" % (id, p_begin)
        # sql_count="select count(t.counts) from (select id,count(*) counts from yw_recording_hd group by user_id) t "
        sql_count = "select count(*)from active_score_user a inner join (select c.user_id,c.id as record_id, c.ch_Code,c.json_info, c.ballot_num,count(distinct c.user_id) from yw_recording_hd as c where ballot_num = (select max(ballot_num) from yw_recording_hd where c.user_id=user_id) group by c.user_id) b on a.user_id =b.user_id  where a.active_id=%s ORDER BY a.score desc ,a.user_id " % id
    else:
        sql_count="select count(*) from active_score_user where user_id in (select user_id from yw_recording_hd GROUP BY user_id) AND active_id=%s AND unit_id=%s" % ( id,is_class )
        sql="""select b.ballot_num,b.json_info,ch_Code,b.user_id  from active_score_user a
                inner join tbkt_ketang.mobile_order_region as d on a.user_id =d.user_id
                inner join
              (select c.user_id,c.id as record_id, c.ch_Code,c.json_info, c.ballot_num,count(distinct c.user_id) from yw_recording_hd as c where ballot_num = (select max(ballot_num) from yw_recording_hd where c.user_id=user_id) group by c.user_id) b on a.user_id =b.user_id 
              where a.active_id=%s and d.unit_class_id =%s ORDER BY a.score desc ,a.user_id limit %s,5""" % (id,is_class,p_begin)
    active = db.tbkt_active_slave.fetchall_dict(sql)

    if active:
        active_count = db.tbkt_active_slave.fetchone(sql_count)
        user_ids=[data.user_id for data in active]
        ch_code_list=[]
        for is_data in active:
            ch_code_list.append(is_data.ch_Code)
        ch_name = db.tbkt_yw_slave.yw_chapter.filter(ch_Code__in=ch_code_list, ch_IsContent=1, enable_flag=0).select("ch_Code","ch_Name")
        ch_name_dict ={int(is_data.ch_Code): is_data.ch_Name for is_data in ch_name}
        school_dict=com_user.users_info(user_ids)

        for is_data in active:
            is_data['ch_name']=  ch_name_dict.get(is_data.ch_Code, "")
            is_data['school_dict'] = school_dict.get(is_data.user_id,"")
        page_count=divmod(active_count[0], 5)
        page_count=page_count[0]if page_count[1]==0 else page_count[0]+1
        return {'active':active,'page_count':page_count,'data_count':active_count[0]}


def end_list(user_type,is_type,p_begin):
    """

    :param user_type:  4学生，5教师
    :param is_type: 1，按奖品，2，按积分来
    :return:
    """
    p_begin= p_begin if p_begin else 0
    b_end = p_begin * 10
    p_begin = (p_begin- 1) * 10

    new_time=time.time()
    active_db = db.tbkt_active.active.filter(id=user_type).select('begin_time','end_time')
    begin_time=active_db[0].begin_time
    end_time=active_db[0].end_time
    is_state=1
    if new_time>end_time or new_time<begin_time:
        is_state=0

    if is_type==1:

        sql = "select user_id,user_name,award_name from active_award where remark= %s and award_name !='谢谢参与' ORDER BY award_type desc limit %s,10" % (
            user_type, p_begin)
        active_data = db.tbkt_active_slave.fetchall_dict(sql)
        if not active_data:
            return {"active_data": '', "is_state": is_state}
        user_ids = [data.user_id for data in active_data]
        school_dict = com_user.users_info(user_ids)
        for active in active_data:
            active['school_dict'] = school_dict.get(active.user_id, "")
    elif is_type==2:
        if user_type==4 and b_end>50:
            return

        sql="select name,start_num,end_num from active_score_gift where active_id=%s and status=1 and active_type=2" % user_type
        active_data = db.tbkt_active_slave.fetchall_dict(sql)
        active_data_dict=[]
        for is_data in active_data:
            for i in range(is_data.start_num,is_data.end_num+1):
                if i !=0:
                    active_data_dict.append(str(is_data.name))

        num=len(active_data_dict)

        sql = "SELECT a.user_id FROM active_score_user as a join active_score_user as b on a.id = b.id WHERE a.active_id= %s ORDER BY a.score desc LIMIT 0,%s" %(user_type,num)
        active_data = db.tbkt_active_slave.fetchall_dict(sql)
        if active_data:
            user_ids = [data.user_id for data in active_data]
            if user_ids:
                school_dict = com_user.users_info(user_ids)
                i=0
                for is_data in active_data:
                    is_data['school_dict'] = school_dict.get(is_data.user_id, "")
                    is_data['award_name'] = active_data_dict[i]
                    is_data['user_name'] = is_data['school_dict']['real_name']
                    i+=1

        # sql="select b.user_id,b.user_name,b.award_name from active_score_user a inner join active_award b on a.user_id =b.user_id where a.active_id=%s and b.remark=%s and award_name !='谢谢参与' ORDER BY a.score desc limit %s,10" % (user_type,user_type, p_begin)
        # active_data = db.tbkt_active_slave.fetchall_dict(sql)
        # if not active_data:
        #     return {"active_data": '', "is_state": is_state}
        # user_ids = [data.user_id for data in active_data]
        # school_dict = com_user.users_info(user_ids)
        # for active in active_data:
        #     active.school_dict= school_dict.get(active.user_id, "")

        return {"active_data":active_data[p_begin:b_end],"is_state":is_state}
    return {"active_data": active_data, "is_state": is_state}










