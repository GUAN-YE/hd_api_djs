# coding: utf-8

BOOK_PAPER = {
    8: (101, 102, 103),   # 1年级
    65: (156, 157, 158),  # 2年级
    10: (106, 107, 108),  # 3年级
    11: (111, 112, 113),  # 4年级
    12: (116, 117, 118),  # 5年级
    13: (121, 122, 123),  # 6年级

}

# 试卷id对应的试卷名字
PAPER = {
    101: '期末提分试卷-(一)',
    102: '期末提分试卷-(二)',
    103: '期末提分试卷-(三)',

    156: '期末提分试卷-(一)',
    157: '期末提分试卷-(二)',
    158: '期末提分试卷-(三)',

    106: '期末提分试卷-(一)',
    107: '期末提分试卷-(二)',
    108: '期末提分试卷-(三)',

    111: '期末提分试卷-(一)',
    112: '期末提分试卷-(二)',
    113: '期末提分试卷-(三)',

    116: '期末提分试卷-(一)',
    117: '期末提分试卷-(二)',
    118: '期末提分试卷-(三)',

    121: '期末提分试卷-(一)',
    122: '期末提分试卷-(二)',
    123: '期末提分试卷-(三)',
}

# 试卷对应的问题
# paper_id: (question_id)
PAPER_QUESTION = {
    # 1
    101: (52, 62, 73, 75, 84, 88, 97, 103, 107, 109, 116, 119, 123, 128, 130, 135, 137, 145, 148, 157),
    102: (164, 169, 175, 180, 182, 183, 184, 185, 187, 189, 195, 200, 204, 208, 211, 215, 225, 228, 235, 240),
    103: (248, 254, 256, 272, 283, 287, 291, 295),

    # 2
    156: (48, 51, 54, 56, 66, 67, 68, 72, 74, 81, 85, 90, 93, 94, 95, 100, 105, 106, 110, 114, 122, 138),
    157: (142, 151, 156, 160, 162, 170, 181, 186, 196, 205, 216, 224, 231, 234, 243, 244, 245, 247, 249, 251, 252, 253),
    158: (258, 260, 269, 277, 289, 294, 296, 297),


    # 3
    106: (29, 30, 31, 36, 37, 39, 40, 41, 43, 44, 49, 127, 131, 132, 140, 141, 144, 146, 150, 158, 161, 166, 174),
    107: (176, 178, 191, 192, 194, 202, 209, 212, 220, 262, 263, 265, 267, 268, 271, 274, 275, 276, 278, 280, 281, 282, 284, 285),
    108: (298, 299, 300, 301, 302, 303, 304, 305),

    # 4
    111: (28, 53, 58, 60, 63, 64, 70, 76, 80, 83, 87, 91, 317, 322, 326, 327, 328, 329, 330, 333),
    112: (306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 318, 320, 321, 324, 325, 332, 335, 338, 339, 341, 342, 343),
    113: (340, 337, 336, 334, 331, 323, 319, 316),

    # 5
    116: (45, 46, 47, 50, 55, 57, 59, 61, 65, 71, 98, 101, 104, 108, 111, 113, 115, 117, 121, 125),
    117: (134, 136, 152, 154, 167, 171, 172, 177, 197, 198, 203, 206, 213, 217, 219, 221, 222, 227, 230, 232, 233, 236, 238, 241),
    118: (250, 255, 259, 261, 266, 273, 286, 293),

    # 6
    121: (77, 79, 82, 86, 89, 92, 96, 99, 102, 118, 120, 124, 126, 129, 133, 139, 143, 147, 149, 155),
    122: (159, 163, 165, 168, 173, 179, 188, 190, 193, 199, 201, 207, 210, 214, 218, 223, 226, 229, 237, 345, 242),
    123: (246, 257, 264, 270, 279, 288, 290, 292),
}
