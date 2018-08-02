# coding: utf-8
from libs.utils import ajax_json as ajax, ajax_try
from com.com_user import need_teacher
from . import common


@ajax_try([])
@need_teacher
def hd_book_papers(request):
    """
    @api {get} /huodong/sx_terminal/paper/list [数学期末提分试卷]提分试卷列表
    @apiGroup sx_terminal
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


