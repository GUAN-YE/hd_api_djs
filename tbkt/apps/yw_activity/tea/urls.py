# coding=utf-8

from django.conf.urls import include, url, patterns
from . import index

urlpatterns = patterns('',
                       # url(r'^index$', index.get_index),  # 教师端首页
                       url(r'^article_list$', index.get_article_list),  # 教师端推荐文章列表
                        url(r'^recommend_article$', index.post_recommend_article),  # 教师端推荐文章给学生入库
                        url(r'^article_details$', index.get_article_details),  # 文章详情页
                       url(r'^teacher_ranking$', index.get_teacher_ranking),  # 教师排名
                       url(r'^class_ranking$', index.get_class_ranking),  # 班级排名
                        url(r'^user_rank$', index.user_rank),  # 排名积分和抽奖次数
                        url(r'^t_integral_list$', index.t_integral_list),  # 老师结束页
                        # url(r'^prize_list$', index.get_prize_list),  # 奖品列表页，活动结束奖品列表页
                       )
