#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/12/20 17:33
"""

import json
import logging

from apps.common import com_yy
from apps.rz_paper import rz_com
from libs.utils import db
from com.com_user import need_login
from libs.utils.ajax import jsonp_ok, jsonp_fail


ACTIVE_ID = 13

@need_login
def p_status(request):
    """
        @api {post} /huodong/rz/status [汝州活动二期]试卷完成状态
        @apiGroup RzPaperActive
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "status": -1       # -1 没有做过， 0 继续答题， 1 查看结果
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                 汝州活动-试卷测试
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-21
    """
    data = {}
    user = request.user
    user_id = user.id
    unit = user.unit
    if not unit:
        return jsonp_fail(request, message=u'没有班级')
    grade_id = int(unit.get('grade_id', 0))
    if not grade_id:
        return jsonp_fail(request, message=u'没有年级')

    logging.info(grade_id)
    paper = db.tbkt_active_slave.active_paper.select('status').get(user_id=user_id, active_id=ACTIVE_ID, paper_id=grade_id)
    paper_status = paper.status if paper else -1
    data['status'] = paper_status
    return jsonp_ok(request, data=data)

@need_login
def do_paper(request):
    """
    @api {post} /huodong/rz/do_paper [汝州活动二期]做试卷
    @apiGroup RzPaperActive
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "sheet": [
                {
                    "answer": "",
                    "ask_id": 3500,
                    "option_id": 0,
                    "result": -1,
                    "question_id": 3300
                },
                {
                    "answer": "",
                    "ask_id": 3292,
                    "option_id": 0,
                    "result": -1,
                    "question_id": 3104
                }
                ],
                "numbers": [
                    {
                        "qid": 3300,
                        "ask_no": 1,
                        "aid": 3500
                    },
                    {
                        "qid": 3104,
                        "ask_no": 2,
                        "aid": 3292
                    }
                ]
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
      {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                汝州活动-做试卷
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-22
    """
    user = request.user
    user_id = user.id
    unit = user.unit
    if not unit:
        return jsonp_fail(request, message=u'没有班级')
    grade_id = int(unit.get('grade_id', 0))
    if not grade_id:
        return jsonp_fail(request, message=u'没有年级')
    data = rz_com.get_paper_question_number_sheet(user_id, ACTIVE_ID, grade_id)
    return jsonp_ok(request, data)

@need_login
def submit_paper(request):
    """
        @api {post} /huodong/rz/submit_paper [汝州活动二期]试卷提交
        @apiGroup RzPaperActive
        @apiParamExample {json} 请求示例
           {
            “status”: "1"           # 1 完成（提交）， 2 未完成（保存）
            "data": [{"question_id":"3104", "ask_id":"3292","answer":"A","option_id":19321,"result":1},
            {"question_id":"3300", "ask_id":"3500","answer":"A","option_id":19321,"result":0}]
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": "",
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                汝州活动-提交试卷
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-22
    """
    args = request.loads() or request.QUERY.casts(status=int, data='json')
    user = request.user
    user_id = user.id
    unit = user.unit
    if not unit:
        return jsonp_fail(request, message=u'没有班级')
    grade_id = int(unit.get('grade_id', 0))
    if not grade_id:
        return jsonp_fail(request, message=u'没有年级')

    status = int(args.status)
    if status not in (1, 2):
        return jsonp_fail(request, u'wrong status: %s' % status)
    if not args.data:
        return jsonp_fail(request, u'no_data')
    if type(args.data) != list:
        args.data = json.loads(args.data)

    status = 1 if status == 1 else 0

    test = db.tbkt_active_slave.active_paper.select('id').get(user_id=user_id, active_id=ACTIVE_ID, paper_id=grade_id)
    if not test:
        return jsonp_fail(request, message=u'没有这个测试')

    rz_com.paper_submit(user_id, ACTIVE_ID, grade_id, status, args.data)
    return jsonp_ok(request)

@need_login
def paper_result(request):
    """
    @api {post} /huodong/rz/paper_result [汝州活动二期]试卷结果
    @apiGroup RzPaperActive
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "number": 2,        # 总习题数
            "wrong_number": 1   # 错误习题数
        },
        "response": "ok",
        "error": ""
    }
   @apiSuccessExample {json} 失败返回
      {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                汝州活动-试卷结果
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-22
    """
    user = request.user
    user_id = user.id
    unit = user.unit
    if not unit:
        return jsonp_fail(request, message=u'没有班级')
    grade_id = int(unit.get('grade_id', 0))
    if not grade_id:
        return jsonp_fail(request, message=u'没有年级')
    test = db.tbkt_active_slave.active_paper.select('id').get(user_id=user_id, active_id=ACTIVE_ID, paper_id=grade_id, status=1)
    if not test:
        return jsonp_fail(request, message=u'没有这个测试')
    data = com_yy.get_paper_result(user_id, ACTIVE_ID, grade_id)
    return jsonp_ok(request, data)

@need_login
def paper_result_detail(request):
    """
        @api {post} /huodong/rz/paper_result_detail [汝州活动二期]试卷结果详情
        @apiGroup RzPaperActive
        @apiParamExample {json} 请求示例
           {
            "type_id": 1    # 1 全部习题， 2 错题
           }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
           "data": {
                "sheet": [
                    {
                        "no": 2,
                        "qid": 3300,
                        "oid": 19321,
                        "result": 0,
                        "right_answer": "A",
                        "answer": "A",
                        "aid": 3500
                    }
                ],
                "question": [
                    {
                        "video_image": "",
                        "asks": [
                            {
                                "video_image": "",
                                "video_url": "",
                                "no": 2,
                                "user_answer": "A",
                                "user_option_id": null,
                                "listen_audio": "",
                                "options": [
                                    {
                                        "content": "No, she can't.",
                                        "option": "A",
                                        "image": "",
                                        "ask_id": 3500,
                                        "link_id": -1,
                                        "id": 10432,
                                        "is_right": 1
                                    },
                                    {
                                        "content": "Can he make a cake?",
                                        "option": "B",
                                        "image": "",
                                        "ask_id": 3500,
                                        "link_id": -1,
                                        "id": 10433,
                                        "is_right": 0
                                    },
                                    {
                                        "content": "No, he can't.",
                                        "option": "C",
                                        "image": "",
                                        "ask_id": 3500,
                                        "link_id": -1,
                                        "id": 10434,
                                        "is_right": 0
                                    },
                                    {
                                        "content": "Yes, he can.",
                                        "option": "D",
                                        "image": "",
                                        "ask_id": 3500,
                                        "link_id": -1,
                                        "id": 10435,
                                        "is_right": 0
                                    }
                                ],
                                "parse": {
                                    "content": "",
                                    "images": []
                                },
                                "answer": "A",
                                "listen_text": "",
                                "user_result": 0,
                                "duration": -1,
                                "user_option": null,
                                "right_option": {
                                    "content": "No, she can't.",
                                    "option": "A",
                                    "image": "",
                                    "ask_id": 3500,
                                    "link_id": -1,
                                    "id": 10432,
                                    "is_right": 1
                                },
                                "subject": {
                                    "content": "<img src=\"http://file.tbkt.cn/upload_media/knowledge/img/2016/09/29/20160929174848767831.png\" alt=\"\" /><br /><br />— Can she ride fast?<br />                  — ___<br />",
                                    "images": []
                                },
                                "qtype": 1,
                                "id": 3500,
                                "question_id": 3300
                            }
                        ],
                        "video_url": "",
                        "i": 0,
                        "type": 1,
                        "id": 3300,
                        "classify": 2,
                        "subject": {
                            "content": "根据图片选择正确的选项。( &nbsp; &nbsp; )",
                            "images": []
                        }
                    }
                ],
                "numbers": [
                    {
                        "qid": 3300,
                        "result": 0,
                        "aid": 3500
                    }
                ]
            },
            "response": "ok",
            "error": ""
        }
       @apiSuccessExample {json} 失败返回
          {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                汝州活动-试卷详细结果
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-22
    """
    args = request.loads() or request.QUERY.casts(type_id=int)
    type_id = int(args.type_id) or 0  # 1 全部， 2 错误
    user = request.user
    user_id = user.id
    unit = user.unit
    if not unit:
        return jsonp_fail(request, message=u'没有班级')
    grade_id = int(unit.get('grade_id', 0))
    if not grade_id:
        return jsonp_fail(request, message=u'没有年级')
    test = db.tbkt_active_slave.active_paper.select('id').get(user_id=user_id, active_id=ACTIVE_ID, paper_id=grade_id,
                                                              status=1)
    if not test:
        return jsonp_fail(request, message=u'没有这个测试')

    data = com_yy.get_paper_result_detail(user_id, ACTIVE_ID, grade_id, type_id)
    return jsonp_ok(request, data)