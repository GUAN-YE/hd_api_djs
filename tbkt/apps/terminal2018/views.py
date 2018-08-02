# coding: utf-8
from apps.terminal2018.common import p_del_pop_up
from com.com_user import need_login
from libs.utils import ajax, ajax_try
from . import common


@need_login
@ajax_try()
def r_book_user(request):
    """
    @api {get} /huodong/terminal/book/user [期末提分试卷]用户教材
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "grade_id": 6,
                "name": "小学数学六年级下册(苏教版)",
                "id": 747
            },
            "response": "ok",
            "error": ""
        }
    """
    user = request.user
    subject_id = user.subject_id
    if not subject_id:
        return ajax.jsonp_fail(request, message="缺少科目id！")
    if subject_id == 51:
        # 语文用户
        data = common.p_yw_user_book(user.id)
        return ajax.jsonp_ok(request, data)
    data = common.p_user_book(user.id, subject_id)
    return ajax.jsonp_ok(request, data)


@need_login
@ajax_try()
def r_book_list(request):
    """
    @api {get} /huodong/terminal/book/list [期末提分试卷教材列表
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "grade_id":1",
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "books": [
                        {
                            "press_name": "人教版",
                            "name": "四年级上册",
                            "subject_id": 21,
                            "grade_id": 4,
                            "volume": 1,
                            "book_type": 1,
                            "grade_name": "四年级",
                            "volume_name": "上册",
                            "id": 366,
                            "press_id": 2
                        },
                        {
                            "press_name": "人教版",
                            "name": "二年级上册",
                            "subject_id": 21,
                            "grade_id": 2,
                            "volume": 1,
                            "book_type": 1,
                            "grade_name": "二年级",
                            "volume_name": "上册",
                            "id": 277,
                            "press_id": 2
                        },
            ]
        },
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(grade_id=str)
    subject_id = user.subject_id
    if not subject_id:
        return ajax.jsonp_fail(request, message="缺少科目id")
    grade_id = args.grade_id or "1"
    grade_id = grade_id.split(',')
    typ = args.type or 1
    book_id = args.book_id or 0
    books = common.p_booklist(subject_id, typ, grade_id, book_id)
    data = {
        'books': books
    }
    return ajax.jsonp_ok(request, data)


@need_login
@ajax_try()
def r_book_set(request):
    """
    @api {post} /huodong/terminal/book/set [期末提分试卷]设置用户教材/教辅
    @apiGroup terminal
    @apiParamExample {json} 请求示例
        {"book_id": 教材ID}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(book_id=int)
    book_id = args.book_id or 0
    if not book_id:
        return ajax.jsonp_fail(request, message=u"没有相对应的教材")
    common.setbook(user, book_id)
    return ajax.jsonp_ok(request)


@need_login
@ajax_try()
def r_pop_up(request):
    """
    @api {post} /huodong/terminal/pop_up [期末提分试卷]活动弹窗
    @apiGroup terminal
    @apiParamExample {json} 请求示例    
    {}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": 0/1,    # 弹/不弹
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    if user.subject_id == 91 and user.grade_id < 3:
        return ajax.ajax_ok(request, 0)
    data = common.p_pop_up(user)
    return ajax.jsonp_ok(request, data)


@need_login
@ajax_try()
def r_paper_list(request):
    """
    @api {post} /huodong/terminal/paper/list [期末提分试卷]试卷列表公共
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "status": 1,    0/1  可以发/不可以发
                "id": 21021,
                "name": "期末提分试卷--(一)"
            },
            {
                "status": 1,
                "id": 21022,
                "name": "期末提分试卷--(二)"
            },
            {
                "status": 1,
                "id": 21023,
                "name": "期末提分试卷--(三)"
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    subject_id = user.subject_id
    if not subject_id:
        return ajax.jsonp_fail(request, message="缺少科目id！")
    data = common.p_paper_list(user, subject_id)
    return ajax.jsonp_ok(request, data)


@need_login
@ajax_try()
def r_task_class(request):
    """
    @api {post} huodong/terminal/task/class [期末提分试卷]用户发送作业班级
    @apiGroup terminal
    @apiParamExample {json} 请求示例
        {"paper_id":"1,2,3"}
    @apiSuccessExample {json} 成功返回
        {
        "message": "",
        "next": "",
        "data": {
            "unit_info": [
                {
                    "status": 0, -1/0/1 --  -1/班级没有学生/0不能发送/1继续发送
                    "unit_name": "128班",
                    "unit_class_id": 2929017
                }
            ],
            "grade_id": 1
        },
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    grade_id = user.grade_id or 1
    args = request.QUERY.casts(paper_id=str)
    paper_id = args.paper_id
    if not paper_id:
        return ajax.jsonp_fail(request, message=u"选择发送的试卷")
    # 获取发试卷的paper_ids
    try:
        paper_ids = map(int, paper_id.split(','))
    except Exception as e:
        print e
        return ajax.jsonp_fail(request, message=u"参数异常")
    data = common.p_task_class(user, grade_id, paper_ids)
    return ajax.jsonp_ok(request, data)


def r_del_cache(request):
    """
    删除缓存
    :param request: 
    :return: 
    """
    args = request.QUERY.casts(user_id=int)
    user_id = args.user_id
    p_del_pop_up(user_id)
    return ajax.jsonp_ok(request)

