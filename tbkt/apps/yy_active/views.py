#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/9/5 14:20
"""

from apps.common import com_yy
from apps.yy_active import common
from apps.yy_normal import views as nor_view
from libs.utils.ajax import jsonp_ok, jsonp_fail

"""
3: 英语常态活动(s1赛季)
"""
ACTIVE_ID_LIST = [3]

ACTIVE_ID_NAME = {
    3: "apps.yy_normal.views",
}



def add_score(request):
    """
    功能说明：                英语活动加减积分
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    user = request.user
    active_list = common.get_actives_status(user, ACTIVE_ID_LIST)
    if active_list:
        args = request.loads() or request.QUERY.casts(item_no=str)
        item_no = args.item_no or ""
        if not item_no:
            return jsonp_fail(request, message="no item_no")
        user_id = user.id
        city = user.city
        unit_id = user.units[0].id if user.units else 0
        for active_id in active_list:
            # pm = __import__(ACTIVE_ID_NAME.get(active_id), fromlist=['add_score'])
            nor_view.add_score(user_id, active_id, item_no, user_id, city, unit_id)
    return jsonp_ok(request)

def get_question(request):
    """
    @api {post} /huodong/yy/active/get_question [英语活动]获取习题详情
    @apiGroup YyActive
    @apiParamExample {json} 请求示例
       {
        'qid': 3104,
        'no': 1
       }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "video_image": "",
            "ask_no": 2,
            "video_url": "",
            "ask": [
                {
                    "video_image": "",
                    "video_url": "",
                    "no": 2,
                    "listen_audio": "",
                    "options": [],
                    "parse": {
                        "content": "",
                        "images": []
                    },
                    "answer": [
                        "Can you "
                    ],
                    "listen_text": "",
                    "duration": -1,
                    "right_option": null,
                    "id": 3292,
                    "subject": {
                        "content": "I can jump high.（变为一般疑问句）<br/><input placeholder=\"点击填写\">jump high?<br />",
                        "images": []
                    }
                }
            ],
            "type": 9,
            "id": 3104,
            "classify": 2,
            "subject": {
                "content": "按要求完成题目。",
                "images": []
            }
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
      {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                英语活动- 获取问题详情
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-22
    """
    args = request.loads() or request.QUERY.casts(no=int, qid=int)
    qid = args.qid or 0
    ask_no = args.no or 0
    ask_no = int(ask_no)
    qid = int(qid)
    if not qid or not ask_no:
        return jsonp_fail(request, message=u'参数错误')
    question = com_yy.get_question_data(qid, ask_no)
    return jsonp_ok(request, question)