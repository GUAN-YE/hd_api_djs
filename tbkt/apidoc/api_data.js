define({ "api": [
  {
    "type": "post",
    "url": "/huodong/rz/do_paper",
    "title": "[汝州活动二期]做试卷",
    "group": "RzPaperActive",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"sheet\": [\n            {\n                \"answer\": \"\",\n                \"ask_id\": 3500,\n                \"option_id\": 0,\n                \"result\": -1,\n                \"question_id\": 3300\n            },\n            {\n                \"answer\": \"\",\n                \"ask_id\": 3292,\n                \"option_id\": 0,\n                \"result\": -1,\n                \"question_id\": 3104\n            }\n            ],\n            \"numbers\": [\n                {\n                    \"qid\": 3300,\n                    \"ask_no\": 1,\n                    \"aid\": 3500\n                },\n                {\n                    \"qid\": 3104,\n                    \"ask_no\": 2,\n                    \"aid\": 3292\n                }\n            ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/rz_paper/views.py",
    "groupTitle": "RzPaperActive",
    "name": "PostHuodongRzDo_paper"
  },
  {
    "type": "post",
    "url": "/huodong/rz/paper_result",
    "title": "[汝州活动二期]试卷结果",
    "group": "RzPaperActive",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"number\": 2,        # 总习题数\n        \"wrong_number\": 1   # 错误习题数\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/rz_paper/views.py",
    "groupTitle": "RzPaperActive",
    "name": "PostHuodongRzPaper_result"
  },
  {
    "type": "post",
    "url": "/huodong/rz/paper_result_detail",
    "title": "[汝州活动二期]试卷结果详情",
    "group": "RzPaperActive",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n \"type_id\": 1    # 1 全部习题， 2 错题\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n   \"data\": {\n        \"sheet\": [\n            {\n                \"no\": 2,\n                \"qid\": 3300,\n                \"oid\": 19321,\n                \"result\": 0,\n                \"right_answer\": \"A\",\n                \"answer\": \"A\",\n                \"aid\": 3500\n            }\n        ],\n        \"question\": [\n            {\n                \"video_image\": \"\",\n                \"asks\": [\n                    {\n                        \"video_image\": \"\",\n                        \"video_url\": \"\",\n                        \"no\": 2,\n                        \"user_answer\": \"A\",\n                        \"user_option_id\": null,\n                        \"listen_audio\": \"\",\n                        \"options\": [\n                            {\n                                \"content\": \"No, she can't.\",\n                                \"option\": \"A\",\n                                \"image\": \"\",\n                                \"ask_id\": 3500,\n                                \"link_id\": -1,\n                                \"id\": 10432,\n                                \"is_right\": 1\n                            },\n                            {\n                                \"content\": \"Can he make a cake?\",\n                                \"option\": \"B\",\n                                \"image\": \"\",\n                                \"ask_id\": 3500,\n                                \"link_id\": -1,\n                                \"id\": 10433,\n                                \"is_right\": 0\n                            },\n                            {\n                                \"content\": \"No, he can't.\",\n                                \"option\": \"C\",\n                                \"image\": \"\",\n                                \"ask_id\": 3500,\n                                \"link_id\": -1,\n                                \"id\": 10434,\n                                \"is_right\": 0\n                            },\n                            {\n                                \"content\": \"Yes, he can.\",\n                                \"option\": \"D\",\n                                \"image\": \"\",\n                                \"ask_id\": 3500,\n                                \"link_id\": -1,\n                                \"id\": 10435,\n                                \"is_right\": 0\n                            }\n                        ],\n                        \"parse\": {\n                            \"content\": \"\",\n                            \"images\": []\n                        },\n                        \"answer\": \"A\",\n                        \"listen_text\": \"\",\n                        \"user_result\": 0,\n                        \"duration\": -1,\n                        \"user_option\": null,\n                        \"right_option\": {\n                            \"content\": \"No, she can't.\",\n                            \"option\": \"A\",\n                            \"image\": \"\",\n                            \"ask_id\": 3500,\n                            \"link_id\": -1,\n                            \"id\": 10432,\n                            \"is_right\": 1\n                        },\n                        \"subject\": {\n                            \"content\": \"<img src=\\\"http://file.tbkt.cn/upload_media/knowledge/img/2016/09/29/20160929174848767831.png\\\" alt=\\\"\\\" /><br /><br />— Can she ride fast?<br />                  — ___<br />\",\n                            \"images\": []\n                        },\n                        \"qtype\": 1,\n                        \"id\": 3500,\n                        \"question_id\": 3300\n                    }\n                ],\n                \"video_url\": \"\",\n                \"i\": 0,\n                \"type\": 1,\n                \"id\": 3300,\n                \"classify\": 2,\n                \"subject\": {\n                    \"content\": \"根据图片选择正确的选项。( &nbsp; &nbsp; )\",\n                    \"images\": []\n                }\n            }\n        ],\n        \"numbers\": [\n            {\n                \"qid\": 3300,\n                \"result\": 0,\n                \"aid\": 3500\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/rz_paper/views.py",
    "groupTitle": "RzPaperActive",
    "name": "PostHuodongRzPaper_result_detail"
  },
  {
    "type": "post",
    "url": "/huodong/rz/status",
    "title": "[汝州活动二期]试卷完成状态",
    "group": "RzPaperActive",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\": -1       # -1 没有做过， 0 继续答题， 1 查看结果\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/rz_paper/views.py",
    "groupTitle": "RzPaperActive",
    "name": "PostHuodongRzStatus"
  },
  {
    "type": "post",
    "url": "/huodong/rz/submit_paper",
    "title": "[汝州活动二期]试卷提交",
    "group": "RzPaperActive",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n “status”: \"1\"           # 1 完成（提交）， 2 未完成（保存）\n \"data\": [{\"question_id\":\"3104\", \"ask_id\":\"3292\",\"answer\":\"A\",\"option_id\":19321,\"result\":1},\n {\"question_id\":\"3300\", \"ask_id\":\"3500\",\"answer\":\"A\",\"option_id\":19321,\"result\":0}]\n }",
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
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/rz_paper/views.py",
    "groupTitle": "RzPaperActive",
    "name": "PostHuodongRzSubmit_paper"
  },
  {
    "type": "post",
    "url": "/huodong/yy/active/get_question",
    "title": "[英语活动]获取习题详情",
    "group": "YyActive",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n 'qid': 3104,\n 'no': 1\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"video_image\": \"\",\n        \"ask_no\": 2,\n        \"video_url\": \"\",\n        \"ask\": [\n            {\n                \"video_image\": \"\",\n                \"video_url\": \"\",\n                \"no\": 2,\n                \"listen_audio\": \"\",\n                \"options\": [],\n                \"parse\": {\n                    \"content\": \"\",\n                    \"images\": []\n                },\n                \"answer\": [\n                    \"Can you \"\n                ],\n                \"listen_text\": \"\",\n                \"duration\": -1,\n                \"right_option\": null,\n                \"id\": 3292,\n                \"subject\": {\n                    \"content\": \"I can jump high.（变为一般疑问句）<br/><input placeholder=\\\"点击填写\\\">jump high?<br />\",\n                    \"images\": []\n                }\n            }\n        ],\n        \"type\": 9,\n        \"id\": 3104,\n        \"classify\": 2,\n        \"subject\": {\n            \"content\": \"按要求完成题目。\",\n            \"images\": []\n        }\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/yy_active/views.py",
    "groupTitle": "YyActive",
    "name": "PostHuodongYyActiveGet_question"
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
    "filename": "apps/active/views.py",
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
    "filename": "apps/active/views.py",
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
    "filename": "apps/active/views.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
    "filename": "apps/com_post/post.py",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\" = {\n        'open_person' : open_person,                //到达多少人开奖\n        'had_join' : had_join,                //已经有多少人参与\n        'had_lottery' : had_lottery,                //已经开奖的次数\n        'lottery_rate' : lottery_rate,                //当前用户的中奖率\n        'lottery_up' : lottery_up,                //使用奖券参与次数上限\n        'had_use_ticket_join' : had_use_ticket_join,                //已经用奖券参与的用户的数量\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/excite_activity/views.py",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"actitity_len\" : 1             // 目前正在进行的活动数量\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityActivity_entrance"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/activity_list",
    "title": "[激励抽奖活动]目前正在进行的活动列表",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        active_data:[\n        {\n          \"id\": \"***\",                   //活动id\n          \"name\": \"***\",               //活动名称\n          \"url\": \"***\",                 //图片url\n          \"open_person\": \"***\"          //开奖人次\n          \"strat_time_month\": \"***\"    //开奖月份\n          \"start_time_date\": \"***\"      //开奖日期\n          \"strat_time_year\": \"***\"      //开奖年份\n           \"sign_gold\": \"***\"          //参与金币\n          \"end_time_month\": \"***\"    //结束月份\n          \"end_time_date\": \"***\"      //结束日期\n          \"end_time_year\": \"***\"       //结束年份\n          'original_price' : 'original_price'    //商品原价\n          'tea_num':1   //参与教师数量\n          'type' ：1   // 0金币，奖券都可以，1，仅限奖券参与\n         },\n      ],\n        winner_data:[# 获奖信息\n        ]\n      }\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activityActivity_list"
  },
  {
    "type": "get",
    "url": "/huodong/excite_activity/submit_address",
    "title": "[激励抽奖活动]填写中奖信息",
    "group": "excite_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     excita_id:1 活动id,\n     address: 地址\n     phone: 手机号\n     addressee: 收件人姓名\n }",
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
        },
        {
          "title": "失败返回",
          "content": "{\"message\": \"\", \"error\": \"\", \"data\": \"\", \"response\": \"fail\", \"next\": \"\"}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "GetHuodongExcite_activitySubmit_address"
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
    "filename": "apps/excite_activity/views.py",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n          \"phone\": \"151****6670\",\n          \"school_name\": \"123\",\n          \"real_name\": \"钱学三\"\n        },\n        {\n          \"phone\": \"151****6670\",\n          \"school_name\": \"123\",\n          \"real_name\": \"钱学三\"\n        }\n        {}，{}，{}......\n      ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/excite_activity/views.py",
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
    "filename": "apps/excite_activity/views.py",
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
    "filename": "apps/excite_activity/views.py",
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
    "filename": "apps/excite_activity/views.py",
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
    "filename": "apps/excite_activity/views.py",
    "groupTitle": "excite_activity",
    "name": "PostHuodongExcite_activityTicket_join_actitvity"
  },
  {
    "type": "",
    "url": "/huodong/full/class/book/list",
    "title": "[满分课堂] 设置教材列表",
    "group": "full_class",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"name\": \"人教版一年级下册\",\n            \"id\": 1\n        },\n        {\n            \"name\": \"人教版二年级下册\",\n            \"id\": 2\n        },\n        {\n            \"name\": \"人教版三年级下册\",\n            \"id\": 3\n        },\n        {\n            \"name\": \"人教版四年级下册\",\n            \"id\": 4\n        },\n        {\n            \"name\": \"人教版五年级下册\",\n            \"id\": 5\n        },\n        {\n            \"name\": \"人教版六年级下册\",\n            \"id\": 6\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n* 满分课堂 暂未开启其他教材\n* 所有本次id 与 年级id一致",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassBookList"
  },
  {
    "type": "",
    "url": "/huodong/full/class/book/set",
    "title": "[满分课堂] 设置用户教材",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "    {\"id\":1}\n* 对应book_list接口 id",
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
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassBookSet"
  },
  {
    "type": "",
    "url": "/huodong/full/class/knowledge/info",
    "title": "[满分课堂] 知识点视频",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"week_id\": 1\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"info\": [\n            {\n                \"video_image\": \"http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150258585349.png\",\n                \"status\": 0,\n                \"name\": \"认识条形图\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150258577942.mp4\",\n                \"content\": \"\",\n                \"id\": 6177\n            },\n            {\n                \"video_image\": \"http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150209277403.png\",\n                \"status\": -1,\n                \"name\": \"绘制条形统计图的方法1\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150209267350.mp4\",\n                \"content\": \"\",\n                \"id\": 6178\n            },\n            {\n                \"video_image\": \"http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150304452684.png\",\n                \"status\": 1,\n                \"name\": \"绘制条形统计图的方法2\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150304444284.mp4\",\n                \"content\": \"\",\n                \"id\": 6179\n            },\n            {\n                \"video_image\": \"http://file.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150349564830.png\",\n                \"status\": 0,\n                \"name\": \"误区警示\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/09/23/20140923150349563580.mp4\",\n                \"content\": \"\",\n                \"id\": 6180\n            }\n        ],\n        \"q_num\": 4\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassKnowledgeInfo"
  },
  {
    "type": "",
    "url": "/huodong/full/class/knowledge/question",
    "title": "[满分课堂] 知识点题目",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\": 1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"info\": [\n            {\n                \"knowledge_id\": 5036,\n                \"id\": 2,\n                \"content\": \"运算中既有加法，又有乘法，应先算<span class=\\\"xheBtnWaKong\\\">乘法</span>。\",\n                \"display_type\": 1,\n                \"q_index\": 1,\n                \"answer\": {\n                    \"content\": \"乘法\",\n                    \"is_correct\": 1,\n                    \"option\": \"A\"\n                },\n                \"options\": [\n                    {\n                        \"content\": \"乘法\",\n                        \"is_correct\": 1,\n                        \"option\": \"A\"\n                    },\n                    {\n                        \"content\": \"加法\",\n                        \"is_correct\": 0,\n                        \"option\": \"B\"\n                    },\n                    {\n                        \"content\": \"前面的\",\n                        \"is_correct\": 0,\n                        \"option\": \"C\"\n                    }\n                ]\n            },\n            {\n                \"knowledge_id\": 8007,\n                \"id\": 1394,\n                \"content\": \"数一数：<img src=\\\"http://file.tbkt.cn/upload_media/knowledge/img/2016/11/24/2016112416060885708.png\\\" alt=\\\"\\\" /><br />一共有<span class=\\\"xheBtnWaKong\\\">（80）</span>根小棒。\",\n                \"display_type\": 2,\n                \"q_index\": 2,\n                \"answer\": [\n                    \"80\"\n                ],\n                \"options\": \"\"\n            }\n        ],\n        \"q_num\": 2\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassKnowledgeQuestion"
  },
  {
    "type": "",
    "url": "/huodong/full/class/knowledge/result",
    "title": "[满分课堂] 知识训练场结果页",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\": 课程id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"info\": [\n            {\n                \"knowledge_id\": 5036,\n                \"name\": \"探究乘加混合运算的计算方法\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/08/18/20140818140249159000.mp4\",\n                \"user_answer\": \"B\",\n                \"id\": 2,\n                \"content\": \"运算中既有加法，又有乘法，应先算<span class=\\\"xheBtnWaKong\\\">乘法</span>。\",\n                \"display_type\": 1,\n                \"q_index\": 1,\n                \"answer\": {\n                    \"content\": \"乘法\",\n                    \"is_correct\": 1,\n                    \"option\": \"A\"\n                },\n                \"options\": [\n                    {\n                        \"content\": \"乘法\",\n                        \"is_correct\": 1,\n                        \"option\": \"A\"\n                    },\n                    {\n                        \"content\": \"加法\",\n                        \"is_correct\": 0,\n                        \"option\": \"B\"\n                    },\n                    {\n                        \"content\": \"前面的\",\n                        \"is_correct\": 0,\n                        \"option\": \"C\"\n                    }\n                ]\n            },\n            {\n                \"knowledge_id\": 8007,\n                \"name\": \"学会十个十个数100以内的数\",\n                \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2015/01/29/20150129084526423753.mp4\",\n                \"user_answer\": [\n                    \"80\"\n                ],\n                \"id\": 1394,\n                \"content\": \"数一数：<img src=\\\"http://file.tbkt.cn/upload_media/knowledge/img/2016/11/24/2016112416060885708.png\\\" alt=\\\"\\\" /><br />一共有<span class=\\\"xheBtnWaKong\\\">（80）</span>根小棒。\",\n                \"display_type\": 2,\n                \"q_index\": 2,\n                \"answer\": [\n                    \"80\"\n                ],\n                \"options\": \"\"\n            }\n        ],\n        \"wrong_name\": [\n            \"探究乘加混合运算的计算方法\"\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassKnowledgeResult"
  },
  {
    "type": "",
    "url": "/huodong/full/class/knowledge/submit",
    "title": "[满分课堂] 知识点题目提交",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"week_id\":1,\n    \"info\":[\n                {\"result\": \"A\", \"kid\": 5036, \"qid\": 2, \"is_right\": 1,\"display_type\":1},\n                {\"result\": \"1\", \"kid\": 8007, \"qid\": 1394, \"is_right\": 0,\"display_type\":2}\n           ]\n}",
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
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassKnowledgeSubmit"
  },
  {
    "type": "",
    "url": "/huodong/full/class/pk/question",
    "title": "[满分课堂] 周竞技题目",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\": 课程id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n\"message\": \"\",\n\"next\": \"\",\n\"data\": {\n    \"num\": 4,\n    \"out\": [\n            {\n                \"q_subject\": {\n                    \"type\": 10,\n                    \"id\": 8145,\n                    \"video_url\": \"http://file.tbkt.cn/upload_media/knowledge/video/2015/10/21/20151021151242119295.mp4\",\n                    \"subject\": {\n                        \"content\": \"在<img src=\\\"http://file.xueceping.cn/upload_media/math_img/round.png\\\" alt=\\\"\\\" /><span class=\\\"round\\\"></span>里填上&quot;&gt;&quot;、&quot;&lt;&quot;、&quot;=&quot;。\",\n                        \"images\": \"\",\n                        \"image\": {}\n                    }\n                },\n                \"subject\": {\n                    \"images\": \"\",\n                    \"content\": \"5−3<img src=\\\"http://file.xueceping.cn/upload_media/math_img/round_big.png\\\" alt=\\\"\\\" /><span class=\\\"round\\\"></span>4 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;3−1<img src=\\\"http://file.xueceping.cn/upload_media/math_img/round_big.png\\\" alt=\\\"\\\" /><span class=\\\"round\\\"></span>4\",\n                    \"image\": {}\n                },\n                \"id\": 8178,\n                \"option\": [\n                    {\n                        \"content\": \"5−3&lt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1&lt;4\",\n                        \"option\": \"A\",\n                        \"image\": {},\n                        \"ask_id\": 8178,\n                        \"is_right\": 1\n                    },\n                    {\n                        \"content\": \"5−3&gt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1&gt;4\",\n                        \"option\": \"B\",\n                        \"image\": {},\n                        \"ask_id\": 8178,\n                        \"is_right\": 0\n                    },\n                    {\n                        \"content\": \"5−3&lt;4 &nbsp; &nbsp; &nbsp; &nbsp;3−1=4\",\n                        \"option\": \"C\",\n                        \"image\": {},\n                        \"ask_id\": 8178,\n                        \"is_right\": 0\n                    }\n                ],\n                \"question_id\": 8145\n            }\n        ]\n},\n\"response\": \"ok\",\n\"error\": \"\"",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassPkQuestion"
  },
  {
    "type": "",
    "url": "/huodong/full/class/pk/rank",
    "title": "[满分课堂] 排行榜",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\":1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":  {\n        \"my_rank\": {\n            \"unit_name\": \"105班\",\n            \"score\": 58,\n            \"user_id\": 7646135,\n            \"border_url\": \"\",\n            \"portrait\": \"http://file.tbkt.cn/upload_media/portrait/2017/12/29/20171229205803595199.png\",\n            \"user_name\": \"人生如戏戏\",\n            \"school_name\": \"郑州市第七十中学\",\n            \"rank\": 1\n        },\n        \"user_rank\": [\n            {\n                \"unit_name\": \"105班\",\n                \"user_id\": 7646135,\n                \"border_url\": \"\",\n                \"school_name\": \"郑州市第七十中学\",\n                \"rank\": 1,\n                \"real_name\": \"人生如戏戏\",\n                \"score\": 58,\n                \"portrait\": \"http://file.tbkt.cn/upload_media/portrait/2017/12/29/20171229205803595199.png\"\n            },{}\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* my_rank 我的排名\n* user_rank 用户排名",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassPkRank"
  },
  {
    "type": "",
    "url": "/huodong/full/class/pk/submit",
    "title": "[满分课堂] 周竞技提交",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": " {\n    \"score\":20,\n    \"use_time\":123,\n    \"status\":0,\n    \"week_id\":1,\n    \"info\":[\n            {\"qid\":8145 , \"aid\": 8178,  \"result\": 1, \"score\": 10,\"option\":\"A\"},\n            {\"qid\":8145 , \"aid\": 8178,  \"result\": 1, \"score\": 10,\"option\":\"B\"}\n    ]\n}\n\n* score 答题积分\n* use_time 测试用时\n* week_id 课程id\n* info 提交数据\n* status = 0 中途退出 1 完成提交 或者答错两题",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"max_score\": 100,\n        \"score\": 0,\n        \"num\": 1,\n        \"rank\": [\n            {\n                \"index\": 0,\n                \"user_id\": 608898,\n                \"border_url\": \"http://file.tbkt.cn/upload_media/border/2017/12/19/20171219210857562900.png\",\n                \"rank\": 1,\n                \"real_name\": \"小小学生\",\n                \"score\": 100,\n                \"portrait\": \"http://file.tbkt.cn/upload_media/portrait/2017/12/18/2017121817284732843.png\",\n                \"is_self\": 1\n            },\n            {\n                \"index\": 1,\n                \"user_id\": 520403,\n                \"border_url\": \"http://file.tbkt.cn/upload_media/border/2017/12/19/20171219165203836034.png\",\n                \"rank\": 2,\n                \"real_name\": \"无法识别\",\n                \"score\": 30,\n                \"portrait\": \"http://file.tbkt.cn/upload_media/portrait/2017/12/14/20171214140147742602.png\",\n                \"is_self\": 0\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassPkSubmit"
  },
  {
    "type": "",
    "url": "/huodong/full/class/pop_up",
    "title": "[满分课堂] 每周模块弹窗",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"pop_type\":home\n}\n* 首页  home\n* 信息确认页  info\n* 知识训练场首页  training\n* 挑战错题首页  wrong\n* 每周竞技首页   game",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\":1,\n        \"border_id\":91,\n        \"border_url\": \"http://file.tbkt.cn/upload_media/border/2018/04/13/20180413103334255\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n \n* pop_up = home 时会判断学段，以及是否获取竞技边框\n* status = 1 本周未弹过、可以进行展示\n* status = 0 本周已谈过",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassPop_up"
  },
  {
    "type": "",
    "url": "/huodong/full/class/user",
    "title": "[满分课堂] 用户教材",
    "group": "full_class",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"school_name\": \"郑州市第七十中学105班\",\n        \"book_name\": \"人教版一年级下册\"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassUser"
  },
  {
    "type": "",
    "url": "/huodong/full/class/user/list",
    "title": "[满分课堂] 首页",
    "group": "full_class",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"know_status\": -1,    # 知识训练场\n        \"month_status\": -1,   # 月竞技\n        \"pk_status\": -1,      # 每周竞技\n        \"wrong_status\": -1,   # 挑战错题\n        \"is_open\": 0,         # 是否在开放时间\n        \"open_time\": \"04月21日 09点\",   # 开放时间点\n        \"once_week\": [                 # 往期课程  \n            {\n                \"name\": \"第一周\",     # 名字\n                \"id\": 1              # 课程id\n            },\n            {\n                \"name\": \"第二周\",\n                \"id\": 2\n            }\n        ], \n        \"id\": 3,               # 本周课程id\n        \"name\": \"第三周\"        # 本周课程名字\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassUserList"
  },
  {
    "type": "",
    "url": "/huodong/full/class/video/submit",
    "title": "[满分课堂] 知识点视频提交",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{ \n    \"week_id\": 1,\n    \"knowledge_id\":6177\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassVideoSubmit"
  },
  {
    "type": "",
    "url": "/huodong/full/class/wrong/question",
    "title": "[满分课堂] 高频错题",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\": 课程id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"count\": 2537,\n            \"ratio\": \"52%\",\n            \"video_url\": \"\",\n            \"asks\": [\n                {\n                    \"knowledge\": [\n                        {\n                            \"ask_id\": 16965,\n                            \"id\": 3531,\n                            \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048598754.mp4\",\n                            \"name\": \"用连除或乘除混合运算解决实际问题\"\n                        },\n                        {\n                            \"ask_id\": 16965,\n                            \"id\": 3530,\n                            \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048498295.mp4\",\n                            \"name\": \"用连乘解决实际问题\"\n                        }\n                    ],\n                    \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173047716451.mp4\",\n                    \"title\": \"1\",\n                    \"user_answer\": \"\",\n                    \"number\": 1,\n                    \"id\": 16965,\n                    \"parse\": [\n                        {\n                            \"images\": \"\",\n                            \"content\": \"168÷4÷7=6（吨）<br />6×5×10=300（吨）<br />答：5辆汽车10次可以运货300吨。\",\n                            \"image\": {}\n                        }\n                    ],\n                    \"user_result\": \"\",\n                    \"right_option\": \"C\",\n                    \"question_id\": 12304,\n                    \"options\": [\n                        {\n                            \"option\": \"A\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"30\",\n                            \"id\": 997267\n                        },\n                        {\n                            \"option\": \"B\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"60\",\n                            \"id\": 997268\n                        },\n                        {\n                            \"option\": \"C\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 1,\n                            \"content\": \"300\",\n                            \"id\": 997269\n                        },\n                        {\n                            \"option\": \"D\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"400\",\n                            \"id\": 997270\n                        }\n                    ],\n                    \"subject\": {\n                        \"images\": \"\",\n                        \"content\": \"4辆汽车7次可以运货168吨，照这样计算，5辆汽车10次可以运货多少吨？\",\n                        \"image\": {}\n                    }\n                }\n            ],\n            \"id\": 12304,\n            \"subject\": {\n                \"content\": \"\",\n                \"images\": \"\",\n                \"image\": {}\n            },\n            \"type\": 11,\n            \"number\": 1,\n            \"display\": 1\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\"response\": \"ok\",\n\"error\": \"\"",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassWrongQuestion"
  },
  {
    "type": "",
    "url": "/huodong/full/class/wrong/question/result",
    "title": "[满分课堂] 高频错题结果",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"week_id\": 课程id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"video_url\": \"\",\n            \"asks\": [\n                {\n                    \"knowledge\": [\n                        {\n                            \"ask_id\": 16965,\n                            \"id\": 3531,\n                            \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048598754.mp4\",\n                            \"name\": \"用连除或乘除混合运算解决实际问题\"\n                        },\n                        {\n                            \"ask_id\": 16965,\n                            \"id\": 3530,\n                            \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173048498295.mp4\",\n                            \"name\": \"用连乘解决实际问题\"\n                        }\n                    ],\n                    \"video_url\": \"http://flv.m.xueceping.cn/upload_media/knowledge/video/2014/03/13/20140313173047716451.mp4\",\n                    \"title\": \"3\",\n                    \"user_answer\": \"B\",\n                    \"number\": 1,\n                    \"options\": [\n                        {\n                            \"option\": \"A\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"30\",\n                            \"id\": 997267\n                        },\n                        {\n                            \"option\": \"B\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"60\",\n                            \"id\": 997268\n                        },\n                        {\n                            \"option\": \"C\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 1,\n                            \"content\": \"300\",\n                            \"id\": 997269\n                        },\n                        {\n                            \"option\": \"D\",\n                            \"image\": {},\n                            \"ask_id\": 16965,\n                            \"is_right\": 0,\n                            \"content\": \"400\",\n                            \"id\": 997270\n                        }\n                    ],\n                    \"parse\": [\n                        {\n                            \"images\": \"\",\n                            \"content\": \"168÷4÷7=6（吨）<br />6×5×10=300（吨）<br />答：5辆汽车10次可以运货300吨。\",\n                            \"image\": {}\n                        }\n                    ],\n                    \"user_result\": 0,\n                    \"right_option\": \"C\",\n                    \"subject\": {\n                        \"images\": \"\",\n                        \"content\": \"4辆汽车7次可以运货168吨，照这样计算，5辆汽车10次可以运货多少吨？\",\n                        \"image\": {}\n                    },\n                    \"id\": 16965,\n                    \"question_id\": 12304\n                }\n            ],\n            \"id\": 12304,\n            \"subject\": {\n                \"content\": \"\",\n                \"images\": \"\",\n                \"image\": {}\n            },\n            \"type\": 11,\n            \"number\": 3,\n            \"display\": 1\n        }\n            ],\n            \"id\": 12319,\n            \"subject\": {\n                \"content\": \"填一填。\",\n                \"images\": \"\",\n                \"image\": {}\n            },\n            \"type\": 1,\n            \"number\": 4,\n            \"display\": 1\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassWrongQuestionResult"
  },
  {
    "type": "",
    "url": "/huodong/full/class/wrong/question/submit",
    "title": "[满分课堂] 高频错题提交",
    "group": "full_class",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"week_id\":1, \n    \"data\":[{\"qid\": 4976, \"aid\": 4976, \"result\": 0, \"option\": \"B\"}]\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"test_id\": 176\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/full_class/views.py",
    "groupTitle": "full_class",
    "name": "HuodongFullClassWrongQuestionSubmit"
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
    "filename": "apps/gift_active/views.py",
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
    "filename": "apps/gift_active/views.py",
    "groupTitle": "gift_active",
    "name": "PostHuodongGift_activeStatus"
  },
  {
    "type": "post",
    "url": "/huodong/sx_sem/task/send",
    "title": "[数学活动]布置活动作业",
    "group": "hd_tea_sx",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"type\": 2\n    \"unit_id\": \"555428,515192\", # 班级ID\n    \"title\": \"作业标题\",\n    \"content\": \"短信内容\",\n    \"begin_time\": \"2017-01-05 09:10:00\", # (可选)定时作业时间\n    \"end_time\": \"2017-02-05 23:59:59\",   # 作业截止时间(必须大于当前时间和begin_time)\n    \"sendpwd\": 1/0,   # 是否下发帐号密码\n    \"sendscope\": 1/0,  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n    \"object_id\":\"试卷ID，可多个\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":\"\"，\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": \"请设置作业的完成时间\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/sx_terminal/send_task.py",
    "groupTitle": "hd_tea_sx",
    "name": "PostHuodongSx_semTaskSend"
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/views.py",
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
    "filename": "apps/sx_normal/stu/views.py",
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
    "filename": "apps/sx_normal/stu/views.py",
    "groupTitle": "math_normal",
    "name": "HuodongSxNormalStuSign"
  },
  {
    "type": "get",
    "url": "/huodong/end_term/book/select",
    "title": "[期中提分试卷]选教材/教辅接口",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"subject_id\":21,  # 英语为91\n \"grade_id\":1, \"\n type\":1教材 2练习册\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"books\": [\n            {\n                \"press_name\": \"人教版\", # 出版社\n                \"press_id\": 1, # 出版社ID\n                \"name\": \"数学一年级上册\",  # 默认书名\n                \"subject_id\": 21,  # 学科\n                \"grade_id\": 1,  # 年级\n                \"volume\": 1,  # 1上册 2下册 3全册\n                \"version_name\": \"新版\",  # 版本\n                \"id\": 276 # 教材/教辅ID\n            },\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/end_term/views.py",
    "groupTitle": "mid_term",
    "name": "GetHuodongEnd_termBookSelect"
  },
  {
    "type": "get",
    "url": "/huodong/mid_term/book/select",
    "title": "[期中提分试卷]选教材/教辅接口",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"subject_id\":21,  # 英语为91\n \"grade_id\":1, \"\n type\":1教材 2练习册\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"books\": [\n            {\n                \"press_name\": \"人教版\", # 出版社\n                \"press_id\": 1, # 出版社ID\n                \"name\": \"数学一年级上册\",  # 默认书名\n                \"subject_id\": 21,  # 学科\n                \"grade_id\": 1,  # 年级\n                \"volume\": 1,  # 1上册 2下册 3全册\n                \"version_name\": \"新版\",  # 版本\n                \"id\": 276 # 教材/教辅ID\n            },\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/mid_term/view.py",
    "groupTitle": "mid_term",
    "name": "GetHuodongMid_termBookSelect"
  },
  {
    "type": "get",
    "url": "/huodong/mid_term/paper/list",
    "title": "[期中提分试卷]数学提分试卷列表",
    "group": "mid_term",
    "success": {
      "examples": [
        {
          "title": "提分试卷列表",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"status\": 0,\n            \"id\": 4168,\n            \"name\": \"提分试卷2\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4208,\n            \"name\": \"提分试卷3\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4379,\n            \"name\": \"提分试卷4\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4398,\n            \"name\": \"提分试卷5\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4400,\n            \"name\": \"提分试卷6\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/mid_term/view.py",
    "groupTitle": "mid_term",
    "name": "GetHuodongMid_termPaperList"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/book/get",
    "title": "[期中提分试卷]获取用户设置的活动教材",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"subject_id\" : 21 / 91  # 21为数学  91为英语\n}",
          "type": "json"
        }
      ]
    },
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
    "filename": "apps/mid_term/view.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termBookGet"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/book/set",
    "title": "[期中提分试卷]设置用户教材/教辅",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"book_id\":教材/教辅ID}",
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
    "filename": "apps/mid_term/view.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termBookSet"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/book/set",
    "title": "[期中提分试卷]设置用户教材/教辅",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"book_id\":教材/教辅ID}",
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
    "filename": "apps/end_term/views.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termBookSet"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/status/get",
    "title": "[期中提分试卷]用户弹窗状态",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\" : 1 0    1 弹  0 不弹\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/mid_term/view.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termStatusGet"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/sx_task/send",
    "title": "[期中提分试卷数学]布置数学提分试卷",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"type\": 2\n    \"unit_id\": \"555428,515192\", # 班级ID\n    \"title\": \"作业标题\",\n    \"content\": \"短信内容\",\n    \"begin_time\": \"2017-01-05 09:10:00\", # (可选)定时作业时间\n    \"end_time\": \"2017-02-05 23:59:59\",   # 作业截止时间(必须大于当前时间和begin_time)\n    \"sendpwd\": 1/0,   # 是否下发帐号密码\n    \"sendscope\": 1/0,  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n    \"object_id\":\"试卷ID，可多个\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":\"\"，\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": \"请设置作业的完成时间\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/mid_term/send_sx_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termSx_taskSend"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/choice_paper",
    "title": "[期中提分试卷英语]选择试卷",
    "group": "mid_term",
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
          "content": "      {\n       \"message\": \"\",\n       \"next\": \"\",\n       \"data\": {\n    \"book\": {\n        \"press_name\": \"人教版\",\n        \"name\": \"小学英语一年级上册\",\n        \"subject_id\": 91,\n        \"grade_id\": 1,\n        \"volume\": 1,\n        \"version_name\": \"一年级起点\",\n        \"id\": 21\n    },\n    \"papers\": [             # 没有试卷则papers = []\n        {\n            \"id\": 1,\n            \"pub\": 0,\n            \"name\": \"一年级卷一\"\n        },\n        {\n            \"id\": 2,\n            \"pub\": 0,\n            \"name\": \"一年级卷二\"\n        },\n        {\n            \"id\": 3,\n            \"pub\": 0,\n            \"name\": \"一年级卷三\"\n        },\n        {\n            \"id\": 4,\n            \"pub\": 0,\n            \"name\": \"二年级卷一\"\n        },\n        {\n            \"id\": 5,\n            \"pub\": 0,\n            \"name\": \"二年级卷二\"\n        }\n    ]\n},\n       \"response\": \"ok\",\n       \"error\": \"\"\n       }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyChoice_paper"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/paper_preview_detail",
    "title": "[期中提分试卷英语]单试卷预览详情",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"task_id\":71539,\"paper_id\":1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"sheet\": [\n         {\n             \"qid\": 418,\n             \"right_answer\": \"A\",\n             \"aid\": 449\n         },\n         {\n             \"qid\": 424,\n             \"right_answer\": \"A\",\n             \"aid\": 455\n         },\n         {\n             \"qid\": 54,\n             \"right_answer\": \"A\",\n             \"aid\": 55\n         }\n     ],\n     \"questions\": [{},{},{}...},\n     \"title\": \"一年级卷一\"\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyPaper_preview_detail"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/paper_preview_list",
    "title": "[期中提分试卷英语]试卷预览列表",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"task_id\":71539}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n      \"rows\": [\n          {\n              \"name\": \"一年级卷一\",\n              \"paper_id\": 1\n          },\n          {\n              \"name\": \"一年级卷二\",\n              \"paper_id\": 2\n          },\n          {\n              \"name\": \"一年级卷三\",\n              \"paper_id\": 3\n          }\n      ]\n  },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyPaper_preview_list"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/preview_paper",
    "title": "[期中提分试卷英语]试卷预览",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"id\":1}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n  \"data\": {\n      \"question\": [\n          {\n          \"video_image\": \"\",\n          \"asks\": [\n              {\n                  \"video_image\": \"\",\n                  \"video_url\": \"\",\n                  \"no\": 0,\n                  \"listen_audio\": \"\",\n                  \"options\": [\n                      {\n                          \"option\": \"A\",\n                          \"image\": \"\",\n                          \"ask_id\": 449,\n                          \"is_right\": 1,\n                          \"content\": \"have\",\n                          \"link_id\": -1,\n                          \"id\": 1187\n                      },\n                      {\n                          \"option\": \"B\",\n                          \"image\": \"\",\n                          \"ask_id\": 449,\n                          \"is_right\": 0,\n                          \"content\": \"has\",\n                          \"link_id\": -1,\n                          \"id\": 1188\n                      },\n                      {\n                          \"option\": \"C\",\n                          \"image\": \"\",\n                          \"ask_id\": 449,\n                          \"is_right\": 0,\n                          \"content\": \"is\",\n                          \"link_id\": -1,\n                          \"id\": 1189\n                      }\n                  ],\n                  \"parse\": {\n                      \"content\": \"\",\n                      \"images\": []\n                  },\n                  \"answer\": \"A\",\n                  \"listen_text\": \"\",\n                  \"duration\": 0,\n                  \"right_option\": {\n                      \"option\": \"A\",\n                      \"image\": \"\",\n                      \"ask_id\": 449,\n                      \"is_right\": 1,\n                      \"content\": \"have\",\n                      \"link_id\": -1,\n                      \"id\": 1187\n                  },\n                  \"id\": 449,\n                  \"subject\": {\n                      \"content\": \"（  ）I＿＿a pencil.\",\n                      \"images\": []\n                  }\n              }\n          ],\n          \"video_url\": \"\",\n          \"ask_no\": 0,\n          \"num\": 1,\n          \"type\": 1,\n          \"id\": 418,\n          \"classify\": 2,\n          \"subject\": {\n              \"content\": \"选择正确的答案，将其序号填入题前括号里。\",\n              \"images\": []\n          }\n      },{},{}....\n      },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyPreview_paper"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/qzyy_web",
    "title": "[期中提分试卷英语]教师发试卷",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{{\"type\": 2,\n\"unit_id\": \"622216,578298\",\n\"title\": \"试卷标题\",\n\"content\": \"短信内容\",\n\"begin_time\": \"2017-04-8 09:10:00\",\n\"end_time\": \"2017-04-9 23:59:59\",\n\"sendpwd\": 0,\n\"sendscope\": 0, # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n\"ids\":\"1\"            # 试卷id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n \"task_id\": 71540        # 作业id\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyQzyy_web"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/s/get_test",
    "title": "[期中提分试卷英语]获取试卷内容",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"task_id\":71539,\"paper_id\":2} # 同学生端",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n  \"data\": {\n     \"test\": {\n         \"id\": 3454,\n         \"nquestion\": 3\n     },\n     \"sheet\": [{\n         \"ask_id\": 389,\n         \"option_id\": 4576,\n         \"result\": 1,\n         \"answer\": \"C\",\n         \"test_id\": 3454,\n         \"id\": 46951,\n         \"question_id\": 360\n     },{},{}....],\n     \"numbers\":[\n          {\n             \"qid\": 360,\n             \"ask_no\": 1,\n             \"aid\": 389\n         },\n         {\n             \"qid\": 50,\n             \"ask_no\": 2,\n             \"aid\": 51\n         },\n         {\n             \"qid\": 99,\n             \"ask_no\": 3,\n             \"aid\": 100\n         }\n     ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYySGet_test"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/s/paper_submit",
    "title": "[期中提分试卷英语]提交保存习题",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"data\":[{\"question_id\":360,\"ask_id\":\"389\",\"answer\":\"C\",\"option_id\":4576},\n        {\"question_id\":50,\"ask_id\":\"51\",\"answer\":\"B\",\"option_id\":158},\n        {\"question_id\":99,\"ask_id\":\"100\",\"answer\":\"B\",\"option_id\":3809}]\n \"status\":1                     # 1提交， 2保存\n \"test_id\": 3454\n        }           # 保存内容同学生保存一样",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": \"\",\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYySPaper_submit"
  },
  {
    "type": "post",
    "url": "/huodong/mid_term/yy/stu_paper_detail",
    "title": "[期中提分试卷英语]单个试卷详情",
    "group": "mid_term",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"test_id\":3445,\"stu_name\":\"小菜\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n  \"sheet\": [\n      {\n          \"qid\": 54,\n          \"ask_id\": 55,\n          \"option_id\": 6276,\n          \"result\": 1,\n          \"right_answer\": \"A\",\n          \"answer\": \"A\"\n      },\n      {\n          \"qid\": 418,\n          \"ask_id\": 449,\n          \"option_id\": 6276,\n          \"result\": 0,\n          \"right_answer\": \"A\",\n          \"answer\": \"C\"\n      },{},{}...\n  ],\n  \"question\": [\n      {},{},{}....\n      ],\n  \"title\": \"小菜一年级卷一\"\n   },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/mid_term/send_yy_task.py",
    "groupTitle": "mid_term",
    "name": "PostHuodongMid_termYyStu_paper_detail"
  },
  {
    "type": "post",
    "url": "/huodong/pds_xcq/index",
    "title": "[活动]活动首页",
    "group": "pds_xcq",
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
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"score\": 30,            # 积分\n     \"rank_no\": 3            # 排名\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/psd_xcq/views.py",
    "groupTitle": "pds_xcq",
    "name": "PostHuodongPds_xcqIndex"
  },
  {
    "type": "post",
    "url": "/huodong/pds_xcq/share",
    "title": "[活动]分享活动",
    "group": "pds_xcq",
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
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": \"不满足条件\",  or   今天已经分享一次了 or 分享成功\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/psd_xcq/views.py",
    "groupTitle": "pds_xcq",
    "name": "PostHuodongPds_xcqShare"
  },
  {
    "type": "post",
    "url": "/huodong/pds_xcq/user_rank",
    "title": "[活动]用户排名",
    "group": "pds_xcq",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"page_no\": 0}           # 每次请求10条",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n    \"data\": {\n \"rank\": [\n         {\n             \"user_name\": \"张大帅\",\n             \"score\": 30,\n             \"class_name\": \"401班\"\n         },{},...\n     ]\n },\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/psd_xcq/views.py",
    "groupTitle": "pds_xcq",
    "name": "PostHuodongPds_xcqUser_rank"
  },
  {
    "type": "",
    "url": "/huodong/sd/info",
    "title": "[双但活动]首页学生获奖信息",
    "group": "sd",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n         \"invite_prop\":{   # 通过邀请获得\n            '圣诞鞋':2,\n            '圣诞手套':2\n         }\n        \"open_prop\": \"通过开通获得圣诞鞋\", # 开通获得奖品，没有为 \"\"\n        \"user_props\": [     # 用户奖品列表\n            {\n                \"item_no\": \"shoe\",\n                \"num\": 1,\n                \"name\": \"圣诞鞋\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdInfo"
  },
  {
    "type": "",
    "url": "/huodong/sd/prop/demand",
    "title": "[双但活动]索要道具道具",
    "group": "sd",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\nprop_item:'shoe'  #索要道具\nstu_id :123   # 被索要道具用户id\n}",
          "type": "json"
        }
      ]
    },
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
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdPropDemand"
  },
  {
    "type": "",
    "url": "/huodong/sd/prop/gain",
    "title": "[双但活动]完成作业获得宝箱",
    "group": "sd",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\nwork_type:1     # 作业类型   1在线作业, 2: 每日任务 3: 诗词大战    4: 同步习题\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"prop\": \"获得圣诞手套\"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdPropGain"
  },
  {
    "type": "",
    "url": "/huodong/sd/prop/give",
    "title": "[双但活动]赠送道具",
    "group": "sd",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\nprop_item:'shoe'  #赠送道具\nstu_id :123   # 被赠送道具用户id\nnew_id:123  # 消息id\n}",
          "type": "json"
        }
      ]
    },
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
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdPropGive"
  },
  {
    "type": "",
    "url": "/huodong/sd/prop/news",
    "title": "[双但活动]道具 详情",
    "group": "sd",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"news\": [ # 赠送详情\n                    {\n                        \"status\": 0,\n                        \"item_no\": \"clothes\",\n                        \"user_id\": 520403,\n                        \"name\": \"圣诞衣服\",\n                        \"date\": \"12月18日 15:42:07\",\n                        \"add_user\": 591113,\n                        \"msg\": \"中学生同学向你索要\",\n                        \"id\": 7,\n                        \"add_time\": 1513582927\n                    },\n                    {\n                        \"status\": 1,    0 ：未赠送  1：以赠送\n                        \"item_no\": \"hat\",\n                        \"user_id\": 520403,\n                        \"name\": \"圣诞帽子\",\n                        \"date\": \"12月18日 15:46:15\",\n                        \"add_user\": 591113,\n                        \"msg\": \"中学生同学向你索要\",\n                        \"id\": 8,\n                        \"add_time\": 1513583175\n                    }\n            ],\n        \"detail\": [ #获得道具详情\n            {\n                \"add_date\": 1513559167,\n                \"date\": \"12月18日 09:06:07\",\n                \"item_no\": \"open_prop\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdPropNews"
  },
  {
    "type": "",
    "url": "/huodong/sd/prop/openBox",
    "title": "[双但活动]开启宝箱",
    "group": "sd",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        gift:\"方特门票一张\"\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdPropOpenbox"
  },
  {
    "type": "",
    "url": "/huodong/sd/stu/class_stu",
    "title": "[双但活动]班级学生",
    "group": "sd",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"pinyin\": \"bm\",\n            \"initial\": \"b\",\n            \"id\": 2754348,\n            \"name\": \"宝马\"\n        },\n        {\n            \"pinyin\": \"ddd\",\n            \"initial\": \"d\",\n            \"id\": 7314774,\n            \"name\": \"得得得\"\n        },\n        {\n            \"pinyin\": \"hh\",\n            \"initial\": \"h\",\n            \"id\": 2022858,\n            \"name\": \"呵呵\"\n        },\n        {\n            \"pinyin\": \"lqm\",\n            \"initial\": \"l\",\n            \"id\": 7497502,\n            \"name\": \"刘启明\"\n        },\n        {\n            \"pinyin\": \"xxxs\",\n            \"initial\": \"x\",\n            \"id\": 608898,\n            \"name\": \"小小学生\"\n        },\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdStuClass_stu"
  },
  {
    "type": "",
    "url": "/huodong/sd/stu/open_invite",
    "title": "[双但活动]请邀开通接口",
    "group": "sd",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\ninvite_user_id：456 #邀请人\nsn_code:123\nsubject_id：2,5,9   开通学科\n}",
          "type": "json"
        }
      ]
    },
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
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdStuOpen_invite"
  },
  {
    "type": "",
    "url": "/huodong/sd/stu/verify",
    "title": "[双但活动]确认用户信息",
    "group": "sd",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\ninvite_user_id：456 #邀请人\nphone:135000000,\nname:张三\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"token\": \"MzEzMzk0OX0wNDA1MDg1MTg4fTA0MDcxODE1OTk\",\n        \"open_info\": [\n            {\n                \"status\": 0,\n                \"pay_type\": 2,\n                \"subject_id\": 2,\n                \"cancel_date\": \"\",\n                \"open_date\": \"1970-01-01 08:00:00\"\n            },\n            {\n                \"status\": 0,\n                \"pay_type\": 0,\n                \"subject_id\": 5,\n                \"cancel_date\": \"\",\n                \"open_date\": \"\"\n            },\n            {\n                \"status\": 0,\n                \"pay_type\": 0,\n                \"subject_id\": 9,\n                \"cancel_date\": \"\",\n                \"open_date\": \"\"\n            }\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/double_festival/views.py",
    "groupTitle": "sd",
    "name": "HuodongSdStuVerify"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/ask_for_debris",
    "title": "[暑假活动]索取碎片",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n   \"ask_for_id\" : 123456 //   索取的用户id\n   \"subject_id\" : 2 5 9\n   \"debris\" : \"hat\"            // \"shoe\"  \"background\"    \"pants\"    \"cloth\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": [\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappAsk_for_debris"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/do_invite",
    "title": "[暑假活动]邀请学生",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n  \"subject_id\" : 2       // 2代表数学  5 代表语文   9 代表英语\n  \"user_id\" : 123456\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": \"\"\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappDo_invite"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/get_ask_message",
    "title": "[暑假活动]我的碎片消息----消息",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n  \"subject_id\" : 2       // 2代表数学  5 代表语文   9 代表英语\n  \"p\" : 1                // 页数  从1 开始\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": [\n          { \"ask_for_user\":123, \"real_name\":\"张三\"， \"add_time\":\"12月11日\" , \"ask_thing\": \"cloth\"  },\n          { \"ask_for_user\":123, \"real_name\":\"张三\"， \"add_time\":\"12月11日\", \"ask_thing\": \"cloth\"   },\n          { \"ask_for_user\":123, \"real_name\":\"张三\"， \"add_time\":\"12月11日\"  , \"ask_thing\": \"cloth\" },\n ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappGet_ask_message"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/get_debris_message",
    "title": "[暑假活动]我的碎片消息----碎片记录",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n  \"subject_id\" : 2       // 2代表数学  5 代表语文   9 代表英语\n  \"p\" : 1                // 页数  从1 开始\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": [\n\n ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappGet_debris_message"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/get_rank",
    "title": "[暑假活动]排行榜",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n   \"p\" : 1,      // 分页 从1开始\n   \"subject_id\" : 2 5 9\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\":  {\n   \"person_rank\" : \"500+\"   // 用户个人排名  str形式\n   \"open_num\" : 100     //用户个人开启次数\n   \"rank\" : [\n           {\"user_id\"： 123456， \"open_num\": 10, \"real_name\": \"张三\", \"school_name\":\"北大附小\"}\n   ]\n }\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappGet_rank"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/get_unit_student",
    "title": "[暑假活动]赠送和索取获取班级下所有学生",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": [\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n       {\"user_id\" : 1234564, \"portrait\": \"很长很长的Url\", \"real_name\": \"张三\"}，\n ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappGet_unit_student"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/give_debris",
    "title": "[暑假活动]赠送碎片",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n   \"give_user_id\" : 123456 //赠与的用户id\n   \"subject_id\" : 2 5 9\n   \"debris\" : \"hat\"            // \"shoe\"  \"background\"    \"pants\"    \"cloth\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": // 如果失败了会返回fail message会带信息， 如果成功啥也不反回\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappGive_debris"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/invite_stu",
    "title": "[暑假活动]邀请页面",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n  \"subject_id\" : 2       // 2代表数学  5 代表语文   9 代表英语\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": [\n          { \"user_id\":123, \"real_name\":\"张三\"， \"portrait\":\"很长很长的头像地址\"   },\n          { \"user_id\":123, \"real_name\":\"张三\"， \"portrait\":\"很长很长的头像地址\"   },\n          { \"user_id\":123, \"real_name\":\"张三\"， \"portrait\":\"很长很长的头像地址\"   },\n ]\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappInvite_stu"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/open_box",
    "title": "[暑假活动]开宝箱",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n   \"box\" : \"copper\",      // copper 铜宝箱 sliver 银宝箱 gold 金宝箱\n   \"subject_id\" : 2 5 9\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\":  //如果失败了会返回fail message会带信息， 如果成功啥也不反回\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappOpen_box"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/service_time",
    "title": "[暑假活动]获取服务器时间",
    "group": "summer2018",
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
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": 123456789  # 服务器时间\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappService_time"
  },
  {
    "type": "post",
    "url": "/huodong/summer_activity/sapp/yw_index",
    "title": "[暑假活动]语文活动首页",
    "group": "summer2018",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     subject_id : 2 5 9\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n \"message\": \"\",\n \"next\": \"\",\n \"data\": {\n     \"phase\" : 1      # 1.2 为 1 2阶段         3.4  为第一阶段结束和第二阶段结束页面\n     \"open_num\" : 1,   # 开启次数\n     \"rank\" : '500+' ,  # 当前排名  （均为字符串数据）\n     \"box_status\" : {\"copper\":0, \"sliver\":0, \"gold\":1},   # 用户宝箱状态    0不可开启   1可开启  2已开启\n     \"user_debris\" :  {\"hat\":0, \"shoe\":0, \"background\":0, \"pants\":0, \"cloth\":0}    # 用户碎片状态  hat 帽子 shoe鞋子  background背景   pants  裤子 cloth 衣服\n     \"open_live\" : [\n                     {\"user_id\":123456, \"user_name\": \"张三\", \"debris\": \"cloth\", \"add_time\": \"14:58:59\", \"remark\": \"gold\"},\n                     {\"user_id\":123456, \"user_name\": \"张三\", \"debris\": \"cloth\", \"add_time\": \"14:58:59\", \"remark\": \"gold\"},\n                     # 开启实况\n                     ...\n                     ]\n     \"message_num\" : 10    # 消息数目\n     \"mission\" : \"yw_reading\"   //英语为'打地鼠'  '同步习题'   '口语流利说'   '情景对话'   '课本点读机'  '单词学习'  '爆破气球'    数学为 sx_test  sx_knowledge\n }\n \"response\": \"ok\",\n \"error\": \"\"\n }",
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
    "filename": "apps/summer_activity/sapp/views.py",
    "groupTitle": "summer2018",
    "name": "PostHuodongSummer_activitySappYw_index"
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/stu.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/summer_word/tea.py",
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
    "filename": "apps/sx_questionnaire/view.py",
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
    "filename": "apps/sx_questionnaire/view.py",
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
    "filename": "apps/sx_questionnaire/view.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/paper.py",
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
    "filename": "apps/sx_summer/stu/paper.py",
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
    "filename": "apps/sx_summer/stu/paper.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/paper.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/stu/paper.py",
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
    "filename": "apps/sx_summer/stu/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
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
    "filename": "apps/sx_summer/tea/post.py",
    "groupTitle": "sx_summer",
    "name": "PostHuodongSx_summerTUser_rank"
  },
  {
    "type": "get",
    "url": "/huodong/sx_terminal/paper/list",
    "title": "[数学期末提分试卷]提分试卷列表",
    "group": "sx_terminal",
    "success": {
      "examples": [
        {
          "title": "提分试卷列表",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"status\": 0,\n            \"id\": 4168,\n            \"name\": \"提分试卷2\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4208,\n            \"name\": \"提分试卷3\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4379,\n            \"name\": \"提分试卷4\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4398,\n            \"name\": \"提分试卷5\"\n        },\n        {\n            \"status\": 0,\n            \"id\": 4400,\n            \"name\": \"提分试卷6\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/sx_terminal/view.py",
    "groupTitle": "sx_terminal",
    "name": "GetHuodongSx_terminalPaperList"
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
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
    "filename": "apps/system/views.py",
    "groupTitle": "system",
    "name": "PostSystemBlocks"
  },
  {
    "type": "post",
    "url": "/huodong/tea/task/get/coin",
    "title": "领取金币",
    "group": "tea_coin",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/tea_task_coin/views.py",
    "groupTitle": "tea_coin",
    "name": "PostHuodongTeaTaskGetCoin"
  },
  {
    "type": "post",
    "url": "/huodong/tea/task/status",
    "title": "返回剩余金币数量和是否可以领取的状态",
    "group": "tea_coin",
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
          "content": "    {\n        \"message\": \"\",\n        \"next\": \"\",\n        \"data\": {\n                \"status\": 0,            #是否可以领取金币 0 不可以 1 可以 2 领取过\n                \"num\":2000              #剩余金币数量\n                }\n        \"response\": \"ok\",\n        \"error\": \"\"\n    }\n\n:return:",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/tea_task_coin/views.py",
    "groupTitle": "tea_coin",
    "name": "PostHuodongTeaTaskStatus"
  },
  {
    "type": "get",
    "url": "/huodong/terminal/book/list",
    "title": "[期末提分试卷教材列表",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"grade_id\":1\",\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"books\": [\n                    {\n                        \"press_name\": \"人教版\",\n                        \"name\": \"四年级上册\",\n                        \"subject_id\": 21,\n                        \"grade_id\": 4,\n                        \"volume\": 1,\n                        \"book_type\": 1,\n                        \"grade_name\": \"四年级\",\n                        \"volume_name\": \"上册\",\n                        \"id\": 366,\n                        \"press_id\": 2\n                    },\n                    {\n                        \"press_name\": \"人教版\",\n                        \"name\": \"二年级上册\",\n                        \"subject_id\": 21,\n                        \"grade_id\": 2,\n                        \"volume\": 1,\n                        \"book_type\": 1,\n                        \"grade_name\": \"二年级\",\n                        \"volume_name\": \"上册\",\n                        \"id\": 277,\n                        \"press_id\": 2\n                    },\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "GetHuodongTerminalBookList"
  },
  {
    "type": "get",
    "url": "/huodong/terminal/book/user",
    "title": "[期末提分试卷]用户教材",
    "group": "terminal",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"grade_id\": 6,\n        \"name\": \"小学数学六年级下册(苏教版)\",\n        \"id\": 747\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "GetHuodongTerminalBookUser"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/book/set",
    "title": "[期末提分试卷]设置用户教材/教辅",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"book_id\": 教材ID}",
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
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalBookSet"
  },
  {
    "type": "post",
    "url": "huodong/terminal/math/send",
    "title": "[期末提分试卷]数学布置作业",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"type\": 103\n    \"unit_id\": \"555428,515192\",     # 班级ID\n    \"title\": \"作业标题\",             # 对应paper_id 多个title以竖线|分割\n    \"content\": \"短信内容\",           \n    \"begin_time\": \"2017-01-05 09:10:00\",    # (可选)定时作业时间\n    \"end_time\": \"2017-02-05 23:59:59\",      # 作业截止时间(必须大于当前时间和begin_time)\n    \"sendpwd\": 1/0,                         # 是否下发帐号密码\n    \"sendscope\": 1/0,                       # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n    \"object_id\":\"试卷ID，可多个\"              # 需要与title对应,多个以逗号分割\n}",
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
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": \"请设置作业的完成时间\",\n    \"next\": \"\",\n    \"data\": \"\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/math.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalMathSend"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/paper/list",
    "title": "[期末提分试卷]试卷列表公共",
    "group": "terminal",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"status\": 1,    0/1  可以发/不可以发\n            \"id\": 21021,\n            \"name\": \"期末提分试卷--(一)\"\n        },\n        {\n            \"status\": 1,\n            \"id\": 21022,\n            \"name\": \"期末提分试卷--(二)\"\n        },\n        {\n            \"status\": 1,\n            \"id\": 21023,\n            \"name\": \"期末提分试卷--(三)\"\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalPaperList"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/pop_up",
    "title": "[期末提分试卷]活动弹窗",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例    ",
          "content": "{}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": 0/1,    # 弹/不弹\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalPop_up"
  },
  {
    "type": "post",
    "url": "huodong/terminal/task/class",
    "title": "[期末提分试卷]用户发送作业班级",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"paper_id\":\"1,2,3\"}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "    {\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"unit_info\": [\n            {\n                \"status\": 0, -1/0/1 --  -1/班级没有学生/0不能发送/1继续发送\n                \"unit_name\": \"128班\",\n                \"unit_class_id\": 2929017\n            }\n        ],\n        \"grade_id\": 1\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/views.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalTaskClass"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/check/task/ask",
    "title": "[期末提分试卷]语文检查作业",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"task_id\": 作业id,    \n    \"unit_id\": 班级id,\n    \"ask_id\": 小题id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"wrong\": [\"错误学生姓名\"],\n        \"right\": [\"正确学生姓名\"],\n        \"question\": [题目信息]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwCheckTaskAsk"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/check/task/info",
    "title": "[期末提分试卷]语文检查作业",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"task_id\": 作业id,    \n    \"unit_id\": 班级id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"is_end\": 1,                        # 是否已截止\n        \"task_date\": \"05-16 9:00(星期三)\"    # 作业时间\n        \"finish_num\": 0                     # 完成人数\n        \"unfinish_num\": 0                   # 未完成人数\n        \"list\":[\n            {\n                \"user_name\": \"张三\",   # 学生姓名\n                \"status\": 0,          # 1 完成 2 未完成\n                \"score\": 0,           # 用户成绩 \n                \"is_after\": 1/0,      # 1补交 0不是\n                \"test_id\": 0          # 测试id                \n                \"date\": \"作业完成时间\"\n            }, ...\n        ],\n        \"wrong_info\": [\n            {\n                \"no\": 题号\n                \"rate\": 错误率\n                \"ask_id\": 小题id\n            },\n        ]\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* list 班级学生完成情况\n  wrong_info  错题率\n  已排序",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwCheckTaskInfo"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/preview",
    "title": "[期末提分试卷]语文试卷预览",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"paper_id\": 试卷id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"category\": 1,                  # 1 一题一问 2 一题多问\n            \"asks\": [                       # 大题下 小题信息\n                {                               \n                    \"point\": \"\",            # 断句题正确文字展示 其他类型为 \"\"\n                    \"parse\": \"\",            # 解析\n                    \"no\": \"\",               # 小题题号\n                    \"image\": \"\",            # 小题图片\n                    \"choice_answer\": [],    # 选择题正确答案\n                    \"options\": [],          # 小题选项\n                    \"content\": \"\",          # 小题题干\n                    \"video\": \"\",            # 小题视频\n                    \"right_answer\": [],     # 正确答案(断句题, 连词成句, 填空题, 连线题)\n                    \"refer\": [],            # 解答题正确答案\n                    \"type\": 7,              # 大题类型\n                    \"id\": 66,               # 小题id\n                    \"question_id\": 29       # 大题id \n                }\n            ],\n            \"no\": \"\",                       # 大题题号\n            \"image\": \"\",                    # 大题图片\n            \"content\": \"\",                  # 大题题干\n            \"video\": \"\",                    # 大题视频\n            \"type\":                         # 大题类型\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* question => type\n1.选择题 \n2.填空题 \n3.判断 \n4.连线题  \n5.连词成句 \n6.断句 \n7.解答题",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwPreview"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/send",
    "title": "[期末提分试卷]语文试卷发送",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"unit_id\": 班级id(多个逗号分隔),\n    \"title\": \"试卷名字(多个逗号分隔)\",\n    \"content\": \"短信内容\",\n    \"begin_time\": \"开始时间(选填定时作业需要)\",\n    \"end_time\": \"结束时间\",\n    \"sendpwd\": 是否下发账号密码 1/0 (选填),\n    \"sendscope\": \"短信发送范围 1 开通 0 全部 (选填)\",\n    \"paper_id\": \"多个试卷逗号分隔\",\n}",
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
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwSend"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/test/info",
    "title": "[期末提分试卷]语文学生做题",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"task_id\": 作业id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"total\": 10,                   # 全部试题                    \n        \"wrong\": 2,                    # 错题数\n        \"title\": \"期末提分试卷-（二）\",   # 试卷标题 \n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwTestInfo"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/test/question",
    "title": "[期末提分试卷]语文学生做题",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\"task_id\": 作业id}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"category\": 2,    # 是否是一题多问  1一题一问 / 2一题多问\n            \"asks\": [\n                {\n                    \"parse\": \"111\",    # 解析\n                    \"no\": \"(1)\",       # 小题号\n                    \"image\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155918610447.jpg\", # 题干图片\n                    \"options\": [  # 选项\n                        {\n                            \"option\": \"A\",   # 选项\n                            \"image\": \"\",     # 选项图片\n                            \"ask_id\": 78,    # 小题id\n                            \"is_right\": 1,   # 是否是正确答案\n                            \"content\": \"A1\", # 小题题干\n                            \"link_id\": \"-1\", # 连线题使用\n                            \"id\": 494        # 选项id\n                        }\n                    ],\n                    \"content\": \"我是选择题第一题\",  # 小题题干\n                    \"video\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155923366948.mp4\", # 小题视频 \n                    \"right_answer\": [   # 正确答案\n                        {\n                            \"option\": \"A\",\n                            \"image\": \"\",\n                            \"ask_id\": 78,\n                            \"is_right\": 1,\n                            \"content\": \"A1\",\n                            \"link_id\": \"-1\",\n                            \"id\": 494\n                        }\n                    ],\n                    \"type\": 1,   # 小题类型\n                    \"id\": 78,    # 小题id\n                    \"question_id\": 28,  # 大题id\n                    \"user_answer\": \"A\", # 用户答案\n                    \"user_result\": \"1\", # 用户是否答对 0/1\n                }\n            ],\n            \"no\": \"一\",\n            \"image\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155820813269.jpg\",\n            \"content\": \"我是选择题公共题干\",\n            \"video\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155826832087.mp4\",\n            \"type\": 1\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* 已完成的题 不会出现",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwTestQuestion"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/test/result",
    "title": "[期末提分试卷]语文学生结果页",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"task_id\": 作业id, \n    \"test_id\": \"测试记录id\",\n    \"show_wrong\": 0/1   # 是否只展示错题\n}\n* 两个参数传其中一个",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"category\": 2,    # 是否是一题多问  1一题一问 / 2一题多问\n            \"asks\": [\n                {\n                    \"parse\": \"111\",    # 解析\n                    \"no\": \"(1)\",       # 小题号\n                    \"image\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155918610447.jpg\", # 题干图片\n                    \"options\": [  # 选项\n                        {\n                            \"option\": \"A\",   # 选项\n                            \"image\": \"\",     # 选项图片\n                            \"ask_id\": 78,    # 小题id\n                            \"is_right\": 1,   # 是否是正确答案\n                            \"content\": \"A1\", # 小题题干\n                            \"link_id\": \"-1\", # 连线题使用\n                            \"id\": 494        # 选项id\n                        }\n                    ],\n                    \"content\": \"我是选择题第一题\",  # 小题题干\n                    \"video\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155923366948.mp4\", # 小题视频 \n                    \"right_answer\": [   # 正确答案\n                        {\n                            \"option\": \"A\",\n                            \"image\": \"\",\n                            \"ask_id\": 78,\n                            \"is_right\": 1,\n                            \"content\": \"A1\",\n                            \"link_id\": \"-1\",\n                            \"id\": 494\n                        }\n                    ],\n                    \"type\": 1,   # 小题类型\n                    \"id\": 78,    # 小题id\n                    \"question_id\": 28,  # 大题id\n                    \"user_answer\": \"A\", # 用户答案\n                    \"user_result\": \"1\", # 用户是否答对 0/1\n                }\n            ],\n            \"no\": \"一\",\n            \"image\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155820813269.jpg\",\n            \"content\": \"我是选择题公共题干\",\n            \"video\": \"http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155826832087.mp4\",\n            \"type\": 1\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}\n\n* question => type\n1.选择题 \n2.填空题 \n3.判断 \n4.连线题  \n5.连词成句 \n6.断句 \n7.解答题",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwTestResult"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yw/test/submit",
    "title": "[期末提分试卷]语文学生提交",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"task_id\": 作业id,\n    \"status\": 是否作业 0/1,\n    \"detail\": [\n                {\n                    \"qid\": 大题id,\n                    \"ask_id\"：小题id,\n                    \"answer\": \"用户答案\",\n                    \"result\": \"正确/错误 1/0\"\n                 }\n             ]\n}",
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
    "filename": "apps/terminal2018/subject/chinese.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYwTestSubmit"
  },
  {
    "type": "post",
    "url": "/huodong/terminal/yy/send",
    "title": "[期末提分试卷英语]教师发试卷",
    "group": "terminal",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"type\": 103,                         # 期末作业类型\n   \"unit_id\": \"622216,578298\",           # 班级id 多个以逗号分割\n   \"title\": \"试卷标题\",                   # 试卷标题 以竖线|分割\n   \"content\": \"短信内容\",                 # 短信内容 \n   \"begin_time\": \"2017-04-8 09:10:00\",   # 开始时间\n   \"end_time\": \"2017-04-9 23:59:59\",     # 结束时间\n   \"sendpwd\": 0,                         # 是否下发账号密码\n   \"sendscope\": 0,          # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n   \"ids\":\"1\"                # 试卷id,多个试卷id以逗号分割\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {},\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/terminal2018/subject/english.py",
    "groupTitle": "terminal",
    "name": "PostHuodongTerminalYySend"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/activity_entrance",
    "title": "[寒假活动]总的活动入口",
    "group": "winter_activity",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"power_num\" : 1                                     // 能量数目\n        \"score\" : 150                                // 积分数量\n        \"range_num\" : 1000                                 // 用户排名\n        \"open_status\" : 1.2.3 or 0                            // 1.2.3为开通科目数量 0为未开通\n        \"award_info\" : [                                 // 奖品信息\n                        {name : \"***\", image_url : \"***\", id : ***},\n                        {name : \"***\", image_url : \"***\", id : ***},\n                        {name : \"***\", image_url : \"***\", id : ***},\n                        ]\n        \"take_a_big_gift\" : 0 or 1.2.3                      //1.2.3为获得了大礼包的数量  0为没有获得\n        \"login_day\" : l2                                 //连续登录日期数 1-8\n        \"notice\" : 0  or  其他Int类型数值        // 0 为不用通知用户 ，其他则为award_id  需要去取award_info内的奖品名称\n        \"award_day\" : 1                         // 0 未不通知用户   1-31为获奖日期\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityActivity_entrance"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/coin_power_detail",
    "title": "[寒假活动]获取积分能量值明细",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n  p : 10 //  请求0则返回0-10条数据 请求10则返回10-20条数据，请求20则返回20-30条数据\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "   {\n       \"message\": \"\",\n       \"next\": \"\",\n       \"data\": [\n                  \"您在2月20日通过PK扣除1个能量值\",\n                  \"您在2月20日通过PK扣除1个能量值\"\n                   ......  // 10个数据\n                ]\n},\n       \"response\": \"ok\",\n       \"error\": \"\"\n   }",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityCoin_power_detail"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/get_user_match",
    "title": "[寒假活动]成语、诗词pk模块选择对手、获取信息",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\"school_id\":1 #学校id\n\"class_id\":1 #班级id\n\"province_id\":1 #省份id\n\"is_type\":1，#类型，1.诗词大战pk,2.成语游戏pk\n\"is_arena\" : 1  # 是否为欢乐竞技场  1 是 0 不是\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"user_id\": 1583213,\n            \"class_id\": 11,\n            \"user_object\": \"{\\\"portrait\\\": \\\"http://student.tbkt.cn/site_media/images/profile/default-student.png\\\", \\\"school\\\": \\\"\\\\u9ec4\\\\u6cb3\\\\u8def\\\\u4e00\\\\u5c0f\\\", \\\"user_id\\\": 1583213, \\\"name\\\": \\\"\\\\u5f20\\\\u4e09\\\"}\",\n            \"right_num\": 3,\n            \"school_id\": 22,\n            \"match_record_id\": 1,\n            \"score\": 88,\n            \"result\": 1,\n            \"pk_user\": \"{\\\"portrait\\\": \\\"http://student.tbkt.cn/site_media/images/profile/default-student.png\\\", \\\"user_id\\\": 1583213, \\\"name\\\": \\\"\\\\u5f20\\\\u4e09\\\"}\",\n            \"province_id\": 1,\n            \"type\": 2,\n            \"id\": 6,\n            \"user_time\": 88,\n            \"add_time\": 1502467\n            \"user_props\" = [1,1,1,1,1,1]  //按顺序依次是1：鲜花数量，2：鸡蛋数量，3：墨镜数量，4：橡皮擦数量，5：放大镜数量，6：超级翻倍卡数量',\n            \"pk_id\" = 100 or 0 //  PKid代表了PK时候扣除能量值明细的id\n        }\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityGet_user_match"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/happy_arena",
    "title": "[寒假活动]欢乐竞技场入口",
    "group": "winter_activity",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"is_type\":1，#类型，1.诗词大战pk,2.成语游戏pk\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityHappy_arena"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/happy_ranking",
    "title": "[寒假活动]欢乐榜",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     \"p\" :  // 我也不知道你会请求啥 反正按老方法来\n            // 尽量不用下拉的时候返回p=0，然后第一次下拉返回p=10， 第二次下拉返回p=20\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n              \"border_url\" : // 用户的头像边框地址 没有则返回空  只有第一名有   为空则证明今天还没开奖\n              \"img\" : //用户的当前头像   为空则证明今天还没开奖\n              \"nowday\" : //当前日期\n              \"nowmon\" : //当前月份\n              \"name\" : '' //真实姓名    为空则证明今天还没开奖\n        }\n        [\n            {\n                \"score\" : 111            //用户积分\n                \"real_name\" : \"***\"     //用户姓名\n                \"user_id\": 800363,      //用户Id\n\n                \"school_name\" : \"***\"  //用户学校名称\n                \"award_id\" : ***      //该字段不为空则排行榜上应显示已领奖\n            },\n            {\n                \"score\" : 111            //用户积分\n                \"real_name\" : \"***\"     //用户姓名\n                \"user_id\": 800363,      //用户Id\n                \"school_name\" : \"***\"  //用户学校名称\n                \"award_id\" : ***      //该字段不为空则排行榜上应显示已领奖\n            },\n            {},{},{}......\n        ]\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityHappy_ranking"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/heroes",
    "title": "[寒假活动]英雄榜",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n     \"p\" :  // 我也不知道你会请求啥 反正按老方法来\n            // 尽量不用下拉的时候返回p=0，然后第一次下拉返回p=20， 第二次下拉返回p=30\n }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"score\" : 111  //用户积分\n            \"user_id\": 800363, // 用户id\n            \"border_url\" : // 用户的头像边框地址 没有则返回空  只有前三名有\n            \"real_name\" : \"***\"  //用户姓名\n            \"school_name\" : \"***\"  //用户学校名称\n        },\n        {\n            \"score\" : 111  //用户积分\n            \"user_id\": 800363, //用户id\n            \"border_url\" : // 用户的头像边框地址 没有则返回空  只有前三名有\n            \"real_name\" : \"***\"  //用户姓名\n            \"school_name\" : \"***\"  //用户学校名称\n        },\n        {},{},{}......  //  备注： 0分用户不显示\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityHeroes"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/invite_get_power",
    "title": "[寒假活动]邀请获得能量接口",
    "group": "winter_activity",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityInvite_get_power"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/my_things",
    "title": "[寒假活动]我的很多东西",
    "group": "winter_activity",
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
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"props\" : [1,1,1,1,1,1]  //按顺序依次是1：鲜花数量，2：鸡蛋数量，3：墨镜数量，4：橡皮擦数量，5：放大镜数量，6：超级翻倍卡数量',\n       \"awards\" : [\n                    {name : \"***\", add_time : \"1\"， \"add_mon\" : 1},   //name : 奖品名称  add_time 获奖那天的日期\n                    {name : \"***\", add_time : \"1\"， \"add_mon\" : 1}\n                    {name : \"***\", add_time : \"1\"， \"add_mon\" : 1}\n                    ......\n                    ]\n     },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
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
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityMy_things"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/r_get_idiom",
    "title": "[寒假活动]学生端 成语pk模块资源接口",
    "group": "winter_activity",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"words_list\": [\n            \"面\",\n            \"创\",\n            \"嘿\",\n            \"穹\",\n            \"泵\",\n            \"爬\",\n            \"路\",\n            \"开\",\n            \"季\",\n            \"疮\",\n            \"廓\",\n            \"一\",\n            \"避\",\n            \"斥\",\n            \"网\",\n            \"绩\",\n            \"蟹\",\n            \"螯\"\n        ],\n        \"cy_Source\": \"清·李绿园《歧路灯》：“先生意欲网开一面；以存忠厚之意；这却使不得。”\",  #成语出处\n        \"cy_Tupian\": \"/UploadFileS/Images/a8ea8b22-4326-40da-9fdf-8ee4ab3aeff2.png\",\n        \"cy_Content\": \"网开一面\",\n        \"cy_Explain\": \"把捕禽的网撤去三面，只留一面。比喻采取宽大态度，给人一条出路。\"   #成语解释\n        \"have_glass\" : 1 为这局用户被使用了墨镜 0 为这局用户没有被使用墨镜\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityR_get_idiom"
  },
  {
    "type": "get",
    "url": "/huodong/winter_activity/r_get_poetry",
    "title": "[寒假活动]学生端 诗词pk模块资源接口",
    "group": "winter_activity",
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n        {\n            \"qu_TitleDry\": \"________________，何时复西归。\",  #qu_TitleDry\n            \"qu_OptionA\": \"空翠湿人衣\",\n            \"qu_OptionB\": \"欲穷千里目\",\n            \"qu_OptionC\": \"今春看又过\",\n            \"qu_OptionD\": \"百川东到海\",\n            \"po_ID\": 3,  #关联诗歌表ID\n            \"po_Name\": \"长歌行\", #诗歌名称\n            \"po_Author\": \"汉乐府\", 作者\n            \"qu_TrueOption\": \"D\"  #正确选项\n            \"answer\" : \"百川东到海，何时复西归。\"\n            \"have_glass\" : 1 为这局用户被使用了墨镜 0 为这局用户没有被使用墨镜\n        },\n    ],\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "GetHuodongWinter_activityR_get_poetry"
  },
  {
    "type": "post",
    "url": "/huodong/winter_activity/post_happy_pk_details",
    "title": "[寒假活动]欢乐竞技场PK结果入库",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n        \"right_num\": \"3\"答对题数,\n        \"user_time\": 总时长,\n        \"score\": \"44\"总数\n        \"user_object\"：用户的信息:头像路径、姓名、user_id、学校名称\n        \"pk_user\"：挑战对象的信息:头像路径、姓名、user_id、学校名称、答对几道题、用时、总分\n        \"result\":1，结果1.赢了，2.输了\n        \"school_id\":学校id\n        \"class_id\"：班级id\n        \"province_id\"：省份id\n        \"add_time\":挑战开始的时间\n        \"is_type\":1 #类型，1.诗词大战pk,2.成语游戏pk\n    }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "    {\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n            add_type: 1    //胜利方获得有一个道具 0：未获得 1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡\n            ids : [score_id, score_detail_id, happy_score_id, pk_happy_record_id]   //分数id 分数详情id 欢乐分数id PK记录ID\n        },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "PostHuodongWinter_activityPost_happy_pk_details"
  },
  {
    "type": "post",
    "url": "/huodong/winter_activity/post_pk_details",
    "title": "[寒假活动]成语、诗词pk模块结果入库",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n        \"right_num\": \"3\"答对题数,\n        \"user_time\": 总时长,\n        \"score\": \"44\"总数\n        \"user_object\"：用户的信息:头像路径、姓名、user_id、学校名称\n        \"pk_user\"：挑战对象的信息:头像路径、姓名、user_id、学校名称、答对几道题、用时、总分\n        \"result\":1，结果1.赢了，2.输了\n        \"school_id\":学校id\n        \"class_id\"：班级id\n        \"province_id\"：省份id\n        \"add_time\":挑战开始的时间\n        \"is_type\":1 #类型，1.诗词大战pk,2.成语游戏pk\n        \"pk_id\" = 100 or 0 //  PKid代表了PK时候扣除能量值明细的id\n    }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "    {\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n            add_type: 1    //胜利方获得有一个道具 0：未获得 1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡  0：未获得\n            ids : [score_id， score_detail_id, pk_record_id]   //分数id 分数详情id\n        },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "PostHuodongWinter_activityPost_pk_details"
  },
  {
    "type": "post",
    "url": "/huodong/winter_activity/use_props",
    "title": "[寒假活动]使用道具",
    "group": "winter_activity",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\n        \"has_use_double\"  : 1//    代表使用了双倍积分卡\n        \"has_use_flower\" : 1    // 代表使用鲜花\n        \"has_use_egg\" : 1       // 代表使用鸡蛋\n        \"has_use_sunglasses\"  : 1      // 代表使用墨镜\n        \"has_use_magnifier\" : 1    // 代表使用放大镜\n        \"has_use_eraser\" :1    //代表适用橡皮擦\n        \"ids\" : [score_id, score_detail_id, happy_score_id, pk_happy_record_id]  //双倍积分卡需要修改记录的数组\n    }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "    {\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/winter_activity/views.py",
    "groupTitle": "winter_activity",
    "name": "PostHuodongWinter_activityUse_props"
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/stu/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
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
    "filename": "apps/yw_activity/tea/index.py",
    "groupTitle": "yw_hd_t",
    "name": "PostHuodongYw_activityTRecommend_article"
  },
  {
    "type": "get",
    "url": "/huodong/reading/get_join_status",
    "title": "[教师端]是否能参与阅读训练活动",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        \"status\" : 1/0  #1可以参与 0不能参与\n    }，\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingGet_join_status"
  },
  {
    "type": "get",
    "url": "/huodong/reading/get_message",
    "title": "[学生端]获取留言",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"tid\": 6   # 文章id\n    \"page\" : 1   #页数 每页20条  ! 不能不传 从1开始\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n             {“user_name”:””, “add_time”:””, “content”:””, \"user_border\":\"\", \"user_portrait\":\"'},\n              {“user_name”:””, “add_time”:””, “content”:””, \"user_border\":\"\", \"user_portrait\":\"'},\n              {“user_name”:””, “add_time”:””, “content”:””, \"user_border\":\"\", \"user_portrait\":\"'},\n              {“user_name”:””, “add_time”:””, “content”:””, \"user_border\":\"\", \"user_portrait\":\"'},\n            ]\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingGet_message"
  },
  {
    "type": "get",
    "url": "/huodong/reading/get_paper",
    "title": "[教师端]获取当前年级下的试卷",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    “grade”: 2\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n                {“title”:””, “question_num”:1, “status”: 1/0},\n                {“title”:””, “question_num”:1, “status”: 1/0},\n                {“title”:””, “question_num”:1, “status”: 1/0},\n            ]\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingGet_paper"
  },
  {
    "type": "get",
    "url": "/huodong/reading/get_recording",
    "title": "[学生端]获取用户的录音（最多五个）",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"tid\": 6   # 文章id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\":\n    \"next\": \"\",\n     \"data\": {\n            \"status\": 0, 1/0,  等于1 已经上传过录音 等于0  则未上传过录音\n            \"video_detail\": [\n                {\n                    \"recording_length\": 5,\n                    \"user_name\": \"refresh\",\n                    \"user_id\": 7646093,\n                    \"id\": 2,\n                    \"recording_path\": \"http://tbktfile.jxrrt.cn/yuwen/201709StuVideos/b99255c5-fc6f-4f60-8b98-fb90f18e6e06.mp3\"\n                },{},{},{},\n            ]\n     },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingGet_recording"
  },
  {
    "type": "get",
    "url": "/huodong/reading/index",
    "title": "[教师端]活动首页",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n        “coins”: 10000,\n        “complete_students”: [\n                             {“unit_name”:””, “complete_num”:100},\n                             {“unit_name”:””, “complete_num”:100},\n        ]\n        “complete_status”: 1 / 0\n\n    }，\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingIndex"
  },
  {
    "type": "get",
    "url": "/huodong/reading/view_paper",
    "title": "[教师端]预览试卷",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"tid“ : 100\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n            \"title\": \"aaaaa\",                     # 文章标题\n            \"article_content\": \"aaa\",    #文章内容\n            }\n\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "GetHuodongReadingView_paper"
  },
  {
    "type": "post",
    "url": "/huodong/reading/get_coin",
    "title": "[教师端]领取金币",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n\n   }",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n            \"num\" : 0/20/40  # 20领取的金币数量 0 领取失败\n            }\n\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "PostHuodongReadingGet_coin"
  },
  {
    "type": "post",
    "url": "/huodong/reading/send_sms",
    "title": "[教师端]发送试卷短信",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"unit_id\": \"555428,515192\", # 班级ID\n    \"title\": \"静夜思，锄禾\", # 逗号分隔的title数组\n    \"begin_time\": \"2017-01-05 09:10:00\", # (可选)定时作业时间\n    \"sendpwd\": 1/0,   # 是否下发帐号密码\n    \"sendscope\": 1/0,  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信\n    \"object_id\":\"试卷ID，可多个， 逗号分隔\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\":\"\"，\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        },
        {
          "title": "失败返回",
          "content": "{\n    \"message\": ,\n    \"next\": \"\",\n    \"data\": \"请设置作业的完成时间\",\n    \"response\": \"fail\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "PostHuodongReadingSend_sms"
  },
  {
    "type": "post",
    "url": "/huodong/reading/set_message",
    "title": "[学生端]发布留言",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"tid\": 6   # 文章id\n    \"content\" : \"荣誉，可是要付出代价的\"\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": [\n            ]\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "PostHuodongReadingSet_message"
  },
  {
    "type": "post",
    "url": "/huodong/reading/set_recording",
    "title": "[学生端]上传录音",
    "group": "yw_reading",
    "parameter": {
      "examples": [
        {
          "title": "请求示例",
          "content": "{\n    \"video_url\": \"http://tbktfile.jxrrt.cn/yuwen/201709StuVideos/b99255c5.mp3\"   # 音频地址\n    \"tid\": 1      #文章id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "examples": [
        {
          "title": "成功返回",
          "content": "{\n    \"message\": \"\",\n    \"next\": \"\",\n    \"data\": {\n\n    },\n    \"response\": \"ok\",\n    \"error\": \"\"\n}",
          "type": "json"
        }
      ]
    },
    "version": "0.0.0",
    "filename": "apps/yw_reading/views.py",
    "groupTitle": "yw_reading",
    "name": "PostHuodongReadingSet_recording"
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
    "filename": "apps/yy_normal/views.py",
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
    "filename": "apps/yy_normal/views.py",
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
    "filename": "apps/yy_normal/views.py",
    "groupTitle": "yy_normal",
    "name": "PostHuodongYyNormalTasks"
  }
] });
