# coding=utf-8
from apps.summer_activity.tapp import common
from libs.utils import ajax,ajax_try
from com.com_user import need_login
import time



status=0
@ajax_try({})
@need_login
def yuyue(request):
    '''

    :param request:
    :return: jeiduan: 活动阶段 1/2/3/4(第一、第二、第三、未开始/未结束)
    {
  "message": "",
  "next": "",
  "data": {
    "status": 1,
    "jieduan": 4
  },
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    global status
    time1 = 1529078400
    time1s = 1530374399
    time2 = 1530374400
    time2s = 1535471999
    time3 = 1535472000
    time3s = 1535731199
    nowtime = str(time.time())
    if nowtime>=time1 and nowtime <= time1s :
         status = 1
    elif nowtime >= time2 and nowtime <=time2s:
         status = 2
    elif nowtime >= time3 and nowtime <= time3s:
         status = 3
    else:
        status = 4
    args = request.QUERY.casts(appointment_status=int)
    appointment_status = args.appointment_status
    if not appointment_status:
        datas = common.appoint_status(teacher_id, class_status)
    else:
        datas = common.save_status(teacher_id, appointment_status, class_status)
    data = {
        'jieduan': status,
        'status': datas
    }
    return ajax.jsonp_ok(request, data)

@ajax_try({})
@need_login
def share(request):
    '''

    :param request:
    :return:
    {
  "message": "",
  "next": "",
  "data": 1,
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    if not teacher_id or class_status:
        print('0000000')
    data = common.save_share_score(teacher_id, class_status)
    return ajax.jsonp_ok(request, data)

@ajax_try({})
@need_login
def ranking(request):
    '''
    :param request:
    :return:
    {
  "message": "",
  "next": "",
  "data": {
    "my_num_score": "100",
    "my_ranking": 19,
    "data": [
      {
        "teacher_school": "河南省郑州市中原区互助路小学",
        "teacher_name": "教师",
        "num_score": 100
      },
      {
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": 7
      },
      {
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": 6
      },
      {
        "teacher_school": "",
        "teacher_name": "23432",
        "num_score": 6
      },
      {
        "teacher_school": "",
        "teacher_name": "98",
        "num_score": 6
      },
      {
        "teacher_school": "",
        "teacher_name": "345",
        "num_score": 5
      },
      {
        "teacher_school": "",
        "teacher_name": "计数法",
        "num_score": 5
      },
      {
        "teacher_school": "",
        "teacher_name": "234",
        "num_score": 4
      },
      {
        "teacher_school": "",
        "teacher_name": "867",
        "num_score": 4
      },
      {
        "teacher_school": "",
        "teacher_name": "",
        "num_score": 4
      }
    ]
  },
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    args = request.QUERY.casts(page=int)
    page = args.page
    print(page)
    if not teacher_id or class_status:
        print('0000000')
    data = common.ranking(teacher_id, class_status, page)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def score(request):
    '''

    :param request:
    :return:
    {
  "message": "",
  "next": "",
  "data": [
    {
      "invite_student_score": "",
      "share_score": 100,
      "sum_score": 100,
      "send_message_score": "",
      "time": "2018-06-08",
      "studnet_finish_score": ""
    }
  ],
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    data = common.see_score(teacher_id, class_status)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def award_name(request):
    '''

    :param request:
    :return:
    {
  "message": "",
  "next": "",
  "data": {
    "number_tree": [],
    "number_two": [
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "23432",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "98",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "345",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "计数法",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "234",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "867",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "12",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "123",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "3453",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "0",
        "num_score": ""
      },
      {
        "phone_number": "",
        "teacher_school": "",
        "teacher_name": "345332",
        "num_score": ""
      }
    ],
    "number_one": [
      {
        "phone_number": 18317892045,
        "teacher_school": "",
        "teacher_name": "教师",
        "num_score": ""
      }
    ]
  },
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    data = common.win_award(teacher_id, class_status)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def send_homework(request):
    '''

    :param request:
    :return:
    {
  "message": "",
  "next": "",
  "data": "",
  "response": "ok",
  "error": ""
}
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    data = common.send_homework_message(request, teacher_id, class_status)
    return ajax.jsonp_ok(request, data)

@ajax_try({})
@need_login
def send_open(request):
    '''
    :param request:
    :return:
    '''
    user = request.user
    class_status=user.subject_id//10
    teacher_id=user.id
    args = request.QUERY.casts(send_status=int)
    # teacher_id = args.teacher_id
    # class_status = args.class_status
    send_status = args.send_status
    # subject_id = request.user.subject_id
    # user = request.user
    # user_id = user.id
    # print subject_id//10

    data = common.send_open_message(request, teacher_id, class_status)
    return ajax.jsonp_ok(request, data)
