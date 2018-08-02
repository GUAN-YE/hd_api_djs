# _*_ coding: utf-8 _*_
from django.conf.urls import url
from apps.paper_active.views import r_stu_list, r_tea_list
# 2017河南全省智能组卷积分活动
# 学生端
# 迁移后只显示 学生端 教师端 获奖列表 其他代码请参考老项目

urlpatterns = [
    url(r'^stu/end_list', r_stu_list),       # 活动首页数据 积分 抽奖 签到状态
    url(r'^tea/end_list', r_tea_list),       # 签到
]