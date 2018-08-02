# coding:utf-8
import json

from apps.full_class import wrong
from apps.full_class.common import get_weekend_stamp
from com.com_cache import cache
from libs.utils import ajax, ajax_json, ajax_try, Struct
from common import need_login
from . import common, knowledge


@ajax_try()
@need_login
def user_index(request):
    """
    @api /huodong/full/class/user/list [满分课堂] 首页
    @apiGroup full_class
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "know_status": -1,    # 知识训练场
            "month_status": -1,   # 月竞技
            "pk_status": -1,      # 每周竞技
            "wrong_status": -1,   # 挑战错题
            "is_open": 0,         # 是否在开放时间
            "open_time": "04月21日 09点",   # 开放时间点
            "once_week": [                 # 往期课程  
                {
                    "name": "第一周",     # 名字
                    "id": 1              # 课程id
                },
                {
                    "name": "第二周",
                    "id": 2
                }
            ], 
            "id": 3,               # 本周课程id
            "name": "第三周"        # 本周课程名字
        },
        "response": "ok",
        "error": ""
    }
    """
    user_id = request.user_id
    data = common.user_index(user_id)
    return ajax_json.jsonp_ok(request, data)


@ajax_try()
@need_login
def get_knowledge(request):
    """
    @api /huodong/full/class/knowledge/info [满分课堂] 知识点视频
    @apiGroup full_class
    @apiParamExample {json} 请求示例
    {
        "week_id": 1
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "info": [
                {
                    "video_image": "http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150258585349.png",
                    "status": 0,
                    "name": "认识条形图",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150258577942.mp4",
                    "content": "",
                    "id": 6177
                },
                {
                    "video_image": "http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150209277403.png",
                    "status": -1,
                    "name": "绘制条形统计图的方法1",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150209267350.mp4",
                    "content": "",
                    "id": 6178
                },
                {
                    "video_image": "http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150304452684.png",
                    "status": 1,
                    "name": "绘制条形统计图的方法2",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150304444284.mp4",
                    "content": "",
                    "id": 6179
                },
                {
                    "video_image": "http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150349564830.png",
                    "status": 0,
                    "name": "误区警示",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150349563580.mp4",
                    "content": "",
                    "id": 6180
                }
            ],
            "q_num": 4
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message="当前周没有视频")
    user_id = request.user_id
    data = knowledge.get_knowledge_list(user_id, week_id)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def video_submit(request):
    """
    @api /huodong/full/class/video/submit [满分课堂] 知识点视频提交
    @apiGroup full_class
    @apiParamExample {json} 请求示例
    { 
        "week_id": 1,
        "knowledge_id":6177
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data":
        "response": "ok",
        "error": ""
    }
    """
    # 提交观看视频的记录
    user_id = request.user_id
    user_city = request.user.city
    args = request.QUERY.casts(knowlodge_id=int, week_id=int)
    week_id = args.week_id
    knowledge_id = args.knowlodge_id
    if not week_id and knowledge_id:
        return ajax.jsonp_fail(request, message=u"缺少参数")
    data = knowledge.video_submit(user_id, knowledge_id, week_id, user_city)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def get_question(request):
    """
    @api /huodong/full/class/knowledge/question [满分课堂] 知识点题目
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id": 1}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "info": [
                {
                    "knowledge_id": 5036,
                    "id": 2,
                    "content": "运算中既有加法，又有乘法，应先算<span class=\"xheBtnWaKong\">乘法</span>。",
                    "display_type": 1,
                    "q_index": 1,
                    "answer": {
                        "content": "乘法",
                        "is_correct": 1,
                        "option": "A"
                    },
                    "options": [
                        {
                            "content": "乘法",
                            "is_correct": 1,
                            "option": "A"
                        },
                        {
                            "content": "加法",
                            "is_correct": 0,
                            "option": "B"
                        },
                        {
                            "content": "前面的",
                            "is_correct": 0,
                            "option": "C"
                        }
                    ]
                },
                {
                    "knowledge_id": 8007,
                    "id": 1394,
                    "content": "数一数：<img src=\"http://file.tbkt.cn/upload_media/knowledge/img/2016/11/24/2016112416060885708.png\" alt=\"\" /><br />一共有<span class=\"xheBtnWaKong\">（80）</span>根小棒。",
                    "display_type": 2,
                    "q_index": 2,
                    "answer": [
                        "80"
                    ],
                    "options": ""
                }
            ],
            "q_num": 2
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message="当前周没有题目")
    user_id = request.user_id
    data = knowledge.knowledge_qid_info(user_id, week_id)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def test_submit(request):
    """
    @api /huodong/full/class/knowledge/submit [满分课堂] 知识点题目提交
    @apiGroup full_class
    @apiParamExample {json} 请求示例
    {
        "week_id":1,
        "info":[
                    {"result": "A", "kid": 5036, "qid": 2, "is_right": 1,"display_type":1},
                    {"result": "1", "kid": 8007, "qid": 1394, "is_right": 0,"display_type":2}
               ]
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(week_id=int, info='json')
    week_id = args.week_id
    info = args.info
    if not week_id:
        return ajax.jsonp_fail(request, message="缺少参数")
    try:
        keys = ["result", "kid", "qid", "is_right", "display_type"]
        for i in info:
            for k in i.keys():
                if k not in keys:
                    return ajax.jsonp_fail(request, message="参数异常")
    except Exception as e:
        print e
        return ajax.jsonp_fail(request, message="错误参数")

    user_id = request.user_id
    user_city = request.user.city
    data = knowledge.test_submit(user_id, week_id, info, user_city)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def pk_submit(request):
    """
    @api /huodong/full/class/pk/submit [满分课堂] 周竞技提交
    @apiGroup full_class
    @apiParamExample {json} 请求示例
     {
        "score":20,
        "use_time":123,
        "status":0,
        "week_id":1,
        "info":[
                {"qid":8145 , "aid": 8178,  "result": 1, "score": 10,"option":"A"},
                {"qid":8145 , "aid": 8178,  "result": 1, "score": 10,"option":"B"}
        ]
    }
    
    * score 答题积分
    * use_time 测试用时
    * week_id 课程id
    * info 提交数据
    * status = 0 中途退出 1 完成提交 或者答错两题
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "max_score": 100,
            "score": 0,
            "num": 1,
            "rank": [
                {
                    "index": 0,
                    "user_id": 608898,
                    "border_url": "http://file.tbkt.cn/upload_media/border/2017/12/19/20171219210857562900.png",
                    "rank": 1,
                    "real_name": "小小学生",
                    "score": 100,
                    "portrait": "http://file.tbkt.cn/upload_media/portrait/2017/12/18/2017121817284732843.png",
                    "is_self": 1
                },
                {
                    "index": 1,
                    "user_id": 520403,
                    "border_url": "http://file.tbkt.cn/upload_media/border/2017/12/19/20171219165203836034.png",
                    "rank": 2,
                    "real_name": "无法识别",
                    "score": 30,
                    "portrait": "http://file.tbkt.cn/upload_media/portrait/2017/12/14/20171214140147742602.png",
                    "is_self": 0
                }
            ]
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(week_id=int, info='json', score=int)
    week_id = args.week_id
    info = args.info or []
    score = args.score
    user_id = request.user_id
    user_city = request.user.city
    if not week_id:
        return ajax.jsonp_fail(request, message=u"缺少参数")
    try:
        keys = ["qid", "aid", "result", "score", "option"]
        for i in info:
            for k in i.keys():
                if k not in keys:
                    return ajax.jsonp_fail(request, message="参数异常")
    except Exception as e:
        print e
        return ajax.jsonp_fail(request, message="错误参数")
    data = common.pk_submit(user_id, week_id, info, score, user_city)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def test_result(request):
    """
    @api /huodong/full/class/knowledge/result [满分课堂] 知识训练场结果页
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id": 课程id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "info": [
                {
                    "knowledge_id": 5036,
                    "name": "探究乘加混合运算的计算方法",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/08/18/20140818140249159000.mp4",
                    "user_answer": "B",
                    "id": 2,
                    "content": "运算中既有加法，又有乘法，应先算<span class=\"xheBtnWaKong\">乘法</span>。",
                    "display_type": 1,
                    "q_index": 1,
                    "answer": {
                        "content": "乘法",
                        "is_correct": 1,
                        "option": "A"
                    },
                    "options": [
                        {
                            "content": "乘法",
                            "is_correct": 1,
                            "option": "A"
                        },
                        {
                            "content": "加法",
                            "is_correct": 0,
                            "option": "B"
                        },
                        {
                            "content": "前面的",
                            "is_correct": 0,
                            "option": "C"
                        }
                    ]
                },
                {
                    "knowledge_id": 8007,
                    "name": "学会十个十个数100以内的数",
                    "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2015/01/29/20150129084526423753.mp4",
                    "user_answer": [
                        "80"
                    ],
                    "id": 1394,
                    "content": "数一数：<img src=\"http://file.tbkt.cn/upload_media/knowledge/img/2016/11/24/2016112416060885708.png\" alt=\"\" /><br />一共有<span class=\"xheBtnWaKong\">（80）</span>根小棒。",
                    "display_type": 2,
                    "q_index": 2,
                    "answer": [
                        "80"
                    ],
                    "options": ""
                }
            ],
            "wrong_name": [
                "探究乘加混合运算的计算方法"
            ]
        },
        "response": "ok",
        "error": ""
    }
    """
    user_id = request.user_id
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message=u"缺少参数")
    data = knowledge.test_result(user_id, week_id)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def get_pk_question(request):
    """
    @api /huodong/full/class/pk/question [满分课堂] 周竞技题目
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id": 课程id}
    @apiSuccessExample {json} 成功返回
    {
    "message": "",
    "next": "",
    "data": {
        "num": 4,
        "out": [
                {
                    "q_subject": {
                        "type": 10,
                        "id": 8145,
                        "video_url": "http://file.tbkt.cn/upload_media/knowledge/video/2015/10/21/20151021151242119295.mp4",
                        "subject": {
                            "content": "在<img src=\"http://file.xueceping.cn/upload_media/math_img/round.png\" alt=\"\" /><span class=\"round\"></span>里填上&quot;&gt;&quot;、&quot;&lt;&quot;、&quot;=&quot;。",
                            "images": "",
                            "image": {}
                        }
                    },
                    "subject": {
                        "images": "",
                        "content": "5−3<img src=\"http://file.xueceping.cn/upload_media/math_img/round_big.png\" alt=\"\" /><span class=\"round\"></span>4 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;3−1<img src=\"http://file.xueceping.cn/upload_media/math_img/round_big.png\" alt=\"\" /><span class=\"round\"></span>4",
                        "image": {}
                    },
                    "id": 8178,
                    "option": [
                        {
                            "content": "5−3&lt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1&lt;4",
                            "option": "A",
                            "image": {},
                            "ask_id": 8178,
                            "is_right": 1
                        },
                        {
                            "content": "5−3&gt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1&gt;4",
                            "option": "B",
                            "image": {},
                            "ask_id": 8178,
                            "is_right": 0
                        },
                        {
                            "content": "5−3&lt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1=4",
                            "option": "C",
                            "image": {},
                            "ask_id": 8178,
                            "is_right": 0
                        }
                    ],
                    "question_id": 8145
                }
            ]
    },
    "response": "ok",
    "error": ""
    """
    args = request.QUERY.casts(week_id=int)
    user_id = request.user_id
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message=u"缺少参数")
    data = common.get_pk_question(user_id, week_id)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def pk_rank(request):
    """
    @api /huodong/full/class/pk/rank [满分课堂] 排行榜
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id":1}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data":  {
            "my_rank": {
                "unit_name": "105班",
                "score": 58,
                "user_id": 7646135,
                "border_url": "",
                "portrait": "http://file.tbkt.cn/upload_media/portrait/2017/12/29/20171229205803595199.png",
                "user_name": "人生如戏戏",
                "school_name": "郑州市第七十中学",
                "rank": 1
            },
            "user_rank": [
                {
                    "unit_name": "105班",
                    "user_id": 7646135,
                    "border_url": "",
                    "school_name": "郑州市第七十中学",
                    "rank": 1,
                    "real_name": "人生如戏戏",
                    "score": 58,
                    "portrait": "http://file.tbkt.cn/upload_media/portrait/2017/12/29/20171229205803595199.png"
                },{}
            ]
        },
        "response": "ok",
        "error": ""
    }
    
    * my_rank 我的排名
    * user_rank 用户排名
    """
    args = request.QUERY.casts(week_id=int)
    user_id = request.user_id
    user_city = request.user.city
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message=u"缺少参数")
    data = common.pk_week_rank(user_id, week_id, user_city)
    return ajax.jsonp_ok(request, data)


@ajax_try()
@need_login
def pop_up(request):
    """
    @api /huodong/full/class/pop_up [满分课堂] 每周模块弹窗
    @apiGroup full_class
    @apiParamExample {json} 请求示例
    {
        "pop_type":home
    }
    * 首页  home
    * 信息确认页  info
    * 知识训练场首页  training
    * 挑战错题首页  wrong
    * 每周竞技首页   game
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "status":1,
            "border_id":91,
            "border_url": "http://file.tbkt.cn/upload_media/border/2018/04/13/20180413103334255
        },
        "response": "ok",
        "error": ""
    }
     
    * pop_up = home 时会判断学段，以及是否获取竞技边框
    * status = 1 本周未弹过、可以进行展示
    * status = 0 本周已谈过
    """
    user = request.user
    args = request.QUERY.casts(pop_type=str)
    pop_type = args.pop_type
    user_city = request.user.city
    if not pop_type:
        return ajax.jsonp_ok(request, message="缺少模块类型")
    data = common.pop_up(user, pop_type, user_city)
    return ajax.jsonp_ok(request, data)


@ajax_try()
def r_book_list(request):
    """
    @api /huodong/full/class/book/list [满分课堂] 设置教材列表
    @apiGroup full_class
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "name": "人教版一年级下册",
                "id": 1
            },
            {
                "name": "人教版二年级下册",
                "id": 2
            },
            {
                "name": "人教版三年级下册",
                "id": 3
            },
            {
                "name": "人教版四年级下册",
                "id": 4
            },
            {
                "name": "人教版五年级下册",
                "id": 5
            },
            {
                "name": "人教版六年级下册",
                "id": 6
            }
        ],
        "response": "ok",
        "error": ""
    }
    * 满分课堂 暂未开启其他教材
    * 所有本次id 与 年级id一致
    """
    return ajax.jsonp_ok(request, common.get_list())


@ajax_try()
@need_login
def r_set_book(request):
    """
    @api /huodong/full/class/book/set [满分课堂] 设置用户教材
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"id":1}
    * 对应book_list接口 id
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """

    args = request.QUERY.casts(id=int)
    grade_id = args.id
    if not grade_id:
        return ajax.jsonp_fail(request, message="缺少id")
    user_id = request.user_id
    common.set_user_book(user_id, grade_id)
    return ajax.jsonp_ok(request)


@ajax_try()
@need_login
def r_wrong_question(request):
    """
    @api /huodong/full/class/wrong/question [满分课堂] 高频错题
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id": 课程id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "count": 2537,
                "ratio": "52%",
                "video_url": "",
                "asks": [
                    {
                        "knowledge": [
                            {
                                "ask_id": 16965,
                                "id": 3531,
                                "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048598754.mp4",
                                "name": "用连除或乘除混合运算解决实际问题"
                            },
                            {
                                "ask_id": 16965,
                                "id": 3530,
                                "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048498295.mp4",
                                "name": "用连乘解决实际问题"
                            }
                        ],
                        "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173047716451.mp4",
                        "title": "1",
                        "user_answer": "",
                        "number": 1,
                        "id": 16965,
                        "parse": [
                            {
                                "images": "",
                                "content": "168÷4÷7=6（吨）<br />6×5×10=300（吨）<br />答：5辆汽车10次可以运货300吨。",
                                "image": {}
                            }
                        ],
                        "user_result": "",
                        "right_option": "C",
                        "question_id": 12304,
                        "options": [
                            {
                                "option": "A",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "30",
                                "id": 997267
                            },
                            {
                                "option": "B",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "60",
                                "id": 997268
                            },
                            {
                                "option": "C",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 1,
                                "content": "300",
                                "id": 997269
                            },
                            {
                                "option": "D",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "400",
                                "id": 997270
                            }
                        ],
                        "subject": {
                            "images": "",
                            "content": "4辆汽车7次可以运货168吨，照这样计算，5辆汽车10次可以运货多少吨？",
                            "image": {}
                        }
                    }
                ],
                "id": 12304,
                "subject": {
                    "content": "",
                    "images": "",
                    "image": {}
                },
                "type": 11,
                "number": 1,
                "display": 1
            }
        ],
        "response": "ok",
        "error": ""
    }
    "response": "ok",
    "error": ""
    """
    user_id = request.user_id
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message="找不到本周课程！")
    grade_id = common.user_grade(user_id)
    question = wrong.get_wrong_question(user_id, week_id, grade_id)
    return ajax.jsonp_ok(request, question)


@ajax_try()
@need_login
def r_wrong_submit(request):
    """
    @api /huodong/full/class/wrong/question/submit [满分课堂] 高频错题提交
    @apiGroup full_class
    @apiParamExample {json} 请求示例
    {
        "week_id":1, 
        "data":[{"qid": 4976, "aid": 4976, "result": 0, "option": "B"}]
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "test_id": 176
        },
        "response": "ok",
        "error": ""
    }
    """
    user_id = request.user_id
    user_city = request.user.city
    args = request.QUERY.casts(week_id=int, data='json')
    week_id = args.week_id
    data = args.data

    if not week_id:
        return ajax.jsonp_fail(request, message="缺少参数")
    try:
        keys = ["result", "aid", "qid", "option"]
        for i in data:
            for k in i.keys():
                if k not in keys:
                    return ajax.jsonp_fail(request, message="参数异常")
    except Exception as e:
        print e
        return ajax.jsonp_fail(request, message="错误参数")
    grade_id = common.user_grade(user_id)
    test_id = wrong.wrong_submit(user_id, week_id, grade_id, data, user_city)
    return ajax.jsonp_ok(request, {"test_id": test_id})


@ajax_try()
@need_login
def r_wrong_result(request):
    """
    @api /huodong/full/class/wrong/question/result [满分课堂] 高频错题结果
    @apiGroup full_class
    @apiParamExample {json} 请求示例
        {"week_id": 课程id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "video_url": "",
                "asks": [
                    {
                        "knowledge": [
                            {
                                "ask_id": 16965,
                                "id": 3531,
                                "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048598754.mp4",
                                "name": "用连除或乘除混合运算解决实际问题"
                            },
                            {
                                "ask_id": 16965,
                                "id": 3530,
                                "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048498295.mp4",
                                "name": "用连乘解决实际问题"
                            }
                        ],
                        "video_url": "http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173047716451.mp4",
                        "title": "3",
                        "user_answer": "B",
                        "number": 1,
                        "options": [
                            {
                                "option": "A",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "30",
                                "id": 997267
                            },
                            {
                                "option": "B",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "60",
                                "id": 997268
                            },
                            {
                                "option": "C",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 1,
                                "content": "300",
                                "id": 997269
                            },
                            {
                                "option": "D",
                                "image": {},
                                "ask_id": 16965,
                                "is_right": 0,
                                "content": "400",
                                "id": 997270
                            }
                        ],
                        "parse": [
                            {
                                "images": "",
                                "content": "168÷4÷7=6（吨）<br />6×5×10=300（吨）<br />答：5辆汽车10次可以运货300吨。",
                                "image": {}
                            }
                        ],
                        "user_result": 0,
                        "right_option": "C",
                        "subject": {
                            "images": "",
                            "content": "4辆汽车7次可以运货168吨，照这样计算，5辆汽车10次可以运货多少吨？",
                            "image": {}
                        },
                        "id": 16965,
                        "question_id": 12304
                    }
                ],
                "id": 12304,
                "subject": {
                    "content": "",
                    "images": "",
                    "image": {}
                },
                "type": 11,
                "number": 3,
                "display": 1
            }
                ],
                "id": 12319,
                "subject": {
                    "content": "填一填。",
                    "images": "",
                    "image": {}
                },
                "type": 1,
                "number": 4,
                "display": 1
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user_id = request.user_id
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message="找不到提交信息！")
    grade_id = common.user_grade(user_id)
    question = wrong.wrong_result(user_id, week_id, grade_id)
    return ajax.jsonp_ok(request, question)


@ajax_try()
@need_login
def r_user_info(request):
    """
    @api /huodong/full/class/user [满分课堂] 用户教材
    @apiGroup full_class
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "school_name": "郑州市第七十中学105班",
            "book_name": "人教版一年级下册"
        },
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    out = Struct()
    out.book_name = common.get_user_book_name(user)
    unit = user.unit
    out.school_name = "%s%s" % (unit.school_name, unit.name) if unit else "--"
    return ajax.jsonp_ok(request, out)


def r_del_cache(request):
    """
    删除对应用户缓存
    :param request: 
    :return: 
    """
    user_id = request.user_id
    args = request.QUERY.casts(pop_type=str)
    pop_type = args.pop_type.split(",")
    for i in pop_type:
        key = (user_id, i, get_weekend_stamp())
        cache.hd_full_pop_up.delete(key)
    return ajax.jsonp_ok(request)


def r_history(request):
    """
    往期回顾接口
    :param request: 
    :return: 
    """
    user_id = request.user_id
    args = request.QUERY.casts(week_id=int)
    week_id = args.week_id
    if not week_id:
        return ajax.jsonp_fail(request, message="缺少参数！")
    data = common.wrong_status(user_id, week_id)
    return ajax.jsonp_ok(request, {"status": data})
