# coding=utf-8


from django.conf.urls import url, patterns
from . import paper, post

urlpatterns = patterns('',
                       url(r'^list$', paper.p_list),  # 卷子列表
                       url(r'^paper$', paper.p_paper),  # 试卷详情
                       url(r'^submit$', paper.p_submit),  # 提交
                       url(r'^result$', paper.test_result),
                       url(r'^question$', paper.get_question),
                       )

urlpatterns += patterns('',
                        url(r'^get_grade$', post.p_get_grade),  # 获取学生年级
                        url(r'^set_grade$', post.p_set_grade),  # 设置学生年级
                        url(r'^user_rank$', post.get_user_info),
                        url(r'^rank$', post.p_rank),
                        url(r'^share$', post.user_share),
                        url(r'^add_tea_score$', post.add_tea_score),
                        url(r'^add_open_score$', post.add_open_score),

                        url(r'^award$', post.p_award),
                        url(r'^award/detail$', post.user_award),

                        url(r'^award/result$', post.p_award_result),

                        # 结果页 (学生教师通用)
                        url(r'^rank/result$', post.p_rank_result),
                        url(r'^award/all$', post.p_award_all),

                        )

urlpatterns += patterns('',
                        url(r'^active/info$', post.p_active_info),

                        # 问卷调查加分查询
                        url(r'^questionnaire$', post.questionnaire),

                        )
