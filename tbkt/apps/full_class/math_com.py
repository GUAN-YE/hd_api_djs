# coding: utf-8
"""小学数学公用模块"""
import random
import time
import logging

import datetime

import re
import simplejson as json

from libs.utils import Struct, db, join, num_to_ch, format_url,get_absurl
from com.com_cache import cache

from django.conf import settings

def get_portrait(portrait, type):
    """
    功能说明:获取用户头像
    ------------------------------------------------------------------------
    修改人            修改时间                修改原因
    ------------------------------------------------------------------------
    杜祖永            2010-7-19
    """
    portrait = portrait.strip() if portrait else None
    if portrait:
        return get_absurl(portrait)
    else:
        if type == 1:
            return '%s/user_media/images/profile/default-student.png' % settings.USER_WEB_DJ_URLROOT
        elif type == 2:
            return '%s/user_media/images/profile/default-parents.png' % settings.USER_WEB_DJ_URLROOT
        elif type == 3:
            return '%s/user_media/images/profile/default-teacher.png' % settings.USER_WEB_DJ_URLROOT
        elif type == 4:
            return '%s/user_media/images/profile/default-teacher.png' % settings.USER_WEB_DJ_URLROOT


def replace_symbol(content=""):
    """
    替换特殊符号
    """
    content = u"%s" % content
    replace_content = content.replace('#y#',
                                      '<img src="%s/upload_media/math_img/round.png" /><span class="round"></span>' % settings.FILE_WEB_URLROOT) \
        .replace('#s#',
                 '<img src="%s/upload_media/math_img/delta.png" /><span class="delta"></span>' % settings.FILE_WEB_URLROOT) \
        .replace('#p#',
                 '<img src="%s/upload_media/math_img/rhomb.png" /><span class="rhomb"></span>' % settings.FILE_WEB_URLROOT) \
        .replace('#px#',
                 '<img src="%s/upload_media/math_img/rhomb_lit.png" /><span class="rhomb_lit"></span>' % settings.FILE_WEB_URLROOT) \
        .replace('#f#', '<img src="%s/upload_media/math_img/tupian.png" />' % settings.FILE_WEB_URLROOT) \
        .replace('#word#', '<input class="underline_input" type="text">') \
        .replace('#df#', '<img src="%s/upload_media/math_img/squares_big.png" />' % settings.FILE_WEB_URLROOT) \
        .replace('#ds#',
                 '<img src="%s/upload_media/math_img/delta_big.png" /><span class="delta"></span>' % settings.FILE_WEB_URLROOT) \
        .replace('#dy#',
                 '<img src="%s/upload_media/math_img/round_big.png" /><span class="round"></span>' % settings.FILE_WEB_URLROOT) \
        .replace(u'\\therefore', u'∴') \
        .replace(u'\\because', u'∵')
    return replace_content


def parse_subject(subject):
    """
    解析题干
    :returns: {'content':内容, 'image':{'url':图片地址, 'align':''}}
    """
    if not subject:
        return {"content": "", "image": {"url": ""}}
    obj = json.loads(subject)
    obj["content"] = replace_symbol(obj["content"])
    images = obj.get("images", [])
    if images:
        image = images[0]
        image['url'] = format_url(image['url'])
        obj["content"] += '<br/><br/><img src="%s">' % format_url(image['url'])
    else:
        image = {}
    obj["image"] = image
    return obj


def parse_parse(parse):
    """
    文字解析
    :returns: [{'content':内容, 'image':{'url':图片地址, 'align':''}}]
    """
    if not parse:
        return [{"content": "", "image": {"url": ""}}]
    object_list = json.loads(parse) if parse else []
    new_object_list = []
    for obj in object_list:
        obj["content"] = replace_symbol(obj.get("content", ''))
        images = obj.get('images', [])
        if images:
            image = images[0]
            image['url'] = format_url(image['url'])
        else:
            image = {}
        obj['image'] = image
        obj = Struct(obj)
        new_object_list.append(obj)
    return new_object_list


def parse_video(video_url):
    """
    解析视频绝对地址
    """
    if not video_url:
        return ''
    return "%s/upload_media/%s" % (settings.FLV_WEB_URLROOT, video_url)


def parse_image(image_url):
    """
    解析视频绝对地址
    """
    return format_url(image_url)


def parse_option(op_content):
    """
    解析选项内容
    :returns: {'content':内容, 'image':{'url':图片地址, 'align':''}, 'option':'A', 'is_right':1或0}
    """
    if not op_content:
        return {}
    option = json.loads(op_content) or {}
    option = Struct(option)
    option["content"] = replace_symbol(option.get("content", ""))
    images = option.pop("images", [])
    if images:
        image = images[0]
        image['url'] = format_url(image['url'])
    else:
        image = {}
    option['image'] = image
    option['is_right'] = int(option.get('is_right') or 0)
    return option


def get_right_option(options):
    """
    获得正确选项
    """
    for op in options:
        if op.get('is_right') == 1:
            return op.get('option') or ''
