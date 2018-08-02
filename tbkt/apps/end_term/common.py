# coding: utf-8
from libs.utils import db, num_to_ch


def get_gradelist(subject_id, type, grade_id, book_id=0):
    """
    选年级教材列表
    ---------------------
    王晨光     2017-1-4
    ---------------------
    :param subject_id: 学科ID
    :param type: 1教材 2教辅
    :param grade_id: 年级ID
    :param book_id: 设置教材要对应年级
    :return: [{id:BOOKID, name:书名, press_name:出版社, version:版本, volume:上下册}]
    """
    if type == 1:
        order_by = "order by press_name,p.id, volume"
    else:
        order_by = "order by name,press_name, volume"
    book_related = ''
    if type == 2 and subject_id in (21, 22) and book_id:
        book_related = 'and b.book_id =%s' % book_id
    if subject_id in(21, 91):
        version_str = 'and p.id in (2,8,4) '
    else:
        version_str = ''
    # and p.id in (2,4,8) 代表教材属于人教 北师大 苏教
    sql = """
    select b.id, b.name, b.subject_id, b.grade_id, p.name press_name, p.id press_id, 
        v.name version_name, b.volume, b.book_type
    from zy_book b
    inner join zy_press p on p.id=b.press_id
    inner join zy_press_version v on v.id=b.version_id
    where b.subject_id=%s and b.grade_id=%s and b.book_type=%s and b.is_active=1 %s %s
    %s
    """ % (subject_id, grade_id, type, book_related, version_str, order_by)
    print sql
    books = db.ziyuan_slave.fetchall_dict(sql)
    for b in books:
        b.volume_name = {1: u'上册', 2: u'下册', 3: u'全册'}.get(b.volume, u'')
        b.grade_name = num_to_ch(b.grade_id) + u'年级'
        if b.book_type == 1:
            b.name = b.grade_name + b.volume_name
    if subject_id == 51:
        return yw_book_list(grade_id)
    return books


def yw_book_list(grade_id):
    """
    语文教材列表--北师,人教,苏教
    :param subject_id:
    :param grade_id:
    :return:
    """
    grade_num = "NJ00100" + str(grade_id)
    sql = '''
            SELECT b.dict_Name,a.ct_SeesawVolumes,a.ct_ID,b.dict_ID,a.version  from yw_chinesetextbooks a INNER JOIN yw_dictionary b ON  b.dict_Code = a.ct_VersionNum where b.dict_ID in(2,3,4) AND
            a.ct_Status = 0 AND a.enable_flag = 0 and a.ct_Grade="%s";
        ''' % grade_num
    data_grade = db.tbkt_yw_slave.fetchall_dict(sql)
    for i in data_grade:
        i.volume_name = {1: u'上册', 2: u'下册', 3: u'全册'}.get(i.ct_SeesawVolumes, u'')
        i.press_name = i.dict_Name
        i.subject_id = 51
        i.grade_id = grade_id
        i.grade_name = num_to_ch(grade_id) + u"年级"
        i.name = i.grade_name + i.volume_name
        i.id = i.ct_ID
        del i.dict_Name
        del i.ct_SeesawVolumes
        del i.ct_ID
    return data_grade


def setbook():
    """
    用户设置教材
    :return:
    """
    return
