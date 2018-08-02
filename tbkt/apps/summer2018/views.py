# coding=utf-8
from apps.summer2018 import common
from libs.utils import ajax


def r_math2_paper(request):
    """
    初中试卷扫一扫
    :param request: 
    :return: 
    """
    args = request.QUERY.casts(object_id=int, type=int, paper_id=int)
    object_id = args.object_id
    typ = args.type
    paper_id = args.paper_id
    if not object_id or not typ or not paper_id:
        return ajax.jsonp_fail(request, message="缺少参数")
    data = common.get_question_by_type(object_id, paper_id, typ)
    return ajax.jsonp_ok(request, data)


def r_math2_paper_explain(request):
    """
    初中试卷扫一扫
    :param request: 
    :return: 
    """
    args = request.QUERY.casts(ask_id=int, paper_id=int)
    ask_id = args.ask_id
    paper_id = args.paper_id
    if not ask_id or not paper_id:
        return ajax.jsonp_fail(request, message="缺少参数")
    data = common.get_ask_explain(ask_id, paper_id)
    return ajax.jsonp_ok(request, data)
