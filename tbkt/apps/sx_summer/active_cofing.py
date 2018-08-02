# coding:utf-8
"""
三门峡活动'作为区分 ：
score_gift表  category_id 1 为三门峡奖品
active_award表   remark:35 34 32  对应active_id
"""

ACTIVE_ID = 35
# 语文活动id
YW_APP_ID_TEA = 42
YW_APP_ID_STU = 43
# 英语活动id
YY_APP_ID_TEA = 34
YY_APP_ID_STU = 32

# 数学stu
APP_ID_STU = 35

OPEN_USER_ADD_SCORE = 1000

SHARE_NUM = 1
SHARE_SCORE = 100
STU_LOTTERY_COST = 500

# 数学tea
APP_ID_TEA = 36

STU_LOGIN_SCORE = 10

SEND_OPEN_NUM = 1
SEND_OPEN_SCORE = 100

SEND_SMS_NUM = 1
SEND_SMS_SCORE = 50

# 抽奖扣积分
TEA_LOTTERY_COST = 1000

ALL_APP_ID = [APP_ID_STU, APP_ID_TEA, YY_APP_ID_TEA, YY_APP_ID_STU, YW_APP_ID_STU, YW_APP_ID_TEA]
TEA_APP_IDS = [APP_ID_TEA, YY_APP_ID_TEA, YW_APP_ID_TEA]
STU_APP_IDS = [APP_ID_STU, YW_APP_ID_STU, YY_APP_ID_STU]

smx_tea_award_1 = {1: u'ipad'}
smx_tea_award_2 = {i: u'志高挂烫机' for i in range(2, 22)}
smx_tea_award_3 = {i: u'精美天堂太阳伞' for i in range(22, 221)}

smx_stu_award_1 = {1: u'ipad'}
smx_stu_award_2 = {i: u'小米电话手表' for i in range(2, 5)}
smx_stu_award_3 = {i: u'四轴高速遥控飞行器' for i in range(5, 11)}

tea_award_1 = {1: u'ipad', 2: u'ipad', 3: u'ipad'}
tea_award_2 = {i: u'志高挂烫机' for i in range(4, 54)}
tea_award_3 = {i: u'精美天堂太阳伞' for i in range(54, 554)}

stu_award_1 = {1: u'ipad'}
stu_award_2 = {i: u'小米电话手表' for i in range(2, 5)}
stu_award_3 = {i: u'四轴高速遥控飞行器' for i in range(5, 11)}

RANK_AWARD = {
    (APP_ID_TEA, 1): dict(smx_tea_award_1.items()+smx_tea_award_2.items()+smx_tea_award_3.items()),
    (APP_ID_STU, 1): dict(smx_stu_award_1.items()+smx_stu_award_2.items()+smx_stu_award_3.items()),

    (APP_ID_TEA, 0): dict(tea_award_1.items()+tea_award_2.items()+tea_award_3.items()),
    (APP_ID_STU, 0): dict(stu_award_1.items()+stu_award_2.items()+stu_award_3.items()),
}
