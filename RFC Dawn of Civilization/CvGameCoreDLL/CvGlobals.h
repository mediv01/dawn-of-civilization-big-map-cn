#pragma once

// CvGlobals.h

// CvGlobals.h

// ������ʹ�ú�ķ�ʽ����Ϊ�޷�ʵ�ֳ��������Ż�
/*
#ifndef FP_PROFILE_ENABLE 
static const int DEBUG_MODE = 1;
//    ����Ϊ0ʱ���ر���Ϸ���е�һЩͳ��ѡ���־��������ݣ����ٿ���
#else
static const int DEBUG_MODE = 0;
#endif
*/

static const int DEBUG_MODE = 0;
//    ����Ϊ0ʱ���ر���Ϸ���е�һЩͳ��ѡ���־��������ݣ����ٿ���

static const int RELEASE_MODE = 0;
//    ����Ϊ1ʱ���ر�Python����������

static const int ANYFUN_MODE = 0;
//    ����Ϊ1ʱ������ANYFUN����ģʽ1�Ĳ���ѡ��

static const CvWString DOCM_BIGMAP_VERSION = L"��Ϸ�汾��V10.5.5 2209 �����";




/*
����ѡ����ͣ�
/D_MOD_SENTRY           BUGģ��� - Sentry Actions��Ĭ�Ͽ�ʼ
/D_MOD_FRACTRADE        ��ֵ��ȷ����ģ�飬��·�����е�֧��2λС����Ĭ�Ͽ���
/D_MOD_GOVWORKERS       BUG - Governor Builds Workboats��Ĭ�Ͽ���
/DQC_MASTERY_VICTORY    �Ѿ��Ҳ���
/DLOG_AI                �Ѿ��Ҳ���
/DFP_PROFILE_ENABLE     �������������������DLL���룬Ŀǰ�ǿ���״̬
/D_MOD_GWARM            BUG - ȫ���ůģ��
/D_MOD_SHAM_SPOILER     Show Hidden Attitude Mod
/DC2C_BUILD             �Ѿ��Ҳ���
/DUSE_INTERNAL_PROFILER �Ѿ��Ҳ���
/DSCALE_CITY_LIMITS     �Ѿ��Ҳ���
*/



// GlobalDefinesALT��ȽϺ�ʱ�Ĳ�����Ԥ�Ƶ�DLL��

static const int ANYFUN_ENABLES_FREE_OUTSIDE_UNIT = 1 && ANYFUN_MODE;
//    <!-- Ϊ1ʱ���ⵥλû��ά����  0ΪĬ��ģʽ  mediv01  -->

static const int ANYFUN_DISABLE_COMBAT_LIMIT = 0;
//     <!-- Ϊ1ʱȡ����λ�˺����ޣ�����Ͷʯ���ȹ�������������75%���˺�����  0ΪĬ��ģʽ  mediv01  -->

static const int ANYFUN_MAX_UNIT = -1;
//     <!-- ����0�����֣�Ϊÿ��������ĵ�λ�� -1ΪĬ��ģʽ  mediv01  -->

static const int ANYFUN_MAX_CITY = -1;
//   <!-- ����0�����֣�Ϊÿ��������ĳ�����  -1ΪĬ��ģʽ  mediv01  -->

static const int CVCITY_MAX_SHRINE_LIMIT = 0;
//     <!-- ����0������Ϊʥ���ܹ�������������� 0����20ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->

static const int CVCITY_RANK_BONUS_TYPE = 2;
//     <!-- ��Դ����ʲô˳�����ȷ��� 1Ϊ�����˿�������0Ϊ��������4DOCԭ��Ĭ�ϵ��Ļ����� 2Ϊ����wunshare������ 0ΪĬ��ģʽ mediv01 -->

static const int CVUNIT_AI_NOT_TAKE_GOODY = 1 && ANYFUN_MODE;
//   <!-- 1ΪAI���������ɼ������ׯ 0ΪĬ��ģʽ mediv01 -->

static const int CVUNITAI_AI_CAN_NOT_TAKE_GOODY = 1 && ANYFUN_MODE;
//    <!-- 1ΪAI���Զ���Ģ����ѡ�� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVUNIT_CAN_ALWAYS_ENTER_TERRITORY = 0;
//   <!-- 1Ϊ���Ե�λ�����߿����������������� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVUNIT_SHIP_CAN_ALWAYS_ENTER_TERRITORY = 1;
//   <!-- 1Ϊ��ֻ�����߿����������������� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_FORT_CAN_CULTURE = 1;
//   <!-- Ϊ1ʱҪ��פ�����Բ����Ļ�  0ΪĬ��ģʽ  mediv01  -->

static const int CVUNIT_MAX_UNIT_PER_PLOT = -1;
//   <!--ÿ���ؿ���൥λ���� - 1ΪĬ��ģʽ mediv01-->

static const int CVUNIT_MOVE_MULTIPILIER = 1;
//       <!-- ����0������Ϊ�ƶ������� 0����1ΪĬ��ģʽ��  mediv01  -->

static const int CVUNIT_OLD_GREAT_WALL_EFFECT = 0;
//  <!-- 1Ϊ֮ǰ������Ч�Ĵ��룬Ұ���˲��ܽ��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVCITY_NOT_HURRY_ANGRY_PUNISHMENT = 0;
//    <!-- 1Ϊû���������˳����ĺ����ͷ� 0ΪĬ��ģʽ�� mediv01  -->

static const int PLOT_CITY_FULL_YIELD_WHEN_SETTLE = 1;
//  <!-- 1Ϊ��Դ���������� 0ΪĬ��ģʽ mediv01 -->

static const int CVPLAYER_NO_EXTRA_COST_FOR_HURRY = 1 && ANYFUN_MODE;
//   <!-- ����0������Ϊ��Ҽ��پ��µ�λ����ʱû�ж������  0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->

static const int CVGAMETEXT_SHOW_BONUS_TRADE_VALUE = 1;
//    <!-- ��ʾ����Դ���׼�ֵ����С��ֵ 0ΪĬ��ģʽ  mediv01 -->

static const int CVPLAYER_AI_CANNOT_BUILD_CITY_IN_NOT_HISTORY = 0;
//   <!-- ����0������ΪAI��Ҳ�������ʷ���⽨������ 0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->


static const int CVPLAYER_HUMAN_CANNOT_BUILD_CITY_IN_NOT_HISTORY = 0;
//  <!-- ����0������Ϊ������Ҳ�������ʷ���⽨������ 0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->


static const int CVGAMETEXT_SHOW_HURRYINFO_IN_CITY_BAR_TOHUMAN = 1;
//      <!-- 1Ϊ�ڳ��н�����H0��ʾ�ܷ���٣��Լ����ٵĺ��� ����������� 0ΪĬ��ģʽ mediv01 2021��11���������� -->

static const int CVGAMETEXT_SHOW_HURRYINFO_IN_CITY_BAR_TOAI = 1;
//   <!-- 1Ϊ�ڳ��н�����H0��ʾ�ܷ���٣��Լ����ٵĺ��� ����AI����  0ΪĬ��ģʽ 2021��11���������� mediv01 -->

static const int CVPLOT_BUILD_FORT_NEAR_CITY_OR_FORT = 1 && ANYFUN_MODE;
//     <!-- 1ΪҪ�����������ޣ�0ΪĬ��ģʽ mediv01  -->

static const int DIPLO_ALLOW_TO_CANCEL_VASSAL = 1;
// <!--��������ȡ����ӹ  0ΪĬ��ģʽ mediv01-->


static const int CVDEAL_ALLOW_TO_CANCEL_DEAL_ANYTIME = 0;
//   <!-- 1Ϊ10�غ�������ȡ������ 0ΪĬ��ģʽ�� mediv01  -->


static const int CVDEAL_NOT_ALLOW_TO_CANCEL_DEAL_ANYTIME = 0;
//   <!-- 1Ϊ������ȡ���κν��ף�����ս�� 0ΪĬ��ģʽ�� mediv01  -->

static const int CVPLOT_BUILD_IMPROVEMENT_OUTSIDE_BORDER = 0;
//  <!-- 1Ϊ�����ڱ߽�������������ʩ��0ΪĬ��ģʽ mediv01  -->


static const int CVPLAYER_AI_CAN_SETTLE_ON_FOOD = 1;
//   <!-- 1ΪAI������ʳ����Դ�Ͻ��� 0ΪĬ��ģʽ��  mediv01  -->




static const int CVINFOS_REAEARCH_COST_MULTIPLIER = 100;
//   <!-- AI��������з��õĳ����ٷֱ� ���Ե��ڿ��з��ñ��� 0����100ΪĬ��ģʽ ��У׼ mediv01  -->

static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC = 1;
//     <!-- 1Ϊ�����Ѷȶ�̬ƽ�������ҵĿƼ����ȣ�ȷ�������Ѷ���AI��ͬһʱ�ڵĿƼ��������������1860������Ѷȵ�AI�����ڵڶ��ι�ҵ�����ĿƼ�ˮƽ�����������AI���н���̫�������� 0ΪĬ��ģʽ  mediv01  -->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_NOT_INCLUDE_HUMAN = 1;
//     <!-- 1Ϊ����Ŀ��ж�̬ƽ�ⲻ����������ң�����������ҵ����飬���鿪�� 0ΪĬ��ģʽ  mediv01  -->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_H1 = 80;
//     <!-- 1���Ѷ���AI���з��õĳ����ٷֱ� 100ΪĬ��ģʽ ��У׼ mediv01  -->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_H2 = 90;
//   <!-- 2���Ѷ���AI���з��õĳ����ٷֱ� 100ΪĬ��ģʽ ��У׼ mediv01-->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_H3 = 100;
//   <!-- 3���Ѷ���AI���з��õĳ����ٷֱ� 100ΪĬ��ģʽ ��У׼ mediv01  -->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_H4 = 110;
// <!-- 4���Ѷ���AI���з��õĳ����ٷֱ� 100ΪĬ��ģʽ  ��У׼ mediv01  -->


static const int CVINFOS_REAEARCH_COST_MULTIPLIER_DYNAMIC_H5 = 120;
//  <!-- 5���Ѷ���AI���з��õĳ����ٷֱ� 100ΪĬ��ģʽ ��У׼ mediv01  -->





static const int CVTEAM_TECH_COST_BY_ERA = 1;
//  <!-- ����0������Ϊ��ҿƼ����ø���ҵ�ǰʱ���ҹ��������ǰ�о�̫�࣬�ͻ����ܳͷ� 0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->


static const int CVTEAM_TECH_COST_BY_ERA_TO_HUMAN = 1 && !ANYFUN_MODE;
//      <!-- ����0������Ϊ������ҿƼ����ø���ҵ�ǰʱ���ҹ��������ǰ�о�̫�࣬�ͻ����ܳͷ� 0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->

static const int CVTEAM_TECH_COST_BY_ERA_TO_AI = 1;
//      <!-- ����0������ΪAI��ҿƼ����ø���ҵ�ǰʱ���ҹ��������ǰ�о�̫�࣬�ͻ����ܳͷ� 0ΪĬ��ģʽ�� mediv01  2021��8�°汾�������� -->


static const int CVCITY_CAN_ALWAYS_HURRY_WITH_CIVICS_AI = 0;
//   <!-- AI��ҿ��Բ������ߵ����Ƽ��ٵ�λ�ͽ���   0ΪĬ��ģʽ  2021��11�°汾��������  mediv01 -->


static const int CVCITY_CAN_ALWAYS_HURRY_WITH_CIVICS_HUMAN = 0;
//     <!-- ������ҿ��Բ������ߵ����Ƽ��ٵ�λ�ͽ���   0ΪĬ��ģʽ 2021��11�°汾��������  mediv01 -->


static const int CVCITY_AI_CANNOT_BUILD_WONDER = 1 && ANYFUN_MODE;
//  <!-- 1Ϊ AI���ܽ�����ۣ���ۿصĸ���  0ΪĬ��ģʽ    mediv01  2021��8�°汾�������� -->


static const int CVCITY_MAX_HURRY_POPULATION = -ANYFUN_MODE;
//      <!-- -1Ϊ���������ļ����˿����ƣ�0ΪĬ��ģʽ��������ֵΪ�̶����� mediv01  -->


static const int MAX_BUILDINGS_PER_CITY = -1;
//   <!--ÿ��������ཨ������ - 1ΪĬ��ģʽ mediv01-->


static const int CVCITY_CAN_ALWAYS_HURRY = 0;
// <!--���Բ������ߵ����Ƽ��ٵ�λ�ͽ�����0ΪĬ��ģʽ  mediv01-->


static const int CVCITY_CAN_HURRY_NONARMY = 1 && ANYFUN_MODE;
//    <!-- ���Իƽ���ٷǾ��µ�λ��0ΪĬ��ģʽ  mediv01 -->


static const int CVGAME_MINOR_CITY_LOW_SCORE_ON_SCREEN = 5;
//  <!-- ����0������Ϊ���ְ��϶����ǰ�Ļ��ֱ���������ı���  0ΪĬ��ģʽ�� mediv01  2021��11�°汾�������� -->


static const int CVTEAMAI_AI_CANNOT_VASSAL_TO_OTHER_WHEN_AT_WAR = 1 && ANYFUN_MODE;
//    <!-- 1ΪAI�ں��������ʱ��������Ͷ������������  0ΪĬ��ģʽ mediv01 -->


static const int CVUNIT_ANIMAL_CAN_ENTER_COUNTRY = 0;
//       <!-- 1Ϊ��������������������� 0ΪĬ��ģʽ��  mediv01  -->


static const int CVCITY_BUILDING_NO_OBSOLETE = 1 && ANYFUN_MODE;
//       <!-- 1Ϊ���н����ﲻ�ٹ��� 0ΪĬ��ģʽ��  mediv01  -->


static const int MAX_WORLD_NATIONAL_WONDERS_PER_CITY_MEDIV01 = -ANYFUN_MODE;
//       <!-- ���еĹ�������������ƣ�-1Ϊ�����ƣ�0ΪDOCĬ�ϻ��ƣ�1-8Ϊ�̶��������� mediv01 -->

static const int MAX_WORLD_WONDERS_PER_CITY_MEDIV01 = -ANYFUN_MODE;
//       <!-- ���е�����������ƣ�-1Ϊ�����ƣ�0ΪDOCĬ�ϻ��ƣ�1-8Ϊ�̶��������� mediv01 -->

static const int CVCITY_CANNOT_BUILD_FIRESTATION_WHEN_HAVE_CLEAN_ENERGY = 0;
//  <!-- 1Ϊ �����������󣬲��ܼ���������վ  0ΪĬ��ģʽ  ���ڻ�糧���˵糧Ĭ������10%���ӣ���������ȡ����    mediv01  2021��8�°汾�������� -->

// static const int CVCITY_RELEASE_PLAYER_NO_LIMIT = 1;
//  <!-- 1Ϊ �ͷŸ�ӹ��ʱ�򣬿����ͷŲ��ܸ���Ĺ��ڹ��ң�0ΪĬ��ģʽ   ��ѡ����ʱ��ֲ��XML������ mediv01  2021��8�°汾�������� -->


static const int CVPLAYER_CAN_ALWAYS_TRADE_TECH = 1 && ANYFUN_MODE;
//  <!-- 1Ϊ ��Զ���Խ��׿Ƽ�   mediv01  2021��8�°汾�������� -->


static const int CVGAME_ALWAYS_SHOW_GOODY_IN_MAP = 1 ;
//  <!-- 1Ϊ �����ڵ�ͼ������ʾ�����ׯ   mediv01  2021��8�°汾�������� -->


static const int CVCITY_PROB_REBELT_MULTIPLIER_WHEN_CULTURE_IN_LOW = -ANYFUN_MODE;
//   <!-- -1 Ϊȡ���Ļ��ͳ������һ��� ����0������Ϊ�����ڵ��Ļ�ʱ���Ҹ��ʵı��� 0ΪĬ��ģʽ mediv01 -->

static const int CVPLAYERAI_CAN_TRADE_GOLD_UNLIMITED = 1 && ANYFUN_MODE;
//    <!-- 1ΪAI���׽�������ƣ����Խ��׹��������еĽ�� 0ΪĬ��ģʽ mediv01 -->


static const int PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD = 1;
//    <!-- 1Ϊ������ʾ������Ϣ��0Ϊ���� 0ΪĬ��ģʽ  mediv01 -->  ������Ҫ��C++����һ��

static const int PLAYER_AI_ALLOW_TO_USE_CONSIDEROFFER_THRESHOLD_MAP = 0;
//     <!-- 1Ϊ������ʾ���׵�ͼ����Ϣ��0Ϊ���� 0ΪĬ��ģʽ  mediv01 -->

/*
��Ϸ������־������������־
*/

static const int CVGAMECORE_DLL_LOG = 1 && DEBUG_MODE;
//       <!-- 1Ϊ���DLL��־��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_RECORED_GLOBAL_DEFINES_ALT_CALL = 1 && DEBUG_MODE;
//       <!-- 1Ϊ����ÿ�غ�globaldefinesalt.xml�ĵ��ô��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_RECORED_DLL_CALL_PYTHON_FUNCTION_CALL = 1 && DEBUG_MODE;
//       <!-- 1Ϊ����ÿ�غ�DLL����Python�����ĵ��ô��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_RECORED_FUNCTION_CALL = 1 && DEBUG_MODE;
//       <!-- 1Ϊ����ÿ�غϵ��ú����Ĵ��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_COUNT_ON_TIME_COST = 1 && DEBUG_MODE;
//       <!-- 1Ϊ����ÿ�غϼ���ĺ�ʱ��� 0ΪĬ��ģʽ��  mediv01  -->

static const int CVGAME_COUNT_ON_TIME_COST_LOG = 1 && DEBUG_MODE;
//       <!-- 1Ϊ����ÿ�غϼ���ĺ�ʱ��������־ 0ΪĬ��ģʽ��  mediv01  -->


static const int CVGAME_DO_UNITTEST_ON_DEBUG = 1 && DEBUG_MODE;
//       <!-- 1Ϊ������ʾ��Ϣ��ʱ�򣬽��е�Ԫ���� 0ΪĬ��ģʽ��  mediv01  -->













static const CvString CVGAMECORE_LOG_PATH = "Mods\\RFC Dawn of Civilization\\Logs\\";
//    <!--��־��ŵ��ļ��� mediv01-->

static const int CVGLOBAL_ENABLE_DLL_LOG= 1 && DEBUG_MODE;
//       <!-- 1Ϊ����DLL��¼��־ DLL��־��¼���ܿ��� 0ΪĬ��ģʽ��  mediv01  -->




/*
�����Ż�ѡ��
*/

static const std::wstring CVGAMECORE_FIX_BUG_PERFORMANCE_UP_EMPTY_STR = L"";
// mediv01  ���ͼ���ַ���������������������  ����by wunshare

static const int DOC_COMPILER_PERFORMANCE_UP = 1;
// ���ٱ��������Ϸ��һЩ������Ϸѡ������ݣ����������ٶ�


static const int CVGLOBAL_DISABLE_USELESS_PYTHON_CALLBACK = 1;
//     <!-- 1Ϊ������Ч��PythonCallBack���������ٶȣ�0Ϊ���� 0ΪĬ��ģʽ  mediv01 -->

static const int DOC_CALCULATE_GAMESCORE_IN_DLL = 1;
// ��DLL�������Ϸ��������������PYTHON����㣬��Ȼÿ�غ�Ҫ���ü����PYTHON���ܺķ�����


static const int DOC_PERFORMANCE_CVPLOT_SETOWNER = 1;
//  �ص��Ż�������������


struct CVPLOT_DOTURN_INFO {
	int plotid;
};

static const int DOC_PERFORMANCE_USE_MULTITHREAD_IN_CVPLOT_DOTURN = 0;
//  ��CvPlot���غ�ʱ���ö��̼߳��㣬���Ч��   ��ѡ������˲����ã�����ر�

static const int DOC_PERFORMANCE_SKIP_SEA_PLOT_IN_CVPLOT_DOTURN = 1;
//  ����1700���ʱ�����������һ�����ʲ�����dotrun����

static const int DOC_PERFORMANCE_SKIP_UpdatePlotGroup_IN_CVPLOT_DOTURN = 1;
//  ����1700���ʱ�����������һ����������plotgroup�ĸ���

static const int DOC_PERFORMANCE_SKIP_updatePlotGroup_IN_CvPlotGroup_recalculatePlots = 1;
//  ����updatePlotGroup���ں�ʱ����recalculatePlots����ʱ������һ���裬��ǿ����



























static const int CVGAMECORE_NEW_AUTOSAVE_FEATURE = 1;
// �����µ�AutoSave���ƣ�����Ϸ�غϽ���ʱ������Ϸ����������Ϸ�غϿ�ʼʱ
//mediv01  ��ϷBUG�޸���������

//ȫ�ֱ�����
static CvWString log_CWstring;
static CvString log_CvString;

static CvWString2 log_CWstring2;
static CvString2 log_CvString2;



// ÿ�пƼ���Ӧ����ʵ���
static const int SIZE_OF_TECH_COL_YEAR = 22;
//static const int TechColYear[SIZE_OF_TECH_COL_YEAR] = { -4000 ,-4000,-4000,    -2000,-1500, -1000,    -500,0,500,   1000,1300,1500,   1600,1700,1800, 1850,1890,1920, 1940,1960,1970,1970 };



static const int TechColYear[SIZE_OF_TECH_COL_YEAR] = { -4000 ,-4000,-2000,    -1000,-500, 0,    500,850,1100,   1300,1450,1600,   1700,1800,1850, 1900,1920,1940, 1960,1970,1980,1990 };


// ÿ��ʱ����Ӧ����ʵ���
const int SIZE_OF_TECH_ERA_YEAR = 7;
static const int TechEraYear[SIZE_OF_TECH_ERA_YEAR] = { -4000 ,-2000,-500, 1000, 1600, 1850,1940 };























// GlobalDefines��ȽϺ�ʱ�Ĳ�����Ԥ�Ƶ�DLL��

static const int BASE_CITY_GROWTH_THRESHOLD = 20;
//   ���л�������

static const int CITY_GROWTH_MULTIPLIER = 2;
//  ���л�����������

static const int BASE_UNIT_UPGRADE_COST = 10;
// ��λ��������


static const int UNIT_UPGRADE_COST_PER_PRODUCTION = 2;

static const int CAPITAL_TRADE_MODIFIER = 25;

static const int CULTURE_PERCENT_ANGER = 400;


static const SpecialistTypes DEFAULT_SPECIALIST = SPECIALIST_CITIZEN;


static const int IGNORE_PLOT_GROUP_FOR_TRADE_ROUTES = 0;


static const int OUR_POPULATION_TRADE_MODIFIER = 5;

static const int OUR_POPULATION_TRADE_MODIFIER_OFFSET = -10;

static const int RELIGION_PERCENT_ANGER = 800;


static const int WATER_POTENTIAL_CITY_WORK_FOR_AREA = 0;

static const int VASSAL_HAPPINESS = 1;

static const int COMBAT_DAMAGE = 20;

static const int UPKEEP_POPULATION_OFFSET = -8;

static const int UPKEEP_CITY_OFFSET = -1;


static const int UNIT_PRODUCTION_PERCENT = 100;

static const int TRADE_PROFIT_PERCENT = 20;

static const int THEIR_POPULATION_TRADE_PERCENT = 50;

static const int TECH_COST_EXTRA_TEAM_MEMBER_MODIFIER = 50;

static const int PEACE_TREATY_LENGTH = 10;


static const int OWNERSHIP_SCORE_DURATION_THRESHOLD = 20;


static const int UNIT_VISIBILITY_RANGE = 1;

static const int NO_MILITARY_PERCENT_ANGER = 334;

static const int MAX_YIELD_STACK = 10;

static const int MAX_TRADE_ROUTES = 10;

static const int GREAT_PEOPLE_THRESHOLD = 100;

static const int HURRY_ANGER_DIVISOR = 10;

static const int AT_WAR_CULTURE_ANGER_MODIFIER = 50;


static const int AI_SHOULDNT_MANAGE_PLOT_ASSIGNMENT = 0;


static const int BASE_FEATURE_PRODUCTION_PERCENT = 67;


static const int FEATURE_PRODUCTION_PERCENT_MULTIPLIER = 0;


static const int BUILDING_PRODUCTION_PERCENT = 100;

static const int CITY_BARBARIAN_DEFENSE_MODIFIER = 25;

static const int CONSCRIPT_ANGER_DIVISOR = 10;

static const int CONSCRIPT_POP_ANGER = 3;


static const int MAX_WITHDRAWAL_PROBABILITY = 90;

static const int MAX_INTERCEPTION_PROBABILITY = 100;


static const int MAX_FORTIFY_TURNS = 5;


static const int OVERSEAS_TRADE_MODIFIER = 0;


static const int FOREIGN_TRADE_FULL_CREDIT_PEACE_TURNS = 50;

static const int DISTANCE_TRADE_MODIFIER = 1;

static const int FOREIGN_TRADE_MODIFIER = 150;

static const int INITIAL_FREE_OUTSIDE_UNITS = 4;
//  �������ĵ�λ����

static const int INITIAL_OUTSIDE_UNIT_GOLD_PERCENT = 50;


static const int MAX_EVASION_PROBABILITY = 90;


static const int HURRY_POP_ANGER = 1;


static const int FRESH_WATER_HEALTH_CHANGE = 2;


static const int CULTURE_COST_DISTANCE = 5;

static const int CULTURE_COST_RIVER = -5;

static const int CULTURE_COST_PEAK = 20;

static const int CULTURE_COST_HILL = 0;

static const int CULTURE_COST_BONUS = -10;

static const int LAND_UNITS_CAN_ATTACK_WATER_CITIES = 0;

static const int PLOT_VISIBILITY_RANGE = 1;


static const int ESPIONAGE_SPENDING_MULTIPLIER = 100;

static const int ESPIONAGE_DISTANCE_MULTIPLIER_MOD = 100;

static const int ESPIONAGE_CITY_POP_EACH_MOD = 0;

static const int ESPIONAGE_CULTURE_MULTIPLIER_MOD = 50;

static const int FREE_VASSAL_LAND_PERCENT = 50;

static const int NEW_HURRY_MODIFIER = 50;

static const int FREE_VASSAL_POPULATION_PERCENT = 50;

static const int CITY_SCREEN_FOG_ENABLED = 1;

static const int MAX_DISTANCE_CITY_MAINTENANCE = 20;
//  �����о���ά����


static const int DIPLOMACY_VALUE_REMAINDER = 10;

static const int RECON_VISIBILITY_RANGE = 5;

static const int FREE_CITY_ADJACENT_CULTURE = 1;

static const int BASE_RESEARCH_RATE = 1;

static const int TECH_COST_KNOWN_PREREQ_MODIFIER = 20;

static const int TECH_COST_TOTAL_KNOWN_TEAM_MODIFIER = 30;

static const int STANDARD_HANDICAP = 1;


static const int LAND_TERRAIN = 0;

static const int RELIGION_FOUNDING_SPREAD_TURNS = 20;

static const int CITY_DEFENSE_DAMAGE_HEAL_RATE = 5;


static const int POWER_HEALTH_CHANGE = 0;


static const int DIRTY_POWER_HEALTH_CHANGE = -2;

static const int ETHNIC_CITY_STYLES = 0;

static const int CITY_FREE_CULTURE_GROWTH_FACTOR = 20;

static const int COMMERCE_PERCENT_CHANGE_INCREMENTS = 10;


static const int TEMP_HAPPY = 1;

static const int WE_LOVE_THE_KING_POPULATION_MIN_POPULATION = 8;

static const int WE_LOVE_THE_KING_RAND = 1000;

static const int CONSCRIPT_POPULATION_PER_COST = 60;


static const int ESPIONAGE_CITY_RELIGION_STATE_MOD = -15;

static const int ESPIONAGE_CITY_HOLY_CITY_MOD = -25;

static const int ESPIONAGE_CITY_TRADE_ROUTE_MOD = -20;

static const int BASE_WAR_WEARINESS_MULTIPLIER = 2;

static const int PROJECT_PRODUCTION_PERCENT = 100;


static const int SHIP_BLOCKADE_RANGE = 2;

static const int CIRCUMNAVIGATE_FREE_MOVES = 1;

static const int BARBARIAN_FREE_TECH_PERCENT = 3;

static const int FREE_CITY_CULTURE = 2;

static const int INITIAL_CITY_POPULATION = 1;

static const int FIRST_EVENT_DELAY_TURNS = 20;

static const int EVENT_PROBABILITY_ROLL_SIDES = 100;

static const int WW_DECAY_RATE = -1;

static const int WW_DECAY_PEACE_PERCENT = 99;

static const int CITY_HEAL_RATE = 20;

static const int ENEMY_HEAL_RATE = 5;

static const int NEUTRAL_HEAL_RATE = 10;

static const int FRIENDLY_HEAL_RATE = 15;

static const int MAXED_UNIT_GOLD_PERCENT = 50;

static const int MAXED_BUILDING_GOLD_PERCENT = 50;

static const int MAX_EXPERIENCE_PER_COMBAT = 10;

static const int MIN_EXPERIENCE_PER_COMBAT = 1;

static const int BARBARIAN_MAX_XP_VALUE = 10;

static const int ANIMAL_MAX_XP_VALUE = 5;

static const int EXPERIENCE_FROM_WITHDRAWL = 5;

static const int CAPITAL_BUILDINGCLASS = 0;

static const int RUINS_IMPROVEMENT = 2;

static const int WAR_SUCCESS_ATTACKING = 4;

static const int WAR_SUCCESS_DEFENDING = 3;

static const int WW_KILLED_UNIT_ATTACKING = 2;

static const int WW_KILLED_UNIT_DEFENDING = 1;

static const int WW_UNIT_KILLED_ATTACKING = 3;

static const int WW_UNIT_KILLED_DEFENDING = 2;

static const int RELIGION_PRESENCE_INFLUENCE = 3;

static const int COMBAT_EXPERIENCE_IN_BORDERS_PERCENT = 100;

static const int EVENT_MESSAGE_TIME_LONG = 20;

static const int CITY_AIR_UNIT_CAPACITY = 4;

static const int COLLATERAL_COMBAT_DAMAGE = 10;


static const int MIN_CIV_STARTING_DISTANCE = 10;

static const int STARTING_DISTANCE_PERCENT = 12;


static const int CONSCRIPT_MIN_CITY_POPULATION = 5;

static const int CONSCRIPT_MIN_CULTURE_PERCENT = 50;

static const int REVOLT_TEST_PROB = 10;

static const int ESPIONAGE_INTERCEPT_SPENDING_MAX = 25;

static const int ESPIONAGE_INTERCEPT_COUNTERSPY = 15;

static const int ESPIONAGE_INTERCEPT_COUNTERESPIONAGE_MISSION = 20;

static const int ESPIONAGE_INTERCEPT_RECENT_MISSION = 15;

static const int CAPTURE_GOLD_MAX_TURNS = 50;

static const int CAPTURE_GOLD_PER_BUILDING_COST = 5;

static const int RAZING_CULTURAL_PERCENT_THRESHOLD = 25;

static const int FORCE_UNOWNED_CITY_TIMER = 2;

static const int WAR_SUCCESS_CITY_CAPTURING = 10;

static const int WW_CAPTURED_CITY = 6;

static const int BASE_CAPTURE_GOLD = 10;

static const int CAPTURE_GOLD_PER_POPULATION = 5;

static const int CAPTURE_GOLD_RAND1 = 50;

static const int CAPTURE_GOLD_RAND2 = 25;

static const int OCCUPATION_CULTURE_PERCENT_THRESHOLD = 75;

static const int NO_AUTOSAVE_DURING_AUTOPLAY = 0;

static const int GLOBAL_WARMING_FOREST = 50;

static const int GLOBAL_WARMING_NUKE_WEIGHT = 50;

static const int GLOBAL_WARMING_TERRAIN = 2;

static const int GLOBAL_WARMING_UNHEALTH_WEIGHT = 20;

static const int MIN_CITY_ATTACK_MODIFIER_FOR_SIEGE_TOWER = 10;

static const int MIN_REVOLUTION_TURNS = 5;

static const int GOLDEN_AGE_LENGTH = 8;

static const int BASE_GOLDEN_AGE_UNITS = 2;

static const int ESPIONAGE_SPY_INTERCEPT_MOD = -75;

static const int ESPIONAGE_SPY_NO_INTRUDE_INTERCEPT_MOD = -90;







static const int minStartingDistanceModifier = 0;  // PYTHON����������Ϊ0 ������������Ż�
























//mediv01  ��ϷBUG�޸�������ʼ�����ͼ������
/*
//��һ�׶��޸�ʹ�õĲ���
static const int CVGAMECORE_FIX_NULL_POINTER_BUG1 = 1; //mediv01 ��Ҫ��PLOT��ָ�����
static const int CVGAMECORE_FIX_NULL_POINTER_BUG2 = 1; //mediv01 ��Ҫ���ڴ�й¶����
static const int CVGAMECORE_FIX_NULL_POINTER_BUG3 = 1; //mediv01 IF�������ظ��жϵ�BUG
static const int CVGAMECORE_FIX_NULL_POINTER_BUG4 = 1; //mediv01 ��̫�а��յĿ�ָ��

//�ڶ��׶��޸�ʹ�õĲ���
static const int CVGAMECORE_FIX_NULL_POINTER_BUG5 = 1; //mediv01 ��Ҫ��PLOT��ָ�����
static const int CVGAMECORE_FIX_NULL_POINTER_BUG6 = 1; //mediv01 ��Ҫ���ڴ�й¶����
static const int CVGAMECORE_FIX_NULL_POINTER_BUG7 = 1; //mediv01 ��̫�а��յĿ�ָ��
static const int CVGAMECORE_FIX_NULL_POINTER_BUG8 = 1; //mediv01 Ԥ��

//����Wunshare Performance UP�е�����
static const int CVGAMECORE_FIX_BUG_PERFORMANCE_UP01 = 1; //mediv01 ����Cyplayer�еĲ�����������
static const int CVGAMECORE_FIX_BUG_PERFORMANCE_UP02 = 1; //mediv01 Ԥ��
static const int CVGAMECORE_FIX_BUG_PERFORMANCE_UP03 = 1; //mediv01 Ԥ��
static const int CVGAMECORE_FIX_BUG_PERFORMANCE_UP04 = 1; //mediv01 Ԥ��
*/


#ifndef CIV4_GLOBALS_H
#define CIV4_GLOBALS_H

//#include "CvStructs.h"
//
// 'global' vars for Civ IV.  singleton class.
// All globals and global types should be contained in this class
//

class FProfiler;
class CvDLLUtilityIFaceBase;
class CvRandom;
class CvGameAI;
class CMessageControl;
class CvDropMgr;
class CMessageQueue;
class CvSetupData;
class CvInitCore;
class CvMessageCodeTranslator;
class CvPortal;
class CvStatsReporter;
class CvDLLInterfaceIFaceBase;
class CvPlayerAI;
class CvDiplomacyScreen;
class CvCivicsScreen;
class CvWBUnitEditScreen;
class CvWBCityEditScreen;
class CMPDiplomacyScreen;
class FMPIManager;
class FAStar;
class CvInterface;
class CMainMenu;
class CvEngine;
class CvArtFileMgr;
class FVariableSystem;
class CvMap;
class CvPlayerAI;
class CvTeamAI;
class CvInterfaceModeInfo;
class CvWorldInfo;
class CvClimateInfo;
class CvSeaLevelInfo;
class CvColorInfo;
class CvPlayerColorInfo;
class CvAdvisorInfo;
class CvRouteModelInfo;
class CvRiverInfo;
class CvRiverModelInfo;
class CvWaterPlaneInfo;
class CvTerrainPlaneInfo;
class CvCameraOverlayInfo;
class CvAnimationPathInfo;
class CvAnimationCategoryInfo;
class CvEntityEventInfo;
class CvEffectInfo;
class CvAttachableInfo;
class CvCameraInfo;
class CvUnitFormationInfo;
class CvGameText;
class CvLandscapeInfo;
class CvTerrainInfo;
class CvBonusClassInfo;
class CvBonusInfo;
class CvFeatureInfo;
class CvCivilizationInfo;
class CvLeaderHeadInfo;
class CvTraitInfo;
class CvCursorInfo;
class CvThroneRoomCamera;
class CvThroneRoomInfo;
class CvThroneRoomStyleInfo;
class CvSlideShowInfo;
class CvSlideShowRandomInfo;
class CvWorldPickerInfo;
class CvSpaceShipInfo;
class CvUnitInfo;
class CvSpecialUnitInfo;
class CvInfoBase;
class CvYieldInfo;
class CvCommerceInfo;
class CvRouteInfo;
class CvImprovementInfo;
class CvGoodyInfo;
class CvBuildInfo;
class CvHandicapInfo;
class CvGameSpeedInfo;
class CvTurnTimerInfo;
class CvProcessInfo;
class CvVoteInfo;
class CvProjectInfo;
class CvBuildingClassInfo;
class CvBuildingInfo;
class CvSpecialBuildingInfo;
class CvUnitClassInfo;
class CvActionInfo;
class CvMissionInfo;
class CvControlInfo;
class CvCommandInfo;
class CvAutomateInfo;
class CvPromotionInfo;
class CvTechInfo;
class CvReligionInfo;
class CvCorporationInfo;
class CvSpecialistInfo;
class CvCivicOptionInfo;
class CvCivicInfo;
class CvDiplomacyInfo;
class CvEraInfo;
class CvHurryInfo;
class CvEmphasizeInfo;
class CvUpkeepInfo;
class CvCultureLevelInfo;
class CvVictoryInfo;
class CvQuestInfo;
class CvGameOptionInfo;
class CvMPOptionInfo;
class CvForceControlInfo;
class CvPlayerOptionInfo;
class CvGraphicOptionInfo;
class CvTutorialInfo;
class CvEventTriggerInfo;
class CvEventInfo;
class CvEspionageMissionInfo;
class CvUnitArtStyleTypeInfo;
class CvVoteSourceInfo;
class CvMainMenuInfo;
class CyArgsList;


class CvGlobals
{
//	friend class CvDLLUtilityIFace;
	friend class CvXMLLoadUtility;
public:

	// mediv01 cache
	int m_iMAX_YIELD_STACK;
	int m_iCVGAMETEXT_MANUAL_DEBUG_TRIGGER;
	int m_iCVGAMETEXT_SHOW_ENERMY_AREA;
	int m_iGAME_TEXT_SHOW_AREA_NAME_IN_ALL_UNIT;
	int m_iGAME_TEXT_SHOW_CITY_X_AND_Y;
	int m_iCVPLAYER_CAN_CONTACT_BARBARIAN;
	int m_iANYFUN_ALERT_FOR_WORLD_WONDER;
	int m_iANYFUN_ALERT_FOR_ANY_BUILDING;
	int m_iCVTECH_SHOW_TECH_DISCOVERY2_MAX;
	int m_iCVTECH_SHOW_TECH_DISCOVERY3_MAX;
	int m_iCVTECH_SHOW_TECH_DISCOVERY2_SHOW_DEAD;
	int m_iCVPLAYERAI_CAN_ALWAYS_TRADE_RESOURCE;
	int m_iCVCITY_INCREASE_RELIGION_CHANCE_ONLY_FOR_STATERELIGION;
	int m_iCVCITY_CAN_CAPTURE_GREAT_PEOPLE_WHEN_RAZE_CITY;
	int m_iPLAYER_TEAMAI_OPEN_BORDER_ATTITUDE_BONUS;

	int m_iCVPLAYERAI_ATTITUDE_BONUS;
	int m_iCVUNIT_CAN_CAPTURE_GREAT_PEOPLE;
	int m_iCVUNITAI_AI_NOT_PILLAGE;
	int m_iCVUNIT_CAN_SPREAD_RELIGON_ANYWHERE;
	int m_iCVCITY_BUILDING_NO_MAXOVERFLOW_LIMIT;
	int m_iCVCITY_FOUND_CITY_CAN_USE_FOREST;
	int m_iCVPLAYERAI_AI_DONNOT_TRADE_MAP_EACH_OTHER;

	int m_iCVUNIT_HUMAN_SPY_CANNOT_REVEAL;
	int m_iCAPTURE_CITY_WITHOUT_ANY_DAMAGE;
	int m_iCAPTURE_CITY_WITH_ALL_DAMAGE;
	int m_iCITY_NO_ALLOW_TO_LIBERATE_TO_PLAYER;
	int m_iCVCITY_HURRY_CALCULATION_WITH_FLOAT;
	int m_iCVUNIT_GREAT_ENGINEER_ACCELERATE_UNLIMITED;
	int m_iCVUNIT_GREAT_ENGINEER_ACCELERATE_USE_MODIFIER;
	int m_iCVUNIT_DISBAND_CAN_GIVE_GOLD;
	int m_iCVUNIT_DISBAND_GIVE_GOLD;
	int m_iCVUNIT_DISBAND_GIVE_GOLD_PERCENT;
	int m_iCVPLAYERAI_CAN_ALWAYS_TRADE_CITY;
	int m_iCVPLAYERAI_CAN_TRADE_GOLD_TURN_UNLIMITED_MULTI;
	int m_iCVGAME_CANNOT_VASSAL_TO_INDEPENDENT;
	int m_iCVUNIT_CAN_CAPTURE_WORKER_WITHOUT_SLAVERY;
	int m_iCVCITY_RELIGON_NO_DISAPPEAR;
	int m_iCVPLAYERAI_CAN_TRADE_GOLD_TURN_BASE_ON_POPULATION;




	// mediv01 cache

	// mediv01 ����
	int m_CVGAMETEXT_SHOW_DEFEND_COMBAT;  // ����ʹ�� ����ʹ��

	// mediv01


	DllExport int AI_foundValue(int PlayerID, int iX, int iY, int iMinRivalRange, bool bStartingLoc) const;

	//mediv01

	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* fxnArg = NULL) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, long* result) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, CvString* result) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, CvWString* result) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<byte>* pList) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<int>* pIntList) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, int* pIntList, int* iListSize) const;
	bool callPythoFunction(CvString PYModule, CvString PYFunction, void* argsList4, std::vector<float>* pFloatList) const;


	int AItradeTechValList(PlayerTypes eWhoTo, PlayerTypes eMyPlayer, TechTypes iTech, OperationType Operation) const;
	bool AIcantradeTech(PlayerTypes eWhoTo, PlayerTypes eMyPlayer, TechTypes iTech) const;

	void CvGlobals::show(CvWString text) const;

	void logswithid(PlayerTypes PlayerID, CvWString2& buf, CvString2 filename) const;
	void logs(CvWString2& buf, CvString2 filename) const;
	void logswithid(PlayerTypes PlayerID, CvWString& buf, CvString filename) const;
	void logs(CvWString& buf, CvString filename) const;


	//DllExport void logs(CvString buf, CvString filename) const;
	void logs(wchar* buf, CvString filename) const;
	void logs(char* buf, CvString filename) const;
	void logs(const CvWString& buf, CvString filename) const;
	//DllExport void logs(const CvString buf, CvString filename) const;
	void logs(const wchar* buf, CvString filename) const;
	void logs(const char* buf, CvString filename) const;
	void countFunctionCall(CvString functionname) const;
	void countFunctionStartTime(CvString functionname) const;
	void countFunctionEndTime(CvString functionname) const;
	void debug() const;
	void doTurn() const;
	int getTimeNow() const;
	int showAIstrategy(int iPlayer) const;
	int getGoldMultiplier() const;

	bool isHuman(PlayerTypes PlayerID) const;
	PlayerTypes getHumanID() const;
	TeamTypes getHumanTeam() const;
	TeamTypes getTeam(PlayerTypes iPlayer) const;
	int getGameTurn() const;
	int getGameTurnYear() const;
	int rand(int range) const;
	int simpleRand(int range) const;
	void updateAllPlotSight(PlayerTypes PlayerID, bool withoutflog) const;
	void FogOfWarOff();

	void doCollapse(PlayerTypes PlayerID) const;
	bool flipCity(int x, int y, bool bFlipType, bool bKillUnits, int iNewOwner) const;
	bool cultureManager(int x, int y, int iCulturePercent, int iNewOwner, int iOldOwner, bool bBarbarian2x2Decay, bool bBarbarian2x2Conversion, bool bAlwaysOwnPlots) const;

	// singleton accessor
	DllExport inline static CvGlobals& getInstance();

	DllExport CvGlobals();
	DllExport virtual ~CvGlobals();

	DllExport void init();
	DllExport void uninit();
	DllExport void clearTypesMap();

	DllExport CvDiplomacyScreen* getDiplomacyScreen();
	DllExport CMPDiplomacyScreen* getMPDiplomacyScreen();

	DllExport FMPIManager*& getFMPMgrPtr();
	DllExport CvPortal& getPortal();
	DllExport CvSetupData& getSetupData();
	DllExport CvInitCore& getInitCore();
	DllExport CvInitCore& getLoadedInitCore();
	DllExport CvInitCore& getIniInitCore();
	DllExport CvMessageCodeTranslator& getMessageCodes();
	DllExport CvStatsReporter& getStatsReporter();
	DllExport CvStatsReporter* getStatsReporterPtr();
	DllExport CvInterface& getInterface();
	DllExport CvInterface* getInterfacePtr();
	DllExport int getMaxCivPlayers() const;
#ifdef _USRDLL
	CvMap& getMapINLINE() { return *m_map; }				// inlined for perf reasons, do not use outside of dll
	CvGameAI& getGameINLINE() { return *m_game; }			// inlined for perf reasons, do not use outside of dll
#endif
	DllExport CvMap& getMap();
	DllExport CvGameAI& getGame();
	DllExport CvGameAI *getGamePointer();
	DllExport CvRandom& getASyncRand();
	DllExport CMessageQueue& getMessageQueue();
	DllExport CMessageQueue& getHotMessageQueue();
	DllExport CMessageControl& getMessageControl();
	DllExport CvDropMgr& getDropMgr();
	DllExport FAStar& getPathFinder();
	DllExport FAStar& getInterfacePathFinder();
	DllExport FAStar& getStepFinder();
	DllExport FAStar& getRouteFinder();
	DllExport FAStar& getBorderFinder();
	DllExport FAStar& getAreaFinder();
	DllExport FAStar& getPlotGroupFinder();
	DllExport NiPoint3& getPt3Origin();

	DllExport std::vector<CvInterfaceModeInfo*>& getInterfaceModeInfo();
	DllExport CvInterfaceModeInfo& getInterfaceModeInfo(InterfaceModeTypes e);

	DllExport NiPoint3& getPt3CameraDir();

	DllExport bool& getLogging();
	DllExport bool& getRandLogging();
	DllExport bool& getSynchLogging();
	DllExport bool& overwriteLogs();

	DllExport int* getPlotDirectionX();
	DllExport int* getPlotDirectionY();
	DllExport int* getPlotCardinalDirectionX();
	DllExport int* getPlotCardinalDirectionY();
	DllExport int* getCityPlotX();
	DllExport int* getCityPlotY();
	DllExport int* getCityPlotPriority();
	DllExport int getXYCityPlot(int i, int j);
	DirectionTypes* getTurnLeftDirection();
	DirectionTypes getTurnLeftDirection(int i);
	DirectionTypes* getTurnRightDirection();
	DirectionTypes getTurnRightDirection(int i);
	DllExport DirectionTypes getXYDirection(int i, int j);

	// Leoreth
	DllExport int* getCityPlot3X();
	DllExport int* getCityPlot3Y();

	// Leoreth: graphics paging
	void setGraphicalDetailPagingEnabled(bool bEnabled);
	bool getGraphicalDetailPagingEnabled();
	int getGraphicalDetailPageInRange();

	//
	// Global Infos
	// All info type strings are upper case and are kept in this hash map for fast lookup
	//
	DllExport int getInfoTypeForString(const char* szType, bool hideAssert = false) const;			// returns the infos index, use this when searching for an info type string
	DllExport void setInfoTypeFromString(const char* szType, int idx);
	DllExport void infoTypeFromStringReset();
	DllExport void addToInfosVectors(void *infoVector);
	DllExport void infosReset();

	DllExport int getNumWorldInfos();
	std::vector<CvWorldInfo*>& getWorldInfo();
	DllExport CvWorldInfo& getWorldInfo(WorldSizeTypes e);

	DllExport int getNumClimateInfos();
	std::vector<CvClimateInfo*>& getClimateInfo();
	DllExport CvClimateInfo& getClimateInfo(ClimateTypes e);

	DllExport int getNumSeaLevelInfos();
	std::vector<CvSeaLevelInfo*>& getSeaLevelInfo();
	DllExport CvSeaLevelInfo& getSeaLevelInfo(SeaLevelTypes e);

	DllExport int getNumColorInfos();
	std::vector<CvColorInfo*>& getColorInfo();
	DllExport CvColorInfo& getColorInfo(ColorTypes e);

	DllExport int getNumPlayerColorInfos();
	std::vector<CvPlayerColorInfo*>& getPlayerColorInfo();
	DllExport CvPlayerColorInfo& getPlayerColorInfo(PlayerColorTypes e);

	int getNumAdvisorInfos();
	std::vector<CvAdvisorInfo*>& getAdvisorInfo();
	CvAdvisorInfo& getAdvisorInfo(AdvisorTypes e);

	DllExport  int getNumHints();
	std::vector<CvInfoBase*>& getHints();
	DllExport CvInfoBase& getHints(int i);

	DllExport int getNumMainMenus();
	std::vector<CvMainMenuInfo*>& getMainMenus();
	DllExport CvMainMenuInfo& getMainMenus(int i);

	DllExport int getNumRouteModelInfos();
	std::vector<CvRouteModelInfo*>& getRouteModelInfo();
	DllExport CvRouteModelInfo& getRouteModelInfo(int i);

	DllExport int getNumRiverInfos();
	std::vector<CvRiverInfo*>& getRiverInfo();
	DllExport CvRiverInfo& getRiverInfo(RiverTypes e);

	DllExport int getNumRiverModelInfos();
	std::vector<CvRiverModelInfo*>& getRiverModelInfo();
	DllExport CvRiverModelInfo& getRiverModelInfo(int i);

	DllExport int getNumWaterPlaneInfos();
	std::vector<CvWaterPlaneInfo*>& getWaterPlaneInfo();
	DllExport CvWaterPlaneInfo& getWaterPlaneInfo(int i);

	DllExport int getNumTerrainPlaneInfos();
	std::vector<CvTerrainPlaneInfo*>& getTerrainPlaneInfo();
	DllExport CvTerrainPlaneInfo& getTerrainPlaneInfo(int i);

	DllExport int getNumCameraOverlayInfos();
	std::vector<CvCameraOverlayInfo*>& getCameraOverlayInfo();
	DllExport CvCameraOverlayInfo& getCameraOverlayInfo(int i);

	DllExport int getNumAnimationPathInfos();
	std::vector<CvAnimationPathInfo*>& getAnimationPathInfo();
	DllExport CvAnimationPathInfo& getAnimationPathInfo(AnimationPathTypes e);

	DllExport int getNumAnimationCategoryInfos();
	std::vector<CvAnimationCategoryInfo*>& getAnimationCategoryInfo();
	DllExport CvAnimationCategoryInfo& getAnimationCategoryInfo(AnimationCategoryTypes e);

	DllExport int getNumEntityEventInfos();
	std::vector<CvEntityEventInfo*>& getEntityEventInfo();
	DllExport CvEntityEventInfo& getEntityEventInfo(EntityEventTypes e);

	DllExport int getNumEffectInfos();
	std::vector<CvEffectInfo*>& getEffectInfo();
	DllExport CvEffectInfo& getEffectInfo(int i);

	DllExport int getNumAttachableInfos();
	std::vector<CvAttachableInfo*>& getAttachableInfo();
	DllExport CvAttachableInfo& getAttachableInfo(int i);

	DllExport int getNumCameraInfos();
	std::vector<CvCameraInfo*>& getCameraInfo();
	DllExport	CvCameraInfo& getCameraInfo(CameraAnimationTypes eCameraAnimationNum);

	DllExport int getNumUnitFormationInfos();
	std::vector<CvUnitFormationInfo*>& getUnitFormationInfo();
	DllExport CvUnitFormationInfo& getUnitFormationInfo(int i);

	int getNumGameTextXML();
	std::vector<CvGameText*>& getGameTextXML();

	DllExport int getNumLandscapeInfos();
	std::vector<CvLandscapeInfo*>& getLandscapeInfo();
	DllExport CvLandscapeInfo& getLandscapeInfo(int iIndex);
	DllExport int getActiveLandscapeID();
	DllExport void setActiveLandscapeID(int iLandscapeID);

	DllExport int getNumTerrainInfos();
	std::vector<CvTerrainInfo*>& getTerrainInfo();
	DllExport CvTerrainInfo& getTerrainInfo(TerrainTypes eTerrainNum);

	int getNumBonusClassInfos();
	std::vector<CvBonusClassInfo*>& getBonusClassInfo();
	CvBonusClassInfo& getBonusClassInfo(BonusClassTypes eBonusNum);

	DllExport int getNumBonusInfos();
	std::vector<CvBonusInfo*>& getBonusInfo();
	DllExport CvBonusInfo& getBonusInfo(BonusTypes eBonusNum);

	DllExport int getNumFeatureInfos();
	std::vector<CvFeatureInfo*>& getFeatureInfo();
	DllExport CvFeatureInfo& getFeatureInfo(FeatureTypes eFeatureNum);

	DllExport int& getNumPlayableCivilizationInfos();
	DllExport int& getNumAIPlayableCivilizationInfos();
	DllExport int getNumCivilizationInfos();
	std::vector<CvCivilizationInfo*>& getCivilizationInfo();
	DllExport CvCivilizationInfo& getCivilizationInfo(CivilizationTypes eCivilizationNum);

	DllExport int getNumLeaderHeadInfos();
	std::vector<CvLeaderHeadInfo*>& getLeaderHeadInfo();
	DllExport CvLeaderHeadInfo& getLeaderHeadInfo(LeaderHeadTypes eLeaderHeadNum);

	int getNumTraitInfos();
	std::vector<CvTraitInfo*>& getTraitInfo();
	CvTraitInfo& getTraitInfo(TraitTypes eTraitNum);

	DllExport int getNumCursorInfos();
	std::vector<CvCursorInfo*>& getCursorInfo();
	DllExport	CvCursorInfo& getCursorInfo(CursorTypes eCursorNum);

	DllExport int getNumThroneRoomCameras();
	std::vector<CvThroneRoomCamera*>& getThroneRoomCamera();
	DllExport	CvThroneRoomCamera& getThroneRoomCamera(int iIndex);

	DllExport int getNumThroneRoomInfos();
	std::vector<CvThroneRoomInfo*>& getThroneRoomInfo();
	DllExport	CvThroneRoomInfo& getThroneRoomInfo(int iIndex);

	DllExport int getNumThroneRoomStyleInfos();
	std::vector<CvThroneRoomStyleInfo*>& getThroneRoomStyleInfo();
	DllExport	CvThroneRoomStyleInfo& getThroneRoomStyleInfo(int iIndex);

	DllExport int getNumSlideShowInfos();
	std::vector<CvSlideShowInfo*>& getSlideShowInfo();
	DllExport	CvSlideShowInfo& getSlideShowInfo(int iIndex);

	DllExport int getNumSlideShowRandomInfos();
	std::vector<CvSlideShowRandomInfo*>& getSlideShowRandomInfo();
	DllExport	CvSlideShowRandomInfo& getSlideShowRandomInfo(int iIndex);

	DllExport int getNumWorldPickerInfos();
	std::vector<CvWorldPickerInfo*>& getWorldPickerInfo();
	DllExport	CvWorldPickerInfo& getWorldPickerInfo(int iIndex);

	DllExport int getNumSpaceShipInfos();
	std::vector<CvSpaceShipInfo*>& getSpaceShipInfo();
	DllExport	CvSpaceShipInfo& getSpaceShipInfo(int iIndex);

	int getNumUnitInfos();
	std::vector<CvUnitInfo*>& getUnitInfo();
	CvUnitInfo& getUnitInfo(UnitTypes eUnitNum);

	int getNumSpecialUnitInfos();
	std::vector<CvSpecialUnitInfo*>& getSpecialUnitInfo();
	CvSpecialUnitInfo& getSpecialUnitInfo(SpecialUnitTypes eSpecialUnitNum);

	int getNumConceptInfos();
	std::vector<CvInfoBase*>& getConceptInfo();
	CvInfoBase& getConceptInfo(ConceptTypes e);

	int getNumNewConceptInfos();
	std::vector<CvInfoBase*>& getNewConceptInfo();
	CvInfoBase& getNewConceptInfo(NewConceptTypes e);

	int getNumCityTabInfos();
	std::vector<CvInfoBase*>& getCityTabInfo();
	CvInfoBase& getCityTabInfo(CityTabTypes e);

	int getNumCalendarInfos();
	std::vector<CvInfoBase*>& getCalendarInfo();
	CvInfoBase& getCalendarInfo(CalendarTypes e);

	int getNumSeasonInfos();
	std::vector<CvInfoBase*>& getSeasonInfo();
	CvInfoBase& getSeasonInfo(SeasonTypes e);

	int getNumMonthInfos();
	std::vector<CvInfoBase*>& getMonthInfo();
	CvInfoBase& getMonthInfo(MonthTypes e);

	int getNumDenialInfos();
	std::vector<CvInfoBase*>& getDenialInfo();
	CvInfoBase& getDenialInfo(DenialTypes e);

	int getNumInvisibleInfos();
	std::vector<CvInfoBase*>& getInvisibleInfo();
	CvInfoBase& getInvisibleInfo(InvisibleTypes e);

	int getNumVoteSourceInfos();
	std::vector<CvVoteSourceInfo*>& getVoteSourceInfo();
	CvVoteSourceInfo& getVoteSourceInfo(VoteSourceTypes e);

	int getNumUnitCombatInfos();
	std::vector<CvInfoBase*>& getUnitCombatInfo();
	CvInfoBase& getUnitCombatInfo(UnitCombatTypes e);

	std::vector<CvInfoBase*>& getDomainInfo();
	CvInfoBase& getDomainInfo(DomainTypes e);

	std::vector<CvInfoBase*>& getUnitAIInfo();
	CvInfoBase& getUnitAIInfo(UnitAITypes eUnitAINum);

	std::vector<CvInfoBase*>& getAttitudeInfo();
	CvInfoBase& getAttitudeInfo(AttitudeTypes eAttitudeNum);

	std::vector<CvInfoBase*>& getMemoryInfo();
	CvInfoBase& getMemoryInfo(MemoryTypes eMemoryNum);

	DllExport int getNumGameOptionInfos();
	std::vector<CvGameOptionInfo*>& getGameOptionInfo();
	DllExport	CvGameOptionInfo& getGameOptionInfo(GameOptionTypes eGameOptionNum);

	DllExport int getNumMPOptionInfos();
	std::vector<CvMPOptionInfo*>& getMPOptionInfo();
	DllExport	CvMPOptionInfo& getMPOptionInfo(MultiplayerOptionTypes eMPOptionNum);

	DllExport int getNumForceControlInfos();
	std::vector<CvForceControlInfo*>& getForceControlInfo();
	DllExport	CvForceControlInfo& getForceControlInfo(ForceControlTypes eForceControlNum);

	std::vector<CvPlayerOptionInfo*>& getPlayerOptionInfo();
	DllExport	CvPlayerOptionInfo& getPlayerOptionInfo(PlayerOptionTypes ePlayerOptionNum);

	std::vector<CvGraphicOptionInfo*>& getGraphicOptionInfo();
	DllExport	CvGraphicOptionInfo& getGraphicOptionInfo(GraphicOptionTypes eGraphicOptionNum);

	std::vector<CvYieldInfo*>& getYieldInfo();
	CvYieldInfo& getYieldInfo(YieldTypes eYieldNum);

	std::vector<CvCommerceInfo*>& getCommerceInfo();
	CvCommerceInfo& getCommerceInfo(CommerceTypes eCommerceNum);

	DllExport int getNumRouteInfos();
	std::vector<CvRouteInfo*>& getRouteInfo();
	DllExport	CvRouteInfo& getRouteInfo(RouteTypes eRouteNum);

	DllExport int getNumImprovementInfos();
	std::vector<CvImprovementInfo*>& getImprovementInfo();
	DllExport CvImprovementInfo& getImprovementInfo(ImprovementTypes eImprovementNum);

	DllExport int getNumGoodyInfos();
	std::vector<CvGoodyInfo*>& getGoodyInfo();
	DllExport CvGoodyInfo& getGoodyInfo(GoodyTypes eGoodyNum);

	DllExport int getNumBuildInfos();
	std::vector<CvBuildInfo*>& getBuildInfo();
	DllExport CvBuildInfo& getBuildInfo(BuildTypes eBuildNum);

	DllExport int getNumHandicapInfos();
	std::vector<CvHandicapInfo*>& getHandicapInfo();
	DllExport CvHandicapInfo& getHandicapInfo(HandicapTypes eHandicapNum);

	DllExport int getNumGameSpeedInfos();
	std::vector<CvGameSpeedInfo*>& getGameSpeedInfo();
	DllExport CvGameSpeedInfo& getGameSpeedInfo(GameSpeedTypes eGameSpeedNum);

	DllExport int getNumTurnTimerInfos();
	std::vector<CvTurnTimerInfo*>& getTurnTimerInfo();
	DllExport CvTurnTimerInfo& getTurnTimerInfo(TurnTimerTypes eTurnTimerNum);

	int getNumProcessInfos();
	std::vector<CvProcessInfo*>& getProcessInfo();
	CvProcessInfo& getProcessInfo(ProcessTypes e);

	int getNumVoteInfos();
	std::vector<CvVoteInfo*>& getVoteInfo();
	CvVoteInfo& getVoteInfo(VoteTypes e);

	int getNumProjectInfos();
	std::vector<CvProjectInfo*>& getProjectInfo();
	CvProjectInfo& getProjectInfo(ProjectTypes e);

	int getNumBuildingClassInfos();
	std::vector<CvBuildingClassInfo*>& getBuildingClassInfo();
	CvBuildingClassInfo& getBuildingClassInfo(BuildingClassTypes eBuildingClassNum);

	int getNumBuildingInfos();
	std::vector<CvBuildingInfo*>& getBuildingInfo();
	CvBuildingInfo& getBuildingInfo(BuildingTypes eBuildingNum);

	int getNumSpecialBuildingInfos();
	std::vector<CvSpecialBuildingInfo*>& getSpecialBuildingInfo();
	CvSpecialBuildingInfo& getSpecialBuildingInfo(SpecialBuildingTypes eSpecialBuildingNum);

	int getNumUnitClassInfos();
	std::vector<CvUnitClassInfo*>& getUnitClassInfo();
	CvUnitClassInfo& getUnitClassInfo(UnitClassTypes eUnitClassNum);

	DllExport int getNumActionInfos();
	std::vector<CvActionInfo*>& getActionInfo();
	DllExport CvActionInfo& getActionInfo(int i);

	std::vector<CvMissionInfo*>& getMissionInfo();
	DllExport CvMissionInfo& getMissionInfo(MissionTypes eMissionNum);

	std::vector<CvControlInfo*>& getControlInfo();
	DllExport CvControlInfo& getControlInfo(ControlTypes eControlNum);

	std::vector<CvCommandInfo*>& getCommandInfo();
	DllExport CvCommandInfo& getCommandInfo(CommandTypes eCommandNum);

	DllExport int getNumAutomateInfos();
	std::vector<CvAutomateInfo*>& getAutomateInfo();
	DllExport CvAutomateInfo& getAutomateInfo(int iAutomateNum);

	int getNumPromotionInfos();
	std::vector<CvPromotionInfo*>& getPromotionInfo();
	CvPromotionInfo& getPromotionInfo(PromotionTypes ePromotionNum);

	int getNumTechInfos();
	std::vector<CvTechInfo*>& getTechInfo();
	CvTechInfo& getTechInfo(TechTypes eTechNum);

	int getNumReligionInfos();
	std::vector<CvReligionInfo*>& getReligionInfo();
	CvReligionInfo& getReligionInfo(ReligionTypes eReligionNum);

	int getNumCorporationInfos();
	std::vector<CvCorporationInfo*>& getCorporationInfo();
	CvCorporationInfo& getCorporationInfo(CorporationTypes eCorporationNum);

	int getNumSpecialistInfos();
	std::vector<CvSpecialistInfo*>& getSpecialistInfo();
	CvSpecialistInfo& getSpecialistInfo(SpecialistTypes eSpecialistNum);

	int getNumCivicOptionInfos();
	std::vector<CvCivicOptionInfo*>& getCivicOptionInfo();
	CvCivicOptionInfo& getCivicOptionInfo(CivicOptionTypes eCivicOptionNum);

	int getNumCivicInfos();
	std::vector<CvCivicInfo*>& getCivicInfo();
	CvCivicInfo& getCivicInfo(CivicTypes eCivicNum);

	int getNumDiplomacyInfos();
	std::vector<CvDiplomacyInfo*>& getDiplomacyInfo();
	CvDiplomacyInfo& getDiplomacyInfo(int iDiplomacyNum);

	DllExport int getNumEraInfos();
	std::vector<CvEraInfo*>& getEraInfo();
	DllExport CvEraInfo& getEraInfo(EraTypes eEraNum);

	int getNumHurryInfos();
	std::vector<CvHurryInfo*>& getHurryInfo();
	CvHurryInfo& getHurryInfo(HurryTypes eHurryNum);

	int getNumEmphasizeInfos();
	std::vector<CvEmphasizeInfo*>& getEmphasizeInfo();
	CvEmphasizeInfo& getEmphasizeInfo(EmphasizeTypes eEmphasizeNum);

	int getNumUpkeepInfos();
	std::vector<CvUpkeepInfo*>& getUpkeepInfo();
	CvUpkeepInfo& getUpkeepInfo(UpkeepTypes eUpkeepNum);

	int getNumCultureLevelInfos();
	std::vector<CvCultureLevelInfo*>& getCultureLevelInfo();
	CvCultureLevelInfo& getCultureLevelInfo(CultureLevelTypes eCultureLevelNum);

	DllExport int getNumVictoryInfos();
	std::vector<CvVictoryInfo*>& getVictoryInfo();
	DllExport CvVictoryInfo& getVictoryInfo(VictoryTypes eVictoryNum);

	int getNumQuestInfos();
	std::vector<CvQuestInfo*>& getQuestInfo();
	CvQuestInfo& getQuestInfo(int iIndex);

	int getNumTutorialInfos();
	std::vector<CvTutorialInfo*>& getTutorialInfo();
	CvTutorialInfo& getTutorialInfo(int i);

	int getNumEventTriggerInfos();
	std::vector<CvEventTriggerInfo*>& getEventTriggerInfo();
	CvEventTriggerInfo& getEventTriggerInfo(EventTriggerTypes eEventTrigger);

	int getNumEventInfos();
	std::vector<CvEventInfo*>& getEventInfo();
	CvEventInfo& getEventInfo(EventTypes eEvent);

	int getNumEspionageMissionInfos();
	std::vector<CvEspionageMissionInfo*>& getEspionageMissionInfo();
	CvEspionageMissionInfo& getEspionageMissionInfo(EspionageMissionTypes eEspionageMissionNum);

	int getNumUnitArtStyleTypeInfos();
	std::vector<CvUnitArtStyleTypeInfo*>& getUnitArtStyleTypeInfo();
	CvUnitArtStyleTypeInfo& getUnitArtStyleTypeInfo(UnitArtStyleTypes eUnitArtStyleTypeNum);

	//
	// Global Types
	// All type strings are upper case and are kept in this hash map for fast lookup
	// The other functions are kept for convenience when enumerating, but most are not used
	//
	DllExport int getTypesEnum(const char* szType) const;				// use this when searching for a type
	DllExport void setTypesEnum(const char* szType, int iEnum);

	DllExport int getNUM_ENGINE_DIRTY_BITS() const;
	DllExport int getNUM_INTERFACE_DIRTY_BITS() const;
	DllExport int getNUM_YIELD_TYPES() const;
	DllExport int getNUM_COMMERCE_TYPES() const;
	DllExport int getNUM_FORCECONTROL_TYPES() const;
	DllExport int getNUM_INFOBAR_TYPES() const;
	DllExport int getNUM_HEALTHBAR_TYPES() const;
	DllExport int getNUM_CONTROL_TYPES() const;
	DllExport int getNUM_LEADERANIM_TYPES() const;

	DllExport int& getNumEntityEventTypes();
	CvString*& getEntityEventTypes();
	DllExport CvString& getEntityEventTypes(EntityEventTypes e);

	DllExport int& getNumAnimationOperatorTypes();
	CvString*& getAnimationOperatorTypes();
	DllExport CvString& getAnimationOperatorTypes(AnimationOperatorTypes e);

	CvString*& getFunctionTypes();
	DllExport CvString& getFunctionTypes(FunctionTypes e);

	int& getNumFlavorTypes();
	CvString*& getFlavorTypes();
	CvString& getFlavorTypes(FlavorTypes e);

	DllExport int& getNumArtStyleTypes();
	CvString*& getArtStyleTypes();
	DllExport CvString& getArtStyleTypes(ArtStyleTypes e);

	int& getNumCitySizeTypes();
	CvString*& getCitySizeTypes();
	CvString& getCitySizeTypes(int i);

	CvString*& getContactTypes();
	CvString& getContactTypes(ContactTypes e);

	CvString*& getDiplomacyPowerTypes();
	CvString& getDiplomacyPowerTypes(DiplomacyPowerTypes e);

	CvString*& getAutomateTypes();
	CvString& getAutomateTypes(AutomateTypes e);

	CvString*& getDirectionTypes();
	DllExport CvString& getDirectionTypes(AutomateTypes e);

	DllExport int& getNumFootstepAudioTypes();
	CvString*& getFootstepAudioTypes();
	DllExport CvString& getFootstepAudioTypes(int i);
	DllExport int getFootstepAudioTypeByTag(CvString strTag);

	CvString*& getFootstepAudioTags();
	DllExport CvString& getFootstepAudioTags(int i);

	CvString& getCurrentXMLFile();
	void setCurrentXMLFile(const TCHAR* szFileName);

	//
	///////////////// BEGIN global defines
	// THESE ARE READ-ONLY
	//

	DllExport FVariableSystem* getDefinesVarSystem();
	DllExport void cacheGlobals();

	// ***** EXPOSED TO PYTHON *****
	DllExport int getDefineINT( const char * szName ) const;
	DllExport float getDefineFLOAT( const char * szName ) const;
	DllExport const char * getDefineSTRING( const char * szName ) const;
	DllExport void setDefineINT( const char * szName, int iValue );
	DllExport void setDefineFLOAT( const char * szName, float fValue );
	DllExport void setDefineSTRING( const char * szName, const char * szValue );

	int getMOVE_DENOMINATOR();
	int getNUM_UNIT_PREREQ_OR_BONUSES();
	int getNUM_BUILDING_PREREQ_OR_BONUSES();
	int getFOOD_CONSUMPTION_PER_POPULATION();
	int getMAX_HIT_POINTS();
	int getPATH_DAMAGE_WEIGHT();
	int getHILLS_EXTRA_DEFENSE();
	int getRIVER_ATTACK_MODIFIER();
	int getAMPHIB_ATTACK_MODIFIER();
	int getHILLS_EXTRA_MOVEMENT();
	DllExport int getMAX_PLOT_LIST_ROWS();
	DllExport int getUNIT_MULTISELECT_MAX();
	int getPERCENT_ANGER_DIVISOR();
	DllExport int getEVENT_MESSAGE_TIME();
	int getROUTE_FEATURE_GROWTH_MODIFIER();
	int getFEATURE_GROWTH_MODIFIER();
	int getMIN_CITY_RANGE();
	int getCITY_MAX_NUM_BUILDINGS();
	int getNUM_UNIT_AND_TECH_PREREQS();
	int getNUM_AND_TECH_PREREQS();
	int getNUM_OR_TECH_PREREQS();
	int getLAKE_MAX_AREA_SIZE();
	int getNUM_ROUTE_PREREQ_OR_BONUSES();
	int getNUM_BUILDING_AND_TECH_PREREQS();
	int getMIN_WATER_SIZE_FOR_OCEAN();
	int getFORTIFY_MODIFIER_PER_TURN();
	int getMAX_CITY_DEFENSE_DAMAGE();
	int getNUM_CORPORATION_PREREQ_BONUSES();
	int getPEAK_SEE_THROUGH_CHANGE();
	int getHILLS_SEE_THROUGH_CHANGE();
	int getSEAWATER_SEE_FROM_CHANGE();
	int getPEAK_SEE_FROM_CHANGE();
	int getHILLS_SEE_FROM_CHANGE();
	int getUSE_SPIES_NO_ENTER_BORDERS();

	DllExport float getCAMERA_MIN_YAW();
	DllExport float getCAMERA_MAX_YAW();
	DllExport float getCAMERA_FAR_CLIP_Z_HEIGHT();
	DllExport float getCAMERA_MAX_TRAVEL_DISTANCE();
	DllExport float getCAMERA_START_DISTANCE();
	DllExport float getAIR_BOMB_HEIGHT();
	DllExport float getPLOT_SIZE();
	DllExport float getCAMERA_SPECIAL_PITCH();
	DllExport float getCAMERA_MAX_TURN_OFFSET();
	DllExport float getCAMERA_MIN_DISTANCE();
	DllExport float getCAMERA_UPPER_PITCH();
	DllExport float getCAMERA_LOWER_PITCH();
	DllExport float getFIELD_OF_VIEW();
	DllExport float getSHADOW_SCALE();
	DllExport float getUNIT_MULTISELECT_DISTANCE();

	int getUSE_CANNOT_FOUND_CITY_CALLBACK();
	int getUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK();
	int getUSE_IS_PLAYER_RESEARCH_CALLBACK();
	int getUSE_CAN_RESEARCH_CALLBACK();
	int getUSE_CANNOT_DO_CIVIC_CALLBACK();
	int getUSE_CAN_DO_CIVIC_CALLBACK();
	int getUSE_CANNOT_CONSTRUCT_CALLBACK();
	int getUSE_CAN_CONSTRUCT_CALLBACK();
	int getUSE_CAN_DECLARE_WAR_CALLBACK();
	int getUSE_CANNOT_RESEARCH_CALLBACK();
	int getUSE_GET_UNIT_COST_MOD_CALLBACK();
	int getUSE_GET_BUILDING_COST_MOD_CALLBACK();
	int getUSE_GET_CITY_FOUND_VALUE_CALLBACK();
	int getUSE_CANNOT_HANDLE_ACTION_CALLBACK();
	int getUSE_CAN_BUILD_CALLBACK();
	int getUSE_CANNOT_TRAIN_CALLBACK();
	int getUSE_CAN_TRAIN_CALLBACK();
	int getUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK();
	int getUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK();
	DllExport int getUSE_FINISH_TEXT_CALLBACK();
	int getUSE_ON_UNIT_SET_XY_CALLBACK();
	int getUSE_ON_UNIT_SELECTED_CALLBACK();
	int getUSE_ON_UPDATE_CALLBACK();
	int getUSE_ON_UNIT_CREATED_CALLBACK();
	int getUSE_ON_UNIT_LOST_CALLBACK();

	DllExport int getMAX_CIV_PLAYERS();
	DllExport int getMAX_PLAYERS();
	DllExport int getMAX_CIV_TEAMS();
	DllExport int getMAX_TEAMS();
	DllExport int getBARBARIAN_PLAYER();
	DllExport int getBARBARIAN_TEAM();
	DllExport int getINVALID_PLOT_COORD();
	DllExport int getNUM_CITY_PLOTS();
	DllExport int getCITY_HOME_PLOT();

	// ***** END EXPOSED TO PYTHON *****

	////////////// END DEFINES //////////////////

	DllExport void setDLLIFace(CvDLLUtilityIFaceBase* pDll);
#ifdef _USRDLL
	CvDLLUtilityIFaceBase* getDLLIFace() { return m_pDLL; }		// inlined for perf reasons, do not use outside of dll
#endif
	DllExport CvDLLUtilityIFaceBase* getDLLIFaceNonInl();
	DllExport void setDLLProfiler(FProfiler* prof);
	FProfiler* getDLLProfiler();
	DllExport void enableDLLProfiler(bool bEnable);
	bool isDLLProfilerEnabled() const;

	DllExport bool IsGraphicsInitialized() const;
	DllExport void SetGraphicsInitialized(bool bVal);

	// for caching
	DllExport bool readBuildingInfoArray(FDataStreamBase* pStream);
	DllExport void writeBuildingInfoArray(FDataStreamBase* pStream);

	DllExport bool readTechInfoArray(FDataStreamBase* pStream);
	DllExport void writeTechInfoArray(FDataStreamBase* pStream);

	DllExport bool readUnitInfoArray(FDataStreamBase* pStream);
	DllExport void writeUnitInfoArray(FDataStreamBase* pStream);

	DllExport bool readLeaderHeadInfoArray(FDataStreamBase* pStream);
	DllExport void writeLeaderHeadInfoArray(FDataStreamBase* pStream);

	DllExport bool readCivilizationInfoArray(FDataStreamBase* pStream);
	DllExport void writeCivilizationInfoArray(FDataStreamBase* pStream);

	DllExport bool readPromotionInfoArray(FDataStreamBase* pStream);
	DllExport void writePromotionInfoArray(FDataStreamBase* pStream);

	DllExport bool readDiplomacyInfoArray(FDataStreamBase* pStream);
	DllExport void writeDiplomacyInfoArray(FDataStreamBase* pStream);

	DllExport bool readCivicInfoArray(FDataStreamBase* pStream);
	DllExport void writeCivicInfoArray(FDataStreamBase* pStream);

	DllExport bool readHandicapInfoArray(FDataStreamBase* pStream);
	DllExport void writeHandicapInfoArray(FDataStreamBase* pStream);

	DllExport bool readBonusInfoArray(FDataStreamBase* pStream);
	DllExport void writeBonusInfoArray(FDataStreamBase* pStream);

	DllExport bool readImprovementInfoArray(FDataStreamBase* pStream);
	DllExport void writeImprovementInfoArray(FDataStreamBase* pStream);

	DllExport bool readEventInfoArray(FDataStreamBase* pStream);
	DllExport void writeEventInfoArray(FDataStreamBase* pStream);

	DllExport bool readEventTriggerInfoArray(FDataStreamBase* pStream);
	DllExport void writeEventTriggerInfoArray(FDataStreamBase* pStream);

	//
	// additional accessors for initting globals
	//

	DllExport void setInterface(CvInterface* pVal);
	DllExport void setDiplomacyScreen(CvDiplomacyScreen* pVal);
	DllExport void setMPDiplomacyScreen(CMPDiplomacyScreen* pVal);
	DllExport void setMessageQueue(CMessageQueue* pVal);
	DllExport void setHotJoinMessageQueue(CMessageQueue* pVal);
	DllExport void setMessageControl(CMessageControl* pVal);
	DllExport void setSetupData(CvSetupData* pVal);
	DllExport void setMessageCodeTranslator(CvMessageCodeTranslator* pVal);
	DllExport void setDropMgr(CvDropMgr* pVal);
	DllExport void setPortal(CvPortal* pVal);
	DllExport void setStatsReport(CvStatsReporter* pVal);
	DllExport void setPathFinder(FAStar* pVal);
	DllExport void setInterfacePathFinder(FAStar* pVal);
	DllExport void setStepFinder(FAStar* pVal);
	DllExport void setRouteFinder(FAStar* pVal);
	DllExport void setBorderFinder(FAStar* pVal);
	DllExport void setAreaFinder(FAStar* pVal);
	DllExport void setPlotGroupFinder(FAStar* pVal);

	// So that CvEnums are moddable in the DLL
	DllExport int getNumDirections() const;
	DllExport int getNumGameOptions() const;
	DllExport int getNumMPOptions() const;
	DllExport int getNumSpecialOptions() const;
	DllExport int getNumGraphicOptions() const;
	DllExport int getNumTradeableItems() const;
	DllExport int getNumBasicItems() const;
	DllExport int getNumTradeableHeadings() const;
	DllExport int getNumCommandInfos() const;
	DllExport int getNumControlInfos() const;
	DllExport int getNumMissionInfos() const;
	DllExport int getNumPlayerOptionInfos() const;
	DllExport int getMaxNumSymbols() const;
	DllExport int getNumGraphicLevels() const;
	DllExport int getNumGlobeLayers() const;

// BUG - DLL Info - start
	bool isBull() const;
	int getBullApiVersion() const;

	const wchar* getBullName() const;
	const wchar* getBullVersion() const;
// BUG - DLL Info - end

// BUG - BUG Info - start
	void setIsBug(bool bIsBug);
// BUG - BUG Info - end

// BUFFY - DLL Info - start
#ifdef _BUFFY
	bool isBuffy() const;
	int getBuffyApiVersion() const;

	const wchar* getBuffyName() const;
	const wchar* getBuffyVersion() const;
#endif
// BUFFY - DLL Info - end

	void deleteInfoArrays();

protected:

	bool m_bGraphicsInitialized;
	bool m_bDLLProfiler;
	bool m_bLogging;
	bool m_bRandLogging;
	bool m_bSynchLogging;
	bool m_bOverwriteLogs;
	NiPoint3  m_pt3CameraDir;
	int m_iNewPlayers;

	CMainMenu* m_pkMainMenu;

	bool m_bZoomOut;
	bool m_bZoomIn;
	bool m_bLoadGameFromFile;

	FMPIManager * m_pFMPMgr;

	CvRandom* m_asyncRand;

	CvGameAI* m_game;

	CMessageQueue* m_messageQueue;
	CMessageQueue* m_hotJoinMsgQueue;
	CMessageControl* m_messageControl;
	CvSetupData* m_setupData;
	CvInitCore* m_iniInitCore;
	CvInitCore* m_loadedInitCore;
	CvInitCore* m_initCore;
	CvMessageCodeTranslator * m_messageCodes;
	CvDropMgr* m_dropMgr;
	CvPortal* m_portal;
	CvStatsReporter * m_statsReporter;
	CvInterface* m_interface;

	CvArtFileMgr* m_pArtFileMgr;

	CvMap* m_map;

	CvDiplomacyScreen* m_diplomacyScreen;
	CMPDiplomacyScreen* m_mpDiplomacyScreen;

	FAStar* m_pathFinder;
	FAStar* m_interfacePathFinder;
	FAStar* m_stepFinder;
	FAStar* m_routeFinder;
	FAStar* m_borderFinder;
	FAStar* m_areaFinder;
	FAStar* m_plotGroupFinder;

	NiPoint3 m_pt3Origin;

	int* m_aiPlotDirectionX;	// [NUM_DIRECTION_TYPES];
	int* m_aiPlotDirectionY;	// [NUM_DIRECTION_TYPES];
	int* m_aiPlotCardinalDirectionX;	// [NUM_CARDINALDIRECTION_TYPES];
	int* m_aiPlotCardinalDirectionY;	// [NUM_CARDINALDIRECTION_TYPES];
	int* m_aiCityPlotX;	// [NUM_CITY_PLOTS];
	int* m_aiCityPlotY;	// [NUM_CITY_PLOTS];
	int* m_aiCityPlotPriority;	// [NUM_CITY_PLOTS];
	int m_aaiXYCityPlot[CITY_PLOTS_DIAMETER][CITY_PLOTS_DIAMETER];

	// Leoreth: index over the third ring as well
	int* m_aiCityPlot3X;
	int* m_aiCityPlot3Y;

	// Leoreth: graphics paging
	bool m_bGraphicalDetailPagingEnabled;

	DirectionTypes* m_aeTurnLeftDirection;	// [NUM_DIRECTION_TYPES];
	DirectionTypes* m_aeTurnRightDirection;	// [NUM_DIRECTION_TYPES];
	DirectionTypes m_aaeXYDirection[DIRECTION_DIAMETER][DIRECTION_DIAMETER];

	//InterfaceModeInfo m_aInterfaceModeInfo[NUM_INTERFACEMODE_TYPES] =
	std::vector<CvInterfaceModeInfo*> m_paInterfaceModeInfo;

	/***********************************************************************************************************************
	Globals loaded from XML
	************************************************************************************************************************/

	// all type strings are upper case and are kept in this hash map for fast lookup, Moose
	typedef stdext::hash_map<std::string /* type string */, int /* info index */> InfosMap;
	InfosMap m_infosMap;
	std::vector<std::vector<CvInfoBase *> *> m_aInfoVectors;

	std::vector<CvColorInfo*> m_paColorInfo;
	std::vector<CvPlayerColorInfo*> m_paPlayerColorInfo;
	std::vector<CvAdvisorInfo*> m_paAdvisorInfo;
	std::vector<CvInfoBase*> m_paHints;
	std::vector<CvMainMenuInfo*> m_paMainMenus;
	std::vector<CvTerrainInfo*> m_paTerrainInfo;
	std::vector<CvLandscapeInfo*> m_paLandscapeInfo;
	int m_iActiveLandscapeID;
	std::vector<CvWorldInfo*> m_paWorldInfo;
	std::vector<CvClimateInfo*> m_paClimateInfo;
	std::vector<CvSeaLevelInfo*> m_paSeaLevelInfo;
	std::vector<CvYieldInfo*> m_paYieldInfo;
	std::vector<CvCommerceInfo*> m_paCommerceInfo;
	std::vector<CvRouteInfo*> m_paRouteInfo;
	std::vector<CvFeatureInfo*> m_paFeatureInfo;
	std::vector<CvBonusClassInfo*> m_paBonusClassInfo;
	std::vector<CvBonusInfo*> m_paBonusInfo;
	std::vector<CvImprovementInfo*> m_paImprovementInfo;
	std::vector<CvGoodyInfo*> m_paGoodyInfo;
	std::vector<CvBuildInfo*> m_paBuildInfo;
	std::vector<CvHandicapInfo*> m_paHandicapInfo;
	std::vector<CvGameSpeedInfo*> m_paGameSpeedInfo;
	std::vector<CvTurnTimerInfo*> m_paTurnTimerInfo;
	std::vector<CvCivilizationInfo*> m_paCivilizationInfo;
	int m_iNumPlayableCivilizationInfos;
	int m_iNumAIPlayableCivilizationInfos;
	std::vector<CvLeaderHeadInfo*> m_paLeaderHeadInfo;
	std::vector<CvTraitInfo*> m_paTraitInfo;
	std::vector<CvCursorInfo*> m_paCursorInfo;
	std::vector<CvThroneRoomCamera*> m_paThroneRoomCamera;
	std::vector<CvThroneRoomInfo*> m_paThroneRoomInfo;
	std::vector<CvThroneRoomStyleInfo*> m_paThroneRoomStyleInfo;
	std::vector<CvSlideShowInfo*> m_paSlideShowInfo;
	std::vector<CvSlideShowRandomInfo*> m_paSlideShowRandomInfo;
	std::vector<CvWorldPickerInfo*> m_paWorldPickerInfo;
	std::vector<CvSpaceShipInfo*> m_paSpaceShipInfo;
	std::vector<CvProcessInfo*> m_paProcessInfo;
	std::vector<CvVoteInfo*> m_paVoteInfo;
	std::vector<CvProjectInfo*> m_paProjectInfo;
	std::vector<CvBuildingClassInfo*> m_paBuildingClassInfo;
	std::vector<CvBuildingInfo*> m_paBuildingInfo;
	std::vector<CvSpecialBuildingInfo*> m_paSpecialBuildingInfo;
	std::vector<CvUnitClassInfo*> m_paUnitClassInfo;
	std::vector<CvUnitInfo*> m_paUnitInfo;
	std::vector<CvSpecialUnitInfo*> m_paSpecialUnitInfo;
	std::vector<CvInfoBase*> m_paConceptInfo;
	std::vector<CvInfoBase*> m_paNewConceptInfo;
	std::vector<CvInfoBase*> m_paCityTabInfo;
	std::vector<CvInfoBase*> m_paCalendarInfo;
	std::vector<CvInfoBase*> m_paSeasonInfo;
	std::vector<CvInfoBase*> m_paMonthInfo;
	std::vector<CvInfoBase*> m_paDenialInfo;
	std::vector<CvInfoBase*> m_paInvisibleInfo;
	std::vector<CvVoteSourceInfo*> m_paVoteSourceInfo;
	std::vector<CvInfoBase*> m_paUnitCombatInfo;
	std::vector<CvInfoBase*> m_paDomainInfo;
	std::vector<CvInfoBase*> m_paUnitAIInfos;
	std::vector<CvInfoBase*> m_paAttitudeInfos;
	std::vector<CvInfoBase*> m_paMemoryInfos;
	std::vector<CvInfoBase*> m_paFeatInfos;
	std::vector<CvGameOptionInfo*> m_paGameOptionInfos;
	std::vector<CvMPOptionInfo*> m_paMPOptionInfos;
	std::vector<CvForceControlInfo*> m_paForceControlInfos;
	std::vector<CvPlayerOptionInfo*> m_paPlayerOptionInfos;
	std::vector<CvGraphicOptionInfo*> m_paGraphicOptionInfos;
	std::vector<CvSpecialistInfo*> m_paSpecialistInfo;
	std::vector<CvEmphasizeInfo*> m_paEmphasizeInfo;
	std::vector<CvUpkeepInfo*> m_paUpkeepInfo;
	std::vector<CvCultureLevelInfo*> m_paCultureLevelInfo;
	std::vector<CvReligionInfo*> m_paReligionInfo;
	std::vector<CvCorporationInfo*> m_paCorporationInfo;
	std::vector<CvActionInfo*> m_paActionInfo;
	std::vector<CvMissionInfo*> m_paMissionInfo;
	std::vector<CvControlInfo*> m_paControlInfo;
	std::vector<CvCommandInfo*> m_paCommandInfo;
	std::vector<CvAutomateInfo*> m_paAutomateInfo;
	std::vector<CvPromotionInfo*> m_paPromotionInfo;
	std::vector<CvTechInfo*> m_paTechInfo;
	std::vector<CvCivicOptionInfo*> m_paCivicOptionInfo;
	std::vector<CvCivicInfo*> m_paCivicInfo;
	std::vector<CvDiplomacyInfo*> m_paDiplomacyInfo;
	std::vector<CvEraInfo*> m_aEraInfo;	// [NUM_ERA_TYPES];
	std::vector<CvHurryInfo*> m_paHurryInfo;
	std::vector<CvVictoryInfo*> m_paVictoryInfo;
	std::vector<CvRouteModelInfo*> m_paRouteModelInfo;
	std::vector<CvRiverInfo*> m_paRiverInfo;
	std::vector<CvRiverModelInfo*> m_paRiverModelInfo;
	std::vector<CvWaterPlaneInfo*> m_paWaterPlaneInfo;
	std::vector<CvTerrainPlaneInfo*> m_paTerrainPlaneInfo;
	std::vector<CvCameraOverlayInfo*> m_paCameraOverlayInfo;
	std::vector<CvAnimationPathInfo*> m_paAnimationPathInfo;
	std::vector<CvAnimationCategoryInfo*> m_paAnimationCategoryInfo;
	std::vector<CvEntityEventInfo*> m_paEntityEventInfo;
	std::vector<CvUnitFormationInfo*> m_paUnitFormationInfo;
	std::vector<CvEffectInfo*> m_paEffectInfo;
	std::vector<CvAttachableInfo*> m_paAttachableInfo;
	std::vector<CvCameraInfo*> m_paCameraInfo;
	std::vector<CvQuestInfo*> m_paQuestInfo;
	std::vector<CvTutorialInfo*> m_paTutorialInfo;
	std::vector<CvEventTriggerInfo*> m_paEventTriggerInfo;
	std::vector<CvEventInfo*> m_paEventInfo;
	std::vector<CvEspionageMissionInfo*> m_paEspionageMissionInfo;
    std::vector<CvUnitArtStyleTypeInfo*> m_paUnitArtStyleTypeInfo;

	// Game Text
	std::vector<CvGameText*> m_paGameTextXML;

	//////////////////////////////////////////////////////////////////////////
	// GLOBAL TYPES
	//////////////////////////////////////////////////////////////////////////

	// all type strings are upper case and are kept in this hash map for fast lookup, Moose
	typedef stdext::hash_map<std::string /* type string */, int /*enum value */> TypesMap;
	TypesMap m_typesMap;

	// XXX These are duplicates and are kept for enumeration convenience - most could be removed, Moose
	CvString *m_paszEntityEventTypes2;
	CvString *m_paszEntityEventTypes;
	int m_iNumEntityEventTypes;

	CvString *m_paszAnimationOperatorTypes;
	int m_iNumAnimationOperatorTypes;

	CvString* m_paszFunctionTypes;

	CvString* m_paszFlavorTypes;
	int m_iNumFlavorTypes;

	CvString *m_paszArtStyleTypes;
	int m_iNumArtStyleTypes;

	CvString *m_paszCitySizeTypes;
	int m_iNumCitySizeTypes;

	CvString *m_paszContactTypes;

	CvString *m_paszDiplomacyPowerTypes;

	CvString *m_paszAutomateTypes;

	CvString *m_paszDirectionTypes;

	CvString *m_paszFootstepAudioTypes;
	int m_iNumFootstepAudioTypes;

	CvString *m_paszFootstepAudioTags;
	int m_iNumFootstepAudioTags;

	CvString m_szCurrentXMLFile;
	//////////////////////////////////////////////////////////////////////////
	// Formerly Global Defines
	//////////////////////////////////////////////////////////////////////////

	FVariableSystem* m_VarSystem;

	int m_iMOVE_DENOMINATOR;
	int m_iNUM_UNIT_PREREQ_OR_BONUSES;
	int m_iNUM_BUILDING_PREREQ_OR_BONUSES;
	int m_iFOOD_CONSUMPTION_PER_POPULATION;
	int m_iMAX_HIT_POINTS;
	int m_iPATH_DAMAGE_WEIGHT;
	int m_iHILLS_EXTRA_DEFENSE;
	int m_iRIVER_ATTACK_MODIFIER;
	int m_iAMPHIB_ATTACK_MODIFIER;
	int m_iHILLS_EXTRA_MOVEMENT;
	int m_iMAX_PLOT_LIST_ROWS;
	int m_iUNIT_MULTISELECT_MAX;
	int m_iPERCENT_ANGER_DIVISOR;
	int m_iEVENT_MESSAGE_TIME;
	int m_iROUTE_FEATURE_GROWTH_MODIFIER;
	int m_iFEATURE_GROWTH_MODIFIER;
	int m_iMIN_CITY_RANGE;
	int m_iCITY_MAX_NUM_BUILDINGS;
	int m_iNUM_UNIT_AND_TECH_PREREQS;
	int m_iNUM_AND_TECH_PREREQS;
	int m_iNUM_OR_TECH_PREREQS;
	int m_iLAKE_MAX_AREA_SIZE;
	int m_iNUM_ROUTE_PREREQ_OR_BONUSES;
	int m_iNUM_BUILDING_AND_TECH_PREREQS;
	int m_iMIN_WATER_SIZE_FOR_OCEAN;
	int m_iFORTIFY_MODIFIER_PER_TURN;
	int m_iMAX_CITY_DEFENSE_DAMAGE;
	int m_iNUM_CORPORATION_PREREQ_BONUSES;
	int m_iPEAK_SEE_THROUGH_CHANGE;
	int m_iHILLS_SEE_THROUGH_CHANGE;
	int m_iSEAWATER_SEE_FROM_CHANGE;
	int m_iPEAK_SEE_FROM_CHANGE;
	int m_iHILLS_SEE_FROM_CHANGE;
	int m_iUSE_SPIES_NO_ENTER_BORDERS;

	float m_fCAMERA_MIN_YAW;
	float m_fCAMERA_MAX_YAW;
	float m_fCAMERA_FAR_CLIP_Z_HEIGHT;
	float m_fCAMERA_MAX_TRAVEL_DISTANCE;
	float m_fCAMERA_START_DISTANCE;
	float m_fAIR_BOMB_HEIGHT;
	float m_fPLOT_SIZE;
	float m_fCAMERA_SPECIAL_PITCH;
	float m_fCAMERA_MAX_TURN_OFFSET;
	float m_fCAMERA_MIN_DISTANCE;
	float m_fCAMERA_UPPER_PITCH;
	float m_fCAMERA_LOWER_PITCH;
	float m_fFIELD_OF_VIEW;
	float m_fSHADOW_SCALE;
	float m_fUNIT_MULTISELECT_DISTANCE;

	int m_iUSE_CANNOT_FOUND_CITY_CALLBACK;
	int m_iUSE_CAN_FOUND_CITIES_ON_WATER_CALLBACK;
	int m_iUSE_IS_PLAYER_RESEARCH_CALLBACK;
	int m_iUSE_CAN_RESEARCH_CALLBACK;
	int m_iUSE_CANNOT_DO_CIVIC_CALLBACK;
	int m_iUSE_CAN_DO_CIVIC_CALLBACK;
	int m_iUSE_CANNOT_CONSTRUCT_CALLBACK;
	int m_iUSE_CAN_CONSTRUCT_CALLBACK;
	int m_iUSE_CAN_DECLARE_WAR_CALLBACK;
	int m_iUSE_CANNOT_RESEARCH_CALLBACK;
	int m_iUSE_GET_UNIT_COST_MOD_CALLBACK;
	int m_iUSE_GET_BUILDING_COST_MOD_CALLBACK;
	int m_iUSE_GET_CITY_FOUND_VALUE_CALLBACK;
	int m_iUSE_CANNOT_HANDLE_ACTION_CALLBACK;
	int m_iUSE_CAN_BUILD_CALLBACK;
	int m_iUSE_CANNOT_TRAIN_CALLBACK;
	int m_iUSE_CAN_TRAIN_CALLBACK;
	int m_iUSE_UNIT_CANNOT_MOVE_INTO_CALLBACK;
	int m_iUSE_USE_CANNOT_SPREAD_RELIGION_CALLBACK;
	int m_iUSE_FINISH_TEXT_CALLBACK;
	int m_iUSE_ON_UNIT_SET_XY_CALLBACK;
	int m_iUSE_ON_UNIT_SELECTED_CALLBACK;
	int m_iUSE_ON_UPDATE_CALLBACK;
	int m_iUSE_ON_UNIT_CREATED_CALLBACK;
	int m_iUSE_ON_UNIT_LOST_CALLBACK;






	// DLL interface
	CvDLLUtilityIFaceBase* m_pDLL;

	FProfiler* m_Profiler;		// profiler
	CvString m_szDllProfileText;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                      02/21/10                                jdog5000      */
/*                                                                                              */
/* Efficiency, Options                                                                          */
/************************************************************************************************/
public:
	int getDefineINT( const char * szName, const int iDefault ) const;
	int getCOMBAT_DIE_SIDES();
	int getCOMBAT_DAMAGE();

protected:
	int m_iCOMBAT_DIE_SIDES;
	int m_iCOMBAT_DAMAGE;
/************************************************************************************************/
/* BETTER_BTS_AI_MOD                       END                                                  */
/************************************************************************************************/
};

extern CvGlobals gGlobals;	// for debugging

//
// inlines
//
inline CvGlobals& CvGlobals::getInstance()
{
	return gGlobals;
}


//
// helpers
//
#define GC CvGlobals::getInstance()
#ifndef _USRDLL
#define gDLL GC.getDLLIFaceNonInl()
#else
#define gDLL GC.getDLLIFace()
#endif

#ifndef _USRDLL
#define NUM_DIRECTION_TYPES (GC.getNumDirections())
#define NUM_GAMEOPTION_TYPES (GC.getNumGameOptions())
#define NUM_MPOPTION_TYPES (GC.getNumMPOptions())
#define NUM_SPECIALOPTION_TYPES (GC.getNumSpecialOptions())
#define NUM_GRAPHICOPTION_TYPES (GC.getNumGraphicOptions())
#define NUM_TRADEABLE_ITEMS (GC.getNumTradeableItems())
#define NUM_BASIC_ITEMS (GC.getNumBasicItems())
#define NUM_TRADEABLE_HEADINGS (GC.getNumTradeableHeadings())
#define NUM_COMMAND_TYPES (GC.getNumCommandInfos())
#define NUM_CONTROL_TYPES (GC.getNumControlInfos())
#define NUM_MISSION_TYPES (GC.getNumMissionInfos())
#define NUM_PLAYEROPTION_TYPES (GC.getNumPlayerOptionInfos())
#define MAX_NUM_SYMBOLS (GC.getMaxNumSymbols())
#define NUM_GRAPHICLEVELS (GC.getNumGraphicLevels())
#define NUM_GLOBE_LAYER_TYPES (GC.getNumGlobeLayers())
#endif

#endif
