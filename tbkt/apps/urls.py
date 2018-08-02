# coding: utf-8
from django.conf.urls import include, url, patterns

urlpatterns = patterns(
    url(r'sx_summer/', include('apps.sx_summer.urls')),  # 数学暑假活动
    url(r'summer_word/', include('apps.summer_word.urls')),  # 英语暑假活动（我爱记单词）
    url(r'^paper/', include('apps.paper_active.urls')),  # 全省智能组卷抽奖活动
    url(r'^sx_questionnaire/', include('apps.sx_questionnaire.urls')),  # 全省智能组卷抽奖活动
    url(r'^sx/normal/', include('apps.sx_normal.urls')),  # 2017数学常态活动
    url(r'^active/', include('apps.active.urls')),  # 活动查询与添加积分
    url(r'^yy/active/', include('apps.yy_active.urls')),  # 英语所有活动加减分
    url(r'^yy/normal/', include('apps.yy_normal.urls')),  # 2017英语常态活动（s1）
    url(r'^com/', include('apps.com_post.urls')),
    url(r'^yw_activity/', include('apps.yw_activity.urls')),  # 语文常态活动
    url(r'^gift_active/', include('apps.gift_active.urls')),  # 金豆商城活动
    url(r'^excite_activity/', include('apps.excite_activity.urls')),  # 激励抽奖活动
    url(r'^sd/', include('apps.double_festival.urls')),  # 双旦活动
    url(r'^sx_terminal/', include('apps.sx_terminal.urls')),  # 双旦活动
    url(r'^rz/', include('apps.rz_paper.urls')),  # 汝州活动二期试卷活动
    url(r'^winter_activity/', include('apps.winter_activity.urls')),  # 寒假活动
    url(r'^tea/task', include('apps.tea_task_coin.urls')),  # 教师发作业领金币活动
    url(r'^mid_term/', include('apps.mid_term.urls')),  # 教师期中活动
    url(r'^full/class', include('apps.full_class.urls')), # 教师发作业领金币活动
    url(r'pds_xcq/', include('apps.psd_xcq.urls')),  # 数学暑假活动
    url(r'^summer/', include('apps.summer2018.urls')),  # 2018暑假数学试卷扫一扫
    url(r'^terminal/', include('apps.terminal2018.urls')),  # 期末试卷
    url(r'^reading/', include('apps.yw_reading.urls')),  # 语文阅读理解卷活动
    url(r'^summer/', include('apps.summer2018.urls')),  # 2018暑假数学试卷扫一扫
    url(r'summer_activity/', include('apps.summer_activity.urls')),  # 2018暑假活动
)
