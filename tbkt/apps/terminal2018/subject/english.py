# coding: utf-8
import time
from apps.terminal2018.subject.common import create_message
from apps.mid_term.com_yy import yy_common as usercom
from apps.mid_term.send_sx_task import send_sms_user_id
from apps.sx_terminal.send_task import get_unit_students
from libs.utils.thread_pool import call
from .math import get_text_content
from com.com_user import need_login
from libs.utils import db, json,join
from libs.utils import sms, ajax_try
from libs.utils.ajax_json import jsonp_fail, jsonp_ok

# 教材对应的试卷 按照上面的版本顺序，和班级，卷的顺序， 一次向下递加
# press: test_id
BOOK_PAPER = {
    44: [159, 160, 161],  # 人教三起点下
    300: [162, 163, 164],
    641: [165, 166, 167],
    642: [168, 169, 170],
    126: [171, 172, 173],  # 外研三起点下
    305: [174, 175, 176],
    647: [177, 178, 179],
    648: [180, 181, 182],
    177: [183, 184, 185],  # 湘鲁三起点下
    322: [186, 187, 188],
    998: [189, 190, 191],
    999: [192, 193, 194],
}

# 试卷id对应的试卷名字
PAPER = {
    159: '期末提分试卷--(一)',
    160: '期末提分试卷--(二)',
    161: '期末提分试卷--(三)',
    162: '期末提分试卷--(一)',
    163: '期末提分试卷--(二)',
    164: '期末提分试卷--(三)',
    165: '期末提分试卷--(一)',
    166: '期末提分试卷--(二)',
    167: '期末提分试卷--(三)',
    168: '期末提分试卷--(一)',
    169: '期末提分试卷--(二)',
    170: '期末提分试卷--(三)',
    171: '期末提分试卷--(一)',
    172: '期末提分试卷--(二)',
    173: '期末提分试卷--(三)',
    174: '期末提分试卷--(一)',
    175: '期末提分试卷--(二)',
    176: '期末提分试卷--(三)',
    177: '期末提分试卷--(一)',
    178: '期末提分试卷--(二)',
    179: '期末提分试卷--(三)',
    180: '期末提分试卷--(一)',
    181: '期末提分试卷--(二)',
    182: '期末提分试卷--(三)',
    183: '期末提分试卷--(一)',
    184: '期末提分试卷--(二)',
    185: '期末提分试卷--(三)',
    186: '期末提分试卷--(一)',
    187: '期末提分试卷--(二)',
    188: '期末提分试卷--(三)',
    189: '期末提分试卷--(一)',
    190: '期末提分试卷--(二)',
    191: '期末提分试卷--(三)',
    192: '期末提分试卷--(一)',
    193: '期末提分试卷--(二)',
    194: '期末提分试卷--(三)',
}

# 试卷对应的问题
# test_id: [question_id]
PAPER_QUESTION = {
    # 人教下三起点期中试卷三年级
    159: [4832, 9728, 9744, 9754, 9762, 9772, 10914, 10915, 10917, 10918, 10922, 10933, 10944, 10954, 10957, 11372,
          18785, 18802, 18931, 18963],
    160: [174, 3878, 4873, 9512, 9709, 9727, 9746, 9761, 9862, 9864, 10878, 10906, 10919, 10931, 10937, 13393, 17859,
          18810, 19051, 22073],
    161: [3213, 4185, 7268, 8233, 9557, 9726, 9752, 9759, 9861, 10283, 10886, 10907, 10934, 10936, 11486, 18641, 18715,
          21443, 22078, 22946],

    # 人教下三起点期中试卷四年级
    162: [175, 3758, 6309, 6697, 9701, 10970, 10976, 11027, 11056, 11065, 11079, 11141, 13848, 14831, 17810, 18928,
          18990, 22295, 22878, 24082],
    163: [3849, 4480, 5689, 7087, 7876, 9649, 9669, 9697, 10076, 10237, 10975, 10982, 10985, 11007, 11053, 11062,
          11063, 14816, 23706, 23893],
    164: [4490, 7388, 7833, 7874, 8947, 9668, 9680, 9683, 9696, 9698, 10977, 10995, 11005, 11028, 11061, 11083,
          14080, 15637, 18425, 20854],

    # 人教下三起点期中试卷五年级
    165: [2331, 4961, 7156, 9811, 9836, 9836, 9845, 11015, 11097, 11101, 11105, 11119, 11148, 11158, 11168, 11182,
          12510, 16614, 21229, 21362],
    166: [5235, 6715, 8162, 9834, 9835, 9843, 10971, 11092, 11120, 11141, 11149, 11166, 11191, 11192, 14082, 15601,
          17289, 21199, 23222, 23363],
    167: [1264, 2375, 3786, 9792, 9804, 9817, 9830, 10969, 11090, 11096, 11099, 11100, 11157, 11159, 11167, 11171,
          11188, 12775, 19288, 23174],

    # 人教下三起点期中试卷六年级
    168: [5871, 7373, 11205, 11221, 11234, 11240, 11241, 11266, 11267, 11270, 11280, 11284, 12144, 15881, 19700, 21201,
          21203, 23348, 23351, 23648],
    169: [4547, 6534, 11214, 11218, 11227, 11236, 11238, 11268, 11271, 11275, 11279, 11286, 11287, 13379, 15127, 19702,
          20623, 22267, 23342, 23344],
    170: [3927, 7358, 11213, 11215, 11217, 11219, 11228, 11232, 11269, 11272, 11278, 11282, 11285, 19625, 19681, 19756,
          21283, 21629, 23108, 23651],

    # :外研下三起点期中试卷三年级
    171: [9754, 9938, 9962, 9968, 9972, 9984, 9997, 10116, 10121, 10131, 10154, 11398, 11509, 11538, 13821, 14929,
          18684, 20345, 23545, 24057],
    172: [3343, 6702, 9559, 9940, 9942, 9944, 9971, 9973, 9989, 9995, 10115, 10129, 10153, 10160, 11433, 11447,
          11504, 20781, 23547, 23567],
    173: [3342, 6700, 7873, 8202, 9557, 9937, 9941, 9988, 9996, 9998, 10006, 10147, 10152, 10158, 11501, 11506, 11548,
          11550, 17497, 23540],

    # :外研下三起点期中试卷四年级
    174: [10632, 11948, 11957, 11963, 11964, 12012, 12025, 12166, 12194, 12195, 12202, 12227, 12316, 12338, 12345, 12347,
          12403, 12406, 12418, 20678],
    175: [11226, 11944, 11952, 12001, 12143, 12146, 12163, 12168, 12178, 12224, 12277, 12344, 12380, 12383, 12388, 12396,
          12398, 12414, 19799, 23266],
    176: [11947, 12000, 12135, 12150, 12152, 12173, 12193, 12218, 12285, 12287, 12293, 12307, 12349, 12381, 12386, 12421,
          12429, 12471, 19678, 21289],

    # :外研下三起点期中试卷五年级
    177: [10016, 12494, 12498, 12625, 12664, 12680, 12794, 12843, 12848, 12861, 12866, 12883, 12909, 12925, 12927, 12938,
          12946, 13016, 17728, 23777],
    178: [10074, 10875, 12505, 12543, 12607, 12665, 12687, 12721, 12762, 12838, 12856, 12864, 12908, 12953, 12964, 13024,
          13320, 15702, 23735, 23785],
    179: [11959, 12547, 12605, 12638, 12647, 12727, 12733, 12768, 12786, 12799, 12804, 12840, 12849, 12858, 12911, 12944,
          13025, 13029, 14527, 21034],

    # :外研下三起点期中试卷六年级
    180: [9251, 13218, 13231, 13250, 13304, 13344, 13356, 13427, 13436, 13439, 13498, 13522, 13558, 13567, 13700, 13738,
          13744, 14908, 23084, 23462],
    181: [13237, 13264, 13296, 13302, 13350, 13368, 13420, 13422, 13430, 13476, 13507, 13525, 13526, 13693, 13741, 13750,
          21560, 21629, 21761, 23265],
    182: [13209, 13214, 13246, 13280, 13314, 13315, 13349, 13429, 13449, 13477, 13482, 13484, 13511, 13528, 13680, 13747,
          13749, 21747, 23654, 23794],

    # :湘鲁下三起点期末试卷三年级
    183: [6848, 9327, 9557, 9595, 9597, 9617, 9620, 9851, 11623, 11692, 11715, 11722, 11739, 11764, 11816, 21468, 22774,
          22832, 22842, 24087],
    184: [3732, 6855, 9578, 9583, 9596, 9598, 9609, 9624, 9779, 11621, 11636, 11698, 11720, 11723, 11749, 11827, 15506,
          15596, 18770, 18778],
    185: [7257, 8138, 8333, 9554, 9559, 9576, 9594, 9607, 9608, 9614, 9628, 11701, 11719, 11721, 11743, 11825, 11835,
          15941, 17860, 22214],

    # :湘鲁下三起点期末试卷四年级
    186: [287, 9477, 9505, 11083, 11928, 11930, 11933, 11987, 12002, 12138, 12141, 12142, 12144, 12149, 14819, 15471,
          16209, 21826, 22877, 23949],
    187: [267, 4313, 4482, 5100, 9363, 9475, 9503, 10355, 11905, 11998, 12033, 12042, 12075, 12079, 12148, 12164, 13591,
          14837, 20854, 21803],
    188: [4510, 9003, 9367, 9421, 9453, 9476, 9506, 11927, 11985, 12035, 12160, 12162, 12177, 13591, 14927, 16149, 18989,
          19914, 22238, 23838],

    # :湘鲁下三起点期末试卷五年级
    189: [12603, 12604, 12616, 12627, 12659, 12661, 12683, 12708, 12725, 12815, 12860, 12873, 12929, 12959, 12967, 12990,
          13057, 13115, 13170, 13177],
    190: [12523, 12584, 12584, 12606, 12688, 12705, 12719, 12800, 12850, 12863, 12871, 12930, 12961, 12974, 13014, 13060,
          13122, 13173, 13179, 23993],
    191: [5577, 12516, 12610, 12695, 12701, 12741, 12743, 12827, 12857, 12865, 12886, 12936, 12939, 12963, 12972, 12985,
          13062, 13112, 13158, 13162],

    # :湘鲁下三起点期末试卷六年级
    192: [13480, 13548, 13583, 13603, 13610, 13620, 13645, 13659, 13670, 13674, 13676, 13753, 13761, 13789, 13798, 13799,
          13822, 13848, 13889, 16985],
    193: [13502, 13518, 13541, 13612, 13622, 13634, 13642, 13672, 13698, 13702, 13706, 13735, 13748, 13758, 13762, 13776,
          13807, 13809, 13832, 24193],
    194: [13486, 13501, 13504, 13593, 13614, 13615, 13623, 13652, 13669, 13682, 13709, 13724, 13745, 13754, 13764, 13787,
          13797, 13806, 13825, 13829],
}


@ajax_try({})
@need_login
def r_yy_send(request):
    """
    @api {post} /huodong/terminal/yy/send [期末提分试卷英语]教师发试卷
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "type": 103,                         # 期末作业类型
       "unit_id": "622216,578298",           # 班级id 多个以逗号分割
       "title": "试卷标题",                   # 试卷标题 以竖线|分割
       "content": "短信内容",                 # 短信内容 
       "begin_time": "2017-04-8 09:10:00",   # 开始时间
       "end_time": "2017-04-9 23:59:59",     # 结束时间
       "sendpwd": 0,                         # 是否下发账号密码
       "sendscope": 0,          # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信
       "ids":"1"                # 试卷id,多个试卷id以逗号分割
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {},
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    grade_id = request.user.grade_id
    args = request.QUERY.casts(type=int, unit_id=str, title=unicode, content=unicode,
                               begin_time='timestamp', end_time='timestamp', sendpwd=int, sendscope=int, ids=str,
                               agent=int)
    typ = args.type  # 1网上作业 2试卷作业 （本函数都是2）
    unit_id = args.unit_id or ''  # 班级id
    unit_ids = [int(s) for s in unit_id.split(',') if s]
    content = args.content or u''  # 短信内容
    now = int(time.time())  # 现在的时间
    begin_time = args.begin_time or now  # 发布时间
    end_time = args.end_time  # 完成时间
    sendpwd = args.sendpwd or 0  # 下发账号密码 0/1
    sendscope = args.sendscope or 0  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信
    ids = args.ids or ''
    ids = [int(id) for id in ids.split(',') if id]  # 试卷
    title = [s for s in args.title.split('|') if s]
    agent = args.agent or 2
    tea_name = user.name
    open_content = get_text_content(grade_id, tea_name, end_time, subject_id=91)

    if not ids:
        return jsonp_fail(request, message='请选择试卷')
    if not typ and typ != 2:
        return jsonp_fail(request, message='作业类型不能为空')

    if not unit_id:
        return jsonp_fail(request, message='请选择您要发布的班级')

    if not content:
        return jsonp_fail(request, message='短信内容不能为空')

    if len(content) > 200:
        return jsonp_fail(request, message='短信内容不能超过200字')

    if not end_time:
        return jsonp_fail(request, message='请设置作业的完成时间')

    if begin_time < now:
        return jsonp_fail(request, message='定时发布时间不得小于当前系统时间')
    if begin_time >= end_time:
        return jsonp_fail(request, message='定时发布时间不得大于完成时间')

    title = title or "%s试卷" % begin_time.strftime("%m月%d日")

    # 1已发 2待发
    status = 1 if begin_time <= now else 2

    # 查询试卷发送作业状态
    sql = """
    select distinct object_id, c.unit_class_id from yy_task t, yy_task_class c
    where t.type = 103 and t.add_user = %s and t.id = c.task_id 
    and t.status > -1 and c.status > -1 and t.object_id in (%s)
    """ % (user.id, join(ids))
    rows = db.tbkt_yingyu.fetchall_dict(sql)
    done_map = {(i.object_id, i.unit_class_id): 1 for i in rows}
    with db.tbkt_yingyu as dt:
        for k, i in enumerate(ids):
            # create task
            task_id = dt.yy_task.create(
                type=103,
                object_id=i,
                add_user=user.id,
                title=title[k],
                sms_content=content,
                status=status,
                add_time=now,
                begin_time=begin_time,
                end_time=end_time,
                is_sendpwd=sendpwd,
            )

            # create task_class
            # 查询试卷是否发送过 和发送的班级
            class_details = []
            unsent = set()
            for unit_id in unit_ids:
                if done_map.get((i, unit_id)):
                    continue
                d = {'task_id': task_id, 'unit_class_id': unit_id,
                     'type': sendscope, 'add_time': now, 'student_id': '', 'status': status}
                # 判断用户试卷发送过的班级 如果发送过 跳过
                unsent.add(unit_id)
                class_details.append(d)
            if class_details:
                dt.yy_task_class.bulk_create(class_details)
                # create task_details
                task_details = []
                questions = PAPER_QUESTION[i]
                # questions.sort()
                questions_array = []
                d = {}
                d['task_id'] = task_id
                # content_type 学生端作业列表显示
                d['content_type'] = 11
                for qid in questions:
                    questions_array.append({"cid": i, "tcid": i, "qid": qid})
                d['text'] = json.dumps(questions_array)
                task_details.append(d)
                dt.yy_task_detail.bulk_create(task_details)
                pub_ids = []
                questions = PAPER_QUESTION[i]
                for qid in questions:
                    d = {}
                    d['user_id'] = user.id
                    d['subject_id'] = 91
                    d['question_id'] = qid
                    d['add_time'] = time.time()
                    pub_ids.append(d)
                dt.yy_publish_question.bulk_create(pub_ids, ignore=True)  # !!!!!!!!!!!!!!!!!!!!!!!!
                create_message(task_id, user.id, title[k], content, begin_time, end_time, unsent, agent, 91)

        user_phone = db.tbkt_user_slave.auth_user.select('phone').get(id=user.id)
        # send sms or password
        if status == 1 or sendpwd:
            call(send_sms_method, request, unit_ids, status, user_phone, open_content, content, sendpwd)

        data = {}
    return jsonp_ok(request, data)


def send_sms_method(request, unit_ids, status, user_phone, open_content, content, sendpwd):
    students = []
    for unit_id in unit_ids:
        students += get_unit_students(request, unit_id)
        # send sms

    open_ids = ','.join(str(s.id) for s in students if s.is_open == 1)
    not_open_ids = ','.join(str(s.id) for s in students if not s.is_open)
    send_sms_user_id(request, not_open_ids, open_content)
    send_sms_user_id(request, open_ids, open_content)

    # send password
    if sendpwd:
        bind_ids = [s.bind_id for s in students]
        usercom.batch_send_password(bind_ids, sender={'send_phone': user_phone.phone})
        # send im
        # user_ids = [s.id for s in students]
