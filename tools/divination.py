from typing import Any, Optional, List, Dict
from langchain_core.tools import tool
from .config import config
from .utils.real_random import get_random_numbers
import datetime
import pytz
import sxtwl
import requests


divination_config = config.get("divination", {})

"""
作者：木花开耶姬
梅花易数的三种起卦方式，结果为列表表示，0为阴，1为阳
"""
r"""         तारका तिमिरं दीपो मायावश्याय बुद्बुदम्।
            स्वप्नं च विद्युदभ्रं च एवं द्रष्टव्य संस्कृतम्॥
            तथा प्रकाशयेत्, तेनोच्यते संप्रकाशयेदिति॥
                        _ooOoo_
                       o8888888o
                       88" . "88
                       (| -_- |)
                       O\  =  /O
                    ____/`---'\____
                  .'  \\|     |//  `.
                 /  \\|||  :  |||//  \
                /  _||||| -:- |||||_  \
                |   | \\\  -  /'| |   |
                | \_|  `\`---'//  |_/ |
                \  .-\__ `-. -'__/-.  /
              ___`. .'  /--.--\  `. .'___
           ."" '<  `.___\_<|>_/___.' _> \"".
          | | :  `- \`. ;`. _/; .'/ /  .' ; |
          \  \ `-.   \_\_`. _.'_/_/  -' _.' /
===========`-.`___`-.__\ \___  /__.-'_.'_.-'================
                        `=--=-'    不会画梅花，画个佛祖保佑"""
                        
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
LUNAR_MONTHS_CN = ["正", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
LUNAR_DAYS_CN = ["初一", "初二", "初三", "初四", "初五", "初六", "初七", "初八", "初九", "初十",
                 "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十",
                 "廿一", "廿二", "廿三", "廿四", "廿五", "廿六", "廿七", "廿八", "廿九", "三十", "卅一"]
EIGHT_TRIGRAMS = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
EIGHT_TRIGRAMS_NUM = {"乾": 1, "兑": 2, "离": 3, "震": 4, "巽": 5, "坎": 6, "艮": 7, "坤": 8}
TRIGRAM_BINARY = {
    "坤": [0, 0, 0], "震": [1, 0, 0], "坎": [0, 1, 0], "兑": [1, 1, 0],
    "艮": [0, 0, 1], "巽": [1, 0, 1], "离": [0, 1, 1], "乾": [1, 1, 1]
}
BINARY_TRIGRAM = {tuple(v): k for k, v in TRIGRAM_BINARY.items()}

def getTrigramByNumber(number: int) -> str:
    return EIGHT_TRIGRAMS[number - 1]

def getInteractingGua(originalGuaUpper: str, originalGuaLower: str):
    lines = TRIGRAM_BINARY[originalGuaLower] + TRIGRAM_BINARY[originalGuaUpper]
    lower = lines[1:4]
    upper = lines[2:5]
    return BINARY_TRIGRAM.get(tuple(upper)), BINARY_TRIGRAM.get(tuple(lower))

def _time_based_divination(year_di_zhi_index: int = 0,
                          lm: int = 0,
                          ld: int = 0,
                          lh: int = 0) -> dict:
    """时间法起卦"""
    total_upper = year_di_zhi_index + lm + ld
    upper_num = total_upper % 8 or 8
    total_lower = year_di_zhi_index + lm + ld + lh
    lower_num = total_lower % 8 or 8
    moving_yao = total_lower % 6 or 6
    
    up = getTrigramByNumber(upper_num)
    low = getTrigramByNumber(lower_num)
    
    return _process_divination_result(up, low, moving_yao)

def _number_based_divination(n1: int = 0,
                           n2: int = 0,
                           n3: int = 0) -> dict:
    """数字法起卦"""
    upper_num = (n1 + n2) % 8 or 8
    lower_num = (n1 + n2 + n3) % 8 or 8
    moving_yao = (n1 + n2 + n3) % 6 or 6
    
    up = getTrigramByNumber(upper_num)
    low = getTrigramByNumber(lower_num)
    
    return _process_divination_result(up, low, moving_yao)

def _random_based_divination() -> dict:
    """随机法起卦"""
    random_index_up = get_random_numbers(divination_config.get("random_api_key"), 1, 0, 7) or [0]
    random_index_low = get_random_numbers(divination_config.get("random_api_key"), 1, 0, 7) or [0]
    up = EIGHT_TRIGRAMS[random_index_up[0]]
    low = EIGHT_TRIGRAMS[random_index_low[0]]
    
    random_index_yao = get_random_numbers(divination_config.get("random_api_key"), 1, 1, 6) or [1]
    moving_yao = random_index_yao[0]
    
    result = _process_divination_result(up, low, moving_yao)
    result.update({
        "random_up": random_index_up[0],
        "random_yao": random_index_yao[0]
    })
    return result

def _process_divination_result(up: str, low: str, moving_yao: int) -> dict:
    """处理卦象结果"""
    iUp, iLow = getInteractingGua(up, low)
    original_hex = TRIGRAM_BINARY[low] + TRIGRAM_BINARY[up]
    mutated_hex = list(original_hex)
    mutated_hex[moving_yao - 1] = 1 - mutated_hex[moving_yao - 1]
    bian_low = BINARY_TRIGRAM.get(tuple(mutated_hex[:3]))
    bian_up = BINARY_TRIGRAM.get(tuple(mutated_hex[3:]))
    
    return {
        "本卦": (up, low),
        "互卦": (iUp, iLow),
        "变卦": (bian_up, bian_low),
        "动爻": moving_yao
    }

def meihua_yi_shu(method_type, lunar_year=None, lunar_month=None, lunar_day=None, hour_12=None,
                  num1=None, num2=None, num3=None):
    """梅花易数主函数"""
    if method_type == 1:
        index_ = (lunar_year % 12) if lunar_year else 0
        result = _time_based_divination(index_, lunar_month or 0, lunar_day or 0, hour_12 or 0)
    elif method_type == 2:
        result = _number_based_divination(num1 or 0, num2 or 0, num3 or 0)
    else:
        result = _random_based_divination()

    up, low = result["本卦"]
    iup, ilow = result["互卦"]
    bup, blow = result["变卦"]
    yao = result["动爻"]

    return (0,                              # gua_ben_index
            up + low,                       # ben_gua_name
            0,                              # gua_bian_index
            (bup or "") + (blow or ""),     # bian_gua_name
            0,                              # gua_hu_index
            (iup or "") + (ilow or ""),     # hu_gua_name
            yao,                            # moving_yao
            result.get("random_up"),        # random_up (None if not random method)
            result.get("random_yao"))       # random_yao (None if not random method)

def _get_current_time_info(dt: Optional[datetime.datetime] = None):

    import pytz, datetime
    import sxtwl
    if dt is None:
        tz = pytz.timezone("Asia/Shanghai")
        china_time = datetime.datetime.now(tz)
    else:
        if dt.tzinfo is None:
            tz = pytz.timezone("Asia/Shanghai")
            china_time = tz.localize(dt)
        else:
            china_time = dt

    day = sxtwl.fromSolar(china_time.year, china_time.month, china_time.day)
    lunar_year_sxtwl = day.getLunarYear(False)
    lunar_month = day.getLunarMonth()
    lunar_day = day.getLunarDay()
    lunar_year_cn = str(lunar_year_sxtwl) + "年"
    lunar_month_cn = ('闰' if day.isLunarLeap() else '') + LUNAR_MONTHS_CN[lunar_month - 1] + "月"
    lunar_day_cn = LUNAR_DAYS_CN[lunar_day - 1]
    lunar_time = f"{lunar_year_cn}{lunar_month_cn}{lunar_day_cn}"
    gregorian_time = china_time.strftime('%Y-%m-%d %H:%M:%S')
    yTG = day.getYearGZ()
    mTG = day.getMonthGZ()
    dTG = day.getDayGZ()
    hTG = day.getHourGZ(china_time.hour % 24)
    sizhu_cn = (f"{HEAVENLY_STEMS[yTG.tg]}{EARTHLY_BRANCHES[yTG.dz]}年 "
                f"{HEAVENLY_STEMS[mTG.tg]}{EARTHLY_BRANCHES[mTG.dz]}月 "
                f"{HEAVENLY_STEMS[dTG.tg]}{EARTHLY_BRANCHES[dTG.dz]}日 "
                f"{HEAVENLY_STEMS[hTG.tg]}{EARTHLY_BRANCHES[hTG.dz]}时")
    return lunar_time, gregorian_time, sizhu_cn

@tool(parse_docstring=True)
def divination(query: str,
               datetime_str: Optional[str] = None,
               method: int = 1,
               num1: Optional[int] = None,
               num2: Optional[int] = None,
               num3: Optional[int] = None) -> str:
    """Plum Blossom Numerology Divination, Fortune Telling, and so on

    Args:
        query: Divination content and related information
        datetime_str: Optional datetime string in format 'YYYY-MM-DD HH:MM:SS'
        method: Method of divination (1: time-based, 2: number-based, 3: random)
        num1: First number for number-based divination
        num2: Second number for number-based divination
        num3: Third number for number-based divination
    """
    if datetime_str:
        try:
            dt = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
            china_time = dt if dt.tzinfo else pytz.timezone("Asia/Shanghai").localize(dt)
        except ValueError as e:
            return f"Error: Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS'. Details: {str(e)}"
    else:
        tz = pytz.timezone("Asia/Shanghai")
        china_time = datetime.datetime.now(tz)
    
    if method == 1:
        lunar_info = sxtwl.fromSolar(china_time.year, china_time.month, china_time.day)
        lunar_year = lunar_info.getLunarYear(False)
        lunar_month = lunar_info.getLunarMonth()
        lunar_day = lunar_info.getLunarDay()
        hour_12 = china_time.hour % 12
        hour_12 = 12 if hour_12 == 0 else hour_12
        result = meihua_yi_shu(1, lunar_year=lunar_year, lunar_month=lunar_month, 
                              lunar_day=lunar_day, hour_12=hour_12)
    elif method == 2:
        result = meihua_yi_shu(2, num1=num1, num2=num2, num3=num3)
    else:
        result = meihua_yi_shu(3)

    gua_ben, ben_gua_name, gua_bian, bian_gua_name, gua_hu, hu_gua_name, dong_yao, random_up, random_yao = result
    lunar_time, gregorian_time, sizhu_cn = _get_current_time_info(china_time)

    random_info = "无"
    if method == 3 and random_up is not None and random_yao is not None:
        random_info = f"up={random_up}, yao={random_yao}"

    system_prompt = f"""## 角色设定
你是一位精通梅花易数的资深算卦先生，拥有数十年周易研究经验。
你将参考下面梅花易数分析流程，严谨、专业、细致地为咨询者进行周易预测，并严格遵循参考格式输出，注意先给出详细分析，一步步推算
按照下面信息起卦，下面信息是以及计算好的不管是明天还是今天，如果是随机数取卦则无视时间：
- 起卦方式：{"时间法" if method == 1 else "数字法" if method == 2 else "随机法"}
- 公历时间：{gregorian_time}
- 农历时间：{lunar_time}
- 四柱：{sizhu_cn}
- 本卦：{ben_gua_name}
- 变卦：{bian_gua_name}
- 互卦：{hu_gua_name}
- 动爻：第{dong_yao}爻
- 随机数: {random_info}

## 梅花易数分析流程
### 1. 分析卦象（多维度解读）

1. **五行生克**：

    *   确定体卦和用卦的五行属性（乾兑为金，震巽为木，坎为水，离为火，坤艮为土）。
    *   分析体卦和用卦之间的生克关系。
        *   体克用： 我去克他，可胜，但需耗费精力，主**小吉，但也代表需要付出努力**。
        *   用克体： 他来克我，主**凶险，不利，需谨慎应对**。
        *   体生用： 我去生他，消耗自身能量，主**不吉，损耗，或破财**。
        *   用生体： 他来生我，对我有利，主**吉利，易得帮助，得利益**。
        *   体用比和： 体用五行相同，主**和谐，平衡，事情顺利，吉利**。
    *   五行之间的生克关系是循环的：
        *   相生： 木生火，火生土，土生金，金生水，水生木。
        *   相克： 木克土，土克水，水克火，火克金，金克木。

    
2. **卦辞、爻辞**：

    *   查阅《易经》，参考本卦、变卦的卦辞和爻辞，理解卦象含义。
    *   尤其注意动爻的爻辞。
    *   卦辞是对整个卦象的概括性描述，而爻辞则是对每个爻的具体解释。在分析时，需要将卦辞和爻辞结合起来理解。

3. **体用关系**：

    *   体卦为本体，为事情主体，为自身；用卦为客体，为外部环境，为所测之事。
    *   体卦强弱代表自身状态，用卦强弱代表外在影响。
    *   体卦和用卦的强弱对比也很重要。体卦旺相则自身力量强，体卦衰弱则自身力量弱；用卦旺相则外部环境有利或阻力大，用卦衰弱则外部环境影响小。
    
4. **互卦分析**：

    *   分析互卦，代表事物变化过程中的中间状态。
    *   它提供更深层的信息，有助于了解事物内在发展趋势。
    *   互卦可以理解为事物发展的内部原因或潜藏的趋势。

5. **外应分析**：

    *   记录起卦时周围发生的事情，如声音、方位、物体等。
    *   结合卦象，外应可提供额外信息，辅助判断。
    *   外应是梅花易数的一大特色，也是其灵活性的体现。外应的种类繁多，需要根据具体情况进行分析。

6. **时间分析**：

    *   结合卦象分析事情可能发生的时间，可能对应五行生克，也可能结合卦象中的数字。
    *   **时间分析可以结合多种方法：**
        *   **五行属性：** 例如震巽卦对应春季、寅卯辰月日，离卦对应夏季、巳午未月日等。
        *   **卦的数字：** 例如用先天八卦数，上卦数加下卦数，或用卦数等，来推测时间。
        *   **卦气旺衰：** 根据卦气的旺衰来判断时间的远近。
        *   **卦象：** 例如，离和震可以表示快速，艮和坤可以表示缓慢。

### 2. 判断吉凶（综合考量）

判断吉凶是整个预测过程的最终目的，需要综合考虑以上所有因素，并结合实际情况进行判断。

1. **综合分析**：

    *   综合以上所有分析，从五行、卦象、爻辞、体用关系等多个角度分析。
    *   把握整体的吉凶导向。

2. **给出建议**：

    *   根据卦象结果，给出合理建议，帮助解决问题或做出决策。
    *   提示需要注意的事项，以及可行的行动方向。


## 输出格式参考
```json
详细给出推理流程，并按下面格式输出结
  "提问": "关于事业发展的一个预测",
  "起卦方式": "时间法",
  "日期": "农历九月初九",
    "时辰": "亥时",
  "本卦": "地天泰(☷☰)",
  "变卦": "地雷复(☷☳)",
  "互卦": "雷泽归妹(☳☱)",
  "体卦": "坤(☷)",
  "用卦": "乾(☰)",
    "外应": "听到汽车鸣笛",
  "五行关系": "土生金",
  "动爻": "第六爻",
  "分析": "初期比较稳定，有利。但动爻显示后期会有变化，需要注意调整。汽车鸣笛提示事情可能会有快速的推动。",
  "卦辞分析": "泰卦表示平安顺利，复卦代表反复，归妹提示可能需要通过合作来解决。",
    "互卦分析":"互卦预示着发展中期可能有调整和变动",
  "吉凶判断": "短期内吉利，长期则需要关注变化，审时度势。",
  "时间应期": "变化可能发生在木或震卦所代表的时间，如寅卯辰月或日",
  "建议": "初期可以积极发展，长期需要警惕变化，灵活调整策略。可考虑通过合作来促进发展。"
```"""
    
    
    payload = {
        "model": divination_config.get("model"),
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        "temperature": 0,
        "max_tokens": 4096,
        "top_p": 1,
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {divination_config.get('openai_api_key')}"
    }
    url = f"{divination_config.get('openai_base_url')}/chat/completions"

    try:
        r = requests.post(url, json=payload, headers=headers)
        r.raise_for_status()
        resp_json = r.json()
        response_text = resp_json["choices"][0]["message"]["content"]
    except Exception as e:
        response_text = f"Error calling API: {e}"

    return response_text


tools = [divination]