#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/8/2 15:52
"""
from django.conf.urls import url
from apps.summer_word import score
from apps.summer_word import stu
from apps.summer_word import tea

# 学生完成练习加分
urlpatterns = [
    url(r'^add_score$', score.add_score)                    # 学生完成自学加分
]

# 学生活动
urlpatterns += [
    url(r'^s/share$', stu.share),                           # 积分 分享活动
    url(r'^s/add_tea_score', stu.add_tea_score),            # 积分 学生进活动加教师积分
    url(r'^s/index$', stu.index),                           # 活动首页
    url(r'^s/index/open_at_once$', stu.open_at_once),       # 首页 立即开通按钮点击统计
    url(r'^s/user_rank', stu.user_rank),                    # 用户排名

    url(r'^s/award/my_score', stu.award_my_score),            # 抽奖 用户积分可用次数
    url(r'^s/award/my_award', stu.award_my_award),            # 抽奖 用户个人奖品列表
    # url(r'^s/award/draw_lottery', stu.award_draw_lottery),  # 抽奖 用户个人奖品列表         # 废弃
    url(r'^s/award/won_list', stu.award_won_list),  # 抽奖 所有最近中奖的随机轮播列表

    url(r'^s/result/total_score_rank', stu.total_score_rank),  # 结束页 积分获奖名单       有排行
    url(r'^s/result/draw_lottery_rank', stu.draw_lottery_rank),  # 结束页 抽奖获奖名单

]

# 教师活动
urlpatterns += [
    url(r'^t/send_sms', tea.send_sms),  # 教师 发送普通短信
    url(r'^t/send_open', tea.send_open),  # 教师 开通班级下学生学科
    url(r'^t/my_rank', tea.my_rank),  # 教师 我的积分排名

    url(r'^t/user_rank', tea.user_rank),  # 教师 排名 所有教师排名
    url(r'^t/my_stu_rank', tea.my_stu_rank),  # 教师 所有班级学生积分排名

    url(r'^t/award/my_score$', tea.award_my_score),            # 抽奖 教师用户积分可用次数
    url(r'^t/award/my_award$', tea.award_my_award),            # 抽奖 教师已抽到的奖品
    url(r'^t/award/won_list$', tea.award_won_list),            # 抽奖 所有最近中奖的随机轮播列表

    url(r'^t/result/total_score_rank', tea.total_score_rank),            # 结束页 积分获奖名单
    url(r'^t/result/draw_lottery_rank', tea.draw_lottery_rank),            # 结束页 抽奖获奖名单
]
