# coding: utf-8
import inspect
import datetime, threading, time,logging
import xmlrpclib
from django.conf import settings as _settings
log = logging.getLogger(__name__)

class SMSInfo(object):
    def __init__(self):
        self.DIANBO = 'AHA3910101'                                 # 点播产品1
        self.DINGO = 'AHA3910101'                                  # 订购产品产品1
        
        self.SPNUMBER = "10657050500001"

        # self.SMS_SERVICE_PATH = 'http://192.168.1.100:9679'        # 服务地址
        self.SMS_SERVICE_PATH = 'http://218.206.202.12:9679'      # 服务地址
        self.SMS_SERVICE_PATH = 'http://218.206.202.12:6083'      # 服务地址
        self.SMS_SPNUMBER = '10657050500001'                       # 网关号
        self.SMS_SERVICECODE = 'AHA3910101'                        # 订购产品代码

        self.SMS_LinkId = ''                                       # 上行的LinkId
        self.SMS__Priority = 2                                     # 优先级1--5
        self.SMS_ScheduleTime = ''                                 # 定时发送时间，格式:yymmddhhmmss
        self.SMS__TimeStamp = int(time.time())                     # 时间戳为大于（1970－1－1　00:00:00 到现在的秒数）

        self.flat_type = 1                                         # 短信平台类型 0、系统发送 1、网站 2、客户端 3、网站后台
        
    def service(self):
        """
        功能说明：获取rpc实例
        -----------------------------
        修改人    修改时间    修改原因
        -----------------------------
        杜祖永   2014-04-11
        -----------------------------
        """
        return xmlrpclib.ServerProxy(self.SMS_SERVICE_PATH)

    def remove_timer_sms(self, data={}):
        """
        功能说明：取消定时短信
        -----------------------------------------
        修改人    修改时间    修改原因
        -----------------------------------------
        杜祖永   2014-04-28
        ----------------------------------------
        data = {"object_id":18,"object_type":3}
        """
        flag = self.service().RemoveTimerSms(data)
        if flag == 0:
            return True
        else:
            return False

    def send_one(self, phone, content, sender={}):
        """
        功能说明：调用同步课堂短信网关单发短信
        -----------------------------------------
        修改人    修改时间    修改原因
        -----------------------------------------
        杜祖永   2014-04-11
        ----------------------------------------
        phone       接收手机号
        content     短信内容
        sender = {
            send_phone  发送手机号
            unit_class_id 发送者班级(主针对教师或学校管理员发送，便于后期短信统计)
            object_id     主记录ID
            object_type   主记录类型 0、系统发送 1、教师发作业 2、批量下发账号密码 3、群发短信
            send_user 发送者账号
            accept_user  接收用户姓名
        }
        ------------------------------
        rpc接口及参数 Submit(self, sp_number, user_number, service_code, msg_content, priority=1, link_id='', schedule_time='', timestamp='')
        """
        # if _settings.URLROOT != "http://192.168.0.100:1356" and _settings.URLROOT != "http://192.168.0.106:83":
        #     log.info("phone_list=%s,content=%s, sender =%s" % (phone, content, sender))
        #     return

        self.SMS__Priority = 1
        sender['flat_type'] = self.flat_type
        if content == '' or phone == '':
            return False

        log.info("SENDONE: phone_list=%s,content=%s, sender =%s" % (phone, content, sender))

        flag = self.service().Submit(self.SMS_SPNUMBER, phone, self.SMS_SERVICECODE, content, self.SMS__Priority, self.SMS_LinkId, self.SMS_ScheduleTime, self.SMS__TimeStamp, sender)

        if flag == 0:
            return True
        else:
            return False
    
    def send_many(self, phone_list, content, sender={}):
        """
        功能说明：同步课堂短信群发
        --------------------------------------------
        修改人    修改时间    修改原因
        --------------------------------------------
        杜祖永   2014-04-11
        --------------------------------------------
        phone_list       接收手机号列表 格式[['手机号','1065705050001','短信内容']...]或['手机号1','手机号2',...]
        content     短信内容
        sender = {
            send_phone  发送手机号
            unit_class_id 发送者班级(主针对教师或学校管理员发送，便于后期短信统计)
            object_id     主记录ID
            object_type   主记录类型默认
            send_user 发送者账号
            accept_user  接收用户姓名
        }
        --------------------------------------------
         rpc接口及参数
        BatchSubmit(self, user_numbers, sp_number, service_code, msg_content, priority=1, link_id='', schedule_time='', timestamp='', sender)
        """
        log.info("SEND_MANY: phone_list=%s,content=%s, sender =%s" % (phone_list, content, sender))
        if self.SMS__Priority == 1:
            self.SMS__Priority = 2
        sender['flat_type'] = self.flat_type
        if not phone_list:
            return False
        flag = self.service().BatchSubmit(phone_list, self.SMS_SPNUMBER, self.SMS_SERVICECODE, content, self.SMS__Priority, self.SMS_LinkId, self.SMS_ScheduleTime, self.SMS__TimeStamp, sender)
        if flag == 0:
            return True
        else:
            return False

    def send_batch(self, phone_list, content, SPNumber="", priority=2, ScheduleTime='', TimeStamp='', sender={}):
        """
        ---------------------------------------------------
        添加人          添加时间           作用
        ----------------------------------------------------
        杜祖永         2014-04-11   多线程发送同步课堂短信
        ----------------------------------------------------
        phone_list       接收手机号列表 格式[['手机号','1065705050001','短信内容']...]或['手机号1','手机号2',...]
        sender = {
            send_phone  发送手机号
            unit_class_id 发送者班级(主针对教师或学校管理员发送，便于后期短信统计)
            object_id     主记录ID
            object_type   主记录类型默认
            send_user 发送者账号
            accept_user  接收用户姓名
            }
        """
        log.info("SEND_BATCH: phone_list=%s,content=%s, sender =%s" % (phone_list, content, sender))
        try:
            sender['flat_type'] = self.flat_type
            t = Mythread(threadFunc, (phone_list, content, SPNumber, priority, ScheduleTime, TimeStamp, sender))
            t.start()
            return True
        except Exception, e:
            print 'send_batch:', str(e)
            return False
    
# 子类化Thread
class Mythread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args
    
    def getResult(self):
        return self.res
    
    def run(self):

        self.res = apply(self.func, self.args)

        
def threadFunc(phone_list, content, SPNumber, priority, ScheduleTime, TimeStamp, sender):
    if _settings.DEBUG:
        if isinstance(content, unicode):
            content = content.encode('utf-8')
        #log.info("THREAD: phone_list=%s,content=%s,SPNumber=%s,priority=%s,ScheduleTime=%s,TimeStamp= %s,sender =%s" % (phone_list, content, SPNumber, priority, ScheduleTime, TimeStamp, sender))
        return
    SmsInfo = SMSInfo()
    SmsInfo.SMS__TimeStamp = TimeStamp or SmsInfo.SMS__TimeStamp
    SmsInfo.SMS_SPNUMBER = SPNumber or SmsInfo.SMS_SPNUMBER
    SmsInfo.SMS__Priority = priority or SmsInfo.SMS__Priority
    SmsInfo.SMS_ScheduleTime = ScheduleTime or SmsInfo.SMS_ScheduleTime
    #总记录数  
    count = len(phone_list)
    #页数
    if count%500:
        pages = count/500+1 
    else:
        pages = count/500

    for i in range(pages):
        try:
            arr_list = []
            start = i*500
            end = (i+1)*500
            for phone_number in phone_list[start:end]:
                if phone_number not in arr_list:
                    arr_list.append(phone_number)
            flag = SmsInfo.send_many(arr_list, content, sender)

        except Exception, e:
            print 'MobileSms1.1.sms.SmsInfo.threadFunc:', str(e)

if __name__ == '__main__':

    SmsInfo = SMSInfo() # 实例化
    SmsInfo.flat_type = 1                                         # 短信平台类型

    sender = {}
    sender['send_phone'] =  '13603450850' # 发送手机号 没有为''
    sender['unit_class_id'] =  889        # 发者班级ID 没有为0
    sender['object_id'] =  888            # 发送对象ID 没有为0
    sender['object_type'] =  888          # 发送类型   没有为0
    sender['send_user'] =  '发送者'       # 发送者账号 没有为''
    sender['accept_user'] =  '接收者'     # 接收者姓名 没有为''
    sender['flat_type'] =  SmsInfo.flat_type

    # 单发
    SmsInfo.SMS_SPNUMBER = '10657050500001' # 可不设置，默认为10657050500001
    SmsInfo.SMS_ScheduleTime = '140428153622' # 定时时间 格式 年月日时分秒 如：140415112622 代表14年04月15日11点26分22少
    #r = SmsInfo.send_one('15290883111',u'单发ddd%s' % datetime.datetime.now(), sender=sender)
    #print  u'单发 %s' % r
    # # 群发
    # r = SmsInfo.send_many(['15290883111'],u'群发%s' % datetime.datetime.now(), sender=sender)
    # print  u'群发 %s' % r
    # 线程群发
    r = SmsInfo.send_batch(['15290883111'], u'线程群发%s' % datetime.datetime.now(), SPNumber="", priority=2, ScheduleTime='', TimeStamp='', sender=sender)
    # 取消定时
    # r = SmsInfo.remove_timer_sms(sender)
    # print  u'取消定时短信 %s' % r
