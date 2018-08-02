# coding=utf-8


from django.conf.urls import url, patterns
from . import index

urlpatterns = patterns('',
                    url(r'^index$', index.post_index),  # 学生端活动首页，判断学生是否已经首次加分
                    url(r'^article_all', index.get_article_all),  # 学生端范文文章列表
                    url(r'^article_recom', index.get_article_recom),  # 学生端老师推荐文章列表
                    url(r'^article_details$', index.get_article_details),  # 文章详情页
                    url(r'^post_recording$', index.post_recording),  # 学生端录音入库
                    url(r'^s_integral_list$', index.s_integral_list),  # 结束页展示
                    url(r'^recording_integral$', index.post_recording_integral),  # 文章当天首次分享加积分
                    url(r'^ballot_integral$', index.post_ballot_integral),  # 分享获得投票入库
                    url(r'^all_recording$', index.get_all_recording),  # 全省学生录音排名
                    url(r'^class_ranking$', index.get_class_ranking),  # 班级排名
                    url(r'^user_rank$', index.user_rank),  # 学生端积分
                    url(r'^share_activity$', index.share_activity),  #学生端分享表
                    # url(r'^prize_list$', index.get_prize_list),  # 奖品列表页，活动结束奖品列表页
                    # url(r'^index_prize$', index.get_index_prize),  # 学生端首页奖品介绍列表页
                       )

