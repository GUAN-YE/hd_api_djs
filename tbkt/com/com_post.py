# coding: utf-8
import logging


def batch_conversion_id(old_user_ids):
    """
    批量操作将旧的user_id 转换为 新user_id
    :param old_user_ids: 
    :return: 
    """
    ids = {o:o for o in old_user_ids}
    return ids
