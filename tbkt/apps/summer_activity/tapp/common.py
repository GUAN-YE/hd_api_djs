 # coding=utf-8
from libs.utils import db, Struct, num_to_ch, format_url
from django.core.paginator import Paginator
import datetime
from apps.mid_term import send_sx_task


share_score=100
nowtime = datetime.date.today()
send_homework_message_score = 1000

number_one = ''
number_two = ''
number_tree = ''
number_four= ''

def appoint_status(teacher_id,class_status):
    """
       功能说明：                查看预约状态
       -----------------------------------------------
       修改人                    修改时间
       -----------------------------------------------
       刘斌                    2018-6-8
       """
    have_teacher_id = db.tbkt_active_slave.summer2018_appoint.select('teacher_id').get(teacher_id=teacher_id, class_status=class_status)
    if not have_teacher_id:
        return 0
    else:
        return 1

def get_dates(teacher_id):
    """
       功能说明：                获取教师详细数据
       -----------------------------------------------
       修改人                    修改时间
       -----------------------------------------------
       刘斌                    2018-6-8
       """

    user_info = db.tbkt_user_slave.auth_user.select('phone', 'real_name').get(id=teacher_id)
    user_massage = db.ketang_slave.mobile_order_region.select('school_name', 'city').get(user_id=teacher_id)
    phone_number = user_info.phone
    username = user_info.real_name
    school_name = user_massage.school_name
    teacher_city = user_massage.city
    dates = {
        'phone_number': phone_number,
        'school_name': school_name,
        'teacher_city': teacher_city,
        'username': username,
    }
    return dates
def save_status(teacher_id, appointment_status, class_status):

    db.tbkt_active_slave.summer2018_appoint.create(teacher_id=teacher_id,
                                                   appointment_status=appointment_status,
                                                   class_status=class_status)
    get_date = get_dates(teacher_id)
    teacher_city = get_date['teacher_city']
    school_name = get_date['school_name']
    phone_number = get_date['phone_number']
    username = get_date['username']
    if not school_name:
        return u'赶快注册吧'
    is_have = db.tbkt_active_slave.summer2018_ranking.get(teacher_id=teacher_id, class_status=class_status)
    if not is_have:
        db.tbkt_active_slave.summer2018_ranking.create(teacher_id=teacher_id, teacher_name=username,
                                                       teacher_school=school_name, class_status=class_status,
                                                       phone_number=phone_number, city=teacher_city)
    return 1


def save_share_score(teacher_id, class_status):

    is_have = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id,
                                                            class_status=class_status,
                                                            time=nowtime)
    if not is_have:
        db.tbkt_active_slave.summer2018_detail.create(teacher_id=teacher_id,
                                                      class_status=class_status,
                                                      share_score=share_score,
                                                      time=nowtime, sum_score=share_score, share_status=1)
        is_have_ranking = db.tbkt_active_slave.summer2018_ranking.get(teacher_id=teacher_id,
                                                       class_status=class_status)
        if not is_have_ranking:
            get_date = get_dates(teacher_id)
            teacher_city = get_date['teacher_city']
            school_name = get_date['school_name']
            phone_number = get_date['phone_number']
            username = get_date['username']
            db.tbkt_active_slave.summer2018_ranking.create(teacher_id=teacher_id, teacher_name=username,
                                                           teacher_school=school_name, class_status=class_status,
                                                           phone_number=phone_number, city=teacher_city, num_score=share_score)
        else:
            db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                       class_status=class_status).update(num_score=share_score)
        return 0
    # sum_score = str(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
    #                                                                class_status=class_status).get('teacher_id')['num_score'])
    sum_score db.tbkt_active_slave.summer2018_ranking.select('num_score').get(teacher_id=teacher_id,class_status=class_status)                                                               
    is_share = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id,
                                                            class_status=class_status,
                                                            time=nowtime, share_status=1)
    if is_share:
        return 1

    sum_score=share_score + sum_score
    db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                   class_status=class_status).update(
        num_score=sum_score)
    db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
                                                  class_status=class_status,
                                                  time=nowtime).update(sum_score=share_score)
    return 'ok'


def ranking(teacher_id, class_status, page):
    is_zhengzhou = db.tbkt_active_slave.summer2018_ranking.get(teacher_id=teacher_id,
                                                                  class_status=class_status,
                                                                  city=410100)
    if is_zhengzhou:
        ranking_data = db.tbkt_active_slave.summer2018_ranking.filter(class_status=class_status,
                                                                      city=410100).\
            select('teacher_name', 'teacher_school', 'num_score').order_by ('-num_score')
    else:
        ranking_data = db.tbkt_active_slave.summer2018_ranking.exclude(city=410100).filter(class_status=class_status). \
            select('teacher_name', 'teacher_school', 'num_score').order_by('-num_score')


    # zheng = str(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
    #                                                            class_status=class_status).get(
    #     'teacher_id')['city'])
    zheng = db.tbkt_active_slave.summer2018_ranking.select('city').get(teacher_id=teacher_id,class_status=class_status)
    ranking_data = class_status_data( class_status, ranking_data, zheng)['active_data']
    # my_num_score = str(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
    #                                                                   class_status=class_status)
    #                    .get(teacher_id=teacher_id)['num_score'])
    my_num_score = db.tbkt_active_slave.summer2018_ranking.select('num_score').get(teacher_id=teacher_id,class_status=class_status)
    no_mumber = db.tbkt_active_slave.summer2018_ranking.filter(num_score__gt=my_num_score).count() + 1
    ranking_datas = []
    for i in ranking_data:
        out={
        'teacher_name':i['teacher_name'],
        'teacher_school' : i['teacher_school'] if i['teacher_school'] else '',
        'num_score' : i['num_score'] if i['num_score'] else '',
        }
        ranking_datas.append(out)
    page_num = len(ranking_data)/10+1
    if page > page_num:
        page_data = []
    else:
        p = Paginator(ranking_datas, 10)
        page_data = p.page(page).object_list
    data = {
        'my_ranking': no_mumber,
        'my_num_score': my_num_score,
        'data': page_data
    }
    return data

def see_score(teacher_id,class_status):

    score_data = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id,
                                                               class_status=class_status)\
        .select('send_message_score', 'invite_student_score', 'share_score', 'studnet_finish_score', 'time', 'sum_score').order_by('-time')
    if not score_data:
        return u'暂无积分'
    score_datas = []
    for i in score_data:
        out = {
            'send_message_score':i.send_message_score if i.send_message_score else '',
            'invite_student_score': i.invite_student_score if i.invite_student_score else '',
            'share_score': i.share_score if i.share_score else '',
            'studnet_finish_score': i.studnet_finish_score if i.studnet_finish_score else '',
            'time': i.time,
            'sum_score': i.sum_score,
        }
        score_datas.append(out)
    return score_datas


def win_award(teacher_id, class_status):
    is_zhengzhou = db.tbkt_active_slave.summer2018_ranking.get(teacher_id=teacher_id,
                                                                  class_status=class_status,
                                                                  city=410100)
    if is_zhengzhou:
        ranking_data = db.tbkt_active_slave.summer2018_ranking.filter(
                                                                      class_status=class_status,
                                                                      city=410100). \
            select('teacher_name', 'phone_number', ).order_by('-num_score')
    else:
        ranking_data = db.tbkt_active_slave.summer2018_ranking.exclude(city=410100).filter( class_status=class_status).\
            select('teacher_name', 'phone_number').order_by('-num_score')
    if not ranking_data:
        return u'还未开奖'
    # zheng = str(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
    #                                                            class_status=class_status).get('teacher_id')['city'])
    # print(zheng)
    zheng db.tbkt_active_slave.summer2018_ranking.select('city').get(teacher_id=teacher_id,class_status=class_status)

    data = class_status_data(class_status, ranking_data, zheng)
    data.pop('active_data')

    return data

def ranking_datas(ranking_data):


    ranking_data_list = []
    for i in ranking_data:
        ranking_datas = {
            'teacher_name': i.teacher_name if i.teacher_name else '',
            'phone_number': i.phone_number if i.phone_number else '',
            'teacher_school': i.teacher_school if i.teacher_school else '',
            'num_score': i.num_score if i.num_score else '',
        }
        ranking_data_list.append(ranking_datas)
    return ranking_data_list


def class_status_data(class_status, ranking_data, zheng):
    global number_one
    global number_two
    global number_tree
    global number_four
    if class_status == 5 or class_status == 9:
        if zheng == 410100:
            ranking_data_list = ranking_datas(ranking_data)

            number_one = ranking_data_list[:3]
            number_two = ranking_data_list[3:50]
            number_tree = ranking_data_list[50:200]
            active_data = ranking_data_list[:200]

            data = {
                'number_one': number_one,
                'number_two': number_two,
                'number_tree': number_tree,
                'active_data': active_data,
            }
            return data
        else:
            ranking_data_list = ranking_datas(ranking_data)
            if class_status == 5:
                number_one = ranking_data_list[:1]
                number_two = ranking_data_list[1:11]
                number_tree = ranking_data_list[11:22]
                number_four = ranking_data_list[22:100]
            elif class_status == 9:
                number_one = ranking_data_list[:10]
                number_two = ranking_data_list[10:25]
                number_tree = ranking_data_list[25:100]
                number_four= ''
            active_data = ranking_data_list[:100]
            data = {
                'number_ones': number_one,
                'number_two': number_two,
                'number_tree': number_tree,
                'number_four': number_four,
                'active_data': active_data,
            }

            return data
    if class_status == 2:
        if zheng == 410100:
            ranking_data_list=ranking_datas(ranking_data)
            number_one = ranking_data_list[:1]
            number_two = ranking_data_list[1:10]
            number_tree = ranking_data_list[10:60]
            number_four = ranking_data_list[60:310]
            number_five = ranking_data_list[310:500]
            active_data = ranking_data_list[:500]
            data={
                'number_one': number_one,
                'number_two': number_two,
                'number_tree': number_tree,
                'number_four': number_four,
                'number_five': number_five,
                'active_data': active_data,
            }
            return data
        else:
            ranking_data_list = ranking_datas(ranking_data)
            number_one = ranking_data_list[:1]
            number_two = ranking_data_list[1:20]
            number_tree = ranking_data_list[20:200]
            active_data = ranking_data_list[:200]
            data = {
                'number_one': number_one,
                'number_two': number_two,
                'number_tree': number_tree,
                'active_data': active_data,
            }
            return data


def send_homework_message(request, teacher_id, class_status):
    is_status = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id,
                                                            class_status=class_status, send_message_status=1)
    class_id = db.ketang_slave.mobile_order_region.get(user_id=teacher_id, user_type=3).get('user_id')['unit_class_id']
    studentid = db.ketang_slave.mobile_order_region.get(unit_class_id=class_id, user_type=1).select('user_id')
    user_id=[]
    for i in studentid:
        user={'user_id':i.user_id}
        users = user['user_id']
        user_id.append(users)
    content='家长您好，我为孩子制定了一份暑期阅读计划，帮助孩子提升写作能力，扩大知识面，为高年级语文学习打下好的基础。记得帮孩子合理安排时间，登录同步课堂APP进行学习（下载地址：m.tbkt.cn）'
    send_sx_task.send_sms_user_id(request, user_id, content)
    get_date = get_dates(teacher_id)
    teacher_city = get_date['teacher_city']
    is_have = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id,
                                                            class_status=class_status)
    if not is_have:
        db.tbkt_active_slave.summer2018_detail.create(teacher_id=teacher_id,
                                                      class_status=class_status,
                                                      share_score=send_homework_message_score,
                                                      city=teacher_city,
                                                      sum_score=send_homework_message_score,
                                                      time=nowtime, send_message_status=1)
        is_have_ranking = db.tbkt_active_slave.summer2018_ranking.get(teacher_id=teacher_id,
                                                                         class_status=class_status)
        if not is_have_ranking:
            get_date = get_dates(teacher_id)
            teacher_city = get_date['teacher_city']
            school_name = get_date['school_name']
            phone_number = get_date['phone_number']
            username = get_date['username']
            db.tbkt_active_slave.summer2018_ranking.create(teacher_id=teacher_id, teacher_name=username,
                                                           teacher_school=school_name, class_status=class_status,
                                                           phone_number=phone_number, city=teacher_city,
                                                           num_score=send_homework_message_score)
        else:
            db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                       class_status=class_status).update(num_score=share_score)
        return ''
    else:
        # sum_score = int(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id).get('teacher_id')['num_score'])
        # sum_scores = int(db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
        #                                                                class_status=class_status,).get('teacher_id')['sum_score'])
        sum_score = db.tbkt_active_slave.summer2018_ranking.select('num_socre').get(teacher_id=teacher_id)
        sum_scores db.tbkt_active_slave.summer2018_detail.select('sum_socre').get(teacher_id=teacher_id,class_status=class_status)
        sum_scoress=send_homework_message_score + sum_scores
        sum=send_homework_message_score + sum_score
        db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
                                                      class_status=class_status,
                                                      time=nowtime).\
                                                      update(send_message_score=send_homework_message_score,
                                                      sum_score=sum_scoress)
        db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                       class_status=class_status).update(
                                                      num_score=sum)
        return ''

def send_open_message(request, teacher_id, class_status):
    class_id = db.ketang_slave.mobile_order_region.filter(user_id=teacher_id, user_type=3).selsect('unit_class_id')
    studentid = db.ketang_slave.mobile_order_region.filter(unit_class_id=class_id, user_type=1).select('user_id')
    user_id = []
    for i in studentid:
        user = {'user_id': i.user_id}
        users = user['user_id']
        db.tbkt_active_slave.summer2018_send_open.create(teacher_id=teacher_id, class_status=class_status, student_id=users, send_open_status=1,send_time=nowtime)
        user_id.append(users)
    content = '家长您好，暑假期间没有老师辅导时，推荐您为开通同步课堂业务，利用知识点讲解视频、课本点读机等功能，帮助孩子做好自主学习，48小时内您将收到10086下发的邀请短信，回复“是”即可成功开通。如使用中遇到问题，请拨打客服热线：12556185进行咨询'
    send_sx_task.send_sms_user_id(request, user_id, content)


def get_student_status(userid, status, class_status, time):




    # is_have = db.tbkt_active_slave.summer2018_send_open(teacher_id=teacher_id, class_status=class_status)
    is_have = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id, class_status=class_status)
    if not is_have:
        db.tbkt_active_slave.summer2018_detail.create(teacher_id=teacher_id,
                                                      class_status=class_status)
    return 0

def get_finash_score(request, teacher_id, score, subject_id):
    is_have = db.tbkt_active_slave.summer2018_detail.get(teacher_id=teacher_id, class_status=subject_id)
    get_date = get_dates(teacher_id)
    teacher_city = get_date['teacher_city']
    if not is_have:
        db.tbkt_active_slave.summer2018_detail.create(teacher_id=teacher_id,
                                                      class_status=subject_id,
                                                      studnet_finish_score=score,
                                                      city=teacher_city,
                                                      sum_score=send_homework_message_score,
                                                      time=nowtime)
        db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                       class_status=subject_id).update(num_score=share_score)
    else:
        # sum_score = int(db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id).get('teacher_id')['num_score'])
        # sum_scores = int(db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
        #                                                                class_status=subject_id, ).get('teacher_id')['sum_score'])
        # finash_score = int(db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
        #                                                                class_status=subject_id, ).get('teacher_id')[
        #                      'studnet_finish_score'])
        sum_score = db.tbkt_active_slave.summer2018_ranking.select('num_score').get(teacher_id=teacher_id)
        scores = db.tbkt_active_slave.summer2018_detail.select('sum_score','studnet_finish_score').get(teacher_id=teacher_id,subject_id=subject_id)
        sum_scores = scores.sum_score
        finash_score = scores.finash_score
        sum_scoress = score + sum_scores
        sum = score + sum_score
        finash_score=finash_score+score
        db.tbkt_active_slave.summer2018_detail.filter(teacher_id=teacher_id,
                                                      class_status=subject_id,
                                                      time=nowtime). \
            update(studnet_finish_score=finash_score,
                   sum_score=sum_scoress)
        db.tbkt_active_slave.summer2018_ranking.filter(teacher_id=teacher_id,
                                                       class_status=subject_id).update(
            num_score=sum)
    return ''

