# coding=utf-8

from django.conf.urls import url
from apps.com_post import post

urlpatterns = [
    url(r'^award$', post.p_award),  # 抽奖
    url(r'^award/list$', post.p_award_list),  # 抽奖获奖列表
    url(r'^award/resent', post.p_award_recent),  # 最近10位获奖用户信息
    url(r'^award/all$', post.p_award_all),  # 分页获取全部获奖信息

    url(r'^user/info$', post.p_user_info),  # 返回用户排名，积分c
    url(r'^user/detail', post.p_score_info),  # 返回用户积分详情
    url(r'^user/today_item', post.p_today_item),  # 当日某加分项是否加分
    url(r'^rank$', post.p_rank),  # 返回排行
    url(r'^rank/units$', post.p_rank_units),  # 班级排行
    url(r'^share$', post.p_share),  # 分享
    url(r'^sign$', post.p_sign),  # 签到

    url(r'^tea/send_sms$', post.p_send_sms),  # 教师发短息加分

]


# urlpatterns +=[
#     url(r'^award/cheat$', post.cheat),  # 作弊加分
# ]