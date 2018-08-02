# coding: utf-8
import random
import time
import datetime
from contextlib import contextmanager
from functools import wraps

from django.conf import settings

from com import com_user
from com.com_cache import cache
from libs.utils import db, Struct, format_url


def ctime(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print (func.__name__, end - begin)
        return result

    return wapper


@contextmanager
def timeblock(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{} : {}'.format(label, end - start))


class Award(object):
    """
    抽奖相关方法
    -----------------------------------------------
    吕杨      2017-09-11
    -----------------------------------------------
    :param :active_id  对应抽奖奖品活动id  ，active_score_gift 表
    :param: app_id  多个活动公用一个抽奖时，用于区分不同活动 , active_award 表 remark字段保存app_id
    :param: lottery_cost  抽奖对应扣积分数
    """

    def __init__(self, active_id, app_id, user=None, lottery_cost=0):
        self.active_id = active_id
        self.app_id = app_id
        self.user = user
        self.lottery_cost = abs(lottery_cost)

    @property
    def award_able(self):
        """是否具有抽奖资格"""
        # 活动结束时间 2017-10-31:23:59:59
        active = db.tbkt_active.active.filter(id=self.app_id).select('begin_time','end_time').last()
        if not active:
            return False,u'没有该活动'
        if int(time.time()) >= active.end_time:
            return False, u'活动已经结束！'

        if not (self.app_id and self.active_id and self.user and self.lottery_cost):
            return False, u'缺少参数'

        if self.user.platform_id != 1:
            return False, u'非河南用户现在无法参与！'

        if not db.tbkt_active.active_score_user.filter(active_id=self.app_id, user_id=self.user.id,
                                                       score__gte=self.lottery_cost).exists():
            return False, u'积分不足，快去赚取积分吧！'
        return True, u''

    @ctime
    def add_award_detail(self, award_sort):
        """读取奖品信息"""
        detail = db.tbkt_active.active_score_gift.filter(active_id=self.active_id, active_type=1, del_state=0).select(
            'name', 'status', 'sequence award_type').order_by('sequence')[:]
        if not detail:
            raise ValueError("lack Value: detail!", detail)
        detail_dict = {int(i.award_type): i for i in detail}
        for a in award_sort:
            d = detail_dict.get(int(a['award_type']) or None)
            a['name'] = d.name if d else ''
            a['status'] = d.status if d else 0
        return award_sort

    @ctime
    def draw_award(self, award_sort=None, once=1, default_award=None):
        """
        抽奖
        :param award_sort:[{award_type:1,rate:0.001,total:3,day_num:1, is_award: 1}]
                    award_type:几等奖，rate:中奖比例，total: 奖品总量，day_num: 单日奖品发放量，-1 为不限量
                    is_award: 1 是奖品，0 谢谢参与
        :param once : 同一个奖品，用户是否只能中奖一次，默认是
        :param default_award:  重复中奖/超出日发奖范围/超出总数 后  改为中奖默认值，
        """
        able, why = self.award_able
        if not able:
            return False, why
        deduct = self._deduct_score()
        if not deduct:
            return False, u'扣分失败'
        # 获取奖品名称
        award_sort = self.add_award_detail(award_sort)
        if not default_award:
            default_award = Struct(name=u'谢谢参与', award_type=len(award_sort) + 1, status=1, rate=1, total=-1,
                                   day_num=-1, is_award=0)

        award = self._probability(award_sort, default_award, once)
        result = self._draw(award, default_award)
        return True, result

    @ctime
    def _draw(self, award, default_award):
        """保存抽奖结果"""
        success = 0
        if int(award.is_award) and award != default_award:
            with db.tbkt_active as c:
                sql = """
                    select id,num from active_score_gift  where sequence=%s and active_id=%s and status=1
                    and active_type=1 and del_state=0  for update
                """ % (award.award_type, self.active_id)
                gift = c.fetchone_dict(sql)
                if gift and gift.num > 0:
                    c.execute("update active_score_gift set num=%s where id=%s" % ((gift.num - 1), gift.id))
                    success = 1
        if not success:
            award = default_award
        db.tbkt_active.active_award.create(
            active_id=self.active_id,
            user_id=self.user.id,
            user_name=self.user.name,
            award_name=award.name,
            award_type=award.award_type,
            city=self.user.city,
            add_time=int(time.time()),
            remark=self.app_id
        )
        del award.rate
        del award.status
        del award.day_num
        del award.total
        return award

    @ctime
    def _deduct_score(self):
        """修改积分"""

        score_user = db.tbkt_active.active_score_user.get(active_id=self.app_id, user_id=self.user.id, )
        if not score_user or not int(self.lottery_cost) or int(self.lottery_cost) > int(score_user.score):
            return False

        city = str(self.user.city or 0)
        unit_id = str(self.user.unit.id if self.user.unit else 0)
        sql_1 = """
            INSERT INTO active_score_user_detail (active_id, user_id, item_no, score, add_date,remark,add_username)
            VALUES (%s,'%s','%s',%s,'%s','抽奖',%s);
        """ % (self.app_id, self.user.id, 'lottery', -self.lottery_cost, str(int(time.time())), self.user.id)

        sql_2 = """
          UPDATE active_score_user SET score = score+%s ,city=%s,unit_id=%s WHERE active_id = %s AND user_id=%s;
        """ % (-self.lottery_cost, city, unit_id, self.app_id, self.user.id)

        try:
            with db.tbkt_active as c:
                c.execute(sql_1)
                c.execute(sql_2)
        except Exception, e:
            print e, sql_1, sql_2
            return False
        return True

    @ctime
    def _probability(self, sort, default_award=None, once=1):
        """
        中奖概率
        :param sort:[{award_type:1,rate:0.001,total:3,day_num:1, is_award: 1}]
                    award_type:几等奖，rate:中奖比例，total: 奖品总量，day_num: 单日奖品发放量，-1 为不限量
                    is_award: 1 是奖品，0 谢谢参与
        :param once : 同一个奖品，用户是否只能中奖一次，默认是
        :param default_award:  重复中奖/超出日发奖范围/超出总数 后  改为中奖默认值，
        :return:
        """
        if not sort:
            raise ValueError("lack Value: sort!", sort)
        if not default_award:
            raise ValueError("lack Value: default_award!", default_award)

        dice = random.random()
        begin = 0
        award = []
        for s in sort:
            if begin < dice <= begin + s['rate'] and s['status'] == 1:
                award = s
                break
            else:
                begin += s['rate']
        if not award:
            award = default_award
        award_type = award['award_type']

        if award != default_award:
            # 判断总量是否发完：
            if int(award['total']) != -1 and self.all_award_num(award_type) >= int(award['total']):
                award = default_award
            # 判断单日奖品是否发完:
            if int(award['day_num']) != -1 and self.day_award_num(award_type) >= int(award['day_num']):
                award = default_award
            # 判断用户是否已经抽过奖:
            if once:
                if self.user_award_num(award_type) >= 1:
                    award = default_award
        return Struct(award)

    @ctime
    def day_award_num(self, award_type):
        """单日奖品已经发出去的数量"""
        sql = """
            select count(1) num from active_award
            where active_id=%s and award_type=%s and add_time>='%s'
        """ % (self.active_id, award_type, today_temp())
        row = db.tbkt_active.fetchone_dict(sql)
        return row.num if row else 0

    @ctime
    def user_award_num(self, award_type):
        """用户抽过该奖品次数"""
        num = db.tbkt_active.active_award.filter(active_id=self.active_id, award_type=award_type,
                                                 user_id=self.user.id).count()
        return num

    @ctime
    def all_award_num(self, award_type):
        """单项奖品中奖次数"""
        num = db.tbkt_active.active_award.filter(active_id=self.active_id, award_type=award_type).count()
        return num

    @ctime
    def user_award_detail(self):
        """返回用户获奖情况"""
        detail = db.tbkt_active.active_award.select('award_name','award_type','user_id','user_name','active_id','city','add_time').filter(
            active_id=self.active_id, user_id=self.user.id,
            remark=str(self.app_id)).exclude(award_name=u'谢谢参与').order_by('-id')[:]

        if not detail:
            return []
        gift = db.tbkt_active.active_score_gift.filter(active_id=self.active_id, active_type=1, del_state=0).select(
            'img_url', 'sequence award_type')[:]
        gift_url = {int(i.award_type): i.img_url for i in gift}
        award_detail = []
        for d in detail:
            img_url = format_url(gift_url.get(int(d.award_type) or ''))
            awd = dict(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d.add_time)).decode('utf-8'),
                       name=d.award_name,
                       url=img_url,
                       award_type=d.award_type)
            award_detail.append(awd)
        return award_detail

    @ctime
    def recent_award(self):
        """返回最近10位用户获奖获奖情况"""
        award_detail = cache.hd_resent_award.get(self.app_id)
        if not award_detail:
            detail = db.tbkt_active.active_award.select('award_name','award_type','user_id','user_name','active_id','city').filter(
                active_id=self.active_id,
                remark=str(self.app_id)
            ).exclude(award_name=u'谢谢参与').order_by('-id')[:10]

            if not detail:
                return []
            gift = db.tbkt_active.active_score_gift.filter(active_id=self.active_id, active_type=1, del_state=0).select(
                'img_url', 'sequence award_type')[:]
            gift_url = {int(i.award_type): i.img_url for i in gift}
            award_detail = []
            for d in detail:
                img_url = format_url(gift_url.get(int(d.award_type) or ''))
                awd = dict(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d.add_time)).decode('utf-8'),
                           award_name=d.award_name,
                           url=img_url,
                           award_type=d.award_type,
                           user_name=d.user_name)
                award_detail.append(awd)
                cache.hd_resent_award.set(self.app_id,award_detail)
        return award_detail

    @ctime
    def all_award_detail(self, p=1):
        """分页返回全部获奖用户"""
        begin = int((p - 1) * 10)
        sql = """
                select (@rowNum:=@rowNum+1) as num ,a.user_name ,a.award_name, a.user_id,a.award_type from active_award a ,
                (select (@rowNum :=%s)) z
                where a.active_id=%s and award_name<>'谢谢参与' order by a.award_type ,a.id DESC limit  %s	 ,%s
        """ % (begin, self.active_id, begin, 10)
        detail = db.tbkt_active.fetchall_dict(sql)
        if not detail:
            return [],0
        user_ids = list(set([a.user_id for a in detail]))
        user_info = com_user.users_info(user_ids)

        gift = db.tbkt_active.active_score_gift.filter(active_id=self.active_id, active_type=1, del_state=0).select(
            'img_url', 'sequence award_type')[:]
        gift_url = {int(i.award_type): i.img_url for i in gift}
        award_detail = []
        for d in detail:
            img_url = format_url(gift_url.get(int(d.award_type) or ''))
            awd = Struct(time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d.add_time)).decode('utf-8'),
                         name=d.award_name,
                         url=img_url,
                         award_type=d.award_type)
            info = user_info.get(d.user_id)
            if info:
                awd.update(info)
            award_detail.append(awd)

        rank = sorted(award_detail, key=lambda x: x.num)
        sql = """
          select count(1) num from active_award a where active_id=%s  and award_name<>'谢谢参与' and remark='%s'
          """ % (self.active_id, self.app_id)
        total = db.tbkt_active.fetchone_dict(sql)
        return rank, total.num


def show_award(active_id, active_type=1):
    """
    根据活动奖品获取展示奖品 及 活动规则
    ————————————————————
    王世成      2017-09-11
    ————————————————————
    :param active_id 活动id
    :param active_type 奖品类型 (默认抽奖)
    :return: 
    """
    award = db.tbkt_active_slave.active_score_gift.filter(
        active_id=active_id, active_type=active_type, status=1, del_state=0).order_by('sequence')[:]

    if not award:
        return []
    out = []
    for a in award:
        arg = {
            'active_name': a.name,
            'active_id': a.active_id,  # 活动id
            'active_type': a.active_type,  # 活动奖品类型 1.抽奖 2.排名
            'sequence': a.sequence,  # 奖品是几等奖
            'num': a.num,  # 奖品数量
            'start_num': a.start_num,  # 该奖品开始范围
            'end_num': a.end_num,  # 该奖品结束范围
            'img_url': format_url(a.img_url)  # 奖品图片绝对url
        }
        out.append(arg)
    return out

def today_temp():
    to_day = datetime.datetime.now()
    d = datetime.datetime(to_day.year, to_day.month, to_day.day, 0, 0, 0)
    return int(time.mktime(d.timetuple()))