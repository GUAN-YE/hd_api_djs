# _*_ coding: utf-8 _*_
# @时间    : 2017/9/5 11:28
# @作者  : 王洒
# @文件名    : index.py

from libs.utils import ajax,ajax_try
from com.com_user import need_teacher
from apps.yw_activity import common as com
from apps.active.common import get_user_rank
import common


@ajax_try([])
@need_teacher
def get_article_list(request):

    """
       @api {get} /huodong/yw_activity/t/article_list  [语文常态活动]教师端推荐文章列表
       @apiGroup yw_hd_t
       @apiParamExample {json} 请求示例
        {
        "p":1 #当前页数
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "data": [
            {
                "ch_Name": "善良的狐狸",
                "ch_Code": "10610101",
                "state": 1
            }
        ],
        "page_count": 33  #总页数
    },
    "response": "ok",
    "error": ""
}
    """
    user_id = request.user_id
    args = request.QUERY.casts(p=int)
    p=args.p
    data = common.article_list(user_id,p)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_teacher
def post_recommend_article(request):

    """
       @api {post} /huodong/yw_activity/t/recommend_article  [语文常态活动]教师端推荐文章给学生入库
       @apiGroup yw_hd_t
       @apiParamExample {json} 请求示例
        {
        "ch_Code":1 #章节的code
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",  #"message": "今日已推荐过文章",
    "next": "",
    "data":""
    "response": "ok",  #"response": "fail",
    "error": ""
}
    """
    user_id = request.user_id
    args = request.QUERY.casts(ch_Code=int)
    ch_Code=args.ch_Code
    city = int(request.user.city)
    data = common.recommend_article(user_id,ch_Code,city)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@need_teacher
def get_article_details(request):

    """
       @api {get} /huodong/yw_activity/t/article_details  [语文常态活动]文章详情页
       @apiGroup yw_hd_t
       @apiParamExample {json} 请求示例
        {
        "ch_Name":艾尔的新毯子 #文章名称
        "state":1,#state是否已推荐: 1，已推荐，0，未推荐
        "ch_Code":1 #文章code
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
    state=args.state
    ch_Code=args.ch_Code
    ch_Name=args.ch_Name

    data = common.article_details(ch_Code,state,ch_Name)
    return ajax.jsonp_ok(request, data)



@ajax_try([])
@need_teacher
def get_teacher_ranking(request):

    """
       @api {get} /huodong/yw_activity/t/teacher_ranking  [语文常态活动]教师排名
       @apiGroup yw_hd_t
      @apiParamExample {json} 请求示例
        {
        "p":1 #当前页数
        }
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "active": [
            {
                "school_dict": {
                    "portrait": "http://user.tbkt.cn/site_media/images/profile/default-student.png",
                    "city": "411200",
                    "user_id": 2661647,
                    "school_name": "湖滨区磁钟乡杨窑中心小学",  #学校名称
                    "real_name": "吴芮老师"   #用户名称
                },
                "score": 47,  #分数
                "user_id": 2661647   #用户id
            }
        ],
        "page_count": 1
    },
    "response": "ok",
    "error": ""
}
    """
    args = request.QUERY.casts(p=int)
    p=args.p

    data = common.teacher_ranking(p)
    return ajax.jsonp_ok(request, data)



@ajax_try([])
@need_teacher
def get_class_ranking(request):

    """
       @api {get} /huodong/yw_activity/t/class_ranking  [语文常态活动]班级排名
       @apiGroup yw_hd_t
       @apiParamExample {json} 请求示例
        {
        "p":1, #当前页数
        "class_id":"1"班级id
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
                "user_id": 591113,  用户id
                "ballot_num": 7,
                "json_info": "http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording", #录音
                "ch_Code": 10610102,  #文章编码
                "unit_id": 7,  #班级id
                "score": 47,  # 积分
                "school_dict": {
                    "portrait": "portrait/2017/06/23/20170623122616857641.png",  #头像
                    "city": "410400",
                    "user_id": 591113,
                    "school_name": "叶县实验学校", #学校
                    "real_name": "创恒"  #姓名
                },
                "record_id": 6, #录音id
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
    class_id=args.class_id
    data = com.integral_list(request,p,1,class_id)
    return ajax.jsonp_ok(request, data)



@ajax_try([])
@need_teacher
def user_rank(request):

    """
       @api {get} /huodong/yw_activity/t/user_rank  [语文常态活动]学生端积分 排名
       @apiGroup yw_hd_t
        @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "sampling": 0,  #抽奖次数
        "score": 0,  #总分数
        "rank_no": 0  #排名
        "city_id":1 #城市id
    },
    "response": "ok",
    "error": ""
}
    """

    user_id = request.user_id
    user_rank = get_user_rank(5,user_id)
    city_id=request.user.city
    sampling = user_rank['score'] / 1000
    user_rank['sampling']=sampling
    user_rank['city_id'] = city_id
    return ajax.jsonp_ok(request, user_rank)


@ajax_try([])
@need_teacher
def t_integral_list(request):

    """
       @api {get} /huodong/yw_activity/t/t_integral_list  [语文常态活动]结束页
       @apiGroup yw_hd_t
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
                "user_id": 378394,
                "school_dict": {
                    "portrait": "http://user.tbkt.cn/site_media/images/profile/default-student.png",
                    "city": "410200",
                    "user_id": 378394,
                    "school_name": "鼓楼区杨砦小学",
                    "real_name": "李果果"
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
    data=com.end_list(5, is_type, p_begin)
    return ajax.jsonp_ok(request, data)