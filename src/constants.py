from string import Template as Template_base
import sys
import os.path


class Template(Template_base):
    # monkeypatch to avoid rstrip and char_guid everywhere

    def fill(self, **kwds: object) -> str:
        if "no_char_guid" not in kwds:
            kwds["char_guid"] = char_guid

        for k, v in kwds.items():
            if isinstance(v,str):
                kwds[k] = v.rstrip("\n")

        return super().safe_substitute(**kwds) #.rstrip("\n")


# region constants
pet_list = ""
action_list = ""
faction_list = ""
macro_list = ""
skills = ""
spells = ""
inventory_list = ""
instance_list = ""
itemguiditr = 10000
char_guid = 500
equip_offset = 14
learned_professions = {
    "alchemy": False,
    "enchanting": False,
    "engineering": False,
    "blacksmithing": False,
    "jewelcrafting": False,
    "leatherworking": False,
    "tailoring": False,
    "cooking": False,
    "firstaid": False,
}
# endregion

# region mappings
slotMap = {
    "head": 0,
    "neck": 1,
    "shoulder": 2,
    "chest": 4,
    "waist": 5,
    "legs": 6,
    "feet": 7,
    "wrist": 8,
    "hands": 9,
    "finger1": 10,
    "finger2": 11,
    "trinket1": 12,
    "trinket2": 13,
    "back": 14,
    "main_hand": 15,
    "off_hand": 16,
    "relic": 17,
    "tabard": 18,
}

maxSkillMap = {
    "professions": {0: 300, 1:375}
}

startPosMap = {0: {"horde": ['1629.36', '-4373.4', '31.26', '1'], "alliance": ['-8833.38', '628.62', '94', '0'],},
               1: {"horde": ['-1817.69', '5321.56', '-12.4282', '530'], "alliance": ['-1817.69', '5321.56', '-12.4282', '530'],},}

factions = {
    "Human": "alliance",
    "Orc": "horde",
    "Dwarf": "alliance",
    "Night Elf": "alliance",
    "Undead": "horde",
    "Tauren": "horde",
    "Gnome": "alliance",
    "Troll": "horde",
    "Blood Elf": "horde",
    "Draenei": "alliance",
}

races = {
    "Human": 1,
    "Orc": 2,
    "Dwarf": 3,
    "Night Elf": 4,
    "Undead": 5,
    "Tauren": 6,
    "Gnome": 7,
    "Troll": 8,
    "Blood Elf": 10,
    "Draenei": 11,
}

classes = {
    "warrior": 1,
    "paladin": 2,
    "hunter": 3,
    "rogue": 4,
    "priest": 5,
    "shaman": 7,
    "mage": 8,
    "warlock": 9,
    "druid": 11,
}

skillmap = {
    "paladin": {"armor": [293], "weapons": [44, 172, 54, 160, 43, 55, 229, 162, 95]},
    "warrior": {
        "armor": [293],
        "weapons": [44, 172, 54, 160, 43, 55, 229, 45, 226, 46, 136, 176, 162, 95, 118],
    },
    "hunter": {
        "armor": [413],
        "weapons": [
            44,
            172,
            54,
            226,
            173,
            45,
            46,
            229,
            136,
            43,
            55,
            176,
            162,
            473,
            95,
            118,
        ],
    },
    "rogue": {"armor": [], "weapons": [45, 226, 173, 46, 54, 43, 176, 162, 95, 118]},
    "priest": {"armor": [], "weapons": [173, 54, 136, 228, 95]},
    "shaman": {
        "armor": [413],
        "weapons": [44, 173, 54, 136, 172, 160, 473, 162, 95, 118],
    },
    "mage": {"armor": [], "weapons": [173, 136, 43, 162, 228, 95]},
    "warlock": {"armor": [], "weapons": [173, 136, 43, 162, 228, 95]},
    "druid": {"armor": [], "weapons": [173, 54, 136, 160, 162, 473, 95]},
}

gemPropertyMap = {0: 0, 2: 2686, 3: 2687, 4: 2688, 5: 2689, 21: 2690, 22: 2691, 23: 2692, 24: 2693, 25: 2694, 26: 2695, 27: 2697,
                  28: 2696, 29: 2698, 30: 2699, 31: 2700, 32: 2701, 41: 2703, 42: 2704, 61: 2705, 62: 2706, 63: 2707, 64: 2708,
                  65: 2709, 66: 2710, 67: 2711, 81: 2725, 82: 2726, 83: 2727, 84: 2728, 85: 2729, 86: 2730, 87: 2731, 88: 2732,
                  89: 2733, 101: 2734, 102: 2735, 121: 2736, 122: 2737, 123: 2738, 124: 2739, 125: 2740, 126: 2741, 127: 2742,
                  128: 2743, 129: 2744, 141: 2752, 142: 2753, 143: 2754, 144: 2755, 145: 2756, 146: 2757, 147: 2758, 148: 2759,
                  49: 2760, 150: 2761, 151: 2762, 152: 2763, 153: 2764, 154: 2765, 161: 2827, 162: 2828, 163: 2829, 164: 2830,
                  165: 2831, 166: 2832, 167: 2833, 168: 2834, 169: 2835, 181: 0, 182: 2891, 201: 2894, 202: 2896, 203: 2897,
                  204: 2898, 205: 2899, 221: 0, 222: 2917, 241: 2911, 242: 2912, 243: 2913, 244: 2914, 261: 2915, 262: 2916,
                  281: 2921, 282: 2922, 283: 2923, 284: 2924, 301: 2942, 321: 2943, 322: 2944, 323: 2945, 324: 2946, 341: 2947,
                  342: 2948, 361: 2949, 362: 2950, 381: 2956, 382: 2957, 383: 2958, 384: 2959, 385: 2960, 386: 2961, 387: 2962,
                  388: 2963, 389: 2964, 390: 2965, 391: 2966, 392: 2967, 393: 2968, 401: 2969, 402: 2970, 421: 2971, 441: 3045,
                  442: 3046, 443: 3047, 444: 3048, 445: 3049, 446: 3050, 447: 3051, 448: 3052, 449: 3053, 450: 3054, 451: 3055,
                  452: 3056, 453: 3057, 454: 3058, 455: 3059, 456: 3060, 457: 3061, 458: 3062, 459: 3063, 460: 3065, 461: 3064,
                  462: 3066, 463: 3067, 464: 3068, 465: 3069, 466: 3070, 467: 3071, 468: 3072, 469: 3073, 470: 3074, 471: 3075,
                  472: 3076, 473: 3077, 474: 3078, 475: 3079, 476: 3080, 477: 3081, 478: 3082, 479: 3103, 480: 3083, 481: 3084,
                  482: 3085, 483: 3086, 484: 3087, 485: 3088, 486: 3089, 487: 3090, 488: 3091, 501: 3099, 502: 3100, 503: 3101,
                  521: 3104, 522: 3105, 523: 3106, 524: 3107, 525: 3108, 526: 3109, 527: 3110, 528: 3111, 529: 3112, 530: 3113,
                  541: 3115, 542: 3116, 543: 3117, 544: 3118, 545: 3119, 546: 3120, 547: 3121, 548: 3122, 549: 3123, 550: 3124,
                  551: 3125, 552: 3126, 553: 3127, 554: 3128, 555: 3129, 556: 3130, 557: 3131, 558: 3132, 559: 3133, 560: 3134,
                  561: 3135, 562: 3136, 563: 3137, 564: 3138, 565: 3139, 566: 3140, 567: 3141, 568: 3142, 569: 3143, 570: 3144,
                  571: 3145, 572: 3146, 573: 3147, 574: 3148, 581: 3154, 582: 3155, 601: 3156, 602: 3157, 603: 3158, 604: 3159,
                  605: 3160, 606: 3161, 607: 3162, 608: 3163, 621: 3197, 641: 3201, 642: 3202, 661: 0, 681: 3206, 701: 3207,
                  702: 3208, 703: 3209, 704: 3210, 705: 3211, 706: 3212, 707: 3213, 708: 3214, 709: 3215, 710: 3216, 711: 3217,
                  712: 3218, 713: 3219, 714: 3220, 715: 3221, 721: 0, 741: 3226, 801: 3261, 821: 3262, 841: 3264, 861: 3268,
                  901: 3270, 902: 3271, 903: 3272, 921: 3281, 922: 3282, 923: 3283, 941: 3274, 942: 3275, 961: 3280, 981: 3284,
                  982: 3285, 983: 3286, 984: 3287, 1041: 3318, 1122: 3335, 1123: 3336, 1124: 3337, 1125: 3338, 1126: 3339, 1127: 3340}

gemIDPropertyMap = {0 : 0, 23233 : 2, 23234 : 3, 23235 : 4, 23094 : 21, 23095 : 22, 23096 : 23, 23097 : 24, 23113 : 25, 23114 : 26, 23116 : 27,
                    23115 : 28, 23118 : 29, 23119 : 30, 23120 : 31, 23121 : 32, 23364 : 41, 23366 : 42, 23099 : 61, 23105 : 62, 23106 : 63, 23108 : 64,
                    23109 : 65, 23110 : 66, 23111 : 67, 24027 : 81, 24028 : 82, 24029 : 83, 24030 : 84, 24031 : 85, 24032 : 86, 24033 : 87, 24035 : 88,
                    24037 : 89, 24047 : 101, 24048 : 102, 24050 : 121, 24052 : 122, 24054 : 123, 24055 : 124, 24056 : 125, 24057 : 126, 24060 : 127,
                    24062 : 128, 24065 : 129, 23098 : 141, 24058 : 142, 24036 : 143, 23100 : 144, 24061 : 145, 23104 : 146, 24067 : 147, 24053 : 148,
                    23101 : 149, 24059 : 150, 23103 : 151, 24066 : 152, 24051 : 153, 24039 : 154, 25890 : 161, 25893 : 162, 25894 : 163, 25895 : 164,
                    25896 : 165, 25897 : 166, 25898 : 167, 25899 : 168, 25901 : 169, 27679 : 182, 27774 : 201, 27777 : 202, 27785 : 204, 27786 : 205,
                    27864 : 222, 28117 : 241, 28118 : 242, 28119 : 243, 28120 : 244, 28122 : 261, 28123 : 262, 27809 : 281, 27811 : 282, 27820 : 283,
                    27812 : 284, 28290 : 301, 28360 : 321, 28361 : 322, 28362 : 323, 28363 : 324, 22460 : 341, 22459 : 342, 28388 : 361, 28389 : 362,
                    28458 : 381, 28459 : 382, 28460 : 383, 28461 : 384, 28462 : 385, 28463 : 386, 28464 : 387, 28465 : 388, 28466 : 389, 28467 : 390,
                    28468 : 391, 28469 : 392, 28470 : 393, 28556 : 401, 28557 : 402, 28595 : 421, 30546 : 441, 30547 : 442, 30548 : 443, 30549 : 444,
                    30550 : 445, 30551 : 446, 30552 : 447, 30553 : 448, 30554 : 449, 30555 : 450, 30556 : 451, 30558 : 452, 30559 : 453, 30560 : 454,
                    30563 : 456, 30564 : 457, 30565 : 458, 30566 : 459, 30571 : 460, 30572 : 461, 30573 : 462, 30574 : 463, 30575 : 464, 30581 : 465,
                    30582 : 466, 30583 : 467, 30584 : 468, 30585 : 469, 30586 : 470, 30587 : 471, 30588 : 472, 30589 : 473, 30590 : 474, 30591 : 475,
                    30592 : 476, 30593 : 477, 30594 : 478, 30598 : 479, 30600 : 480, 30601 : 481, 30602 : 482, 30603 : 483, 30604 : 484, 30605 : 485,
                    30606 : 486, 30607 : 487, 30608 : 488, 31116 : 501, 31117 : 502, 31118 : 503, 31860 : 521, 31861 : 522, 31862 : 523, 31863 : 524,
                    31864 : 525, 31865 : 526, 31866 : 527, 31867 : 528, 31868 : 529, 31869 : 530, 32193 : 541, 32194 : 542, 32195 : 543, 32196 : 544,
                    32197 : 545, 32198 : 546, 32199 : 547, 32200 : 548, 32201 : 549, 32202 : 550, 32203 : 551, 32204 : 552, 32205 : 553, 32206 : 554,
                    32207 : 555, 32208 : 556, 32209 : 557, 32210 : 558, 32211 : 559, 32212 : 560, 32213 : 561, 32214 : 562, 32215 : 563, 32216 : 564,
                    32217 : 565, 32218 : 566, 32219 : 567, 32220 : 568, 32221 : 569, 32222 : 570, 32223 : 571, 32224 : 572, 32225 : 573, 32226 : 574,
                    32409 : 581, 32410 : 582, 32634 : 601, 32635 : 602, 32636 : 603, 32637 : 604, 32638 : 605, 32639 : 606, 32640 : 607, 32641 : 608,
                    32735 : 621, 32833 : 641, 32836 : 642, 33060 : 681, 33131 : 702, 33132 : 703, 33133 : 704, 33134 : 705, 33135 : 706, 33137 : 708,
                    33138 : 709, 33139 : 710, 33140 : 711, 33141 : 712, 33142 : 713, 33143 : 714, 33144 : 715, 33782 : 741, 34220 : 801, 34256 : 821,
                    34831 : 861, 35315 : 901, 35316 : 902, 35318 : 903, 35487 : 921, 35488 : 922, 35489 : 923, 35501 : 941, 35503 : 942, 35707 : 961,
                    35758 : 981, 35759 : 982, 35760 : 983, 35761 : 984, 37503 : 1041, 38545 : 1122, 38546 : 1123, 38547 : 1124, 38548 : 1125, 38549 : 1126,
                    38550 : 1127}

actionMap = {"spell": 0, "macro": 64, "item": 128}

professionMap = {
    "alchemy": [3101, 3464, 11611, 28596, 2259, 28677, 28675, 28672],
    "enchanting": [13262, 7412, 7413, 13920, 28029, 7411],
    "engineering": [4037, 4038, 12656, 30350, 4036, 20219, 20222],
    "blacksmithing": [9788, 3100, 3538, 9785, 29844, 2018, 17041, 17040, 17039, 9787],
    "jewelcrafting": [25230, 28894, 28895, 28897, 25229, 31252],
    "leatherworking": [10656, 10658, 3104, 3811, 10662, 32549, 2108, 10660],
    "tailoring": [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
    "cooking": [26798, 26801, 26797, 3909, 3910, 12180, 26790, 3908],
    "firstaid": [3274, 3273, 7924, 10846, 27028],
}
all_prof_skill_ids = [v1 for v in professionMap.values() for v1 in v]


professionSkillMap = {
    "alchemy": 171,
    "enchanting": 333,
    "engineering": 202,
    "blacksmithing": 164,
    "jewelcrafting": 755,
    "leatherworking": 165,
    "tailoring": 197,
    "cooking": 185,
    "firstaid": 192,
}

professionSpellMap = { 0 : {
    "alchemy": 11611,
    "enchanting": 13920,
    "engineering": 12656,
    "blacksmithing": 9785,
    "leatherworking": 10662,
    "tailoring": 12180,
    "cooking": 18260,
    "firstaid": 10846,
    }, 1 : {
    "alchemy" : 28596,
    "enchanting": 28029,
    "engineering": 30350,
    "blacksmithing": 29844,
    "jewelcrafting": 28897,
    "leatherworking": 32549,
    "tailoring": 26790,
    "cooking": 33359,
    "firstaid": 27028,
    }
}

genericPetModelMap = {
    "Bat": 7894,
    "Bear": 706,
    "Boar": 4714,
    "Carrion Bird": 20348,
    "Cat": 9954,
    "Crab": 699,
    "Crocolisk": 2850,
    "Dragonhawk": 20263,
    "Gorilla": 8129,
    "Hyena": 10904,
    "Nether Ray": 20098,
    "Bird of Prey": 10831,
    "Raptor": 19758,
    "Ravager": 20063,
    "Scorpid": 15433,
    "Serpent": 4312,
    "Spider": 17180,
    "Sporebat": 17751,
    "Tallstrider": 38,
    "Turtle": 5027,
    "Warp Stalker": 19998,
    "Wind Serpent": 3204,
    "Wolf": 741,
}

suffixTable = {
    "0": [0, 0, 0],
    "5": [2802, 2803, 0],
    "6": [2804, 2803, 0],
    "7": [2803, 2805, 0],
    "8": [2806, 2803, 0],
    "9": [2804, 2806, 0],
    "10": [2804, 2805, 0],
    "11": [2802, 2804, 0],
    "12": [2806, 2805, 0],
    "13": [2802, 2806, 0],
    "14": [2802, 2805, 0],
    "15": [2806, 0, 0],
    "16": [2803, 0, 0],
    "17": [2805, 0, 0],
    "18": [2802, 0, 0],
    "19": [2804, 0, 0],
    "20": [2825, 0, 0],
    "21": [2807, 0, 0],
    "22": [2808, 0, 0],
    "23": [2810, 0, 0],
    "24": [2809, 0, 0],
    "25": [2811, 0, 0, 0],
    "26": [2812, 0, 0],
    "27": [2813, 0, 0],
    "28": [2814, 0, 0],
    "29": [2815, 2802, 0],
    "30": [2816, 0, 0],
    "31": [2803, 2817, 0],
    "32": [2803, 2818, 0],
    "33": [2803, 2819, 0],
    "34": [2803, 2820, 0],
    "35": [2803, 2821, 0],
    "36": [2803, 2804, 2824],
    "37": [2803, 2804, 2812],
    "38": [2804, 2806, 2812],
    "39": [2804, 2824, 2822],
    "40": [2802, 2803, 2825],
    "41": [2805, 2802, 2803],
    "42": [2803, 2806, 2812],
    "43": [2805, 2803, 2823],
    "44": [2803, 2804, 2816],
    "45": [2805, 2803, 2813],
    "47": [2826, 2805, 0],
    "48": [2805, 2906, 2824],
    "49": [2805, 2802, 2803],
    "50": [2825, 2802, 2804],
    "51": [2824, 2822, 2804],
    "52": [2824, 2804, 2813],
    "53": [2824, 2804, 2803],
    "54": [2805, 2823, 2803],
    "55": [2811, 2803, 2804],
    "56": [2805, 2803, 2823],
    "57": [2825, 2802, 2803],
    "58": [2824, 2803, 2804],
    "59": [2804, 2803, 2806],
    "60": [2825, 2803, 2802],
    "61": [2812, 0, 0],
    "62": [2805, 0, 0],
    "63": [2802, 0, 0],
    "64": [2825, 0, 0],
    "65": [2824, 0, 0],
    "66": [2803, 2813, 2824],
}
# endregion

# region sql
pdumpTemplate = Template(
    """IMPORTANT NOTE: This sql queries not created for apply directly, use '.pdump load' command in console or client chat instead.
IMPORTANT NOTE: NOT APPLY ITS DIRECTLY to character DB or you will DAMAGE and CORRUPT character DB

UPDATE character_db_version SET $database_version = 1 WHERE FALSE;

INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '300000000', '0', '0', '65568', '$pos_x', '$pos_y', '$pos_z', '$start_map', '0', '1.86449', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1642414101', '1', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '3703', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '2147483647', '0', '5594', '0', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', NULL, '0', '0 0 ', '0', '0', NULL, NULL, NULL);
INSERT INTO `character_homebind` VALUES ('$char_guid', '$start_map', '3703', '$pos_x', '$pos_y', '$pos_z');
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '24', '184', '6948'); -- Hearthstone
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '19', '217', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '22', '218', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '21', '219', '23162'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '20', '220', '23162'); -- Large Bag
$inventory_list$pet_list
$skills
$spells
INSERT INTO `item_instance` VALUES ('184', '$char_guid', '6948', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('217', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('218', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('219', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('220', '$char_guid', '23162', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ', '0', '100', '0');
$instance_list
$actions
$factions
"""
)

#'-1817.69', '5321.56', '-12.4282'

skillsTemplate = Template(
    """INSERT INTO `character_skills` VALUES ('$char_guid', '$skill_id', '$current_skill', '$max_skill');
"""
)

wornTemplate = Template(
    """INSERT INTO `character_inventory` VALUES ('$char_guid', '$bag_id', '$slot_id', '$item_guid', '$item_entry');
"""
)

instanceTemplate = Template(
    """INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '-1 0 0 0 0 ', '1', '$main_enchant 0 0 0 0 0 $gem1 0 0 $gem2 0 0 $gem3 0 0 0 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 ', '$item_suffix', '100', '0');
"""
)

actionTemplate = Template(
    "INSERT INTO `character_action` VALUES ('$char_guid', '$slot_id', '$action_id', '$action_type');\n"
)

petTemplate = Template(
    "\nINSERT INTO `character_pet` VALUES ('10000', '$pet_entry', '$pet_owner', '$pet_model', '13481', '1', '$pet_level', '0', '1', '1000', '6', '0', '300', '$pet_name', '1', '0', '$pet_health', '$pet_resource', '157750', '1642440972', '0', '0', '7 2 7 1 7 0 129 0 129 0 129 0 129 0 6 2 6 1 6 0 ', '0 0 0 0 0 0 0 0 ');"
)

spellTemplate = Template(
    "INSERT INTO `character_spell` VALUES ('$char_guid', '$spell_id', '1', '0');\n"
)

factionTemplate = Template(
    "INSERT INTO `character_reputation` VALUES ('$char_guid', '$faction_id', '$faction_standing', '1');\n"
)

singleMacroTemplate = Template(
    """MACRO $macro_guid "$macro_name" INV_Misc_QuestionMark
$macro_body
END\n"""
)

# endregion
