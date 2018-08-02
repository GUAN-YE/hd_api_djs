# coding:utf-8
from __future__ import division
import json
from . import common
from com.com_user import need_teacher
from libs.utils import db, ajax_try, ajax_json


@ajax_try([])
@need_teacher
def status(request):
    """
    @api {post} /huodong/sx_questionnaire/status [问卷调查] 提交
    @apiGroup  sx_questionnaire
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": {status:1},  # 1:已做 , 0:未作
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "请勿重复提交", "data": "", "response": "fail", "next": ""}

    """
    user_id = request.user_id
    exist = db.tbkt_web.active_questionnaire.get(user_id=user_id)
    user_status = 0
    if exist:
        user_status = 1
    return ajax_json.jsonp_ok(request, {'status': user_status})


@ajax_try([])
@need_teacher
def submit(request):
    """
    @api {post} /huodong/sx_questionnaire/submit [问卷调查] 提交
    @apiGroup  sx_questionnaire
    @apiParamExample {json} 请求示例
       {data:[{qid:1,option:'A,C',content:'叮叮叮，当当当'},{qid:2,option:''A,B,C,content:''}]}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": {},
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "请勿重复提交", "data": "", "response": "fail", "next": ""}

    """
    args = request.QUERY.casts(data='json')
    data = args.data
    _result, err = common.submit(request.user, data)
    if result:
        return ajax_json.jsonp_ok(request, {'result': _result})
    return ajax_json.jsonp_fail(request, error=err)


@ajax_try([])
@need_teacher
def result(request):
    """
    @api {post} /huodong/sx_questionnaire/result [问卷调查] 结果
    @apiGroup  sx_questionnaire
    @apiParamExample {json} 请求示例
        {}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data":[{qid:1,option:'A,C',content:'叮叮叮，当当当'},{qid:2,option:''A,B,C,content:''}]
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "请勿重复提交", "data": "", "response": "fail", "next": ""}

    """
    user = request.user
    data = common.user_detail(user.id)
    return ajax_json.jsonp_ok(request, {'data': data})


def detail(request):
    from excel_response3 import ExcelResponse
    _detail = db.tbkt_web.active_questionnaire.filter(user_id__gt=0)[:]
    data = [
        [u'题目', u'选项', u'手动输入'],
    ]

    for o in _detail:
        data.append(['', '', ''])
        text = json.loads(o.text)
        for d in text:
            qid = d['qid']
            option = d['option']
            content = d['content']
            data.append([qid, option, content])
    return ExcelResponse(data, 'detail')


def detail_all(request):
    from excel_response3 import ExcelResponse
    num = db.tbkt_web.active_questionnaire.filter(user_id__gt=0).count()
    _detail = db.tbkt_web.active_questionnaire_detail.filter(id__gt=0)[:]
    _detail = sorted(_detail, key=lambda x: (x['qid'], x['option']))

    data = [
        [u'题目', u'选项', u'有效人数', u'比例'],
    ]
    for d in _detail:
        qid = u'第%s题' % d['qid']
        option = d['option']
        n = d['num']
        rate = str('%.2f' % (n / num * 100)) + '%'
        data.append([qid, option, n, rate])
    return ExcelResponse(data, 'statistics')
