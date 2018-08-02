# coding:utf8
"""
满分课堂模块
"""
from django.conf.urls import url
from . import views

# 公共视图
urlpatterns = [
    url(r'book/list$', views.r_book_list),       # 设置教材列表
    url(r'book/set$', views.r_set_book),         # 设置用户教材
    url(r'pop_up$', views.pop_up),               # 弹框接口
    url(r'user$', views.r_user_info),            # 用户信息接口
    url(r'del_cache$', views.r_del_cache),       # 删除缓存接口
    url(r'user/list$', views.user_index),        # 首页任务列表
    url(r'history$', views.r_history)            # 往期获取任务状态
]

# 知识点训练场
urlpatterns += [
    url(r'knowledge/info$', views.get_knowledge),     # 获取测试知识点(视频)
    url(r'video/submit$', views.video_submit),        # 观看视频提交
    url(r'knowledge/question$', views.get_question),  # 获取测试知识点题目信息
    url(r'knowledge/submit$', views.test_submit),     # 提交测试结果
    url(r'knowledge/result$', views.test_result),     # 测试结果页
]

# 高频错题
urlpatterns += [
    url(r'wrong/question$', views.r_wrong_question),       # 获取高频错题
    url(r'wrong/question/submit$', views.r_wrong_submit),  # 提交错题测试结果
    url(r'wrong/question/result$', views.r_wrong_result),  # 提交错题测试结果
]

# 每周竞技
urlpatterns += [
    url(r'pk/question$', views.get_pk_question),  # 获取竞技题目
    url(r'pk/submit$', views.pk_submit),          # 提交竞技题目
    url(r'pk/rank$', views.pk_rank),              # 竞技结果排行
]
