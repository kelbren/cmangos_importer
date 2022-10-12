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
equip_offset = 15
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
    "inscription": False,
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

itemSocketBonusMap = {0: 0, 21846: 2895, 21847: 2895, 21848: 2895, 21863: 2863, 21864: 2863, 21865: 2869, 21869: 2880, 21870: 2880, 21871: 2880, 21873: 2863,
21875: 2863, 23506: 1583, 23507: 1585, 23508: 1584, 23509: 2873, 23510: 112, 23511: 2876, 23512: 113, 23513: 113, 23514: 2870, 23515: 2907, 23516: 2873,
23517: 2870, 23518: 2871, 23519: 2873, 23526: 76, 23531: 2860, 23532: 2879, 23533: 2887, 23534: 2882, 23535: 2892, 23536: 2908, 23542: 2925, 23563: 90,
23564: 90, 23565: 90, 24021: 2889, 24022: 2865, 24046: 2864, 24063: 2876, 24064: 2861, 24083: 2865, 24090: 2863, 24091: 2862, 24249: 2909, 24250: 2884,
24251: 3153, 24255: 81, 24256: 2883, 24257: 2900, 24259: 2941, 24261: 94, 24262: 2882, 24263: 2875, 24264: 94, 24266: 2868, 24267: 2875, 24357: 2872,
24363: 113, 24365: 2860, 24366: 2863, 24387: 2870, 24388: 2863, 24391: 2890, 24393: 2866, 24395: 2880, 24396: 2871, 24397: 2868, 24450: 2875, 24452: 2889,
24455: 2865, 24456: 2873, 24457: 2875, 24458: 2874, 24461: 106, 24463: 2876, 24465: 2877, 24466: 2871, 24481: 2864, 24544: 2874, 24545: 2927, 24546: 2879,
24552: 2856, 24553: 2878, 24554: 2859, 25685: 1584, 25686: 1584, 25687: 1585, 25689: 2871, 25690: 2871, 25691: 2876, 25692: 2864, 25693: 2875, 25694: 2875,
25695: 2895, 25696: 104, 25697: 2925, 25830: 2878, 25831: 2874, 25832: 2859, 25838: 2873, 25854: 2859, 25855: 2878, 25856: 2951, 25922: 2860, 25923: 2881,
25924: 2866, 25925: 2875, 25929: 2864, 25930: 2882, 25931: 2882, 25932: 2882, 25942: 2860, 25955: 2865, 25967: 2881, 25968: 2883, 25969: 2882, 25970: 2883,
25997: 2874, 25998: 2878, 25999: 2859, 27408: 2865, 27409: 2865, 27411: 2859, 27414: 2865, 27417: 2863, 27427: 2878, 27428: 2879, 27430: 2871, 27433: 2859,
27434: 2876, 27465: 2859, 27469: 2951, 27471: 2878, 27473: 2859, 27474: 2860, 27475: 2870, 27478: 2863, 27487: 2882, 27492: 2865, 27497: 2860, 27514: 2877,
27527: 2888, 27528: 2859, 27531: 2876, 27545: 2871, 27647: 2867, 27648: 2859, 27649: 2867, 27650: 2867, 27652: 2867, 27653: 2867, 27654: 2867, 27672: 2876,
27702: 2951, 27704: 2878, 27706: 2859, 27708: 2878, 27710: 2859, 27711: 2856, 27713: 2860, 27715: 2892, 27717: 2874, 27718: 2874, 27719: 2874, 27720: 2889,
27737: 2863, 27738: 2875, 27739: 2861, 27743: 2875, 27755: 2859, 27760: 2893, 27771: 2870, 27773: 2869, 27775: 2863, 27776: 2895, 27778: 2880, 27793: 2863,
27796: 2859, 27797: 2887, 27798: 2859, 27801: 2895, 27802: 2900, 27803: 2876, 27813: 2861, 27830: 3153, 27832: 1583, 27833: 1583, 27834: 3153, 27837: 2878,
27843: 2900, 27846: 2887, 27847: 2870, 27879: 2874, 27881: 2878, 27883: 2859, 27893: 2865, 27901: 1584, 27985: 2893, 27986: 2868, 28124: 2876, 28127: 2878,
28129: 2859, 28130: 2874, 28137: 2878, 28139: 2859, 28140: 2856, 28167: 2925, 28170: 2881, 28171: 2926, 28174: 2925, 28176: 2859, 28177: 2875, 28178: 2895,
28179: 2863, 28180: 2927, 28181: 2877, 28182: 2878, 28183: 2889, 28185: 2889, 28186: 2865, 28191: 2889, 28192: 2873, 28193: 2878, 28202: 2874, 28203: 2865,
28204: 2871, 28205: 2932, 28212: 2889, 28218: 2868, 28219: 2936, 28222: 2878, 28224: 2936, 28225: 2873, 28228: 2877, 28229: 2869, 28230: 2868, 28231: 2889,
28232: 2868, 28244: 2886, 28245: 2884, 28264: 2877, 28275: 2865, 28278: 2890, 28285: 2869, 28318: 2879, 28331: 2878, 28333: 2859, 28334: 2874, 28337: 2865,
28338: 2889, 28339: 2860, 28342: 2864, 28348: 2890, 28349: 2869, 28350: 2927, 28381: 2867, 28393: 2889, 28396: 2862, 28401: 2952, 28403: 2952, 28405: 2953,
28406: 2863, 28411: 2953, 28413: 2890, 28414: 2871, 28415: 2889, 28424: 2867, 28445: 2867, 28448: 2867, 28451: 2867, 28483: 2874, 28484: 2874, 28485: 2874,
28502: 2926, 28505: 2863, 28506: 3092, 28507: 2880, 28508: 2974, 28517: 2863, 28518: 2972, 28519: 2893, 28520: 2863, 28521: 2866, 28545: 2860, 28559: 2879,
28560: 3204, 28561: 2973, 28566: 2870, 28572: 2936, 28574: 2973, 28575: 2900, 28576: 2893, 28577: 3205, 28591: 2890, 28593: 2871, 28594: 2889, 28597: 2972,
28605: 2867, 28608: 2879, 28610: 2973, 28613: 2874, 28615: 2878, 28617: 2859, 28619: 2878, 28621: 2868, 28622: 2859, 28623: 2874, 28625: 2878, 28627: 2859,
28628: 2856, 28638: 2867, 28643: 2867, 28646: 2867, 28657: 2925, 28679: 2951, 28681: 2878, 28683: 2859, 28685: 2878, 28687: 2859, 28688: 2874, 28689: 2874,
28691: 2878, 28693: 2859, 28694: 2951, 28696: 2878, 28698: 2859, 28699: 2874, 28701: 2878, 28703: 2859, 28705: 2878, 28707: 2859, 28708: 2856, 28709: 2874,
28711: 2878, 28713: 2859, 28714: 2859, 28715: 2878, 28717: 2951, 28720: 2878, 28722: 2859, 28723: 2856, 28740: 2868, 28741: 2871, 28742: 2890, 28743: 2876,
28746: 2893, 28747: 2870, 28748: 2869, 28750: 2893, 28751: 2869, 28752: 2974, 28755: 2860, 28758: 3204, 28759: 2880, 28760: 2880, 28761: 2879, 28774: 2952,
28776: 2887, 28778: 2895, 28779: 2887, 28780: 2900, 28795: 2879, 28799: 2900, 28800: 2869, 28805: 2874, 28807: 2878, 28809: 2859, 28812: 2878, 28814: 2859,
28815: 2874, 28818: 2878, 28820: 2859, 28821: 2856, 28824: 2879, 28825: 2976, 28827: 2863, 28828: 2887, 28831: 2951, 28833: 2878, 28835: 2859, 28837: 2878,
28839: 2859, 28840: 2874, 28841: 2874, 28843: 2878, 28845: 2859, 28846: 2951, 28848: 2878, 28850: 2859, 28851: 2874, 28853: 2878, 28855: 2859, 28857: 2878,
28859: 2859, 28860: 2856, 28861: 2874, 28863: 2878, 28865: 2859, 28866: 2859, 28867: 2878, 28869: 2951, 28872: 2878, 28874: 2859, 28875: 2856, 28963: 2908,
28964: 2868, 28967: 2900, 28973: 2867, 28978: 2867, 28981: 2953, 28984: 2867, 28988: 2867, 28989: 2867, 28992: 2867, 28996: 2867, 28999: 2867, 29002: 2953,
29006: 2867, 29011: 2972, 29012: 2871, 29016: 2861, 29019: 2952, 29021: 2873, 29023: 2879, 29028: 2872, 29029: 2869, 29031: 2881, 29033: 2908, 29035: 2889,
29037: 2900, 29038: 2927, 29040: 2873, 29043: 2860, 29044: 2877, 29045: 2877, 29047: 2895, 29049: 2872, 29050: 2869, 29054: 2895, 29056: 2864, 29058: 2889,
29060: 2880, 29061: 2865, 29062: 2868, 29064: 2863, 29066: 2932, 29068: 2871, 29070: 2895, 29071: 2868, 29073: 2873, 29075: 2860, 29076: 2889, 29077: 2889,
29079: 2900, 29081: 2877, 29082: 2936, 29084: 2863, 29086: 2869, 29087: 2872, 29089: 2866, 29091: 2908, 29093: 2908, 29095: 2900, 29096: 2873, 29098: 2877,
29100: 2887, 29122: 2900, 29129: 2865, 29135: 2874, 29136: 2874, 29141: 2865, 29142: 2865, 29176: 2876, 29184: 2888, 29316: 2887, 29317: 2875, 29318: 2973,
29319: 2863, 29337: 2868, 29339: 2952, 29340: 2973, 29341: 2864, 29342: 2872, 29343: 2889, 29344: 2869, 29345: 2890, 29489: 1585, 29490: 1584, 29491: 1584,
29492: 1585, 29493: 1584, 29494: 1585, 29495: 1585, 29496: 1584, 29497: 1584, 29498: 1585, 29499: 1584, 29500: 1585, 29515: 2877, 29516: 2893, 29517: 75,
29519: 2889, 29520: 2875, 29521: 3153, 29522: 2889, 29523: 3016, 29524: 2900, 29950: 2927, 29951: 2973, 29966: 3114, 29972: 2889, 29976: 2895, 29984: 2974,
29985: 2877, 29986: 2889, 29991: 2872, 29993: 2936, 29998: 2876, 30030: 2974, 30032: 2887, 30034: 2895, 30036: 2974, 30038: 2900, 30040: 2893, 30042: 2895,
30044: 2900, 30046: 2893, 30047: 2881, 30053: 2887, 30054: 2877, 30055: 3149, 30056: 2868, 30057: 3015, 30064: 2895, 30074: 2952, 30076: 2952, 30079: 2900,
30091: 2925, 30092: 2866, 30096: 2895, 30097: 2974, 30100: 2974, 30101: 2936, 30104: 2893, 30106: 2893, 30107: 2889, 30112: 2974, 30113: 2868, 30115: 2871,
30116: 2925, 30117: 3017, 30118: 2927, 30120: 2927, 30121: 2885, 30122: 2879, 30123: 2932, 30125: 2868, 30126: 2925, 30127: 2895, 30129: 2927, 30131: 2877,
30132: 3015, 30133: 2895, 30134: 2872, 30136: 2865, 30137: 3152, 30138: 2895, 30139: 2877, 30141: 2868, 30142: 2902, 30143: 2895, 30144: 2877, 30146: 2936,
30148: 3114, 30149: 2887, 30150: 2872, 30152: 2865, 30153: 3151, 30154: 2974, 30159: 2889, 30161: 2889, 30162: 3153, 30163: 2900, 30164: 2872, 30166: 2865,
30167: 3151, 30168: 2974, 30169: 2889, 30171: 2908, 30172: 3153, 30173: 2875, 30185: 2952, 30186: 2859, 30187: 2878, 30190: 2877, 30192: 3149, 30194: 2887,
30196: 2889, 30200: 2951, 30206: 2908, 30207: 2909, 30210: 2900, 30212: 2889, 30213: 2925, 30214: 2889, 30215: 2900, 30216: 2872, 30219: 2865, 30220: 3151,
30221: 2974, 30222: 2927, 30228: 2868, 30229: 3149, 30230: 2879, 30231: 2864, 30233: 2889, 30234: 3153, 30235: 2900, 30486: 2874, 30488: 2892, 30490: 2879,
30531: 2889, 30532: 2908, 30533: 2873, 30534: 2936, 30535: 2927, 30536: 2927, 30538: 2873, 30541: 2889, 30543: 2872, 30722: 3094, 30723: 2863, 30724: 2887,
30725: 2875, 30727: 2872, 30728: 2872, 30730: 2952, 30731: 2868, 30732: 2865, 30734: 2889, 30737: 2974, 30739: 2877, 30740: 2879, 30741: 2975, 30861: 2925,
30862: 2925, 30863: 2925, 30864: 2902, 30868: 3151, 30869: 2881, 30870: 2925, 30871: 3098, 30878: 2875, 30879: 2895, 30880: 2893, 30882: 2881, 30884: 2875,
30888: 2900, 30889: 2925, 30893: 2872, 30897: 2863, 30900: 2952, 30905: 2936, 30912: 2872, 30916: 2889, 30969: 2902, 30970: 2925, 30972: 2927, 30974: 2868,
30975: 2952, 30976: 2868, 30977: 3015, 30978: 2925, 30979: 2887, 30980: 2876, 30982: 2941, 30983: 3152, 30985: 2925, 30987: 2871, 30988: 2865, 30989: 2873,
30990: 2889, 30991: 2868, 30992: 2872, 30993: 2941, 30994: 3151, 30995: 2976, 30996: 2974, 30997: 2900, 30998: 2876, 31001: 2902, 31003: 2952, 31004: 2877,
31005: 3149, 31006: 2887, 31007: 3151, 31008: 3153, 31011: 3015, 31012: 2872, 31014: 2889, 31015: 2868, 31016: 2865, 31017: 2889, 31018: 2927, 31019: 2881,
31020: 3153, 31021: 3015, 31022: 2974, 31023: 2900, 31024: 2879, 31026: 3114, 31027: 2873, 31028: 2936, 31029: 3114, 31030: 2973, 31032: 3151, 31034: 3015,
31035: 3153, 31037: 2872, 31039: 2927, 31040: 2889, 31041: 2872, 31042: 2927, 31043: 2889, 31044: 3015, 31045: 3098, 31046: 3153, 31047: 2974, 31048: 2879,
31049: 2900, 31050: 2909, 31051: 2889, 31052: 2889, 31053: 2909, 31054: 2900, 31055: 3153, 31056: 2868, 31057: 2889, 31058: 3153, 31059: 2900, 31060: 2881,
31061: 3153, 31063: 2872, 31064: 2889, 31065: 2889, 31066: 2872, 31067: 3153, 31068: 3151, 31069: 2974, 31070: 2900, 31104: 2889, 31105: 2927, 31106: 2936,
31107: 2889, 31109: 2936, 31110: 2889, 31376: 2878, 31378: 2859, 31379: 2856, 31396: 2951, 31400: 2878, 31407: 2859, 31410: 2878, 31412: 2859, 31413: 2856,
31585: 2878, 31587: 2859, 31588: 2856, 31590: 2878, 31592: 2859, 31593: 2856, 31598: 2867, 31599: 2867, 31613: 2951, 31616: 2878, 31619: 2859, 31622: 2878,
31624: 2859, 31625: 2856, 31626: 2878, 31628: 2859, 31629: 2856, 31630: 2951, 31632: 2878, 31634: 2859, 31635: 2951, 31637: 2878, 31639: 2859, 31640: 2951,
31642: 2878, 31644: 2859, 31646: 2951, 31648: 2878, 31650: 2859, 31657: 2889, 31658: 2877, 31960: 2874, 31962: 2878, 31964: 2859, 31968: 2878, 31971: 2859,
31972: 2874, 31974: 2878, 31976: 2859, 31977: 2856, 31979: 2859, 31980: 2878, 31982: 2951, 31988: 2878, 31990: 2859, 31991: 2856, 31992: 2951, 31996: 2859,
31997: 2878, 31999: 2878, 32001: 2859, 32002: 2874, 32004: 2874, 32006: 2878, 32008: 2859, 32009: 2951, 32011: 2878, 32013: 2859, 32016: 2878, 32018: 2859,
32019: 2856, 32020: 2951, 32022: 2878, 32024: 2859, 32029: 2951, 32031: 2878, 32033: 2859, 32035: 2878, 32037: 2859, 32038: 2856, 32039: 2874, 32041: 2878,
32043: 2859, 32047: 2859, 32048: 2878, 32050: 2951, 32057: 2878, 32059: 2859, 32060: 2856, 32083: 2868, 32084: 2865, 32085: 2865, 32086: 2864, 32087: 2877,
32088: 2927, 32089: 2889, 32090: 2872, 32239: 2900, 32240: 2865, 32241: 2872, 32245: 2895, 32252: 2936, 32263: 2868, 32267: 2895, 32268: 2876, 32271: 2872,
32278: 2895, 32324: 3149, 32328: 2974, 32329: 2872, 32333: 2895, 32342: 2876, 32345: 2879, 32352: 2900, 32353: 2881, 32354: 2864, 32366: 2887, 32367: 2889,
32373: 2868, 32376: 2865, 32461: 2874, 32472: 2951, 32473: 2882, 32474: 2877, 32475: 2872, 32476: 2889, 32478: 2877, 32479: 2872, 32480: 2889, 32494: 2889,
32495: 2872, 32508: 2860, 32519: 2974, 32521: 2868, 32525: 2889, 32609: 2974, 32647: 3114, 32648: 2879, 32652: 3017, 32655: 3153, 32656: 2863, 32675: 2863,
32756: 3164, 32769: 2893, 32776: 2889, 32781: 2925, 32809: 2867, 32810: 2867, 32811: 2953, 32812: 2867, 32813: 2867, 32814: 2867, 32816: 2867, 32817: 2867,
32818: 2867, 32819: 2867, 32820: 2953, 32821: 2867, 32865: 2893, 32866: 2883, 32867: 2900, 32868: 2973, 32869: 2877, 32870: 2936, 32871: 2882, 32872: 3153,
32980: 2953, 32989: 2867, 32997: 2867, 33065: 3164, 33066: 2925, 33067: 3164, 33068: 3164, 32235: 2868, 33122: 2885, 33173: 3205, 33204: 2877, 33808: 2927,
33483: 2974, 33522: 2868, 33524: 2895, 33740: 2878, 33677: 2878, 33640: 3114, 33724: 2878, 33718: 2878, 33745: 2878, 33973: 2900, 33758: 2878, 33711: 2951,
33713: 2878, 33206: 2895, 33530: 2865, 33730: 2874, 33728: 2874, 33675: 2874, 33580: 3015, 33331: 2860, 33680: 2856, 33701: 2878, 33749: 2874, 33192: 3153,
33285: 3153, 33920: 3164, 33913: 2953, 33540: 2902, 33287: 2974, 33589: 3153, 33587: 2974, 33586: 2900, 33528: 2973, 33518: 2872, 33520: 2881, 33191: 2975,
33324: 2974, 33537: 2875, 33534: 2900, 33810: 2868, 33501: 2927, 33517: 2895, 33279: 2876, 33512: 2879, 33515: 2868, 33207: 2863, 33523: 2895, 33535: 3153,
33536: 2900, 33222: 2860, 33578: 3153, 33566: 2889, 33582: 2879, 33577: 2880, 33552: 2865, 33557: 3151, 33559: 2900, 33972: 2889, 33583: 2879, 33211: 3114,
33203: 2872, 33216: 2865, 33480: 2881, 33490: 2872, 33327: 2872, 33286: 2865, 33481: 3017, 33332: 2881, 33479: 2936, 33293: 3153, 33476: 2925, 33326: 2925,
33446: 2974, 33471: 2974, 33453: 2889, 33922: 3164, 33721: 2856, 33760: 2951, 33904: 2867, 33708: 2878, 33813: 3015, 33923: 2925, 33876: 2867, 33704: 2874,
33664: 2874, 33683: 2878, 33906: 2867, 33893: 2867, 33533: 2889, 33666: 2878, 33494: 2889, 33921: 3164, 33901: 2925, 33883: 2953, 33691: 2878, 33694: 2856,
33887: 2867, 33672: 2878, 33738: 2951, 33881: 2867, 33706: 2874, 33751: 2878, 33897: 2867, 33695: 2951, 33685: 2951, 33432: 2936, 33463: 2865, 33748: 2856,
33722: 2951, 33303: 2857, 33894: 2867, 33356: 2872, 33910: 2867, 33917: 2867, 33697: 2878, 33421: 2868, 33473: 2868, 33493: 2973, 33495: 3114, 33768: 2878,
33771: 2856, 33889: 2867, 33492: 2973, 33668: 2859, 33699: 2859, 33726: 2859, 33753: 2859, 33679: 2859, 33682: 2859, 33693: 2859, 33674: 2859, 33770: 2859,
33747: 2859, 33720: 2859, 33732: 3205, 33742: 2859, 33710: 2859, 33703: 2859, 33757: 2859, 33715: 2859, 33971: 2865, 34167: 2865, 34168: 2936, 34169: 2889,
34170: 2890, 34180: 2927, 34181: 2889, 34182: 2889, 34183: 3114, 34185: 2925, 34186: 2864, 34188: 2877, 34192: 2895, 34193: 2875, 34202: 2881, 34208: 2881,
34209: 2881, 34211: 2877, 34212: 2865, 34215: 2927, 34216: 2868, 34229: 2865, 34233: 2890, 34234: 2893, 34243: 2864, 34244: 2873, 34245: 2865, 34332: 2889,
34339: 2865, 34342: 2881, 34345: 3263, 34346: 2879, 34347: 3153, 34348: 3097, 34349: 3114, 34350: 3152, 34351: 2866, 34352: 2895, 34353: 2877, 34354: 2874,
34356: 2877, 34357: 2882, 34358: 3114, 34359: 3153, 34360: 2881, 34364: 2889, 34365: 2865, 34366: 2900, 34367: 2866, 34369: 2936, 34370: 3092, 34371: 2865,
34373: 2936, 34375: 2865, 34377: 3263, 34379: 2865, 34380: 2881, 34381: 2868, 34382: 2868, 34383: 2865, 34384: 2866, 34385: 2877, 34386: 2889, 34388: 2879,
34389: 2895, 34390: 2900, 34391: 2900, 34392: 2893, 34393: 2900, 34394: 2868, 34395: 2865, 34396: 2889, 34397: 2936, 34398: 2865, 34399: 2889, 34400: 2868,
34401: 2868, 34402: 2865, 34403: 2889, 34404: 2868, 34405: 2889, 34406: 2900, 34407: 2900, 34408: 2893, 34409: 2881, 34431: 2925, 34432: 2881, 34433: 3153,
34434: 3153, 34435: 3097, 34436: 3153, 34437: 3153, 34438: 2881, 34439: 2925, 34441: 2925, 34442: 2926, 34443: 3149, 34444: 2925, 34445: 3151, 34446: 3153,
34447: 3152, 34448: 2925, 34485: 2857, 34487: 2881, 34488: 2926, 34527: 3098, 34528: 3153, 34541: 3153, 34542: 3153, 34543: 2881, 34545: 2857, 34546: 3015,
34547: 2925, 34549: 2902, 34554: 3097, 34555: 3152, 34556: 2925, 34557: 3153, 34558: 2902, 34559: 2884, 34560: 2925, 34561: 2902, 34562: 3098, 34563: 3153,
34564: 3153, 34565: 2881, 34566: 3153, 34567: 3015, 34568: 2925, 34569: 3015, 34570: 3149, 34571: 3097, 34572: 2884, 34573: 2925, 34574: 3153, 34575: 2941,
34601: 2879, 34602: 3097, 34605: 2864, 34607: 2900, 34608: 2890, 34610: 2889, 34611: 3153, 34612: 2881, 34615: 2927, 34616: 3114, 34625: 2925, 34697: 3153,
34698: 3114, 34700: 2881, 34701: 3267, 34705: 2881, 34707: 2881, 34788: 2900, 34789: 3015, 34790: 2881, 34791: 2881, 34792: 3153, 34793: 2866, 34795: 2865,
34796: 2865, 34797: 2889, 34799: 2936, 34807: 2879, 34808: 2900, 34809: 3164, 34847: 2889, 34900: 3097, 34901: 2866, 34902: 3097, 34903: 2925, 34904: 3153,
34905: 2900, 34906: 2925, 34910: 2895, 34911: 3149, 34912: 3114, 34914: 2893, 34916: 3149, 34917: 3153, 34918: 2900, 34919: 3153, 34921: 3152, 34922: 2881,
34923: 3152, 34924: 3097, 34925: 2895, 34926: 3097, 34927: 2925, 34928: 2860, 34929: 3149, 34930: 2881, 34931: 2881, 34932: 2925, 34933: 3153, 34934: 2900,
34935: 2925, 34936: 3153, 34937: 2900, 34938: 3153, 34939: 2925, 34940: 2876, 34941: 2925, 34942: 2925, 34943: 2879, 34944: 3015, 34945: 2926, 34946: 2895,
34947: 2925, 35181: 2872, 35182: 2889, 35183: 2872, 35184: 2872, 35185: 2951, 35290: 3153, 35291: 3098, 35292: 3114, 35317: 3164, 35319: 3164, 35329: 2878,
35331: 2859, 35332: 2856, 35333: 2878, 35336: 2859, 35337: 2856, 35339: 2878, 35341: 2859, 35342: 2856, 35343: 2859, 35344: 2878, 35346: 2951, 35357: 2878,
35359: 2859, 35360: 2874, 35362: 2878, 35364: 2859, 35365: 2856, 35367: 2878, 35369: 2859, 35370: 2874, 35372: 2878, 35374: 2859, 35375: 2856, 35376: 2874,
35378: 2878, 35380: 2859, 35381: 2874, 35383: 2878, 35385: 2859, 35386: 2951, 35388: 2878, 35390: 2859, 35391: 2951, 35393: 2878, 35395: 2859, 35402: 2951,
35404: 2878, 35406: 2859, 35407: 2874, 35409: 2878, 35411: 2859, 35412: 2874, 35414: 2878, 35416: 2859, 35464: 2856, 35465: 2859, 35466: 2878, 35467: 2856,
35469: 2874, 35470: 2859, 35472: 2951, 35474: 2878, 35476: 2859, 35478: 2878, 34210: 2900, 34199: 2881, 34194: 2893, 34240: 2881, 34372: 2866, 34374: 2973,
34247: 2868, 34228: 2936, 34329: 3114, 34337: 2890, 34343: 2893, 34333: 2877, 34340: 2889, 34344: 2900, 34341: 2879, 34242: 3153, 34241: 3114, 34355: 2889,
34378: 2879, 34376: 2881, 34232: 2889, 34331: 2973, 35025: 2859, 35026: 2856, 35023: 2878, 35001: 2859, 35002: 2874, 34999: 2878, 35114: 2859, 35115: 2856,
35112: 2878, 35099: 2951, 35096: 2859, 35097: 2878, 34994: 2859, 34992: 2878, 34990: 2874, 35036: 2874, 35033: 2878, 35035: 2859, 35007: 2856, 35006: 2859,
35004: 2878, 35009: 2859, 35012: 2951, 35010: 2878, 35042: 2874, 35046: 2859, 35044: 2878, 35079: 2878, 35081: 2859, 35077: 2951, 35050: 2878, 35052: 2859,
35048: 2951, 35066: 2874, 35070: 3205, 35068: 2874, 35063: 2859, 35059: 2951, 35061: 2878, 35031: 2859, 35027: 2951, 35092: 2859, 35088: 2874, 35090: 2878,
35029: 2878, 35135: 2925, 35133: 3164, 35134: 3164, 35132: 3164, 37928: 3164, 35167: 2867, 35178: 2867, 35171: 2867, 35168: 2953, 35174: 2925, 35179: 2953,
35176: 3015, 35166: 2867, 35169: 2867, 35177: 2867, 35057: 2856, 35054: 2878, 35087: 2856, 35086: 2859, 35084: 2878, 35056: 2859, 35175: 2867, 35170: 2867,
35173: 2867, 35172: 2867, 35180: 2867, 37929: 3164, 34335: 2881}

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
    "firstaid": 129,
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
    "68": [2805, 2803, 0],
    "69": [2803, 2804, 0],
    "78": [2802, 2803, 0],
    "81": [2803, 2806, 0],
    "84": [2803, 0, 0],
    "324": [2817, 0, 0],
    "325": [2815, 0, 0],
    "326": [2818, 0, 0],
    "327": [2819, 0, 0],
    "328": [2820, 0, 0],
    "329": [2821, 0, 0],
    "330": [2803, 2804, 2806],
    "331": [2803, 2825, 3726],
    "332": [2803, 2804, 3726],
}
# endregion

# region sql
pdumpTemplate = Template(
    """IMPORTANT NOTE: This sql queries not created for apply directly, use '.pdump load' command in console or client chat instead.
IMPORTANT NOTE: NOT APPLY ITS DIRECTLY to character DB or you will DAMAGE and CORRUPT character DB

UPDATE character_db_version SET $database_version = 1 WHERE FALSE;

$characters_row
INSERT INTO `character_homebind` VALUES ('$char_guid', '$start_map', '3703', '$pos_x', '$pos_y', '$pos_z');
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '24', '184', '6948'); -- Hearthstone
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '19', '217', '$bag_id'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '22', '218', '$bag_id'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '21', '219', '$bag_id'); -- Large Bag
INSERT INTO `character_inventory` VALUES ('$char_guid', '0', '20', '220', '$bag_id'); -- Large Bag
$inventory_list$pet_list
$skills
$spells
INSERT INTO `item_instance` VALUES ('184', '$char_guid', '6948', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '$enchantments', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('217', '$char_guid', '$bag_id', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '$enchantments', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('218', '$char_guid', '$bag_id', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '$enchantments', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('219', '$char_guid', '$bag_id', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '$enchantments', '0', '100', '0');
INSERT INTO `item_instance` VALUES ('220', '$char_guid', '$bag_id', '0', '0', '1', '0', '0 0 0 0 0 ', '1', '$enchantments', '0', '100', '0');
$instance_list
$actions
$factions
"""
)

instanceEnchantTemplateTBC = Template("$main_enchant 0 0 0 0 0 $gem1 0 0 $gem2 0 0 $gem3 0 0 $socket_bonus 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 0 0 0 ")

instanceEnchantTemplateVan = Template("$main_enchant 0 0 0 0 0 0 0 0 $enchant_1 0 0 $enchant_2 0 0 $enchant_3 0 0 0 0 0 ")

charactersTemplateTBC = Template("INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '300000000', '0', '0', '65568', '$pos_x', '$pos_y', '$pos_z', '$start_map', '0', '1.86449', '2 0 0 8 0 0 1048576 0 0 0 0 0 0 0 0 0 ', '0', '1', '200', '175', '1642414101', '1', '0', '0', '0', '0', '0', '0', '0', '0', '10', '0', '0', '3703', '0', '', '0', '0', '0', '0', '0', '0', '0', '0', '2147483647', '0', '5594', '0', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', NULL, '0', '0 0 ', '0', '0', '0', NULL, NULL, NULL);")

charactersTemplateVan = Template("INSERT INTO `characters` VALUES ('$char_guid', '5', '$char_name', '$char_race', '$char_class', '$char_gender', '$char_level', '0', '300000000', '0', '0', '0', '$pos_x', '$pos_y', '$pos_z', '$start_map', '2.70526', '1024 0 0 0 0 0 0 0 ', '0', '1', '0', '0', '1642834034', '1', '0', '0', '0', '0', '0', '0', '0', '0', '2', '0', '32', '0', '0', '', '0', '0', '0', '0', '0', '0', '0', '63', '79', '0', '0', '100', '0', '4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 4294967295 ', NULL, '0', '0', '0', '0', NULL, NULL, NULL);")

skillsTemplate = Template(
    """INSERT INTO `character_skills` VALUES ('$char_guid', '$skill_id', '$current_skill', '$max_skill');
"""
)

wornTemplate = Template(
    """INSERT INTO `character_inventory` VALUES ('$char_guid', '$bag_id', '$slot_id', '$item_guid', '$item_entry');
"""
)

instanceTemplate = Template(
    """INSERT INTO `item_instance` VALUES ('$item_guid', '$char_guid', '$item_entry', '0', '0', '$item_count', '0', '-1 0 0 0 0 ', '1', '$enchantments', '$item_suffix', '100', '0');
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
