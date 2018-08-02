# _*_ coding: utf-8 _*_
# @时间    : 2017/9/5 11:28
# @作者  : 王洒
# @文件名    : index.py

from libs.utils import ajax,tbktapi,ajax_try
from com.com_user import need_login
from apps.yw_activity import common as com
from apps.active.common import get_user_rank
import common


@ajax_try([])
@need_login
def post_index(request):

    """
       @api {post} /huodong/yw_activity/s/index  [语文常态活动]学生端活动首页，判断学生和对应老师是否要加积分（学生首进/每日首次入学生/老师加积分,）
       @apiGroup yw_hd_s
        @apiParamExample {json} 请求示例
        {
        "t_id":1，老师id
        "class_id":1 #班级id
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data":[1,"开通成功！获得 1000积分"],# 1:已开通2：未开通
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(t_id=int,class_id=int)
    t_id = args.t_id
    class_id = args.class_id
    user_id = request.user_id
    is_open=request.user.openstatus(5)
    city=int(request.user.city)
    data=common.index(request,user_id,is_open,t_id,class_id,city)
    return ajax.jsonp_ok(request, [is_open,data,city])


@ajax_try([])
@need_login
def get_article_all(request):

    """
       @api {get} /huodong/yw_activity/s/article_all  [语文常态活动]学生端范文文章列表
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "p":1 #范文朗读的页数
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": [
        {
            "recording": {
                "ballot_num": 3,  #票数
                "user_id": 1,  #用户id
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording",#录音
                "ch_Code": 10610101,  #文章编码
                "state": 2,  #状态 #0未录制，1，已录制，2已分享
                "id": 3,  #录音id
                "add_time": 1505188588  #录音时间
            },
            "ch_Name": "善良的狐狸",  #文章id
            "ch_Code": "10610101"   #文章编码
        },
        {
            "recording": 0,    #0：未录音
            "ch_Name": "狐假虎威",  #文章名称
            "ch_Code": "10610102"  #文章编码
        }
    ],
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(p=int)
    p = args.p
    user_id = request.user_id

    data = common.article_all(p,user_id)
    return ajax.jsonp_ok(request, data)






@ajax_try([])
@need_login
def get_article_recom(request):

    """
       @api {get} /huodong/yw_activity/s/article_recom  [语文常态活动]学生端老师推荐文章列表
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "p":1 #页数
        "t_id": 1 #老师id
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": [
        {
            "recording": 0,  #0，未录音
            "ch_Name": "艾尔的新毯子",  #文章名称
            "ch_Code": 10610103,  #文章编码
            "add_time": "2017-09-11"  #推荐日期
        },
        {
            "recording": {
                "ballot_num": 3,  #票数
                "user_id": 1,  #学生id
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording",  #录音路径
                "ch_Code": 10610101,#文章编码
                "state": 2,  #状态1，已录制，2已分享
                "id": 3,  #录音id
                "add_time": 1505188588  #录音/分享的最后时间
            },
            "ch_Name": "善良的狐狸", #文章名称
            "ch_Code": 10610101,   #文章编码
            "add_time": "2017-09-12"  "  #推荐日期
        }
    ],
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(t_id=int, p=int)
    p = args.p
    t_id = args.t_id
    user_id = request.user_id

    data = common.article_recom(p,user_id,t_id)
    return ajax.jsonp_ok(request, data)




@ajax_try([])
@need_login
def get_article_details(request):

    """
       @api {get} /huodong/yw_activity/s/article_details  [语文常态活动]文章详情页
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "ch_Name":艾尔的新毯子 #文章名称
        "ch_Code":1 #文章code
        "state":0，#0未录制，1，已录制，2已分享
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
       "ch_Name": "艾尔的新毯子",
        "state": 1, #state是否已推荐: 1，已推荐，0，未推荐
        "ti_Contents": "从前在大森林里有一只叫森森的小狐狸，他很孤独，因为他没有朋友，小动物们都不和他玩，因为动物们都觉的狐狸是最坏的动物，再加上他的爸爸是骗走乌鸦肉的那只狐狸乌鸦们更是对他恨之入骨，但森森一点也不坏，他连一只蚂蚁都没伤害过。但动物们都不相信他。森森感到十分伤心。 ||一天，森森正在森林里闲逛 ，突然听到前面有动物喊“救命”，森森寻着声音跑过去，发现一只大灰狼正张牙舞爪地扑向一只小白兔，正在这危急关头，森森突然向前一跃，挡住了大灰狼扑向小白兔爪子，并大声向居住在附近的动物们求救。大灰狼锋利的爪子刺进了森森的肉里，森森顿时流了许多血，不一会就昏了过去。这时动物们听到求救声都纷纷拿着工具陆续赶了过来，大灰狼见势不妙，慌忙逃走了。 ||当森森醒来时，发现自己躺在一张床上，动物们都围在他的床边，看到它醒来都露出了笑容，这时兔妈妈拉住森森的手说“ 谢谢你救了我的孩子，我们以前错怪了你，你是一个勇敢而又善良的好孩子！” ||从此森森和其他动物们成了好朋友，一起快乐的生活在森林里。 "
    },
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(ch_Code=int,state=int,ch_Name='json')
    ch_Code=args.ch_Code
    state = args.state
    ch_Name= args.ch_Name
    user_id = request.user_id

    data = common.article_details(state,ch_Code,user_id,ch_Name)
    return ajax.jsonp_ok(request, data)




@ajax_try([])
@need_login
def post_recording(request):

    """
       @api {post} /huodong/yw_activity/s/post_recording  [语文常态活动]学生端录音入库
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "ch_Code":1, #文章code
        "json_info":""#录音路径
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data":1 #录音路径
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(ch_Code=int,json_info='json')
    ch_Code=args.ch_Code
    json_info = args.json_info
    user_id = request.user_id
    data = common.post_recording(json_info,ch_Code,user_id)
    return ajax.jsonp_ok(request, data)



@ajax_try([])
@need_login
def post_recording_integral(request):

    """
       @api {post} /huodong/yw_activity/s/recording_integral  [语文常态活动]文章当天首次分享加积分
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "recording_id" :录音id
        "share_time" :最新分享时间
        "state": 1,  #状态 #0未录制，1，已录制，2已分享
        "is_open":1，已开通，0未开通
        "class_id":1 #班级id
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data":{}
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(recording_id=int,share_time=int,state=int,is_open=int,class_id=int)
    recording_id=args.recording_id
    share_time = args.share_time
    state = args.state
    is_open=args.is_open
    class_id = args.class_id
    user_id=request.user_id
    city = int(request.user.city)
    data = common.recording_integral(recording_id, share_time,state,user_id,is_open,class_id,city)
    return ajax.jsonp_ok(request, data)







# @need_login
@ajax_try([])
def post_ballot_integral(request):

    """
       @api {post} /huodong/yw_activity/s/ballot_integral  [语文常态活动]分享获得投票入库
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "ch_Code":111 #文章编码
        "recording_id" :录音id,
        "is_open":1 #"is_open":1，已开通，0未开通
        "user_id":1 #登录的用户
        "class_id":班级id
        "city_id":城市id
        ""
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data":1，#1，投票成功，0投票失败
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(user_id=int,class_id=int,ch_Code=int,city_id=int)
    # recording_id = args.recording_id
    # is_open = args.is_open
    user_id = args.user_id
    class_id = args.class_id
    ch_Code= args.ch_Code
    city_id=args.city_id
    data = common.ballot_integral(user_id,class_id,ch_Code,city_id)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_login
def get_all_recording(request):

    """
       @api {get} /huodong/yw_activity/s/all_recording  [语文常态活动]全省学生录音排名
       @apiGroup yw_hd_s
      @apiParamExample {json} 请求示例
{
    "message": "",
    "next": "",
    "data": {
        "active": [
            {
                "city": "0",
                "ch_name": "狐假虎威",  #文章名称
                "user_id": 591113,  #用户id
                "ballot_num": 7,  #票数
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording",  #录音
                "ch_Code": 10610102,  #文章code
                "unit_id": 0,  #班级id
                "score": 47,  #积分
                "school_dict": {
                    "portrait": "portrait/2017/06/23/20170623122616857641.png",
                    "city": "410400",
                    "user_id": 591113,
                    "school_name": "叶县实验学校",  #学校
                    "real_name": "创恒"  #姓名
                },
                "record_id": 6,  #录音id
                "id": 1020030,
                "active_id": 4
            },
            {
                "city": "0",
                "ch_name": "善良的狐狸",
                "user_id": 378394,
                "ballot_num": 5,
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording",
                "ch_Code": 10610101,
                "unit_id": 0,
                "score": 45,
                "school_dict": {
                    "portrait": "http://user.tbkt.cn/site_media/images/profile/default-student.png",
                    "city": "410200",
                    "user_id": 378394,
                    "school_name": "鼓楼区杨砦小学",
                    "real_name": "李果果"
                },
                "record_id": 5,
                "id": 1020028,
                "active_id": 4
            }
        ],
        "page_count": 1
    },
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(p=int)
    p = args.p
    data = com.integral_list(request,p,1,0)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_login
def get_class_ranking(request):

    """
       @api {get} /huodong/yw_activity/s/class_ranking  [语文常态活动]班级排名
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "p":1, #当前页数
        "class_id":1班级id
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "active": [
            {
                "city": "0",
                "ch_name": "狐假虎威",  #文章名称
                "user_id": 591113,
                "ballot_num": 7,  #票数
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording", #录音
                "ch_Code": 10610102,  #文章code
                "unit_id": 7,  #年级id
                "score": 47,  #积分
                "school_dict": {
                    "portrait": "portrait/2017/06/23/20170623122616857641.png",  #头像
                    "city": "410400",
                    "user_id": 591113,
                    "school_name": "叶县实验学校",  #学校
                    "real_name": "创恒" #姓名
                },
                "record_id": 6,  录音id
                "id": 1020030,
                "active_id": 4
            },
            {
                "city": "0",
                "ch_name": "善良的狐狸",
                "user_id": 378394,
                "ballot_num": 5,
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording",
                "ch_Code": 10610101,
                "unit_id": 7,
                "score": 45,
                "school_dict": {
                    "portrait": "http://user.tbkt.cn/site_media/images/profile/default-student.png",
                    "city": "410200",
                    "user_id": 378394,
                    "school_name": "鼓楼区杨砦小学",
                    "real_name": "李果果"
                },
                "record_id": 5,
                "id": 1020028,
                "active_id": 4
            }
        ],
        "page_count": 1
    },
    "response": "ok",
    "error": ""
}
    """

    args = request.QUERY.casts(p=int,class_id=int)
    p = args.p
    class_id = args.class_id
    data = com.integral_list(request,p,1,class_id)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_login
def user_rank(request):

    """
       @api {get} /huodong/yw_activity/s/user_rank  [语文常态活动]学生端积分 排名
       @apiGroup yw_hd_s
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "sampling": 0,  #抽奖次数
        "score": 0,  #总分数
        "rank_no": 0  #排名
    },
    "response": "ok",
    "error": ""
}
    """

    user_id = request.user_id
    user_rank = get_user_rank(4,user_id)
    sampling = user_rank['score'] / 1000
    user_rank['sampling']=sampling
    return ajax.jsonp_ok(request, user_rank)

@ajax_try([])
@need_login
def s_integral_list(request):

    """
       @api {get} /huodong/yw_activity/s/s_integral_list  [语文常态活动]结束页
       @apiGroup yw_hd_s
       @apiParamExample {json} 请求示例
        {
        "p_begin":1, #当前页数
        "is_type":1，按奖品，2，按积分来
        }

        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "is_state": 1,
        "active_data": [
            {
                "user_name": "李果果",
                "user_id": 2661647,
                "school_dict": {
                    "portrait": "http://user.tbkt.cn/site_media/images/profile/default-student.png",
                    "city": "411200",
                    "user_id": 2661647,
                    "school_name": "湖滨区磁钟乡杨窑中心小学",
                    "real_name": "吴芮老师"
                },
                "award_name": "谢谢参与"
            }
        ]
    },
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(is_type=int, p_begin=int)
    is_type = args.is_type
    p_begin = args.p_begin
    data=com.end_list(4, is_type, p_begin)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_login
def share_activity(request):

    """
       @api {get} /huodong/yw_activity/s/share_activity  [语文常态活动]活动页面分享
       @apiGroup yw_hd_s
              @apiParamExample {json} 请求示例
        {
        "is_open":1  #是否开通
        "class_id":1, #班级id
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": 1, #添加成功，2#添加失败
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(class_id=int,is_open=int)
    class_id=args.class_id
    is_open = args.is_open
    user_id = request.user_id
    city = int(request.user.city)
    data=common.share_activity(user_id,class_id,is_open,city)
    return ajax.jsonp_ok(request, data)