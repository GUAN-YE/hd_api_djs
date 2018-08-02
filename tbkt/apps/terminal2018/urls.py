# coding: utf-8
from django.conf.urls import url
from apps.terminal2018 import views
from apps.terminal2018.subject import math
from apps.terminal2018.subject import chinese
from apps.terminal2018.subject import english


# com views
urlpatterns = [
    url(r"^book/user$", views.r_book_user),     # 用户活动教材
    url(r"^book/list$", views.r_book_list),     # 活动教材列表
    url(r"^book/set$", views.r_book_set),       # 用户教材设置
    url(r"^pop_up$", views.r_pop_up),           # 首页弹框
    url(r"^paper/list$", views.r_paper_list),   # 教材试卷列表
    url(r"^task/class$", views.r_task_class),   # 活动教材发送状态
    url(r"^del_cache$", views.r_del_cache),   # 活动教材发送状态
]

# math
urlpatterns += [
    url(r"^math/send$", math.r_sx_send),         # 数学试卷发送
]


# chinese
urlpatterns += [
    url(r"^yw/preview$", chinese.r_yw_preview),     # 语文试卷预览
    url(r"^yw/send$", chinese.r_yw_send),           # 语文试卷发送
    url(r'^yw/test/result$', chinese.r_stu_test_result),       # 学生结果页
    url(r'^yw/test/submit$', chinese.r_stu_test_submit),       # 学生提交
    url(r'^yw/test/question$', chinese.r_stu_test_question),   # 学生做题页
    url(r'^yw/test/info$', chinese.r_stu_test_info),           # 作业完成详情
    url(r'^yw/check/task/info$', chinese.r_check_task),        # 检查作业
    url(r'^yw/check/task/ask$', chinese.get_ask_info),         # 小题完成情况
]


# English
urlpatterns += [
    url(r"^yy/send$", english.r_yy_send),           # 英语试卷发送
]
