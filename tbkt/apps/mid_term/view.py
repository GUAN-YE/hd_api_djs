# coding: utf-8
from libs.utils import ajax_json as ajax, ajax_try
from com.com_user import need_teacher
from . import common

@ajax_try({})
@need_teacher
def hd_book_papers(request):
    """
    @api {get} /huodong/mid_term/paper/list [期中提分试卷]数学提分试卷列表
    @apiGroup mid_term
    @apiSuccessExample {json} 提分试卷列表
    {
        "message": "",
        "next": "",
        "data": [
            {
                "status": 0,
                "id": 4168,
                "name": "提分试卷2"
            },
            {
                "status": 0,
                "id": 4208,
                "name": "提分试卷3"
            },
            {
                "status": 0,
                "id": 4379,
                "name": "提分试卷4"
            },
            {
                "status": 0,
                "id": 4398,
                "name": "提分试卷5"
            },
            {
                "status": 0,
                "id": 4400,
                "name": "提分试卷6"
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    subject_id = user.subject_id
    data = common.paper_list(user.id, subject_id)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_teacher
def p_select(request):
    """
    @api {get} /huodong/mid_term/book/select [期中提分试卷]选教材/教辅接口
    @apiGroup mid_term
    @apiParamExample {json} 请求示例
        {"subject_id":21,  # 英语为91
         "grade_id":1, "
         type":1教材 2练习册
         }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "books": [
                {
                    "press_name": "人教版", # 出版社
                    "press_id": 1, # 出版社ID
                    "name": "数学一年级上册",  # 默认书名
                    "subject_id": 21,  # 学科
                    "grade_id": 1,  # 年级
                    "volume": 1,  # 1上册 2下册 3全册
                    "version_name": "新版",  # 版本
                    "id": 276 # 教材/教辅ID
                },
            ]
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(subject_id=int, grade_id=int, type=int, book_id=int)
    subject_id = args.subject_id or 0
    grade_id = args.grade_id or 1
    type = args.type or 1
    book_id = args.book_id or 0

    books = common.get_gradelist(subject_id, type, grade_id, book_id)
    data = {
        'books': books
    }
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_teacher
def p_setbook(request):
    """
    @api {post} /huodong/mid_term/book/set [期中提分试卷]设置用户教材/教辅
    @apiGroup mid_term
    @apiParamExample {json} 请求示例
        {"book_id":教材/教辅ID}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(book_id=int)
    book_id = args.book_id or 0

    if not book_id:
        return ajax.jsonp_fail(request, message='参数错误: book_id')

    user_id = request.user_id
    common.setbook(user_id, book_id)
    return ajax.jsonp_ok(request)


@ajax_try({})
@need_teacher
def p_getbook(request):
    """
    @api {post} /huodong/mid_term/book/get [期中提分试卷]获取用户设置的活动教材
    @apiGroup mid_term
    @apiParamExample {json} 请求示例
        {
            "subject_id" : 21 / 91  # 21为数学  91为英语
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {},
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(subject_id=int)
    subject_id = args.subject_id or 0
    if not subject_id:
        return ajax.jsonp_fail(request, "没有subject_id")
    user_id = request.user_id
    data = common.getbook(user_id, subject_id)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_teacher
def get_status(request):
    """
    @api {post} /huodong/mid_term/status/get [期中提分试卷]用户弹窗状态
    @apiGroup mid_term
    @apiParamExample {json} 请求示例
        {
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "status" : 1 0    1 弹  0 不弹
        },
        "response": "ok",
        "error": ""
    }
    """

    user_id = request.user.id
    data = common.get_status(user_id)
    return ajax.jsonp_ok(request, data)