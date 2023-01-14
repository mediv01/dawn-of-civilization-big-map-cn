# coding=utf-8
from Consts_Basic import *

PYTHON_DEBUG_MODE = 0
#  1为调试模式，可以输出调试日志，发版时设置为0


# 禁用的国家的ID，该国家不会出生
PYTHON_NO_BIRTH_COUNTRY = ()

# 禁用的AIWAR ID，该AIWAR不会发生
PYTHON_NO_AIWAR_ID = ()

#  人类玩家修正系数是否启用
PYTHON_HUMAN_MODIFIER_ENABLE = 0
#  S表示数值越小对人类玩家惩罚越大，B表示数值越大对人类玩家的惩罚越大
#                         文化（S）  升级经验阈值（B）  科研惩罚（B）  距离维护费（B）  城市数量维护费（B） 政策经验阈值（B） 此项别改   造单位费用（B）    造奇观费用（B）      造建筑费用（B）     通胀率（B）     伟人阈值（B）    人口增长阈值（B）
PYTHON_HUMAN_MODIFIER = (100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100)


#  AI玩家修正系数是否启用
PYTHON_AI_MODIFIER_ENABLE = 0
#  S表示数值越小对AI玩家惩罚越大，B表示数值越大对AI玩家的惩罚越大
#                         文化（S）  升级经验阈值（B）  科研惩罚（B）  距离维护费（B）  城市数量维护费（B） 政策经验阈值（B） 此项别改   造单位费用（B）    造奇观费用（B）      造建筑费用（B）     通胀率（B）     伟人阈值（B）    人口增长阈值（B）
PYTHON_AI_MODIFIER = (100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100)



PYTHON_HARRAPA_NO_AUTO_DECLINE = 1
# 哈拉帕不会自动消失

# 例如：增大人类玩家难度的参数组合
# PYTHON_HUMAN_MODIFIER =(     80,       150,            1000,          150,            150,           150,            100,          150,               150,               150,             120,            120,             120)


################       GlobalDefineAlt.xml仅与Python相关的移植到这里了       ##########################


#     <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON1   公共选项 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

PYTHON_ENABLE_OBSERVER_MODE = 1
# 1为启用观海模式选项，0为默认模式

PYTHON_USE_ADVANCE_ALERT = 1
# 1为可以使用高级提示信息 0为默认模式

PYTHON_SHOW_MINOR_CITY_TEXT = 1
# 1为显示独立城邦建城的信息  0为默认模式

PYTHON_SHOW_BARBARIAN_TEXT = 1
# 1为显示野蛮人入侵的信息  0为默认模式

AIWAR_PY_HUMAN_AI_WAR_ALERT = 1
# 1为AIWAR.py里的提前预警  0为默认模式

PYTHON_CAN_USE_TECHTRADE_VALUE_ALERT = 1
# 大于0的数字为开启科技交易提示功能，0为默认模式

PYTHON_TECHTRADE_VALUE_MIN_PERCENT = 90
# 大于0的数字为显示可交易科技最低价值的阈值，95代表95%，0为默认模式

PYTHON_CAN_USE_ASK_MONEY_ALERT = 0
# 大于0的数字为开启可勒索金币弹出框提醒，由于积分版已经有类似的功能，建议设置为0不开启，以免重复提醒，0为默认模式

PYTHON_CIV4_ALERT_ON_HURRY_ONLY_IN_HURRYANGER_ZERO = 1
# 大于0的数字为加速额外愤怒人口为0时才提示加速信息，0为默认模式

PYTHON_CIV4_ALWAYS_SHOW_STRNGTH_IN_SCRREN = 1
# 大于0的数字为在界面总是显示军力占比，0为默认模式

PYTHON_ENABLE_GAMETURN_CALCLATOR = 1
# 1为启用回合计算器，0为默认模式

PYTHON_ENABLE_HISTORY_DAY = 1
# 1为启用历史上的今日功能，0为默认模式

#      <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON2  特色选项 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

PYTHON_ALLOW_HISTORY_FORTUNE_TO_AI = 1
#    <!--  1为仿照欧陆风云，对AI设置历史幸运，0为默认模式  mediv01 2021年8月版本 -->

PYTHON_ALLOW_HISTORY_FORTUNE_TO_HUMAN = 1
#    <!--  1为仿照欧陆风云，对人类设置历史幸运，0为默认模式  mediv01 2021年8月版本 -->

PYTHON_MANUAL_RESURRECTION_CIV = 1
#    <!-- 1为启用主动复活文明的机制，在特定的节点复活比较重要的文明 0为默认模式 mediv01 -->

PYTHON_MANUAL_RESURRECTION_CIV_MAINCIV = 1
#   <!-- 1为启用主动复活英法等主要文明的机制，在特定的节点复活比较重要的文明 0为默认模式 mediv01 -->

PYTHON_MANUAL_RESURRECTION_AFTER_MONGOLIA = 1
#   <!-- 1为蒙古崩溃后主动复活明朝、帖木儿和瓦剌 0为默认模式 mediv01 -->

PYTHON_ONLY_RESPAWN_IN_CORE = 1
#     <!-- 1为只在核心区复活 0为默认模式，在历史区复活 mediv01 -->

PYTHON_ALWAYS_SHOW_WONDER_BEING_BUILD = 1
#     <!-- 1为永远显示正在建筑的奇观 0为默认模式 mediv01 -->

#      <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON3  稳定度选项 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

STABILITY_RESURRECTION_ARMY_SIZE = 0
#  <!-- 大于0的数字为复活军队的数量 0为默认模式 mediv01 -->

STABILITY_PY_ONLY_COLLAPSE_TO_INDEPENDENT = 0
#  <!-- 1为崩溃时仅允许崩溃给独立城邦,代码在stability.py   0为默认模式 mediv01 -->

STABILITY_PY_ERA_STABILITY_FOR_BIG_COUNTRY  = 1
#    <!-- 1为设立时代稳定度  0为默认模式 mediv01 -->

STABILITY_PY_COLONY_COLLAPSE = 1
#   <!-- 1为按照历史时期设定殖民体系的崩溃   0为默认模式 mediv01 -->

STABILITY_PY_AI_COLLAPSE_TO_CORE_REGULARLY = 1
#      <!-- 1为AI控制的大帝国会经历不稳定时期，崩溃至核心,代码在stability.py   0为默认模式 mediv01 -->

STABILITY_NEWLY_CAPTURE_CITY_WITH_MORE_PUNISHMENT = 1
#    <!--  大于0的数字表示计算稳定度时，新占领的城市惩罚较大，0为默认模式  mediv01 2021年11月版本 -->

STABILITY_CORE_POPULATION_HELPER_WITH_NETHERLAND = 5
#    <!--  大于0的数字表示荷兰计算稳定度的时候额外的核心人口，防止荷兰丢失阿姆斯特丹后崩溃，0为默认模式  mediv01 2021年8月版本 -->

STABILITY_CORE_POPULATION_MULTIPLIER = 0
#     <!-- 玩家控制的文明的核心人口扩张倍数，0为默认模式  mediv01 -->

STABILITY_PY_AI_STABILITY_BONUS = 2
#     <!-- AI负面稳定度修正系数，最终AI的稳定度=稳定度/2，减小AI负面稳定度的惩罚  2为默认模式 mediv01 -->

STABILITY_PY_BONUS_FOR_SOCIALIST_COUNTRY = 0
#     <!-- 1为社会主义国家的稳定度选项  0为默认模式 mediv01 -->

STABILITY_PY_HANDICAP_BONUS = 0
#   <!-- 1为不同难度下稳定度的红利  0为默认模式 mediv01 -->

STABILITY_PY_DIPO_STABILITY_MODIFIER = 0
#    <!-- 外交稳定度修正系数，真实外交稳定度=外交稳定度/修正系数  1为默认模式 mediv01 -->

STABILITY_PY_NOT_CHECK_STABILITY_FOR_AI = 0
#     <!-- 1为不检查稳定度，稳定度恒为0，相当于取消了稳定度机制  0为默认模式 mediv01 -->

STABILITY_PY_NOT_CHECK_STABILITY_FOR_HUMAN = 0
#      <!-- 1为不检查稳定度，稳定度恒为0，相当于取消了稳定度机制  0为默认模式 mediv01 -->

STABILITY_PY_FOR_CHECK_STABILITY_FOR_HUMAN = 0
#   <!-- 1为每5回合强制检测人类玩家的稳定度   0为默认模式 mediv01 -->

STABILITY_PY_FOR_CHECK_STABILITY_FOR_AI = 0
# <!-- 强制每5回合检查AI的稳定度，0为默认模式  mediv01 -->

STABILITY_PY_HUMAN_BONUS = 0
#   <!-- 大于0的数字为人类玩家固定增加的稳定度，如果数字为10，人类玩家的稳定度就是从10开始计算  0为默认模式 mediv01 -->

STABILITY_MAX_FOREIGN_STABILITY = 12
#  最大的外交稳定度加成




STABILITY_PY_VASSALS_CAN_IMPROVE_STABILITY_FROM_MASTER = 1
#     <!-- 大于0的数字表明AI附庸于其他国家时，可以获得宗主国稳定度红利。如果宗主国不稳定，则附庸也受到影响。增强了附庸和宗主之间的联动关系  0为默认模式 mediv01 -->

STABILITY_AUTOPLAY_MAINTANCE_STABILITY = 1
#     <!-- 大于0的数字在看海模式的过程中，增加原有国家的稳定度  0为默认模式 mediv01 -->


STABILITY_SHOW_CIVICS_STABILITY_IN_CIVIC_SCREEN = 1
#     <!-- 大于0的数字在选择政策界面，实时计算政策组合稳定度 0为默认模式 mediv01 -->



#     <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON4  ANYFUN选项  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->

AIWAR_PY_CAN_USE_SUPER_AI_WAR = 1
#  <!-- 1为可以使用新增的一战二战AIWAR  0为默认模式 mediv01 -->

AIWAR_PY_HUMAN_CAN_USE_AI_WAR = 0
#    <!-- 1为人类可以使用AIWAR  0为默认模式 mediv01 -->

AIWAR_PY_CANNOT_DO_AIWAR_TO_HUMAN = 0
#  <!-- 1为不可以对人类进行AIWAR刷兵  0为默认模式 mediv01 -->

AIWAR_PY_DEAD_CIV_CANNOT_USE_AI_WAR = 1
#   <!-- 1为死亡文明不能AIWAR刷兵  0为默认模式 mediv01 -->

AIWAR_PY_CAN_USE_AI_WAR_TO_DEAD_CIV = 0
#  <!-- 1为可以对死亡文明刷兵  1为默认模式 mediv01 -->

AIWAR_NO_MONGO_MEET_WAR = 0
#  <!-- 1为取消蒙古见面刷兵的AIWAR  0为默认模式 mediv01 -->

AIWAR_NO_MONGO_MEET_WAR_TO_HUMAN = 0
#  <!-- 1为取消蒙古给人类的见面刷兵的AIWAR  0为默认模式 mediv01 -->

PYTHON_NOAIWAR_WHEN_VASSAL = 1
#   <!--  1为当AIWAR的发起国和目标国存在任意附庸关系时，不能发动AIWAR，0为默认模式  mediv01 2021年8月版本 -->

PYTHON_NOAIWAR_WHEN_VASSAL_MASTER = 1
#   <!--  1为当AIWAR的发起国附庸其他人时，不能发动AIWAR，0为默认模式  mediv01 2021年8月版本 -->

PYTHON_NOAIWAR_WHEN_VASSAL_TO_OTHER = 0
#  <!--  1为当AIWAR的对象附庸其他人时，不能发动AIWAR，0为默认模式  mediv01 2021年8月版本 -->

PYTHON_DISABLE_RAILWAY_WAR_TO_HUMAN = 0
# <!--  1为禁用对人类玩家的铁路战争，0为默认模式  mediv01 2021年8月版本 -->

PLAGUE_DONNOT_INFECT_HUMAN = 0
#   <!-- 1为瘟疫不会感染人类的城市 0为默认模式 mediv01 -->

STABILITY_RESURRECTION_NOT_FLIP_HUMAN_CITY = 0
#    <!-- 1为复活时不翻转人类控制的城市 0为默认模式 mediv01 -->


AIWAR_PY_HUMAN_CAN_USE_RISE_AND_FALL = 0
#  <!-- 1为人类可以使用AI殖民加成  0为默认模式 mediv01 -->


PYTHON_CHECK_RESPAWN_TURN = 0
#   <!-- 大于0的数字为检查复活的回合间隔 10为默认模式，此选项为了减少卡顿 mediv01 -->

PYTHON_DISABLE_AIWAR_TO_INCA_WHEN_HUMAN_PLAY = 0
#   <!-- 1为当人类玩家玩印加和阿兹特克时，关闭对新大陆刷兵的AIWAR 0为默认模式 mediv01 -->


PYTHON_DIPO_NO_DECAY = 0
#  <!-- 1为Communication.py里不自动切断外交关系 0为默认模式，  mediv01  -->

PYTHON_RISEANDFALL_NO_TRADE_COMPANY_WAR = 0
#    <!-- 1为AI贸易公司不会要求玩家城市 0为默认模式 mediv01 -->

PYTHON_ARMY_NOT_FLIP_HUMAN = 0
#   <!-- 1为人类玩家待在AI翻转区内的军队不会叛变 0为默认模式 mediv01 -->

PYTHON_ARMY_NOT_FLIP_AI = 0
#  <!-- 1为AI玩家待在任意翻转区内的军队不会叛变 0为默认模式 mediv01 -->

PYTHON_CITY_NOT_FLIP = 0
#     <!-- 1为人类玩家在AI翻转区内的城市不会叛变 0为默认模式 mediv01 -->

PYTHON_CONGRESS_CANNOT_ASK_HUMAN_CITY = 0
#   <!-- 	 国际会议不能要求人类的城市 0为默认模式 mediv01 -->


PYTHON_CONGRESS_VOTE_FOR_EMPTY_TERROR_WITH_RANDOM = 1
#    <!--  1为当投票发现未知领土时，不再是ALWAYS YES，按照概率计算，0为默认模式  mediv01 2021年8月版本 -->



PYTHON_DYNAMIC_GREAT_WALL_TURN = 20
#    <!--  1为长城边界每多少回合重新计算一次，0为默认模式  mediv01 2021年8月版本 -->


PYTHON_LIBERATE_PLAYER_VALSSAL_TO_HUMAN = 1
#    <!-- 1为人类主动释放的玩家对人类附庸 0为默认模式 mediv01 -->


PYTHON_ALLOW_DYNAMIC_CORE = 1
#    <!-- 1为允许使用动态核心 0为默认模式 mediv01 -->

PYTHON_ALLOW_DYNAMIC_HISTORY = 0
#    <!-- 1为允许使用动态历史区  0为默认模式 mediv01 -->

PYTHON_ESPION_RESET_DEFAULT_WEIGHT = 0
#    <!-- 大于0的数字为谍报重置后的默认权重  0为默认模式 mediv01 -->

PYTHON_ALLOW_TO_USE_HISTORY_EVENT = 1
#    <!-- 大于0的数字为允许使用历史事件系统  0为默认模式 mediv01 -->


PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD = 1
#      <!-- 1为可以提示勒索信息，0为禁用 0为默认模式  mediv01 -->  此项需要与C++保持一致


PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD_MAP = 0
#   <!-- 1为可以提示交易地图的信息，0为禁用 0为默认模式  mediv01 -->  此项需要与C++保持一致

PYTHON_STABILITY_DISABLE_CONTINOUS_COLLAPSE = 0
#    1为启用连续性崩溃到核心的特性


PYTHON_USE_cultureManager_IN_DLL = 0
#  1为使用DLL里的cultureManager方法，提升效率  似乎会闪退

PYTHON_USE_flipCity_IN_DLL = 0
#  1为使用DLL里的flipCity方法，提升效率 似乎会闪退

PYTHON_SCOREBOARD_DISPLAY_Y_ADD = 20
#  积分版显示位置向下偏移，能显示更多的国家

PYTHON_STABILITY_MAX_COUNTRY_ALIVE = 32
#    最大可存活的国家数，超过这个数目，就会按照重要性排序，完全崩溃掉稳定度最低的AI国家 小于0时不启用


#     <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON  SCREEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->


PYTHON_SCREEN_ACHIEVEMENT_INFO_TIPS = 1
# <!-- 1为显示成就提示系统 0为默认模式 mediv01 -->


#     <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  PYTHON  SCREENTIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->


PYTHON_SCREEN_VICTORY_TIPS = 1
# <!-- 1为显示高级信息提示系统 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_00 = 1
#   <!-- 1为显示游戏基本信息 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_01 = 1
#    <!-- 1为显示国际会议回合进度 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_GREATPEOPLE = 1
#    <!-- 1为显示伟人计算器   0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_02 = 1
#      <!-- 1为显示殖民地进度 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_03 = 1
#    <!-- 1为显示瘟疫进度 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_04 = 10
#  <!-- 大于0的数字为显示世界科技最先进的N个文明 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_05  = 10
# <!-- 大于0的数字为显示世界军力最强大的N个文明 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_06 = 10
#      <!-- 大于0的数字为显示世界最大N座城市的排名 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_07 = 10
#   <!-- 大于0的数字为显示世界文化昌盛N座城市的排名 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_08 = 10
#   <!-- 大于0的数字为显示世界工业产出最高N座城市的排名 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_09 = 10
#    <!-- 大于0的数字为显示世界商业产出最高N座城市的排名 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_10 = 10
#      <!-- 大于0的数字为显示世界粮食产出最高N座城市的排名 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_11 = 10
#    <!-- 大于0的数字为提示部落村庄的位置 0为默认模式 mediv01 -->

PYTHON_SCREEN_VICTORY_TIPS_12 = 1
#  <!-- 大于0的数字为提示每个国家稳定度、战争的免疫信息 0为默认模式 mediv01 -->


PYTHON_SCREEN_VICTORY_TIPS_13 = 10
#  <!-- 大于0的数字为显示世界最繁荣的N座城市的排名 0为默认模式 mediv01 -->


PYTHON_SCREEN_VICTORY_TIPS_SHOW_AITRADE_ON_MONEY = 1
# <!-- 大于0的数字为提示可勒索金币数量 0为默认模式 mediv01 2021年11月新增内容 -->

PYTHON_SCREEN_VICTORY_TIPS_SHOW_AITRADE_ON_TECH = 1
# <!-- 大于0的数字为提示可勒索金币数量 0为默认模式 2021年11月新增内容  mediv01 -->

PYTHON_SHOW_CIV_MONEY_ON_PANNEL = 1
#  <!--  大于0的数字为在界面显示国家可用金币，0为默认模式  mediv01 2021年8月版本 -->


PYTHON_SHOW_CIV_STABILITY_ON_PANNEL = 1
#     <!--  大于0的数字为在界面显示国家稳定度，0为默认模式 该参数没有成功  mediv01 2021年8月版本 -->

PYTHON_SHOW_CIV_ASKMONEY_ON_PANNEL = 1
#   <!--  大于0的数字为在界面显示可勒索金币，0为默认模式 该参数没有成功  mediv01 2021年8月版本 -->

PYTHON_READ_CITYNAME_FROM_CSV = 1
#  <!-- 1为从CSV读取城市名称  0为默认模式 mediv01 -->

PYTHON_USE_CHINESE_CITYNAME = 0
#  <!-- 1为使用中文城市名 0为默认模式 mediv01 -->

PYTHON_READ_REGIONMAP_FROM_CSV = 1
#  <!-- 1为从CSV读取REGIONMAP  0为默认模式 mediv01 -->

#     <!--  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  LOG !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! -->
PYTHON_USE_LOG = 1 and PYTHON_DEBUG_MODE
# <!-- 1为打开日志功能 此选项为日志功能的总开关   0为默认模式 mediv01 -->

PYTHON_LOG_ON_MAIN_AIWAR = 1
#   <!-- 1为记录AIWAR的日志 0为默认模式 mediv01 -->

PYTHON_OUTPUT_DEBUG_TEXT_TO_LOG = 0
#   <!-- 1为将DEBUG的信息输出为LOG文件 0为默认模式 mediv01 -->

PYTHON_LOG_ON_AIACTION = 0
#<!-- 1为记录AI行为的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_CONGRESS = 1
#  <!-- 1为记录国际会议的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_STABILITY = 1
#   <!-- 1为记录稳定度详情的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_MAIN_BARBS = 1
#  <!-- 1为记录野蛮人入侵的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_MAIN_MINOR = 1
#    <!-- 1为记录独立城邦的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_MAIN_RISE_AND_FALL = 1
#  <!-- 1为记录国家兴起与崩溃的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_MAIN_PLAGUE = 1
#   <!-- 1为记录瘟疫的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_WONDER = 1
#    <!-- 1为记录奇观建成的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_BUILDING = 1
#   <!-- 1为记录普通建筑的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_GREATPEOPLE = 1
#  <!-- 1为记录伟人的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_UNIT = 1
#    <!-- 1为记录普通单位的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_TECH = 1
#  <!-- 1为记录科技获取的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_CITY_BUILD = 1
#  <!-- 1为记录城市建立的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_CITY_CONQUEST = 1
#  <!-- 1为记录城市被攻占的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_RELIGION = 1
# <!-- 1为记录城市宗教传播的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_TECHSCORE = 1
#  <!-- 1为记录科技得分的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_POWERSCORE = 1
# <!-- 1为记录军事实力传播的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_MODIFIER_CHANGE = 1
#   <!-- 1为记录文明科研参数变动的的日志 0为默认模式 mediv01 -->

PYTHON_LOG_MANUAL_DEBUG_SCORE = 0
# <!-- 1为在打开信息界面时自动输出每回合科技、军事排名信息，仅为调试时使用 0为默认模式 mediv01 -->

PYTHON_LOG_ON_RANDOMEVENT = 1
#   <!-- 1为记录日常随机事件 0为默认模式 mediv01 -->

PYTHON_LOG_ON_CONGRESS_PROB = 0
#  <!-- 1为记录国际会议概率计算的日志 0为默认模式 mediv01 -->

PYTHON_LOG_ON_WUNSHARE_DEBUG = 0 and PYTHON_DEBUG_MODE
#  <!-- 1为开启WunShare的DEBUG日志  0为默认模式 mediv01 -->

PYTHON_LOG_ON_CHECKTURN_TIME = 1 and PYTHON_DEBUG_MODE
#  <!-- 1为开启过回合耗时的DEBUG日志  0为默认模式 mediv01 -->

PYTHON_LOG_ON_CHECKTURN_TIME_DETAIL = 0 and PYTHON_DEBUG_MODE
#  <!-- 1为开启过回合耗时的DEBUG详细日志  0为默认模式 mediv01 -->

PYTHON_LOG_ENABLE_DEBUG_CHECKTURN = 1 and PYTHON_DEBUG_MODE
#    开启定期debug checkturn模式

PYTHON_LOG_ON_RELEASE_ERROR = 1
#    开启RELEASE版记录日志错误的模式

CVGAMECORE_LOG_PATH = "Mods\\RFC Dawn of Civilization\\Logs\\"

CVGAMECORE_PYTHON_CSV_PATH = "Mods\\RFC Dawn of Civilization\\Assets\\Python\\CSVData\\"

CVGAMECORE_PYTHON_CSV_PATH_CITYNAME = "Mods\\RFC Dawn of Civilization\\Assets\\Python\\CSVData\\CityNameData\\"

CVGAMECORE_PYTHON_CSV_PATH_REGIONMAP = "Mods\\RFC Dawn of Civilization\\Assets\\Python\\CSVData\\RegionMapData\\"

CVGAMECORE_PYTHON_USERDATA_PATH= "Mods\\RFC Dawn of Civilization\\UserData\\"

PYTHON_FIX_UHV_TEXTBUG_IN_CHINESE = 1
#  <!--  1为修复在中文模式下UHV文本的BUG，0为默认模式  mediv01 2021年11月版本 -->

PYTHON_FIX_URV_TEXTBUG_IN_CHINESE = 1
#  <!--  1为修复在中文模式下URV文本的BUG，0为默认模式  mediv01 2021年11月版本 -->
