# coding: utf-8
from django.conf.urls import url
from apps.mid_term import view, send_sx_task, send_yy_task

# 数学期末活动
urlpatterns = [
    url(r'^book/select$', view.p_select),          # 获取活动教材下的教材
    url(r'^book/set$', view.p_setbook),          # 设置活动教材
    url(r'^paper/list$', view.hd_book_papers),                # 数学试卷列表
    url(r'^sx_task/send$', send_sx_task.p_give_web),          # 发数学试卷
    url(r'^book/get$', view.p_getbook),                     # 获取活动教材
    url(r'^yy/qzyy_web$', send_yy_task.send_qzyy),          # 发英语试卷
    url(r'^yy/choice_paper$', send_yy_task.choice_paper),   #  英语选择试卷
    url(r'^yy/preview_paper$', send_yy_task.preview_paper),   #  英语试卷预览
    # url(r'^yy/paper_detail$', send_yy_task.paper_detail),  # 试卷作业-班级
    # url(r'^yy/stu_detail$', send_yy_task.stu_detail),  # 学生完成作业列表
    url(r'^yy/stu_paper_detail$', send_yy_task.stu_paper_detail),  # 单个试卷详情
    url(r'^yy/paper_preview_list$', send_yy_task.paper_preview_list),  # 试卷预览列表
    url(r'^yy/paper_preview_detail$', send_yy_task.paper_preview_detail),  # 单试卷预览详情
    url(r'^yy/s/get_test$', send_yy_task.do_paper),  # 获取试卷内容
    url(r'^yy/s/paper_submit$', send_yy_task.paper_submit),  # 提交保存试题
    url(r'^status/get$', view.get_status),  # 提交保存试题
]