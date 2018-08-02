# coding:utf-8
from com.com_user import need_login
from libs.utils import ajax_json, Struct, db, ajax_try
from . import com_stu
from apps.sx_summer import common


@ajax_try({})
@need_login
def p_list(request):
    """
    @api {post} /huodong/sx_summer/s/list [暑假活动 学生]试卷列表
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
        grade_id:1
       }
    @apiSuccessExample {json} 成功返回
    {
      "message": "",
      "error": "",
      "data": {
        "苏教版": [
          {
            "status": "-1",-1：未作  0： 未完成，1：已完成
            "name": "二年级",
            "paper_name": "暑假天天练（一）",
            "v_name": "苏教版",
            "id": "231",
            "paper_id": "19828"
          },
          {
            "status": "0",
            "name": "二年级",
            "paper_name": "暑假天天练（二）",
            "v_name": "苏教版",
            "id": "231",
            "paper_id": "19829"
          }]
          "人教版":[...]
      },
      "response": "ok",
      "next": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    args = request.QUERY.casts(grade_id=int)
    if not args.grade_id:
        return ajax_json.jsonp_fail(request,error="no_grade_Id")
    paper = com_stu.get_paper_list(args.grade_id, user.old_user_id)
    return ajax_json.jsonp_ok(request,paper)


@ajax_try({})
@need_login
def p_paper(request):
    """
    @api {post} /huodong/sx_summer/s/paper [暑假活动 学生]试卷详情
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
        object_id:19858 #试卷id
       }
    @apiSuccessExample {json} 成功返回
    {
      "message": "",
      "error": "",
      "data": {
          "answer": [
          {
            "ask_list": [
              {
                "ask_id": "125401",
                "option": "C",
                "result": 1
              }
            ],
            "question_id": "67725"
          }...
        ],
        "status": 1,
        "qid": [
          "67725","67726",...
        ],
        "test_id": "109257",
        "name": "暑假天天练（一）",
        "questions": [
          {
            "asks": [
              {
                "knowledge": [
                  {
                    "ask_id": 93402,
                    "id": 3447,
                    "video_url": "http://file.tbkt.cn/upload_media/knowledge/video/2014/03/19/20140319112221404718.mp4",
                    "name": "100以内数的顺序"
                  }
                ],
                "video_url": "http://file.tbkt.cn/upload_media/knowledge/video/2014/03/19/20140319112219825730.mp4",
                "title": "1",
                "user_answer": "",
                "number": 1,
                "options": [
                  {
                    "option": "A",
                    "image": {},
                    "ask_id": 93402,
                    "is_right": 0,
                    "content": "41、42、43、44、45、46、47、48、49",
                    "id": 489626
                  },
                  {
                    "option": "B",
                    "image": {},
                    "ask_id": 93402,
                    "is_right": 0,
                    "content": "44",
                    "id": 489627
                  },
                  {
                    "option": "C",
                    "image": {},
                    "ask_id": 93402,
                    "is_right": 1,
                    "content": "40、41、42、43、44、45、46、47、48、49",
                    "id": 489628
                  },
                  {
                    "option": "D",
                    "image": {},
                    "ask_id": 93402,
                    "is_right": 0,
                    "content": "14、24、34、44、54、65、74、84、94",
                    "id": 489629
                  }
                ],
                "parse": [
                  {
                    "content": "十位上是4的两位数有（40、41、42、43、44、45、46、47、48、49）。",
                    "images": "",
                    "image": {}
                  }
                ],
                "user_result": "",
                "right_option": "C",
                "subject": {
                  "content": "十位上是4的两位数有。",
                  "images": "",
                  "image": {}
                },
                "id": 93402,
                "question_id": 67725
              }
            ],
            "video_url": "",
            "number": 1,
            "display": 1,
            "type": 1,
            "id": 67725,
            "subject": {
              "content": "",
              "image": {
                "url": ""
              }
            }
          },
          {...}
        ]
      },
      "response": "ok",
      "next": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    args = request.QUERY.casts(object_id=int)
    if not args.object_id:
        return ajax_json.jsonp_fail(request,error='no_object_id')
    test = com_stu.get_or_creat_test(user.old_user_id, args.object_id)
    paper = com_stu.get_paper_detail(args.object_id)
    qid = list(common.dedupe([i.question_id for i in paper]))
    questions, answer = com_stu.get_test_question(user.old_user_id, qid, args.object_id)
    data = Struct()
    data.qid = qid
    data.questions = questions
    data.answer = answer
    data.status = test.status
    data.name = test.title
    data.test_id = test.id
    return ajax_json.jsonp_ok(request,data)


@ajax_try({})
@need_login
def p_submit(request):
    """
    @api {post} /huodong/sx_summer/s/submit [暑假活动 学生]提交
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
        {
        "type":1,   1卷子，3个性化
        "object_id":"19858",    paper_id /个性化测试id
        "status":1,1 完成 0 未完成
        "data":[{"ask_list":[{"ask_id":61745,"option":"C","result":1}],"question_id":45949}...]
        }
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": {"test_id": "109257"}, "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u"学生用户才能使用")
    args = request.QUERY.casts(object_id=int, status=int, data='json', type=int)
    status = args.status
    data = args.data or []
    if args.type == 3:
        result = com_stu.test_special(user.id, args.object_id, status, data)
    else:
        result = com_stu.test_submit(user, args.object_id, status, data, args.type)

    return ajax_json.jsonp_ok(request,result)


@ajax_try({})
@need_login
def test_result(request):
    """
    @api {post} /huodong/sx_summer/s/result [暑假活动 学生]结果页
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
        {test_id:109257}
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {
            "knowledge_list": [
              {
                "knowledge_id": "3085",
                "name": "十几减8"
              },
              {
                "knowledge_id": "3080",
                "name": "十几减9"
              },
              {
                "knowledge_id": "3088",
                "name": "十几减5、4、3、2"
              },
              {
                "knowledge_id": "3447",
                "name": "100以内数的顺序"
              }
            ],
            "all_qid": [
              "67725",
              "67726",
              "11303",
              "11997"
            ],
            "knowledge_count": 4,
            "wrong_qid": [
              "67726",
              "11303"
            ],
            "test_name": "暑假天天练（一）",
            "test_id": 109257
          },
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(test_id=int)
    test_id = args.test_id
    data = com_stu.test_evaluate(test_id)
    return ajax_json.jsonp_ok(request,data)


@need_login
@ajax_try({})
def get_question(request):
    """
    @api {post} /huodong/sx_summer/s/question [暑假活动 学生]获取试题
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
        {
        "object_id": 8459 ,试卷id
         "qid":49484
         }
    @apiSuccessExample {json} 成功返回
    {
            "message": "",
            "next": "",
            "data": [
                        {
                            "category": 1,
                            "asks": [
                                {
                                    "title": "1",
                                    "user_answer": "",
                                    "number": 1,
                                    "id": 22260,
                                    "right_option": "C",
                                    "question_id": 49484,
                                    "options": [
                                        {
                                            "content": "原计划每天完成$130$套服装",
                                            "option": "A",
                                            "image": {},
                                            "ask_id": 22260,
                                            "id": 317695,
                                            "is_right": 0
                                        },
                                        {
                                            "content": "原计划每天完成$135$套服装",
                                            "option": "B",
                                            "image": {},
                                            "ask_id": 22260,
                                            "id": 317696,
                                            "is_right": 0
                                        },
                                        {
                                            "content": "原计划每天完成$125$套服装",
                                            "option": "C",
                                            "image": {},
                                            "ask_id": 22260,
                                            "id": 317697,
                                            "is_right": 1
                                        },
                                        {
                                            "content": "原计划每天完成$140$套服装",
                                            "option": "D",
                                            "image": {},
                                            "ask_id": 22260,
                                            "id": 317698,
                                            "is_right": 0
                                    }
                                ],
                                "subject": {
                                    "content": "某服装制造厂要在开学前赶制$3000$套校服",
                                    "images": "",
                                    "image": {}
                                }
                            }
                        ],
                        "video_url": "",
                        "number": 1,
                        "id": 49484,
                        "display": 1,
                        "structure": 3,
                        "subject": {}
                    }
                ],
                "response": "ok",
                "error": ""
        }
    """
    user = request.user
    args = request.QUERY.casts(qid=str, object_id=int)
    qids = args.qid or ''
    qids = [int(s) for s in qids.split(',') if s]
    object_id = args.object_id
    data, __ = com_stu.get_test_question(user.old_user_id, qids, object_id)
    return ajax_json.jsonp_ok(request,data)
