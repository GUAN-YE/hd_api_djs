# coding:utf-8
"""
@author: lvyang
@time: 2017/12/14
"""

"""
规则如下：
1、 圣诞老人帽子、衣服、手套数量不设限制分布于“在线作业”、“每日任务”、“诗词大战”、“同步习题”
    内，用户完成任意功能均有机会获得随机的任务道具；
2、 圣诞老人鞋设置 10 万个，分布于“在线作业”、“每日任务”、“诗词大战”、“同步习题”内，其中“在
    线作业”1 万，“每日任务”1 万、“诗词大战”4 万、 “同步习题”3 万，邀请用户开通成功 1 万，
    开通用户首次进入奖励圣诞老人鞋不在总数之内
3、 圣诞老人背包设置 1000 个
    A、通过任务获取的背包设置上限 400 个：分布于“在线作业”、“每日任务”、“诗词大战”、“同步题”
        内，其中“在线作业”100 个，“每日任务”各 100 个、“诗词大战”100 个、 “同步习题”100 个
    B、圣诞老人背包通过邀请同学获取的数量上限是 600 个
    C、圣诞老人背包道具需设置成仅开通用户才能获得，未开通用户参加活动无法获得圣诞老人背包道具
4、任务道具可重复获得，每位学生每日仅可获得一次系统发放的任务道具
5、每天活动学生之间相互赠送、索取道具的数量不受限制
6、每天学生邀请用户成功开通获得的圣诞背包数量不受限制
7、赠送、索取的道具需设置成仅开通用户才可使用，未开通用户点击“赠送”“索取”按钮时，吐司提示“仅开
    通用户才可以使用”
8、活动共 17 天，暂定前十天，每天各放出圣诞老人背包 57 个，圣诞老人鞋 6000 个，后七天，每天放出圣诞老人
    背包 61 个，圣诞老人鞋 5714 个
9、圣诞鞋、背包出现概率：
      圣诞鞋：每 5 个用户爆出一个
      圣诞背包：每 500 个人爆出一个
10、如当天道具未发放完毕，则留至第二天继续发放；如当天道具发放完毕出现道具不足的情况，则调用第二天的
    道具继续发放(圣诞老人背包除外)，后期运营会根据实际情况调整道具数量
"""

ACTIVE_ID = 12

# 道具：
PROPS_REMARK = dict(
    hat=u'圣诞帽',
    clothes=u'圣诞衣服',
    shoe=u'圣诞鞋',
    glove=u'圣诞手套',
    bag=u'圣诞背包'
)


# 作业兑换道具
WORK_PROPS = {
    1: dict(name=u'在线作业', hat=-1, clothes=-1, glove=-1, shoe=10000, bag=100),
    2: dict(name=u'每日任务', hat=-1, clothes=-1, glove=-1, shoe=10000, bag=100),
    3: dict(name=u'诗词大战', hat=-1, clothes=-1, glove=-1, shoe=40000, bag=100),
    4: dict(name=u'同步习题', hat=-1, clothes=-1, glove=-1, shoe=30000, bag=100),
    5: dict(name=u'邀请开通', hat=-1, clothes=-1, glove=-1, shoe=10000, bag=600)
}

# 道具发放表
PROPS_WORD = dict(
    hat=dict(name=u'圣诞帽', total=-1, day_num=-1, rate=0.263, item_no='hat'),
    clothes=dict(name=u'圣诞衣服', total=-1, day_num=-1, rate=0.263, item_no='clothes'),
    shoe=dict(name=u'圣诞鞋', total=100000, day_num=6000, rate=0.2, item_no='shoe'),
    glove=dict(name=u'圣诞手套', total=-1, day_num=-1, rate=0.263, item_no='glove'),
    bag=dict(name=u'圣诞背包', total=1000, day_num=57, rate=0.011, item_no='bag')
)
