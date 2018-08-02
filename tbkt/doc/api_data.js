define({ "api": [
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./apidoc/main.js",
    "group": "G__Work_hd_api_dj_tbkt_apidoc_main_js",
    "groupTitle": "G__Work_hd_api_dj_tbkt_apidoc_main_js",
    "name": ""
  },
  {
    "type": "post",
    "url": "/huodong/active/active_status",
    "title": "[活动]用户某个活动是否能加分",
    "group": "active",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"active_id\": 3\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\": 1             # 1 能加分， 2 不能加分,只显示排行\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/active/views.py",
    "groupTitle": "active",
    "name": "PostHuodongActiveActive_status"
  },
  {
    "type": "post",
    "url": "/huodong/active/actives_info",
    "title": "[活动]满足用户条件的活动",
    "group": "active",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"extend\": {},\n            \"banner_url\": \"\",\n            \"banner_end\": \"2017-10-31 23:59:59\",\n            \"name\": \"英语常态活动(S1赛季)\",\n            \"banner_begin\": \"2017-09-11 17:21:31\",\n            \"is_open\": 1,       1 表示能加分， 2 表示不能加分\n            \"begin_url\": \"\",\n            \"active_id\": 3\n        }, {}, {},....\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/active/views.py",
    "groupTitle": "active",
    "name": "PostHuodongActiveActives_info"
  },
  {
    "type": "post",
    "url": "/huodong/active/add_score",
    "title": "[活动]活动加减分",
    "group": "active",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     \"user_id\": 2465828,             # 要加分的用户id\n     \"active_id\": 3,                 # 活动id\n     \"item_no\": \"mouse\"              # 活动加减分规则标识\n     \"city\": 4500000,                # 省，市, 区\n     \"unit_id\": \"\"                   # 班级\n     \"is_open\":                      # 用户开通状态 0:未开通， 1: 开通\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/active/views.py",
    "groupTitle": "active",
    "name": "PostHuodongActiveAdd_score"
  },
  {
    "type": "",
    "url": "/huodong/com/rank/units",
    "title": "[公共]班级排行",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n     unit_id:123 班级id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"tbkt_token\": \"NDgwMDAyfTA0MDAzMzcxNTB9MDQwMDc1MDY2Ng\",\n    \"next\": \"\",\n    \"error\": \"\",\n    \"message\": \"\",\n    \"data\": {\n        [\n            {\n                \"score\": 0,\n                \"id\": 591113,\n                \"real_name\": \"翟于讳\"\n            },\n            {\n                \"score\": 0,\n                \"id\": 1470977,\n                \"real_name\": \"汤鹏程\"\n            },\n            {\n                \"score\": 0,\n                \"id\": 2144020,\n                \"real_name\": \"柳絮\"\n            },\n            {\n                \"score\": 0,\n                \"id\": 2884805,\n                \"real_name\": \"欧阳慧兰\"\n            }\n        ]\n    },\n    \"response\": \"ok\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "HuodongComRankUnits"
  },
  {
    "type": "",
    "url": "/huodong/com/share",
    "title": "[公共]学生分享",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "HuodongComShare"
  },
  {
    "type": "",
    "url": "/huodong/com/sign",
    "title": "[公共]学生签到",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "HuodongComSign"
  },
  {
    "type": "",
    "url": "/huodong/com/tea/send_sms",
    "title": "[公共]教师发短信",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\nactive_id:6   活动id\ncontent:'123' 短息内容\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n\"tbkt_token\": \"NDgwMDAyfTA0MDAzMzcxNTB9MDQwMDc1MDY2Ng\",\n\"next\": \"\",\n\"error\": \"\",\n\"message\": \"\",\n\"data\": {},\n\"response\": \"ok\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "HuodongComTeaSend_sms"
  },
  {
    "type": "",
    "url": "/huodong/com/user/detail",
    "title": "[公共]用户积分详情",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"item_name\": \"做作业\",\n            \"add_date\": \"09月12日 11:43:52\",\n            \"score\": 120\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "HuodongComUserDetail"
  },
  {
    "type": "post",
    "url": "/huodong/com/award",
    "title": "[公共 ]活动抽奖",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     app_id:1   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"award_type\": 1,\n        \"name\": \"ipad\",\n        \"is_award\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"积分不足\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComAward"
  },
  {
    "type": "post",
    "url": "/huodong/com/award/all",
    "title": "[公共] 分页返回中奖用户",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     app_id:1   抽奖奖品对应id\n     p:1   页码\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"total\": 1,\n        \"detail\": [\n            {\n                \"city\": \"410200\",\n                \"user_id\": 378394,\n                \"name\": \"三等奖\",\n                \"url\": \"http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n                \"school_name\": \"鼓楼区杨砦小学\",\n                \"real_name\": \"李果果\",\n                \"award_type\": \"3\",\n                \"time\": \"2017-09-12 18:30:21\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComAwardAll"
  },
  {
    "type": "post",
    "url": "/huodong/com/award/list",
    "title": "[公共] 用户获奖详情",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     app_id:1   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"url\": \"http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n            \"award_type\": \"1\",\n            \"name\": \"ipad\",\n            \"time\": \"2017-09-11 18:23:55\"\n        },\n        {\n            \"url\": \"http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n            \"award_type\": \"3\",\n            \"name\": \"三等奖\",\n            \"time\": \"2017-09-11 18:21:03\"\n        },\n        {\n            \"url\": \"http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n            \"award_type\": \"4\",\n            \"name\": \"四等奖\",\n            \"time\": \"2017-09-11 18:19:34\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComAwardList"
  },
  {
    "type": "post",
    "url": "/huodong/com/award/recent",
    "title": "[公共] 获取最近10位中奖用户",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     app_id:1   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"url\": \"http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n            \"user_name\": \"李果果\",\n            \"award_type\": \"3\",\n            \"award_name\": \"三等奖\",\n            \"time\": \"2017-09-12 16:34:58\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComAwardRecent"
  },
  {
    "type": "post",
    "url": "/huodong/com/rank",
    "title": "[公共] 分页返回活动积分排行",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     grade_id：1  按年级排行时需要传入\n     unit_id:123   按班级排行时需要传入，p=-1 返回全班\n     active_id:6   活动id\n     p:1   页码\n     page_num:10 每页排行数量  ，不传时默认20\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"rank_info\": [\n            {\n                 \"portrait\": \"https://file.m.tbkt.cn/upload_media/portrait/2017/03/06/20170306102941170594.png\",\n                \"score\": 190,\n                \"user_id\": 2465828,\n                \"school_name\": \"创恒中学\",\n                \"real_name\": \"小张\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComRank"
  },
  {
    "type": "post",
    "url": "/huodong/com/user/info",
    "title": "[公共]首页",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"score\": 210,\n        \"rank_no\": 1,\n        \"is_sign\":True,True签过，Flase未签\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComUserInfo"
  },
  {
    "type": "post",
    "url": "/huodong/com/user/today_item",
    "title": "[公共]返回当日某加分项是否加分",
    "group": "com",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     active_id:6   活动id\n     item: send_sms   加分项 如：sign ：签到，send_sms:发作业，stu_do_task 做作业 等\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\":True,True加过分，Flase未加分\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/com_post/post.py",
    "groupTitle": "com",
    "name": "PostHuodongComUserToday_item"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/activity",
    "title": "[激励抽奖活动]抽奖活动详情页面",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"excite_activity_id\" : 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\" = {\n        'name' : name,                   //活动名称\n        'image_url' :url,                //图片URL\n        'strat_time_month' : strat_time_month,                //开始时间的月份\n        'start_time_date' : start_time_date,                //开始时间的日期\n        'end_time_month' : end_time_month,                //结束时间的月份\n        'end_time_date' : end_time_date,                //结束时间的日期\n        'remark' : remark,                //活动规则\n        'open_person' : open_person,                //到达多少人开奖\n        'had_join' : had_join,                //已经有多少人参与\n        'had_lottery' : had_lottery,                //已经开奖的次数\n        'lottery_rate' : lottery_rate,                //当前用户的中奖率\n        'excite_activity_left' : excite_activity_left,                //上一个活动  有的话是活动id 没有的话是0\n        'excite_activity_right' : excite_activity_right,              //下一个活动  有的话是活动id 没有的话是0\n        'lottery_up' : lottery_up,                //使用奖券参与次数上限\n        'had_use_ticket_join' : had_use_ticket_join,                //已经用奖券参与的用户的数量\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityActivity"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/activity_entrance",
    "title": "[激励抽奖活动]活动入口",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"excite_activity_id\" : 1       // 最近一个活动的ID\n        \"actitity_len\" : 1             // 目前正在进行的活动数量\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityActivity_entrance"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/ticket_num",
    "title": "[激励抽奖活动]用户抽奖券个数",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"ticket_num\":1     //该用户剩余的奖券数量\n        \"now_month\":12     //当前月份\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityTicket_num"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/winning_list",
    "title": "[激励抽奖活动]获取获奖教师名单",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"excite_activity_id\" : 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n          \"phone\": \"151****6670\",\n          \"user_id\": 897447,\n          \"school_name\": \"123\",\n          \"real_name\": \"钱学三\"\n        },\n        {\n          \"phone\": \"151****6670\",\n          \"user_id\": 897447,\n          \"school_name\": \"123\",\n          \"real_name\": \"钱学三\"\n        }\n        {}，{}，{}......\n      ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityWinning_list"
  },
  {
    "type": "post",
    "url": "/huodong/excite_activity/coin_join_actitvity",
    "title": "[激励抽奖活动]用户使用金币参与抽奖",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"excite_activity_id\" : 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "PostHuodongExcite_activityCoin_join_actitvity"
  },
  {
    "type": "post",
    "url": "/huodong/excite_activity/invite_stu",
    "title": "[激励抽奖活动]将邀请学生的信息存到数据库",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"stu_id\" : \"10000,10001,10002,10003,10004\"\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "PostHuodongExcite_activityInvite_stu"
  },
  {
    "type": "post",
    "url": "/huodong/excite_activity/invite_teacher",
    "title": "[激励抽奖活动]邀请老师用来获得抽奖券",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"phone_num\" : 13303330333\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "PostHuodongExcite_activityInvite_teacher"
  },
  {
    "type": "post",
    "url": "/huodong/excite_activity/ticket_join_actitvity",
    "title": "[激励抽奖活动]用户使用抽奖券参与抽奖",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"excite_activity_id\" : 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "PostHuodongExcite_activityTicket_join_actitvity"
  },
  {
    "type": "post",
    "url": "/huodong/gift_active/join",
    "title": "[金豆商城活动]参加活动",
    "group": "gift_active",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"active_id\": 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/gift_active/views.py",
    "groupTitle": "gift_active",
    "name": "PostHuodongGift_activeJoin"
  },
  {
    "type": "post",
    "url": "/huodong/gift_active/status",
    "title": "[金豆商城活动]用户是否参加活动",
    "group": "gift_active",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"active_id\": 1\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\": 1             # 0 没有参加过， 1 参加过\n        \"active_num\": 0         # 0 参与人数为0  n 参与人数为n\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/gift_active/views.py",
    "groupTitle": "gift_active",
    "name": "PostHuodongGift_activeStatus"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/award/winner",
    "title": "[数学常态活动] 河南抽奖排名",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"award_name\": \"ipad\",\n            \"user_id\": 591113,\n            \"city\": \"410400\",\n            \"portrait\": \"portrait/2017/09/09/2017090918151214417.png\",\n            \"school_name\": \"平顶山市卫东区矿工路小学\",\n            \"real_name\": \"啊啊啊\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* 显示登录身份的排名",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalAwardWinner"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/class/ranks",
    "title": "[数学常态活动]班级排名",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"phone\": \"13900000000\",\n            \"score\": 280,\n            \"is_open\": 1,\n            \"portrait\": \"https://file.m.tbkt.cn/upload_media/portrait/2015/05/26/20150526191718620086.png\",\n            \"user_name\": \"赵勇铮\",\n            \"id\": 383892\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalClassRanks"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/com/award/display",
    "title": "[数学常态活动]奖品信息",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"num\": 3,  # 奖品数量\n            \"sequence\": 1,  # 几等奖\n            \"end_num\": 0,     \n            \"active_type\": 1, # 奖品类型 1抽奖奖品 2排名奖品\n            \"start_num\": 0,   \n            \"active_id\": 1,  # 活动id\n            \"img_url\": \"http://file.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png\",\n            \"active_name\": \"ipad\"   # 奖品名字\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalComAwardDisplay"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/com/info",
    "title": "[数学常态活动]积分信息",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"score\": 0,   # 用户积分\n        \"num\": 0,\n        \"top\": 0\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalComInfo"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/com/score/detail",
    "title": "[数学常态活动]积分详情",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"item_name\": \"做作业\",\n            \"add_date\": \"09月12日 11:43:52\",\n            \"score\": 120\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalComScoreDetail"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/score/ranks",
    "title": "[数学常态活动]河南积分排名",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"city\": \"411700\",\n            \"score\": 1082111,\n            \"user_id\": 405269,\n            \"portrait\": \"portrait/2017/09/09/2017090915481764690.png\",\n            \"school_name\": \"创恒中学\",\n            \"real_name\": \"呃呃呃呃\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* 显示登录身份的排名",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalScoreRanks"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/stu/share",
    "title": "[数学常态活动]学生分享",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/stu/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalStuShare"
  },
  {
    "type": "",
    "url": "/huodong/sx/normal/stu/sign",
    "title": "[数学常态活动]学生签到",
    "group": "math_normal",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"msg\": \"签到获取60积分\"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "其他返回",
          "content": "{\n    \"message\": \"已签到\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_normal/stu/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalStuSign"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/add_tea_score",
    "title": "[暑假活动-学生] 学生进入活动教师加积分",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{    \"message\": \"没有对应教师\" or \"今天已经积过分了\" or \"积分成功\", \"next\": \"\", \"data\": \"\" , response\": \"ok\", \"error\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSAdd_tea_score"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/award/my_award",
    "title": "[暑假活动-学生]抽奖 我的奖品列表",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"user_id\": 405365,\n     \"user_name\": \"张笑\",\n     \"award_list\":[\n         {\n             \"award_type\": 4            # 1ipad    2卡通文具套盒  3卡通文具袋  4学科免费体验1个月  5谢谢参与\n             \"award_type\": \"语文学科体验一个月\"\n             \"add_time\":\"1496668496\"        # 获奖时间        时间戳格式\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSAwardMy_award"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/award/my_score",
    "title": "[暑假活动-学生]抽奖 用户自己总积分和可用抽奖次数",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"score\": 1140,            # 总积分  没有积分0\n     \"times\": 3            # 可以抽奖的次数    没有次数0\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSAwardMy_score"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/award/won_list",
    "title": "[暑假活动-学生] 轮播已获奖名单 取最近获得的",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"won_list\": [\n         {\"user_name\": \"杨铮\",\n         \"award_name\": \"文具套装\"     # 奖品名称\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSAwardWon_list"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/index",
    "title": "[暑假活动-学生]活动首页",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"score\": 30,            # 积分\n     \"rank_no\": 3            # 排名\n     \"open_status\": 1            # 英语学科  1开通 0未开通\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSIndex"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/index/open_at_once",
    "title": "[暑假活动-学生]首页 [公共]立即开通点击统计",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{app_id=32 # 英语学生32 数学学生35 语文学生43}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"status\": 1\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"缺少app_id 参数\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSIndexOpen_at_once"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/result/draw_lottery_rank",
    "title": "[暑假活动-学生]结束页 抽奖获奖名单",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{page_no=1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"rank_info\": [      # 请求的那一页为空的话，\"rank_info\":[]\n         {\"user_name\": \"杨铮\",\n         \"award_type\": 2\n         \"award_name\": \"宝视达护眼\"     # 奖品名称\n         \"school_name\":\"穿各行中学\"\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSResultDraw_lottery_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/result/total_score_rank",
    "title": "[暑假活动-学生]结束页 积分获奖名单",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{ page_no=1 }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"page_no\": 1,       # 当前页\n     \"rank_info\": [\n         {\"user_name\": \"杨铮\",\n         \"award_name\": \"小米平衡车\",\n         \"rank_no\": 1,\n         \"school_name\": \"创恒中学\",\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSResultTotal_score_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/share",
    "title": "[暑假活动-学生]分享活动",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{    \"message\": \"\",\n \"next\": \"\",\n \"data\": \"分享成功\",  or   \"今天已经分享一次了\"\n \"response\": \"ok\",\n \"error\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSShare"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/s/user_rank",
    "title": "[暑假活动-学生]所有用户排名",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"page_no\": 1}           # 每次请求10条",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n  \"data\": {\n     \"rank_info\": [\n             {\n                 \"user_name\": \"小明\",\n                 \"score\": 30,\n                 \"school_name\": \"创恒中学\"\n             },{},...\n         ],\n     \"page_num\":20\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"缺少page_no参数\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/stu.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordSUser_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/award/my_award",
    "title": "[暑假活动-教师]抽奖 我的奖品列表",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"user_id\": 405365,\n     \"user_name\": \"张笑\",\n     \"award_list\":[\n         {\n             \"award_type\": 4            # 1 ipad    2志高挂烫机  3精美天堂太阳伞   4金豆2个   5谢谢参与\n             \"award_name\": \"语文学科体验一个月\"\n             \"add_time\":\"1496668496\"        # 获奖时间        时间戳格式\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTAwardMy_award"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/award/my_score",
    "title": "[暑假活动-教师]抽奖 教师用户自己总积分和可用抽奖次数",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"score\": 8140,           # 总积分  没有积分0\n     \"times\": 4            # 可以抽奖的次数    没有次数0\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTAwardMy_score"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/award/won_list",
    "title": "[暑假活动-教师] 轮播已获奖名单",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"won_list\": [\n         {\"user_name\": \"杨铮\",\n         \"award_name\": \"文具套装\"     # 奖品名称\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTAwardWon_list"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/my_rank",
    "title": "[暑假活动-教师]我的积分、排名",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\",\n\"data\": {'rank_no':122, 'score': 1000 }, \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTMy_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/my_stu_rank",
    "title": "[暑假活动-教师]排名 所有班级学生积分排名",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{page_no=1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"page_num\": 5,      # 总业数\n     \"page_no\": 1,       # 当前页\n     \"rank_info\": [      # (1)请求的那一页为空 (2)教师班级下无学生，\"rank_info\":[]\n         {\"user_name\": \"杨铮\",\n         \"score\": 2000\n         \"rank_no\": 1\n         \"school_name\":\"创新中学\"\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回 注意，此信息由中间件返回",
          "content": "{\"message\": \"请先加入一个班级\", \"error\": \"no_class\", \"data\": null, \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTMy_stu_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/result/draw_lottery_rank",
    "title": "[暑假活动-教师]结束页 抽奖获奖名单",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"rank_info\": [      # 请求的那一页为空的话，\"rank_info\":[]\n         {\"user_name\": \"杨铮\",\n         \"award_type\": 2\n         \"award_name\": \"宝视达护眼\"     # 奖品名称\n         \"school_name\":\"创新中学\"\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTResultDraw_lottery_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/result/total_score_rank",
    "title": "[暑假活动-教师]结束页 总积分获奖名单",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{ page_no=1 }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"page_no\": 1,       # 当前页\n     \"rank_info\": [\n         {\n             \"award_name\": \"小米平衡车\",\n             \"score\": 100000,\n             \"award_type\": 1,\n             \"school_name\": \"创恒中学\",\n             \"user_name\": \"铮教师\"\n         },{},{}, ...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTResultTotal_score_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/send_open",
    "title": "[暑假活动-教师] 开通班级下学生学科",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": ', \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTSend_open"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/send_sms",
    "title": "[暑假活动-教师] 发短信给班级下学生",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{'content':'家长您好....',type:1 开通短信 0 普通短息}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"积分成功\", \"error\": \"\", \"data\": ', \"response\": \"ok\" , \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"发送短信，每天只能加分一次\", \"error\": \"\", \"data\": \"null\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTSend_sms"
  },
  {
    "type": "post",
    "url": "/huodong/summer_word/t/user_rank",
    "title": "[暑假活动-教师] 所有教师排名",
    "group": "summer_word",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n  \"data\": {\n      \"page_num\": 20,     # 总页数\n      \"page_no\": 1,       # 当前页\n     \"rank_info\": [\n             {\n                 \"user_name\": \"13600000000xs\",\n                 \"score\": 30,\n                 \"school_name\": \"创恒中学\"\n             },{},...\n         ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/summer_word/tea.py",
    "groupTitle": "summer_word",
    "name": "PostHuodongSummer_wordTUser_rank"
  },
  {
    "type": "post",
    "url": "/huodong/sx_questionnaire/result",
    "title": "[问卷调查] 结果",
    "group": "sx_questionnaire",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\":[{qid:1,option:'A,C',content:'叮叮叮，当当当'},{qid:2,option:''A,B,C,content:''}]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"请勿重复提交\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_questionnaire/view.py",
    "groupTitle": "sx_questionnaire",
    "name": "PostHuodongSx_questionnaireResult"
  },
  {
    "type": "post",
    "url": "/huodong/sx_questionnaire/status",
    "title": "[问卷调查] 提交",
    "group": "sx_questionnaire",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {status:1},  # 1:已做 , 0:未作\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"请勿重复提交\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_questionnaire/view.py",
    "groupTitle": "sx_questionnaire",
    "name": "PostHuodongSx_questionnaireStatus"
  },
  {
    "type": "post",
    "url": "/huodong/sx_questionnaire/submit",
    "title": "[问卷调查] 提交",
    "group": "sx_questionnaire",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{data:[{qid:1,option:'A,C',content:'叮叮叮，当当当'},{qid:2,option:''A,B,C,content:''}]}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {},\n \"response\": \"ok\",\n \"error\": \"\"\n }",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"请勿重复提交\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_questionnaire/view.py",
    "groupTitle": "sx_questionnaire",
    "name": "PostHuodongSx_questionnaireSubmit"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/add_open_score",
    "title": "[暑假活动 学生]学生开通加积分",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {\n    \"add_score\":0     # 1 加1000 积分   0 未开通不加积分\n  }\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAdd_open_score"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/add_tea_score",
    "title": "[暑假活动 学生]学生登录教师加积分",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {}\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAdd_tea_score"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/award",
    "title": "[暑假活动 抽奖]抽奖",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{app_id:35}   35：数学学生     43：语文学生    ,  32：英语学生",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"很遗憾，您本次未抽中任何奖品！\",\n  \"error\": \"\",\n  \"data\": {award:1} 1~4 中奖，5： 谢谢参与，6 积分不足\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"手速太快了，请稍后尝试\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAward"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/award/all",
    "title": "[暑假活动 学生]活动结果页 抽奖结果",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     app_id:35,   #35 学生   36 教师\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {}\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAwardAll"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/award/detail",
    "title": "[暑假活动 抽奖]抽奖详情",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{app_id:45}    # 36：教师，  35：学生，",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {\n        my_award:['2017年6月23日 22：35',  '精美雨伞一个'...],\n        all_award:['张晓燕在抽奖活动中获得精美天堂太阳伞1个'...]\n        is_smx: 1    1:表示三门峡获奖情况\n        }\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAwardDetail"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/award/result",
    "title": "[暑假活动 学生]滚动显示 抽奖结果",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     app_id:35,   #35 学生   36 教师\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {}\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSAwardResult"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/get_grade",
    "title": "[暑假活动 学生]获取所选年级",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": {\"grade_id\": \"1\"}, \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSGet_grade"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/list",
    "title": "[暑假活动 学生]试卷列表",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n grade_id:1\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {\n    \"苏教版\": [\n      {\n        \"status\": \"-1\",-1：未作  0： 未完成，1：已完成\n        \"name\": \"二年级\",\n        \"paper_name\": \"暑假天天练（一）\",\n        \"v_name\": \"苏教版\",\n        \"id\": \"231\",\n        \"paper_id\": \"19828\"\n      },\n      {\n        \"status\": \"0\",\n        \"name\": \"二年级\",\n        \"paper_name\": \"暑假天天练（二）\",\n        \"v_name\": \"苏教版\",\n        \"id\": \"231\",\n        \"paper_id\": \"19829\"\n      }]\n      \"人教版\":[...]\n  },\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/paper.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSList"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/paper",
    "title": "[暑假活动 学生]试卷详情",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n object_id:19858 #试卷id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {\n      \"answer\": [\n      {\n        \"ask_list\": [\n          {\n            \"ask_id\": \"125401\",\n            \"option\": \"C\",\n            \"result\": 1\n          }\n        ],\n        \"question_id\": \"67725\"\n      }...\n    ],\n    \"status\": 1,\n    \"qid\": [\n      \"67725\",\"67726\",...\n    ],\n    \"test_id\": \"109257\",\n    \"name\": \"暑假天天练（一）\",\n    \"questions\": [\n      {\n        \"asks\": [\n          {\n            \"knowledge\": [\n              {\n                \"ask_id\": 93402,\n                \"id\": 3447,\n                \"video_url\": \"http://file.tbkt.cn/upload_media/knowledge/video/2014/03/19/20140319112221404718.mp4\",\n                \"name\": \"100以内数的顺序\"\n              }\n            ],\n            \"video_url\": \"http://file.tbkt.cn/upload_media/knowledge/video/2014/03/19/20140319112219825730.mp4\",\n            \"title\": \"1\",\n            \"user_answer\": \"\",\n            \"number\": 1,\n            \"options\": [\n              {\n                \"option\": \"A\",\n                \"image\": {},\n                \"ask_id\": 93402,\n                \"is_right\": 0,\n                \"content\": \"41、42、43、44、45、46、47、48、49\",\n                \"id\": 489626\n              },\n              {\n                \"option\": \"B\",\n                \"image\": {},\n                \"ask_id\": 93402,\n                \"is_right\": 0,\n                \"content\": \"44\",\n                \"id\": 489627\n              },\n              {\n                \"option\": \"C\",\n                \"image\": {},\n                \"ask_id\": 93402,\n                \"is_right\": 1,\n                \"content\": \"40、41、42、43、44、45、46、47、48、49\",\n                \"id\": 489628\n              },\n              {\n                \"option\": \"D\",\n                \"image\": {},\n                \"ask_id\": 93402,\n                \"is_right\": 0,\n                \"content\": \"14、24、34、44、54、65、74、84、94\",\n                \"id\": 489629\n              }\n            ],\n            \"parse\": [\n              {\n                \"content\": \"十位上是4的两位数有（40、41、42、43、44、45、46、47、48、49）。\",\n                \"images\": \"\",\n                \"image\": {}\n              }\n            ],\n            \"user_result\": \"\",\n            \"right_option\": \"C\",\n            \"subject\": {\n              \"content\": \"十位上是4的两位数有。\",\n              \"images\": \"\",\n              \"image\": {}\n            },\n            \"id\": 93402,\n            \"question_id\": 67725\n          }\n        ],\n        \"video_url\": \"\",\n        \"number\": 1,\n        \"display\": 1,\n        \"type\": 1,\n        \"id\": 67725,\n        \"subject\": {\n          \"content\": \"\",\n          \"image\": {\n            \"url\": \"\"\n          }\n        }\n      },\n      {...}\n    ]\n  },\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/paper.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSPaper"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/question",
    "title": "[暑假活动 学生]获取试题",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"object_id\": 8459 ,试卷id\n \"qid\":49484\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n        \"message\": \"\",\n        \"next\": \"\",\n        \"data\": [\n                    {\n                        \"category\": 1,\n                        \"asks\": [\n                            {\n                                \"title\": \"1\",\n                                \"user_answer\": \"\",\n                                \"number\": 1,\n                                \"id\": 22260,\n                                \"right_option\": \"C\",\n                                \"question_id\": 49484,\n                                \"options\": [\n                                    {\n                                        \"content\": \"原计划每天完成$130$套服装\",\n                                        \"option\": \"A\",\n                                        \"image\": {},\n                                        \"ask_id\": 22260,\n                                        \"id\": 317695,\n                                        \"is_right\": 0\n                                    },\n                                    {\n                                        \"content\": \"原计划每天完成$135$套服装\",\n                                        \"option\": \"B\",\n                                        \"image\": {},\n                                        \"ask_id\": 22260,\n                                        \"id\": 317696,\n                                        \"is_right\": 0\n                                    },\n                                    {\n                                        \"content\": \"原计划每天完成$125$套服装\",\n                                        \"option\": \"C\",\n                                        \"image\": {},\n                                        \"ask_id\": 22260,\n                                        \"id\": 317697,\n                                        \"is_right\": 1\n                                    },\n                                    {\n                                        \"content\": \"原计划每天完成$140$套服装\",\n                                        \"option\": \"D\",\n                                        \"image\": {},\n                                        \"ask_id\": 22260,\n                                        \"id\": 317698,\n                                        \"is_right\": 0\n                                }\n                            ],\n                            \"subject\": {\n                                \"content\": \"某服装制造厂要在开学前赶制$3000$套校服\",\n                                \"images\": \"\",\n                                \"image\": {}\n                            }\n                        }\n                    ],\n                    \"video_url\": \"\",\n                    \"number\": 1,\n                    \"id\": 49484,\n                    \"display\": 1,\n                    \"structure\": 3,\n                    \"subject\": {}\n                }\n            ],\n            \"response\": \"ok\",\n            \"error\": \"\"\n    }",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/paper.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSQuestion"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/rank",
    "title": "[暑假活动 学生]排行",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     is_smx: 1       1:是三门峡排行\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": [\n  \"rank\":\n    {\n      \"user_id\": \"1185342\",\n      \"num\": 1,\n      \"user_name\": \"郭小帅\",\n      \"score\": \"370\",\n      \"school_name\": \"睢县河堤乡姜庄小学\"\n    },\n    {\n      \"user_id\": \"2180866\",\n      \"num\": 2,\n      \"user_name\": \"杨铮\",\n      \"score\": \"110\",\n      \"school_name\": \"商丘市八一路小学\"\n    }...\n  ],\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSRank"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/rank/result",
    "title": "[暑假活动 学生]活动结果页 排行结果",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     app_id:35,    35：学生   36：教师\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {}\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSRankResult"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/rank/result",
    "title": "[暑假活动 学生]活动结果页 排行结果",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     app_id:35,    35：学生   36：教师\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {status:True } # True 未结束，False :结束\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSRankResult"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/result",
    "title": "[暑假活动 学生]结果页",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{test_id:109257}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": {\n    \"knowledge_list\": [\n      {\n        \"knowledge_id\": \"3085\",\n        \"name\": \"十几减8\"\n      },\n      {\n        \"knowledge_id\": \"3080\",\n        \"name\": \"十几减9\"\n      },\n      {\n        \"knowledge_id\": \"3088\",\n        \"name\": \"十几减5、4、3、2\"\n      },\n      {\n        \"knowledge_id\": \"3447\",\n        \"name\": \"100以内数的顺序\"\n      }\n    ],\n    \"all_qid\": [\n      \"67725\",\n      \"67726\",\n      \"11303\",\n      \"11997\"\n    ],\n    \"knowledge_count\": 4,\n    \"wrong_qid\": [\n      \"67726\",\n      \"11303\"\n    ],\n    \"test_name\": \"暑假天天练（一）\",\n    \"test_id\": 109257\n  },\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/paper.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSResult"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/set_grade",
    "title": "[暑假活动 学生]设置年级",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{'grade_id':1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": [], \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n  \"message\": \"已设置过班级，不能重复设置\",\n  \"error\": \"\",\n  \"data\": \"\",\n  \"response\": \"fail\",\n  \"next\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSSet_grade"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/share",
    "title": "[暑假活动 学生]分享",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"分享成功，加10分\",\n  \"error\": \"\",\n  \"data\": \"\",\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"每天只能分享一次\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSShare"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/submit",
    "title": "[暑假活动 学生]提交",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"type\":1,   1卷子，3个性化\n\"object_id\":\"19858\",    paper_id /个性化测试id\n\"status\":1,1 完成 0 未完成\n\"data\":[{\"ask_list\":[{\"ask_id\":61745,\"option\":\"C\",\"result\":1}],\"question_id\":45949}...]\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": {\"test_id\": \"109257\"}, \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/paper.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSSubmit"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/s/user_rank",
    "title": "[暑假活动 学生]获取学生 分数和排行",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{'grade_id':1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": {\"score\": 100, \"rank\": 2}, \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/stu/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerSUser_rank"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/award",
    "title": "[暑假活动 抽奖]教师抽奖",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{app_id:35}   36：数学教师     42 ：语文教师   ,  34：英语教师",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"很遗憾，您本次未抽中任何奖品！\",\n  \"error\": \"\",\n  \"data\": {award:1} 1~4 中奖，5： 谢谢参与，6 积分不足\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"手速太快了，请稍后尝试\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTAward"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/rank",
    "title": "[暑假活动 教师]排行",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n     is_smx:0   1:是三门峡\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": [\n  \"rank\":\n    {\n      \"user_id\": \"1185342\",\n      \"num\": 1,\n      \"user_name\": \"郭小帅\",\n      \"score\": \"370\",\n      \"school_name\": \"睢县河堤乡姜庄小学\"\n    },\n    {\n      \"user_id\": \"2180866\",\n      \"num\": 2,\n      \"user_name\": \"杨铮\",\n      \"score\": \"110\",\n      \"school_name\": \"商丘市八一路小学\"\n    }...\n  ],\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTRank"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/send_open",
    "title": "[暑假活动 教师]发送开通短信",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": ', \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTSend_open"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/send_sms",
    "title": "[暑假活动 教师]发送短信",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{'content':'家长您好....'}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": ', \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTSend_sms"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/unit_rank",
    "title": "[暑假活动 教师]排行",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     p:1,\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n  \"message\": \"\",\n  \"error\": \"\",\n  \"data\": [\n  \"rank\":\n    {\n      \"user_id\": \"1185342\",\n      \"num\": 1,\n      \"user_name\": \"郭小帅\",\n      \"score\": \"370\",\n      \"school_name\": \"睢县河堤乡姜庄小学\"\n    },\n    {\n      \"user_id\": \"2180866\",\n      \"num\": 2,\n      \"user_name\": \"杨铮\",\n      \"score\": \"110\",\n      \"school_name\": \"睢县河堤乡姜庄小学\"\n    }...\n  ],\n  \"response\": \"ok\",\n  \"next\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"no_app_id\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTUnit_rank"
  },
  {
    "type": "post",
    "url": "/huodong/sx_summer/t/user_rank",
    "title": "[暑假活动 教师]获取教师 分数和排行",
    "group": "sx_summer",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": {\"score\": 100, \"rank\": 2}, \"response\": \"ok\", \"next\": \"\"}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTUser_rank"
  },
  {
    "type": "get",
    "url": "/system/bump_version",
    "title": "[系统]升级版本号",
    "group": "system",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"type\":客户端类型}\n\ntype客户端类型:\n9安卓学生 10安卓教师 11苹果学生 12苹果教师 13 H5学生 14 H5教师 15 H5活动 16 H5学测评学生 17 H5学测评教师",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"id\": 1,  # system_version表主键ID\n        \"api\": 99  # 升级后的内部版本号\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": \"找不到该类型的版本信息\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemBump_version"
  },
  {
    "type": "get",
    "url": "/system/download/<type>",
    "title": "[系统]APK下载地址",
    "group": "system",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "type: 客户端类型 9安卓学生 10安卓教师",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "成功直接开始下载文件",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "失败返回404",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemDownloadType"
  },
  {
    "type": "get",
    "url": "/system/info",
    "title": "[系统]系统信息",
    "group": "system",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"cs_phone\": \"12556185\",  # 客服电话\n        \"file_size\": 1024*1024,  # 语文上传大小\n        \"upload_url\": \"http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=\",  # 上传服务器URL\n        \"hosts\": {\n            \"api\": \"http://mapi.m.jxtbkt.com\", # 公共接口\n            \"apisx\": \"http://mapisx.m.jxtbkt.com\",  # 数学接口\n            \"apisx2\": \"http://mapisx2.m.jxtbkt.com\",  # 数学接口\n            \"apiyy\": \"http://mapiyy.m.jxtbkt.com\"   # 英语接口\n            \"apiyw\": \"http://mapiyw.m.jxtbkt.com\"   # 语文接口\n            \"vuestu\": \"http://stu.m.jxtbkt.com\"   # 英语接口\n            \"vuestusx\": \"http://stusx.m.jxtbkt.com\"   # 英语接口\n            \"vuestusx2\": \"http://stusx2.m.jxtbkt.com\"   # 英语接口\n            \"vuestuyy\": \"http://stuyy.m.jxtbkt.com\"   # 英语接口\n            \"vuestuyw\": \"http://stuyw.m.jxtbkt.com\"   # 英语接口\n            \"vuetea\": \"http://tea.m.jxtbkt.com\"   # 英语接口\n            \"joinclass_style\": 1, # 1只能输入老师手机号加班级 2是允许手工选地市学校加班级\n        },  # 接口地址\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* upload_url最后的upType=xxx需要调用者补充完整. \n  比如头像是http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=portrait, \n  学测评是http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=xcp",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemInfo"
  },
  {
    "type": "get",
    "url": "/system/ping",
    "title": "[系统]检查网站是否可用",
    "group": "system",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {},\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemPing"
  },
  {
    "type": "get",
    "url": "/system/platforms",
    "title": "[系统]平台配置列表",
    "group": "system",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"id\":平台ID}\n\n*如果不指定平台ID则返回所有平台配置",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"province\": \"410000\",  # 省行政编码\n            \"is_sms\": 1,    # 是否能发短信\n            \"is_open\": 1,   # 是否要开通学科\n            \"id\": 1,        # 平台ID\n            \"name\": \"河南\"  # 平台名称\n            \"is_setprofile\":1       # 是否可以设置个人信息或班级\n        },\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemPlatforms"
  },
  {
    "type": "get",
    "url": "/system/version",
    "title": "[系统]检查版本",
    "group": "system",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"type\":客户端类型, \"api\":客户端当前内部版本号}\n\ntype客户端类型:\n9安卓学生 10安卓教师 11苹果学生 12苹果教师 13 H5学生 14 H5教师 15 H5活动 16 H5学测评学生 17 H5学测评教师",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"title\": \"同步课堂手机客户端\",\n        \"last_version\": \"2.3.12\",\n        \"release_date\": \"2016-06-27 10:55:04\",\n        \"update\": 2,  # 0:不更新  1:选择性更新  2:强制更新\n        \"content\": \"2.2.3巫妖王\",\n        \"download\": \"http://file.tbkt.cn/upload_media/apk/tbkt_stu_android/tbkt_stu_android-release-16.apk\"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": \"找不到该类型的版本信息\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "GetSystemVersion"
  },
  {
    "type": "post",
    "url": "/system/active_info",
    "title": "[系统]是否开启活动权限",
    "group": "system",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"extend\": {},\n            \"banner_url\": \"\",           # banner 地址\n            \"banner_end\": \"2017-05-21 23:59:59\",    # banner图上的结束时间\n            \"name\": \"商丘市拓城县我爱记单词\",          # 活动时间\n            \"banner_begin\": \"2017-05-09 00:00:00\",      # banner图上的开始时间\n            \"is_open\": 2,                               # is_open = 0, banner不显示， 否则显示\n            \"begin_url\": \"/huodong/sq_word/index\",      # 活动的入口地址\n            \"active_id\": 26                             # 活动id\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "PostSystemActive_info"
  },
  {
    "type": "post",
    "url": "/system/blocks",
    "title": "[系统]模块展示接口",
    "group": "system",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"type\":\"类型名\"}\n\n*type: APP数学appsx, APP语文appyw, APP英语appyy, APP其他appqt",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"opensubject_alert\": \"您还未开通数学\",\n        \"blocks\": [\n            {\n                \"alias\": \"think\",\n                \"charge\": 1\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/system/views.py",
    "groupTitle": "system",
    "name": "PostSystemBlocks"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/all_recording",
    "title": "[语文常态活动]全省学生录音排名",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"active\": [\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"狐假虎威\",  #文章名称\n                \"user_id\": 591113,  #用户id\n                \"ballot_num\": 7,  #票数\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",  #录音\n                \"ch_Code\": 10610102,  #文章code\n                \"unit_id\": 0,  #班级id\n                \"score\": 47,  #积分\n                \"school_dict\": {\n                    \"portrait\": \"portrait/2017/06/23/20170623122616857641.png\",\n                    \"city\": \"410400\",\n                    \"user_id\": 591113,\n                    \"school_name\": \"叶县实验学校\",  #学校\n                    \"real_name\": \"创恒\"  #姓名\n                },\n                \"record_id\": 6,  #录音id\n                \"id\": 1020030,\n                \"active_id\": 4\n            },\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"善良的狐狸\",\n                \"user_id\": 378394,\n                \"ballot_num\": 5,\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",\n                \"ch_Code\": 10610101,\n                \"unit_id\": 0,\n                \"score\": 45,\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"410200\",\n                    \"user_id\": 378394,\n                    \"school_name\": \"鼓楼区杨砦小学\",\n                    \"real_name\": \"李果果\"\n                },\n                \"record_id\": 5,\n                \"id\": 1020028,\n                \"active_id\": 4\n            }\n        ],\n        \"page_count\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySAll_recording"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/article_all",
    "title": "[语文常态活动]学生端范文文章列表",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1 #范文朗读的页数\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"recording\": {\n                \"ballot_num\": 3,  #票数\n                \"user_id\": 1,  #用户id\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",#录音\n                \"ch_Code\": 10610101,  #文章编码\n                \"state\": 2,  #状态 #0未录制，1，已录制，2已分享\n                \"id\": 3,  #录音id\n                \"add_time\": 1505188588  #录音时间\n            },\n            \"ch_Name\": \"善良的狐狸\",  #文章id\n            \"ch_Code\": \"10610101\"   #文章编码\n        },\n        {\n            \"recording\": 0,    #0：未录音\n            \"ch_Name\": \"狐假虎威\",  #文章名称\n            \"ch_Code\": \"10610102\"  #文章编码\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySArticle_all"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/article_details",
    "title": "[语文常态活动]文章详情页",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"ch_Name\":艾尔的新毯子 #文章名称\n\"ch_Code\":1 #文章code\n\"state\":0，#0未录制，1，已录制，2已分享\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n       \"ch_Name\": \"艾尔的新毯子\",\n        \"state\": 1, #state是否已推荐: 1，已推荐，0，未推荐\n        \"ti_Contents\": \"从前在大森林里有一只叫森森的小狐狸，他很孤独，因为他没有朋友，小动物们都不和他玩，因为动物们都觉的狐狸是最坏的动物，再加上他的爸爸是骗走乌鸦肉的那只狐狸乌鸦们更是对他恨之入骨，但森森一点也不坏，他连一只蚂蚁都没伤害过。但动物们都不相信他。森森感到十分伤心。 ||一天，森森正在森林里闲逛 ，突然听到前面有动物喊“救命”，森森寻着声音跑过去，发现一只大灰狼正张牙舞爪地扑向一只小白兔，正在这危急关头，森森突然向前一跃，挡住了大灰狼扑向小白兔爪子，并大声向居住在附近的动物们求救。大灰狼锋利的爪子刺进了森森的肉里，森森顿时流了许多血，不一会就昏了过去。这时动物们听到求救声都纷纷拿着工具陆续赶了过来，大灰狼见势不妙，慌忙逃走了。 ||当森森醒来时，发现自己躺在一张床上，动物们都围在他的床边，看到它醒来都露出了笑容，这时兔妈妈拉住森森的手说“ 谢谢你救了我的孩子，我们以前错怪了你，你是一个勇敢而又善良的好孩子！” ||从此森森和其他动物们成了好朋友，一起快乐的生活在森林里。 \"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySArticle_details"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/article_recom",
    "title": "[语文常态活动]学生端老师推荐文章列表",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1 #页数\n\"t_id\": 1 #老师id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"recording\": 0,  #0，未录音\n            \"ch_Name\": \"艾尔的新毯子\",  #文章名称\n            \"ch_Code\": 10610103,  #文章编码\n            \"add_time\": \"2017-09-11\"  #推荐日期\n        },\n        {\n            \"recording\": {\n                \"ballot_num\": 3,  #票数\n                \"user_id\": 1,  #学生id\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",  #录音路径\n                \"ch_Code\": 10610101,#文章编码\n                \"state\": 2,  #状态1，已录制，2已分享\n                \"id\": 3,  #录音id\n                \"add_time\": 1505188588  #录音/分享的最后时间\n            },\n            \"ch_Name\": \"善良的狐狸\", #文章名称\n            \"ch_Code\": 10610101,   #文章编码\n            \"add_time\": \"2017-09-12\"  \"  #推荐日期\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySArticle_recom"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/class_ranking",
    "title": "[语文常态活动]班级排名",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1, #当前页数\n\"class_id\":1班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"active\": [\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"狐假虎威\",  #文章名称\n                \"user_id\": 591113,\n                \"ballot_num\": 7,  #票数\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\", #录音\n                \"ch_Code\": 10610102,  #文章code\n                \"unit_id\": 7,  #年级id\n                \"score\": 47,  #积分\n                \"school_dict\": {\n                    \"portrait\": \"portrait/2017/06/23/20170623122616857641.png\",  #头像\n                    \"city\": \"410400\",\n                    \"user_id\": 591113,\n                    \"school_name\": \"叶县实验学校\",  #学校\n                    \"real_name\": \"创恒\" #姓名\n                },\n                \"record_id\": 6,  录音id\n                \"id\": 1020030,\n                \"active_id\": 4\n            },\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"善良的狐狸\",\n                \"user_id\": 378394,\n                \"ballot_num\": 5,\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",\n                \"ch_Code\": 10610101,\n                \"unit_id\": 7,\n                \"score\": 45,\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"410200\",\n                    \"user_id\": 378394,\n                    \"school_name\": \"鼓楼区杨砦小学\",\n                    \"real_name\": \"李果果\"\n                },\n                \"record_id\": 5,\n                \"id\": 1020028,\n                \"active_id\": 4\n            }\n        ],\n        \"page_count\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySClass_ranking"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/s_integral_list",
    "title": "[语文常态活动]结束页",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p_begin\":1, #当前页数\n\"is_type\":1，按奖品，2，按积分来\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"is_state\": 1,\n        \"active_data\": [\n            {\n                \"user_name\": \"李果果\",\n                \"user_id\": 2661647,\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"411200\",\n                    \"user_id\": 2661647,\n                    \"school_name\": \"湖滨区磁钟乡杨窑中心小学\",\n                    \"real_name\": \"吴芮老师\"\n                },\n                \"award_name\": \"谢谢参与\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySS_integral_list"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/share_activity",
    "title": "[语文常态活动]活动页面分享",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"is_open\":1  #是否开通\n\"class_id\":1, #班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": 1, #添加成功，2#添加失败\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySShare_activity"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/s/user_rank",
    "title": "[语文常态活动]学生端积分 排名",
    "group": "yw_hd_s",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"sampling\": 0,  #抽奖次数\n        \"score\": 0,  #总分数\n        \"rank_no\": 0  #排名\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "GetHuodongYw_activitySUser_rank"
  },
  {
    "type": "post",
    "url": "/huodong/yw_activity/s/ballot_integral",
    "title": "[语文常态活动]分享获得投票入库",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"ch_Code\":111 #文章编码\n\"recording_id\" :录音id,\n\"is_open\":1 #\"is_open\":1，已开通，0未开通\n\"user_id\":1 #登录的用户\n\"class_id\":班级id\n\"city_id\":城市id\n\"\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":1，#1，投票成功，0投票失败\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "PostHuodongYw_activitySBallot_integral"
  },
  {
    "type": "post",
    "url": "/huodong/yw_activity/s/index",
    "title": "[语文常态活动]学生端活动首页，判断学生和对应老师是否要加积分（学生首进/每日首次入学生/老师加积分,）",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"t_id\":1，老师id\n\"class_id\":1 #班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":[1,\"开通成功！获得 1000积分\"],# 1:已开通2：未开通\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "PostHuodongYw_activitySIndex"
  },
  {
    "type": "post",
    "url": "/huodong/yw_activity/s/post_recording",
    "title": "[语文常态活动]学生端录音入库",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"ch_Code\":1, #文章code\n\"json_info\":\"\"#录音路径\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":1 #录音路径\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "PostHuodongYw_activitySPost_recording"
  },
  {
    "type": "post",
    "url": "/huodong/yw_activity/s/recording_integral",
    "title": "[语文常态活动]文章当天首次分享加积分",
    "group": "yw_hd_s",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"recording_id\" :录音id\n\"share_time\" :最新分享时间\n\"state\": 1,  #状态 #0未录制，1，已录制，2已分享\n\"is_open\":1，已开通，0未开通\n\"class_id\":1 #班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":{}\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/stu/index.py",
    "groupTitle": "yw_hd_s",
    "name": "PostHuodongYw_activitySRecording_integral"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/article_details",
    "title": "[语文常态活动]文章详情页",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"ch_Name\":艾尔的新毯子 #文章名称\n\"state\":1,#state是否已推荐: 1，已推荐，0，未推荐\n\"ch_Code\":1 #文章code\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n       \"ch_Name\": \"艾尔的新毯子\",\n        \"state\": 1, #state是否已推荐: 1，已推荐，0，未推荐\n        \"ti_Contents\": \"从前在大森林里有一只叫森森的小狐狸，他很孤独，因为他没有朋友，小动物们都不和他玩，因为动物们都觉的狐狸是最坏的动物，再加上他的爸爸是骗走乌鸦肉的那只狐狸乌鸦们更是对他恨之入骨，但森森一点也不坏，他连一只蚂蚁都没伤害过。但动物们都不相信他。森森感到十分伤心。 ||一天，森森正在森林里闲逛 ，突然听到前面有动物喊“救命”，森森寻着声音跑过去，发现一只大灰狼正张牙舞爪地扑向一只小白兔，正在这危急关头，森森突然向前一跃，挡住了大灰狼扑向小白兔爪子，并大声向居住在附近的动物们求救。大灰狼锋利的爪子刺进了森森的肉里，森森顿时流了许多血，不一会就昏了过去。这时动物们听到求救声都纷纷拿着工具陆续赶了过来，大灰狼见势不妙，慌忙逃走了。 ||当森森醒来时，发现自己躺在一张床上，动物们都围在他的床边，看到它醒来都露出了笑容，这时兔妈妈拉住森森的手说“ 谢谢你救了我的孩子，我们以前错怪了你，你是一个勇敢而又善良的好孩子！” ||从此森森和其他动物们成了好朋友，一起快乐的生活在森林里。 \"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTArticle_details"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/article_list",
    "title": "[语文常态活动]教师端推荐文章列表",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1 #当前页数\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"data\": [\n            {\n                \"ch_Name\": \"善良的狐狸\",\n                \"ch_Code\": \"10610101\",\n                \"state\": 1\n            }\n        ],\n        \"page_count\": 33  #总页数\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTArticle_list"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/class_ranking",
    "title": "[语文常态活动]班级排名",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1, #当前页数\n\"class_id\":\"1\"班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"active\": [\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"狐假虎威\",  #文章名称\n                \"user_id\": 591113,  用户id\n                \"ballot_num\": 7,\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\", #录音\n                \"ch_Code\": 10610102,  #文章编码\n                \"unit_id\": 7,  #班级id\n                \"score\": 47,  # 积分\n                \"school_dict\": {\n                    \"portrait\": \"portrait/2017/06/23/20170623122616857641.png\",  #头像\n                    \"city\": \"410400\",\n                    \"user_id\": 591113,\n                    \"school_name\": \"叶县实验学校\", #学校\n                    \"real_name\": \"创恒\"  #姓名\n                },\n                \"record_id\": 6, #录音id\n                \"id\": 1020030,\n                \"active_id\": 4\n            },\n            {\n                \"city\": \"0\",\n                \"ch_name\": \"善良的狐狸\",\n                \"user_id\": 378394,\n                \"ballot_num\": 5,\n                \"json_info\": \"http://11192.168.99.100:8008/huodong/yw_activity/s/post_recording\",\n                \"ch_Code\": 10610101,\n                \"unit_id\": 7,\n                \"score\": 45,\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"410200\",\n                    \"user_id\": 378394,\n                    \"school_name\": \"鼓楼区杨砦小学\",\n                    \"real_name\": \"李果果\"\n                },\n                \"record_id\": 5,\n                \"id\": 1020028,\n                \"active_id\": 4\n            }\n        ],\n        \"page_count\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTClass_ranking"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/t_integral_list",
    "title": "[语文常态活动]结束页",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p_begin\":1, #当前页数\n\"is_type\":1，按奖品，2，按积分来\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"is_state\": 1,\n        \"active_data\": [\n            {\n                \"user_name\": \"李果果\",\n                \"user_id\": 378394,\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"410200\",\n                    \"user_id\": 378394,\n                    \"school_name\": \"鼓楼区杨砦小学\",\n                    \"real_name\": \"李果果\"\n                },\n                \"award_name\": \"谢谢参与\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTT_integral_list"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/teacher_ranking",
    "title": "[语文常态活动]教师排名",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"p\":1 #当前页数\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"active\": [\n            {\n                \"school_dict\": {\n                    \"portrait\": \"http://user.tbkt.cn/site_media/images/profile/default-student.png\",\n                    \"city\": \"411200\",\n                    \"user_id\": 2661647,\n                    \"school_name\": \"湖滨区磁钟乡杨窑中心小学\",  #学校名称\n                    \"real_name\": \"吴芮老师\"   #用户名称\n                },\n                \"score\": 47,  #分数\n                \"user_id\": 2661647   #用户id\n            }\n        ],\n        \"page_count\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTTeacher_ranking"
  },
  {
    "type": "get",
    "url": "/huodong/yw_activity/t/user_rank",
    "title": "[语文常态活动]学生端积分 排名",
    "group": "yw_hd_t",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"sampling\": 0,  #抽奖次数\n        \"score\": 0,  #总分数\n        \"rank_no\": 0  #排名\n        \"city_id\":1 #城市id\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "GetHuodongYw_activityTUser_rank"
  },
  {
    "type": "post",
    "url": "/huodong/yw_activity/t/recommend_article",
    "title": "[语文常态活动]教师端推荐文章给学生入库",
    "group": "yw_hd_t",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"ch_Code\":1 #章节的code\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",  #\"message\": \"今日已推荐过文章\",\n    \"next\": \"\",\n    \"data\":\"\"\n    \"response\": \"ok\",  #\"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "PostHuodongYw_activityTRecommend_article"
  },
  {
    "type": "post",
    "url": "/huodong/yy/normal/index",
    "title": "[英语常态活动]首页",
    "group": "yy_normal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"score\": 210,\n        \"rank_no\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yy_normal/views.py",
    "groupTitle": "yy_normal",
    "name": "PostHuodongYyNormalIndex"
  },
  {
    "type": "post",
    "url": "/huodong/yy/normal/rank",
    "title": "[英语常态活动]用户排名",
    "group": "yy_normal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"rank_info\": [\n            {\n                 \"portrait\": \"https://file.m.tbkt.cn/upload_media/portrait/2017/03/06/20170306102941170594.png\",\n                \"score\": 190,\n                \"user_id\": 2465828,\n                \"school_name\": \"创恒中学\",\n                \"real_name\": \"小张\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yy_normal/views.py",
    "groupTitle": "yy_normal",
    "name": "PostHuodongYyNormalRank"
  },
  {
    "type": "post",
    "url": "/huodong/yy/normal/tasks",
    "title": "[英语常态活动]每日任务完成情况",
    "group": "yy_normal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"test\": 0,\n        \"receive\": 0,\n        \"status\": 0,\n        \"mouse\": 0,\n        \"ballon\": 0,\n        \"time_def\": \"13:42:07\",\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "./apps/yy_normal/views.py",
    "groupTitle": "yy_normal",
    "name": "PostHuodongYyNormalTasks"
  }
] });
