#coding=utf-8



import time
from libs.utils.ajax import jsonp_ok, jsonp_fail
from . import common
from com.com_user import need_login

@need_login
def set_recording(request):
    """
    @api {post} /huodong/reading/set_recording   [学生端]上传录音
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "video_url": "http://tbktfile.jxrrt.cn/yuwen/201709StuVideos/b99255c5.mp3"   # 音频地址
        "tid": 1      #文章id
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {

        },
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(video_url=str, tid=int)
    video_url = args.video_url
    tid = args.tid
    if not (video_url.startswith('http') and video_url.endswith('.mp3')):
        return jsonp_fail(request, message="参数错误")
    if not video_url or not tid:
        return jsonp_fail(request, message="缺少参数")
    data = common.set_video(user, video_url, tid)
    if not data:
        return jsonp_fail(request, message="添加失败")
    return jsonp_ok(request, data)


@need_login
def get_recording(request):
    """
    @api {get} /huodong/reading/get_recording   [学生端]获取用户的录音（最多五个）
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "tid": 6   # 文章id
    }
    @apiSuccessExample {json} 成功返回
    {
        "message":
        "next": "",
         "data": {
                "status": 0, 1/0,  等于1 已经上传过录音 等于0  则未上传过录音
                "video_detail": [
                    {
                        "recording_length": 5,
                        "user_name": "refresh",
                        "user_id": 7646093,
                        "id": 2,
                        "recording_path": "http://tbktfile.jxrrt.cn/yuwen/201709StuVideos/b99255c5-fc6f-4f60-8b98-fb90f18e6e06.mp3"
                    },{},{},{},
                ]
         },
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(tid=int)
    tid = args.tid
    if not tid:
        return jsonp_fail(request, message="缺少参数")
    data = common.get_video(user, tid)
    return jsonp_ok(request, data)


@need_login
def set_message(request):
    """
    @api {post} /huodong/reading/set_message   [学生端]发布留言
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "tid": 6   # 文章id
        "content" : "荣誉，可是要付出代价的"
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
                ]
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(tid=int, content=str)
    tid = args.tid
    content = args.content
    if not tid or not content:
        return jsonp_fail(request, message="缺少参数")
    data = common.set_message(user, tid, content)
    return jsonp_ok(request, data)


@need_login
def get_message(request):
    """
    @api {get} /huodong/reading/get_message   [学生端]获取留言
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "tid": 6   # 文章id
        "page" : 1   #页数 每页20条  ! 不能不传 从1开始
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
                 {“user_name”:””, “add_time”:””, “content”:””, "user_border":"", "user_portrait":"'},
                  {“user_name”:””, “add_time”:””, “content”:””, "user_border":"", "user_portrait":"'},
                  {“user_name”:””, “add_time”:””, “content”:””, "user_border":"", "user_portrait":"'},
                  {“user_name”:””, “add_time”:””, “content”:””, "user_border":"", "user_portrait":"'},
                ]
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(tid=int, page=int)
    tid = args.tid
    page = args.page
    if not tid or not page:
        return jsonp_fail(request, message="缺少参数")
    data = common.get_message(user, tid, page)
    return jsonp_ok(request, data)


@need_login
def get_join_status(request):
    """
    @api {get} /huodong/reading/get_join_status   [教师端]是否能参与阅读训练活动
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "status" : 1/0  #1可以参与 0不能参与
        }，
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    data = common.get_join_status(user)
    return jsonp_ok(request, data)


@need_login
def index(request):
    """
    @api {get} /huodong/reading/index   [教师端]活动首页
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            “coins”: 10000,
            “complete_students”: [
                                 {“unit_name”:””, “complete_num”:100},
                                 {“unit_name”:””, “complete_num”:100},
            ]
            “complete_status”: 1 / 0

        }，
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    data = common.index(user)
    return jsonp_ok(request, data)


@need_login
def get_paper(request):
    """
    @api {get} /huodong/reading/get_paper   [教师端]获取当前年级下的试卷
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        “grade”: 2
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
                    {“title”:””, “question_num”:1, “status”: 1/0},
                    {“title”:””, “question_num”:1, “status”: 1/0},
                    {“title”:””, “question_num”:1, “status”: 1/0},
                ]
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(grade=int)
    user = request.user
    grade = args.grade
    if not grade:
        return jsonp_fail(request, message="缺少参数")
    data = common.get_paper(grade, user)
    return jsonp_ok(request, data)


@need_login
def view_paper(request):
    """
    @api {get} /huodong/reading/view_paper   [教师端]预览试卷
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "tid“ : 100
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
                "title": "aaaaa",                     # 文章标题
                "article_content": "aaa",    #文章内容
                }

        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(tid=int)
    tid = args.tid
    if not tid:
        return jsonp_fail(request, message="缺少参数")
    data = common.view_paper(tid)
    return jsonp_ok(request, data)


@need_login
def send_sms(request):
    """
    @api {post} /huodong/reading/send_sms   [教师端]发送试卷短信
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {
        "unit_id": "555428,515192", # 班级ID
        "title": "静夜思，锄禾", # 逗号分隔的title数组
        "begin_time": "2017-01-05 09:10:00", # (可选)定时作业时间
        "sendpwd": 1/0,   # 是否下发帐号密码
        "sendscope": 1/0,  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信
        "object_id":"试卷ID，可多个， 逗号分隔"
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data":""，
        "response": "ok",
        "error": ""
    }
     @apiSuccessExample {json} 失败返回
    {
        "message": ,
        "next": "",
        "data": "请设置作业的完成时间",
        "response": "fail",
        "error": ""
    }
    """
    args = request.QUERY.casts(type=int, unit_id=str, title=unicode, begin_time='timestamp', sendpwd=int, sendscope=int,
                               object_id=str)
    unit_id = args.unit_id or ''
    unit_ids = [int(s) for s in unit_id.split(',') if s]
    title = args.title or u''
    now = int(time.time())
    begin_time = args.begin_time or now
    sendpwd = args.sendpwd or 0
    sendscope = args.sendscope or 0
    object_id = args.object_id or '' # 很多很多卷子
    object_ids = [int(s) for s in object_id.split(',') if s]
    title_array = [s for s in title.split(u'，')]
    if not unit_id:
        return jsonp_fail(request, message='请选择您要发布的班级')

    if begin_time < now:
        return jsonp_fail(request, message='定时发布时间不得小于当前系统时间')

    user = request.user

    # title = title or "%s作业" % begin_time.strftime("%m月%d日")

    # 1已发 2待发
    status = 1 if begin_time <= now else 2

    data = common.send_sms(request, user, status, unit_ids, title, begin_time, sendpwd, sendscope, object_ids, title_array)
    return jsonp_ok(request, data)


@need_login
def get_coin(request):
    """
    @api {post} /huodong/reading/get_coin   [教师端]领取金币
    @apiGroup yw_reading
    @apiParamExample {json} 请求示例
    {

       }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
                "num" : 0/20/40  # 20领取的金币数量 0 领取失败
                }

        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    data = common.get_coin(user)
    if data == u'金币不足':
        return jsonp_fail(request, message=data)
    return jsonp_ok(request, data)
