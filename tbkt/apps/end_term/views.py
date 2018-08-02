# coding: utf-8
from libs.utils import ajax_json as ajax, ajax_try
from com.com_user import need_teacher
from . import common


@ajax_try({})
@need_teacher
def p_list(request):
    """
    @api {get} /huodong/end_term/book/select [期中提分试卷]选教材/教辅接口
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
def set_book(request):
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