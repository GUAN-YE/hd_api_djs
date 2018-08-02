#coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2018/1/16 17:30
"""
from com.com_user import need_login
from . import common
from libs.utils import ajax, sms, settings
from tbkt.settings import FILE_MEDIA_URLROOT, FILE_VIEW_URLROOT

import json


@need_login
def get_activity_entrance(request):
    """
        @api {get} /huodong/winter_activity/activity_entrance [寒假活动]总的活动入口
        @apiGroup winter_activity
        @apiParamExample {json} 请求示例
           {
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "power_num" : 1                                     // 能量数目
                "score" : 150                                // 积分数量
                "range_num" : 1000                                 // 用户排名
                "open_status" : 1.2.3 or 0                            // 1.2.3为开通科目数量 0为未开通
                "award_info" : [                                 // 奖品信息
                                {name : "***", image_url : "***", id : ***},
                                {name : "***", image_url : "***", id : ***},
                                {name : "***", image_url : "***", id : ***},
                                ]
                "take_a_big_gift" : 0 or 1.2.3                      //1.2.3为获得了大礼包的数量  0为没有获得
                "login_day" : l2                                 //连续登录日期数 1-8
                "notice" : 0  or  其他Int类型数值        // 0 为不用通知用户 ，其他则为award_id  需要去取award_info内的奖品名称
                "award_day" : 1                         // 0 未不通知用户   1-31为获奖日期
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                活动入口的第一个界面
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2018-1-16
    """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    user_id = request.user_id
    data = common.get_user_info(user_id)
    return ajax.jsonp_ok(request, data)


@need_login
def get_user_match(request):
    """
       @api {get} /huodong/winter_activity/get_user_match  [寒假活动]成语、诗词pk模块选择对手、获取信息
       @apiGroup winter_activity
       @apiParamExample {json} 请求示例
        {
        "school_id":1 #学校id
        "class_id":1 #班级id
        "province_id":1 #省份id
        "is_type":1，#类型，1.诗词大战pk,2.成语游戏pk
        "is_arena" : 1  # 是否为欢乐竞技场  1 是 0 不是
        }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": [
                {
                    "user_id": 1583213,
                    "class_id": 11,
                    "user_object": "{\"portrait\": \"http://student.tbkt.cn/site_media/images/profile/default-student.png\", \"school\": \"\\u9ec4\\u6cb3\\u8def\\u4e00\\u5c0f\", \"user_id\": 1583213, \"name\": \"\\u5f20\\u4e09\"}",
                    "right_num": 3,
                    "school_id": 22,
                    "match_record_id": 1,
                    "score": 88,
                    "result": 1,
                    "pk_user": "{\"portrait\": \"http://student.tbkt.cn/site_media/images/profile/default-student.png\", \"user_id\": 1583213, \"name\": \"\\u5f20\\u4e09\"}",
                    "province_id": 1,
                    "type": 2,
                    "id": 6,
                    "user_time": 88,
                    "add_time": 1502467
                    "user_props" = [1,1,1,1,1,1]  //按顺序依次是1：鲜花数量，2：鸡蛋数量，3：墨镜数量，4：橡皮擦数量，5：放大镜数量，6：超级翻倍卡数量',
                    "pk_id" = 100 or 0 //  PKid代表了PK时候扣除能量值明细的id
                }
            ],
            "response": "ok",
            "error": ""
        }
    """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    args = request.QUERY.casts(school_id=int, class_id=int, province_id=int, is_type=int, is_arena=int)
    school_id = args.school_id
    class_id = args.class_id
    province_id = args.province_id
    is_type = args.is_type
    is_arena = args.is_arena
    user_id = request.user_id
    if not school_id:
        return ajax.jsonp_fail(request, "缺少参数school_id")
    if not class_id:
        return ajax.jsonp_fail(request, "缺少参数class_id")
    if not province_id:
        return ajax.jsonp_fail(request, "缺少参数province_id")
    if not is_type:
        return ajax.jsonp_fail(request, "缺少参数is_type")
    if is_arena != 1:  # 非欢乐榜逻辑 需要操作能量值
        power = common.get_user_power(user_id)
        if not power:
            return ajax.jsonp_fail(request, "您的能量值不足")
        pk_id = common.use_user_power(user_id)
    else:
        pk_id = 0
    data = common.pk_user_info(user_id, school_id, class_id, province_id, is_type)
    # if "default-student.png" in data["user_object"]:
    #     d = json.loads(data["user_object"])
    #     d["img"] = FILE_MEDIA_URLROOT + "/user_media/images/profile/default-student.png"
    #     data['user_object'] = json.dumps(d)
    # else:
    #     d = json.loads(data["user_object"])
    #     if d["img"]:
    #         d["img"] = FILE_VIEW_URLROOT + d["img"]
    #         data['user_object'] = json.dumps(d)
    #     else:
    #         d["img"] = FILE_MEDIA_URLROOT + "/user_media/images/profile/default-student.png"
    # data['user_object'] = json.dumps(d)
    # if "default-student.png" in data["pk_user"]:
    #     d = json.loads(data["pk_user"])
    #     d["img"] = FILE_MEDIA_URLROOT + d["img"]
    #     data['pk_user'] = json.dumps(d)
    # else:
    #     d["img"] = FILE_VIEW_URLROOT + d["img"]
    #     data['pk_user'] = json.dumps(d)
    user_props = common.get_user_props(user_id)
    # 前端是按照设计图给出的道具顺序, 所以需要修改一下道具顺序
    # 数据库的道具顺序为： 1：鲜花数量，2：鸡蛋数量，3：墨镜数量，4：橡皮擦数量，5：放大镜数量，6：超级翻倍卡数量'
    # 设计图的道具顺序为：1：鲜花数量，2：鸡蛋数量，3：放大镜数量，4：墨镜数量，5：橡皮擦数量，6：超级翻倍卡数量'
    num_three = user_props[4]
    num_four = user_props[2]
    num_five = user_props[3]
    user_props[2], user_props[3], user_props[4] = num_three ,num_four, num_five
    data['user_props'] = user_props
    data['pk_id'] = pk_id
    return ajax.jsonp_ok(request, data)


@need_login
def r_get_poetry(request):
    """
       @api {get} /huodong/winter_activity/r_get_poetry  [寒假活动]学生端 诗词pk模块资源接口
       @apiGroup winter_activity
       @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": [
        {
            "qu_TitleDry": "________________，何时复西归。",  #qu_TitleDry
            "qu_OptionA": "空翠湿人衣",
            "qu_OptionB": "欲穷千里目",
            "qu_OptionC": "今春看又过",
            "qu_OptionD": "百川东到海",
            "po_ID": 3,  #关联诗歌表ID
            "po_Name": "长歌行", #诗歌名称
            "po_Author": "汉乐府", 作者
            "qu_TrueOption": "D"  #正确选项
            "answer" : "百川东到海，何时复西归。"
            "have_glass" : 1 为这局用户被使用了墨镜 0 为这局用户没有被使用墨镜
        },
    ],
    "response": "ok",
    "error": ""
}
       """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    data = common.get_poetry()
    return ajax.jsonp_ok(request, data)


@need_login
def r_get_idiom(request):
    """
       @api {get} /huodong/winter_activity/r_get_idiom  [寒假活动]学生端 成语pk模块资源接口
       @apiGroup winter_activity
       @apiSuccessExample {json} 成功返回
{
    "message": "",
    "next": "",
    "data": {
        "words_list": [
            "面",
            "创",
            "嘿",
            "穹",
            "泵",
            "爬",
            "路",
            "开",
            "季",
            "疮",
            "廓",
            "一",
            "避",
            "斥",
            "网",
            "绩",
            "蟹",
            "螯"
        ],
        "cy_Source": "清·李绿园《歧路灯》：“先生意欲网开一面；以存忠厚之意；这却使不得。”",  #成语出处
        "cy_Tupian": "/UploadFileS/Images/a8ea8b22-4326-40da-9fdf-8ee4ab3aeff2.png",
        "cy_Content": "网开一面",
        "cy_Explain": "把捕禽的网撤去三面，只留一面。比喻采取宽大态度，给人一条出路。"   #成语解释
        "have_glass" : 1 为这局用户被使用了墨镜 0 为这局用户没有被使用墨镜
    },
    "response": "ok",
    "error": ""
}
       """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    data = common.get_idiom()
    return ajax.jsonp_ok(request, data)


@need_login
def post_pk_details(request):
    """
       @api {post} /huodong/winter_activity/post_pk_details  [寒假活动]成语、诗词pk模块结果入库
       @apiGroup winter_activity
       @apiParamExample {json} 请求示例
        {
                "right_num": "3"答对题数,
                "user_time": 总时长,
                "score": "44"总数
                "user_object"：用户的信息:头像路径、姓名、user_id、学校名称
                "pk_user"：挑战对象的信息:头像路径、姓名、user_id、学校名称、答对几道题、用时、总分
                "result":1，结果1.赢了，2.输了
                "school_id":学校id
                "class_id"：班级id
                "province_id"：省份id
                "add_time":挑战开始的时间
                "is_type":1 #类型，1.诗词大战pk,2.成语游戏pk
                "pk_id" = 100 or 0 //  PKid代表了PK时候扣除能量值明细的id
            }
        @apiSuccessExample {json} 成功返回
        {
        "message": "",
        "next": "",
        "data": {
                add_type: 1    //胜利方获得有一个道具 0：未获得 1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡  0：未获得
                ids : [score_id， score_detail_id, pk_record_id]   //分数id 分数详情id
            },
        "response": "ok",
        "error": ""
    }
        """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    args = request.QUERY.casts(right_num=int, user_time=int, score=int, user_object='json',
                               pk_user='json', result=int, school_id=int, province_id=int, class_id=int, add_time=int,
                               is_type=int, pk_id=int)
    # 基本信息
    add_time = args.add_time
    right_num = args.right_num
    user_time = args.user_time
    score = args.score
    user_object = args.user_object
    pk_user = args.pk_user
    result = args.result
    school_id = args.school_id
    province_id = args.province_id
    class_id = args.class_id
    is_type = args.is_type
    pk_id = args.pk_id
    user_id = request.user_id

    data = common.post_pk_details(user_id, add_time, right_num, user_time, score, user_object, pk_user, result,
                                  school_id, province_id, class_id, is_type, pk_id)

    return ajax.jsonp_ok(request, data)


@need_login
def happy_arena(request):
    """
        @api {get} /huodong/winter_activity/happy_arena [寒假活动]欢乐竞技场入口
        @apiGroup winter_activity
        @apiParamExample {json} 请求示例
           {
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "is_type":1，#类型，1.诗词大战pk,2.成语游戏pk
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    user_id = request.user_id
    time_limit = common.time_limmit()
    if not time_limit:
        return ajax.jsonp_fail(request, "未到开放时间！")
    open_status = common.get_user_open_status(user_id)
    if not open_status:
        return ajax.jsonp_fail(request, "欢乐竞技场仅开通用户可以参加！")
    data = common.get_type(user_id)
    return ajax.jsonp_ok(request, data)


@need_login
def post_happy_pk_details(request):
    """
       @api {post} /huodong/winter_activity/post_happy_pk_details  [寒假活动]欢乐竞技场PK结果入库
       @apiGroup winter_activity
       @apiParamExample {json} 请求示例
        {
                "right_num": "3"答对题数,
                "user_time": 总时长,
                "score": "44"总数
                "user_object"：用户的信息:头像路径、姓名、user_id、学校名称
                "pk_user"：挑战对象的信息:头像路径、姓名、user_id、学校名称、答对几道题、用时、总分
                "result":1，结果1.赢了，2.输了
                "school_id":学校id
                "class_id"：班级id
                "province_id"：省份id
                "add_time":挑战开始的时间
                "is_type":1 #类型，1.诗词大战pk,2.成语游戏pk
            }
        @apiSuccessExample {json} 成功返回
        {
        "message": "",
        "next": "",
        "data": {
                add_type: 1    //胜利方获得有一个道具 0：未获得 1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡
                ids : [score_id, score_detail_id, happy_score_id, pk_happy_record_id]   //分数id 分数详情id 欢乐分数id PK记录ID
            },
        "response": "ok",
        "error": ""
    }
        """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    time_limit = common.time_limmit()
    if not time_limit:
        return ajax.jsonp_fail(request, "未到开放时间！")

    args = request.QUERY.casts(right_num=int, user_time=int, score=int, user_object='json',
                               pk_user='json', result=int, school_id=int, province_id=int, class_id=int, add_time=int,
                               is_type=int)
    # 基本信息
    add_time = args.add_time
    right_num = args.right_num
    user_time = args.user_time
    score = args.score
    user_object = args.user_object
    pk_user = args.pk_user
    result = args.result
    school_id = args.school_id
    province_id = args.province_id
    class_id = args.class_id
    is_type = args.is_type
    user_id = request.user_id



    #增加积分
    data = common.post_happy_pk_details(user_id, add_time, right_num, user_time, score, user_object, pk_user, result,
                                  school_id, province_id, class_id, is_type)


    return ajax.jsonp_ok(request, data)


@need_login
def use_props(request):
    """
           @api {post} /huodong/winter_activity/use_props  [寒假活动]使用道具
           @apiGroup winter_activity
           @apiParamExample {json} 请求示例
            {

                    "has_use_double"  : 1//    代表使用了双倍积分卡
                    "has_use_flower" : 1    // 代表使用鲜花
                    "has_use_egg" : 1       // 代表使用鸡蛋
                    "has_use_sunglasses"  : 1      // 代表使用墨镜
                    "has_use_magnifier" : 1    // 代表使用放大镜
                    "has_use_eraser" :1    //代表适用橡皮擦
                    "ids" : [score_id, score_detail_id, happy_score_id, pk_happy_record_id]  //双倍积分卡需要修改记录的数组
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
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    args = request.QUERY.casts(has_use_double=int, has_use_flower=int, has_use_egg=int,
                               has_use_sunglasses=int, has_use_magnifier=int, has_use_eraser=int, ids='json')

    user_id = request.user_id
    # 道具信息
    add_time = args.add_time
    has_use_double = args.has_use_double or 0
    has_use_flower = args.has_use_flower or 0
    has_use_egg = args.has_use_egg or 0
    has_use_sunglasses = args.has_use_sunglasses or 0
    has_use_magnifier = args.has_use_magnifier or 0
    has_use_eraser = args.has_use_eraser or 0
    ids = args.ids or []
    # 双倍积分卡及使用
    if has_use_double and ids:
        common.use_double(ids, user_id, add_time)

    # 减少消耗道具(除双倍积分卡外)
    props = common.post_props_details(user_id, 0, has_use_flower,
                                     has_use_egg, has_use_sunglasses, has_use_magnifier, has_use_eraser, add_time)
    if props:
        return ajax.jsonp_fail(request, props)

    return ajax.jsonp_ok(request)


@need_login
def heroes(request):
    """
        @api {get} /huodong/winter_activity/heroes [寒假活动]英雄榜
        @apiGroup winter_activity
        @apiParamExample {json} 请求示例
           {
                "p" :  // 我也不知道你会请求啥 反正按老方法来
                       // 尽量不用下拉的时候返回p=0，然后第一次下拉返回p=20， 第二次下拉返回p=30
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": [
                {
                    "score" : 111  //用户积分
                    "user_id": 800363, // 用户id
                    "border_url" : // 用户的头像边框地址 没有则返回空  只有前三名有
                    "real_name" : "***"  //用户姓名
                    "school_name" : "***"  //用户学校名称
                },
                {
                    "score" : 111  //用户积分
                    "user_id": 800363, //用户id
                    "border_url" : // 用户的头像边框地址 没有则返回空  只有前三名有
                    "real_name" : "***"  //用户姓名
                    "school_name" : "***"  //用户学校名称
                },
                {},{},{}......  //  备注： 0分用户不显示
            ],
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    arg = request.QUERY.casts(p=int)
    pages_no = arg.p or 0
    page_no = pages_no / 10 + 1
    data = common.get_heros_info(page_no)

    return ajax.jsonp_ok(request, data)


@need_login
def my_things(request):
    """
            @api {get} /huodong/winter_activity/my_things [寒假活动]我的很多东西
            @apiGroup winter_activity
            @apiParamExample {json} 请求示例
               {
                }
            @apiSuccessExample {json} 成功返回
            {
                "message": "",
                "next": "",
                "data": {
                    "props" : [1,1,1,1,1,1]  //按顺序依次是1：鲜花数量，2：鸡蛋数量，3：墨镜数量，4：橡皮擦数量，5：放大镜数量，6：超级翻倍卡数量',
                   "awards" : [
                                {name : "***", add_time : "1"， "add_mon" : 1},   //name : 奖品名称  add_time 获奖那天的日期
                                {name : "***", add_time : "1"， "add_mon" : 1}
                                {name : "***", add_time : "1"， "add_mon" : 1}
                                ......
                                ]
                 },
                "response": "ok",
                "error": ""
            }
            @apiSuccessExample {json} 失败返回
               {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    user_id = request.user_id
    data = common.get_my_things(user_id)
    return ajax.jsonp_ok(request, data)


@need_login
def happy_ranking(request):
    """
            @api {get} /huodong/winter_activity/happy_ranking [寒假活动]欢乐榜
            @apiGroup winter_activity
            @apiParamExample {json} 请求示例
               {
                    "p" :  // 我也不知道你会请求啥 反正按老方法来
                           // 尽量不用下拉的时候返回p=0，然后第一次下拉返回p=10， 第二次下拉返回p=20
                }
            @apiSuccessExample {json} 成功返回
            {
                "message": "",
                "next": "",
                "data": [
                    {
                          "border_url" : // 用户的头像边框地址 没有则返回空  只有第一名有   为空则证明今天还没开奖
                          "img" : //用户的当前头像   为空则证明今天还没开奖
                          "nowday" : //当前日期
                          "nowmon" : //当前月份
                          "name" : '' //真实姓名    为空则证明今天还没开奖
                    }
                    [
                        {
                            "score" : 111            //用户积分
                            "real_name" : "***"     //用户姓名
                            "user_id": 800363,      //用户Id

                            "school_name" : "***"  //用户学校名称
                            "award_id" : ***      //该字段不为空则排行榜上应显示已领奖
                        },
                        {
                            "score" : 111            //用户积分
                            "real_name" : "***"     //用户姓名
                            "user_id": 800363,      //用户Id
                            "school_name" : "***"  //用户学校名称
                            "award_id" : ***      //该字段不为空则排行榜上应显示已领奖
                        },
                        {},{},{}......
                    ]
                ],
                "response": "ok",
                "error": ""
            }
            @apiSuccessExample {json} 失败返回
               {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    arg = request.QUERY.casts(p=int)
    pages_no = arg.p or 0
    user_id = request.user_id
    data = common.get_happy_ranking(pages_no)

    return ajax.jsonp_ok(request, data)


@need_login
def invite_get_power(request):
    """
        @api {get} /huodong/winter_activity/invite_get_power [寒假活动]邀请获得能量接口
        @apiGroup winter_activity
        @apiParamExample {json} 请求示例
           {
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": [
            ],
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    user_id = request.user_id
    data = common.invite_get_power(user_id)
    if not data:
        return ajax.jsonp_fail(request, "当日邀请次数超过五次")
    return ajax.jsonp_ok(request, data)


@need_login
def get_user_coin_power_detail(request):
    """
       @api {get} /huodong/winter_activity/coin_power_detail [寒假活动]获取积分能量值明细
       @apiGroup winter_activity
       @apiParamExample {json} 请求示例
          {
            p : 10 //  请求0则返回0-10条数据 请求10则返回10-20条数据，请求20则返回20-30条数据
           }
       @apiSuccessExample {json} 成功返回
       {
           "message": "",
           "next": "",
           "data": [
                      "您在2月20日通过PK扣除1个能量值",
                      "您在2月20日通过PK扣除1个能量值"
                       ......  // 10个数据
                    ]
    },
           "response": "ok",
           "error": ""
       }
       @apiSuccessExample {json} 失败返回
          {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
   """
    if not common.end_acitvtiy():
        return ajax.jsonp_fail(request, "活动已经结束")
    user_id = request.user_id
    arg = request.QUERY.casts(p=int)
    pages_no = arg.p or 0
    data = common.get_my_detail(user_id, pages_no)
    return ajax.jsonp_ok(request, data)