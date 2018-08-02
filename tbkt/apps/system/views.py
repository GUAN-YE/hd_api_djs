# coding: utf-8
import random
import time
import datetime

from libs.utils import db, ajax, Struct, ajax_try
from com import com_user
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.cache import cache as icache
from django.conf import settings

from . import common

PLATFORM_INFO = {1: 'IOS', 2: 'IOS', 3: 'Android', 4: 'Android'}


@ajax_try({})
def p_version(request):
    """
    @api {get} /system/version [系统]检查版本
    @apiGroup system
    @apiParamExample {json} 请求示例
        {"type":客户端类型, "api":客户端当前内部版本号}

        type客户端类型:
        9安卓学生 10安卓教师 11苹果学生 12苹果教师 13 H5学生 14 H5教师 15 H5活动 16 H5学测评学生 17 H5学测评教师
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "title": "同步课堂手机客户端",
            "last_version": "2.3.12",
            "release_date": "2016-06-27 10:55:04",
            "update": 2,  # 0:不更新  1:选择性更新  2:强制更新
            "content": "2.2.3巫妖王",
            "download": "http://file.tbkt.cn/upload_media/apk/tbkt_stu_android/tbkt_stu_android-release-16.apk"
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
    {
        "message": "找不到该类型的版本信息",
        "next": "",
        "data": "",
        "response": "fail",
        "error": ""
    }
    """
    args = request.QUERY.casts(type=int, api=int)
    type = args.type or 0
    user_api = args.api or 0

    version = db.slave.system_version.filter(type=type).order_by('api', 'release_date').last()

    if not version:
        return ajax.jsonp_fail(request, message="找不到该类型的版本信息")

    data = Struct()
    data.last_version = version.version
    data.release_date = version.release_date
    data.title = version.title
    data.content = version.content
    data.download = version.download
    data.update = 0  # 0:不更新  1:选择性更新  2:强制更新
    min_version = db.slave.system_version.filter(type=type, must=1).order_by('api', 'release_date').last()  # 最低版本
    if min_version and user_api < min_version.api:
        data.update = 2  # 用户版本小于系统设置最低版本则强制更新
    elif user_api < version.api:  # 小于最新版本
        data.update = 2 if version.must else 1  # 根据最新版本设置返回是否需要强制更新

    return ajax.jsonp_ok(request, data)


def p_ping(request):
    """
    @api {get} /system/ping [系统]检查网站是否可用
    @apiGroup system
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {},
        "response": "ok",
        "error": ""
    }
    """
    try:
        row = db.slave.fetchone("select 1")
    except:
        return ajax.ajax_fail(message="数据库出问题了")

    v = random.randint(0, 1000)
    v = str(v)
    icache.set('x', v)
    r = icache.get('x')
    if r is None:
        return ajax.ajax_fail(message="缓存出问题了")

    return ajax.ajax_ok()


def p_info(request):
    """
    @api {get} /system/info [系统]系统信息
    @apiGroup system
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "cs_phone": "12556185",  # 客服电话
            "file_size": 1024*1024,  # 语文上传大小
            "upload_url": "http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=",  # 上传服务器URL
            "hosts": {
                "api": "http://mapi.m.jxtbkt.com", # 公共接口
                "apisx": "http://mapisx.m.jxtbkt.com",  # 数学接口
                "apisx2": "http://mapisx2.m.jxtbkt.com",  # 数学接口
                "apiyy": "http://mapiyy.m.jxtbkt.com"   # 英语接口
                "apiyw": "http://mapiyw.m.jxtbkt.com"   # 语文接口
                "vuestu": "http://stu.m.jxtbkt.com"   # 英语接口
                "vuestusx": "http://stusx.m.jxtbkt.com"   # 英语接口
                "vuestusx2": "http://stusx2.m.jxtbkt.com"   # 英语接口
                "vuestuyy": "http://stuyy.m.jxtbkt.com"   # 英语接口
                "vuestuyw": "http://stuyw.m.jxtbkt.com"   # 英语接口
                "vuetea": "http://tea.m.jxtbkt.com"   # 英语接口
                "joinclass_style": 1, # 1只能输入老师手机号加班级 2是允许手工选地市学校加班级
            },  # 接口地址
        },
        "response": "ok",
        "error": ""
    }

    * upload_url最后的upType=xxx需要调用者补充完整. 
      比如头像是http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=portrait, 
      学测评是http://file.tbkt.cn/swf_upload/?upcheck=e36637e0019323357cfad92fb9a64d17&upType=xcp
    """
    args = request.QUERY.casts(platform=int, version=str, user_id=int)
    platform = args.platform
    version = args.version

    upload_key = common.get_upload_key()
    upload_url = settings.FILE_UPLOAD_URLROOT + "/swf_upload/?upcheck=%s&upType=" % upload_key
    platform_dict = "360000:2,450000:3,320000:4,140000:5,110000:6"

    hosts = {
        'api': settings.URLROOT,
        'apisx': settings.API_URLROOT["sx"],
        'apisx2': settings.API_URLROOT["sx2"],
        'apiyy': settings.API_URLROOT["yy"],
        'vuestu': settings.VUE_URLROOT["com_stu"],
        'vuestusx': settings.VUE_URLROOT["sx_stu"],
        'vuestusx2': settings.VUE_URLROOT["sx2_stu"],
        'vuestuyy': settings.VUE_URLROOT["yy_stu"],
        'vuestuyw': settings.VUE_URLROOT["yw_stu"],
        'vuetea': settings.VUE_URLROOT["com_tea"],
        'vueteacom': settings.VUE_URLROOT["com_tea"],
        'vueteayy': settings.VUE_URLROOT["yy_tea"],
        'vueteayw': settings.VUE_URLROOT["yw_tea"],
        'vueteasx': settings.VUE_URLROOT["sx_tea"],
        'vueteasx2': settings.VUE_URLROOT["sx2_tea"],
        'vuestuxcps': settings.VUE_URLROOT["xcp_stu"],
        'vueteaxcps': settings.VUE_URLROOT["xcp_tea"],
        'apixcps': settings.API_URLROOT["xcp"],
        'qr': "tbkt.cn",
        'goqgurl': settings.GO_URLROOT["qg"],  # 北京和教育对接接口
        'userurl': settings.WEB_URLROOT['user'],  # 网站公共部分
        'other_login_url': 'https://edu.10086.cn/sso/login?service=https://edu.10086.cn/oauth/oauth/authorize?response_type=code&client_id=aMNxVV16&redirect_uri=http%3A%2F%2Fgoqg.tbkt.cn%3Ffrom%3Dwebstu1',
        'h5s': settings.VUE_URLROOT["com_stu"],  # 可以去掉
        'h5t': settings.VUE_URLROOT["com_tea"],  # 可以去掉
        'apiyw': 'https://tbktfile.jxrrt.cn',  # 不要去掉
        'h5syw': 'https://ywstu.m.jxtbkt.cn',  # 可以去掉
        'h5tyw': 'https://ywtea.m.jxtbkt.cn',  # 可以去掉
        'apixcp': settings.API_URLROOT["xcp"],  # 可以去掉
        'xcps': settings.VUE_URLROOT["xcp_stu"],  # 可以去掉
    }

    # ios审核需要
    # if platform == 2 and version == '2.2.2':
    #     hosts['api'] = 'http://v6-mapi.m.tbkt.cn'
    #     hosts['apiyy'] = 'http://v6-mapiyy.m.tbkt.cn'
    #     hosts['h5s'] = 'http://v6-stu.m.tbkt.cn'
    #     hosts['apisx'] = 'http://v6-mapisx.m.tbkt.cn'
    #     hosts['xcps'] = 'http://v6-xcpstu.m.tbkt.cn'
    #     hosts['apixcp'] = 'http://v6-mapixcp.m.tbkt.cn'
    # ios 教师端
    # if platform == 1 and version == '2.2.3':
    #     hosts['api'] = 'https://v6-mapi.m.tbkt.cn'
    #     hosts['vuetea'] = 'https://v6-tea.m.tbkt.cn'
    #     hosts['vueteaxcps'] = 'https://v6-xcpstu.m.tbkt.cn'

    if platform == 3:
        # hosts['vuestuxcps'] = 'https://teaxcp8.m.tbkt.cn/index/0'
        # hosts['vueteaxcps'] = 'https://teaxcp8.m.tbkt.cn/index/0'
        hosts['vuestuxcps'] = 'https://teaxcp8.m.tbkt.cn'
        hosts['vueteaxcps'] = 'https://teaxcp8.m.tbkt.cn'

    if platform == 1 or platform == 2:
        # hosts['vuestuxcps'] = 'https://stuxcp8.m.tbkt.cn/detail/2'
        # hosts['vueteaxcps'] = 'https://teaxcp8.m.tbkt.cn/index/0'
        hosts['vuestuxcps'] = 'https://stuxcp8.m.tbkt.cn'
        hosts['vueteaxcps'] = 'https://teaxcp8.m.tbkt.cn'
    data = {
        # 'cs_phone': '0371-63373776',
        'cs_phone': '12556185',
        'file_size': 1024 * 1024,  # 语文上传大小
        'upload_url': upload_url,  # 上传服务器URL
        'joinclass_style': 0,
        'hosts': hosts,
        'is_show': '1',
        'platform_dict': platform_dict
    }
    return ajax.jsonp_ok(request, data)


def p_download(request, type):
    """
    @api {get} /system/download/<type> [系统]APK下载地址
    @apiGroup system
    @apiParamExample {json} 请求示例
        type: 客户端类型 9安卓学生 10安卓教师
    @apiSuccessExample {json} 成功返回
    成功直接开始下载文件
    @apiSuccessExample {json} 失败返回
    失败返回404
    """
    type = int(type)

    if type not in (9, 10):
        raise Http404()

    # 商店地址
    url = common.get_download_url(type)
    # 官方地址
    if not url:
        version = db.slave.system_version.filter(type=type).order_by('api', 'release_date').last()
        url = version.download if version else ''

    if not url:
        raise Http404()

    # 添加下载记录
    nowt = int(time.time())
    db.default.system_download_type_log.create(
        add_time=nowt,
        down_type=type,
        down_url=url,
    )

    return HttpResponseRedirect(url)


@ajax_try({})
def p_bump_version(request):
    """
    @api {get} /system/bump_version [系统]升级版本号
    @apiGroup system
    @apiParamExample {json} 请求示例
        {"type":客户端类型}

        type客户端类型:
        9安卓学生 10安卓教师 11苹果学生 12苹果教师 13 H5学生 14 H5教师 15 H5活动 16 H5学测评学生 17 H5学测评教师
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "id": 1,  # system_version表主键ID
            "api": 99  # 升级后的内部版本号
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
    {
        "message": "找不到该类型的版本信息",
        "next": "",
        "data": "",
        "response": "fail",
        "error": ""
    }
    """
    args = request.QUERY.casts(type=int, api=int)
    type = args.type or 0

    version = db.slave.system_version.filter(type=type).last()
    if not version:
        return ajax.jsonp_fail(request, message="找不到该类型的版本信息")

    new_api = version.api + 1
    # db.default.system_version.filter(id=version.id).update(api=new_api)

    data = {
        "id": version.id,
        "api": new_api,
    }
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@com_user.need_login
def p_active_info(request):
    """
    @api {post} /system/active_info [系统]是否开启活动权限
    @apiGroup system
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "extend": {},
                "banner_url": "",           # banner 地址
                "banner_end": "2017-05-21 23:59:59",    # banner图上的结束时间
                "name": "商丘市拓城县我爱记单词",          # 活动时间
                "banner_begin": "2017-05-09 00:00:00",      # banner图上的开始时间
                "is_open": 2,                               # is_open = 0, banner不显示， 否则显示
                "begin_url": "/huodong/sq_word/index",      # 活动的入口地址
                "active_id": 26                             # 活动id
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    data = common.active_info(user)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
@com_user.need_login
def p_blocks(request):
    """
    @api {post} /system/blocks [系统]模块展示接口
    @apiGroup system
    @apiParamExample {json} 请求示例
        {"type":"类型名"}

        *type: APP数学appsx, APP语文appyw, APP英语appyy, APP其他appqt
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "opensubject_alert": "您还未开通数学",
            "blocks": [
                {
                    "alias": "think",
                    "charge": 1
                }
            ]
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(type=str)
    type_alias = args.type
    if not type_alias:
        return ajax.jsonp_fail(request, message='缺少参数: type')
    user = request.user
    data = common.get_user_block_info(user, type_alias)
    return ajax.jsonp_ok(request, data)


@ajax_try([])
def p_platforms(request):
    """
    @api {get} /system/platforms [系统]平台配置列表
    @apiGroup system
    @apiParamExample {json} 请求示例
        {"id":平台ID}

        *如果不指定平台ID则返回所有平台配置
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "province": "410000",  # 省行政编码
                "is_sms": 1,    # 是否能发短信
                "is_open": 1,   # 是否要开通学科
                "id": 1,        # 平台ID
                "name": "河南"  # 平台名称
                "is_setprofile":1       # 是否可以设置个人信息或班级
            },
        ],
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(id=int)
    id = args.id
    if id:
        platforms = db.user_slave.platform.filter(id=id)[:]
    else:
        platforms = db.user_slave.platform[:]
    return ajax.ajax_ok(data=platforms)
