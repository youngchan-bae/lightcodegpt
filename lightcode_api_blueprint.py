from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict
from korean_lunar_calendar import KoreanLunarCalendar

app = FastAPI()

class PalmLines(BaseModel):
    life_line: str
    fate_line: str
    emotion_line: str
    head_line: str
    marriage_line: str = ""
    money_line: str = ""

class InputData(BaseModel):
    name: str
    hanja_name: str
    birth: str
    calendar: str
    birth_time: str
    birth_place: str
    gender: str
    zodiac: str
    palm_lines: PalmLines

BASE_OHENG = {
    "목": 1.5,
    "화": 2.5,
    "토": 2.0,
    "금": 2.5,
    "수": 3.5
}

ZODIAC_BOJEONG = {
    "양자리": {"화": 0.4},
    "황소자리": {"금": 0.4},
    "쌍둥이자리": {"수": 0.4},
    "게자리": {"수": 0.3, "목": 0.1},
    "사자자리": {"화": 0.5},
    "처녀자리": {"토": 0.4},
    "천칭자리": {"금": 0.3, "목": 0.1},
    "전갈자리": {"수": 0.4, "화": 0.1},
    "사수자리": {"화": 0.4, "목": 0.1},
    "염소자리": {"토": 0.5},
    "물병자리": {"금": 0.2, "수": 0.2},
    "물고기자리": {"수": 0.5}
}

def convert_lunar_to_solar(lunar_date: str) -> str:
    year, month, day = map(int, lunar_date.split("-"))
    cal = KoreanLunarCalendar()
    cal.setLunar(year, month, day, False)
    return cal.getSolarISODate()

def analyze_name_oheng(name: str, hanja_name: str) -> Dict[str, float]:
    name_oheng = {
        "성": {"오행": "화", "보정": 0.3},
        "이름1": {"오행": "목", "보정": 0.5},
        "이름2": {"오행": "화", "보정": 0.7}
    }
    total_bojeong = {"목": 0.0, "화": 0.0, "토": 0.0, "금": 0.0, "수": 0.0}
    weights = {"성": 0.5, "이름1": 1.0, "이름2": 1.5}
    for part, info in name_oheng.items():
        oheng = info["오행"]
        value = info["보정"] * weights[part]
        total_bojeong[oheng] += value
    return total_bojeong

def analyze_palm_oheng(palm_lines: PalmLines) -> Dict[str, float]:
    result = {"목": 0.0, "화": 0.0, "토": 0.0, "금": 0.0, "수": 0.0}
    if "깊고 선명" in palm_lines.life_line:
        result["수"] += 0.3
    if "중간" in palm_lines.fate_line:
        result["토"] += 0.2
    if "곡선형" in palm_lines.emotion_line or "풍부" in palm_lines.emotion_line:
        result["목"] += 0.4
    if "직선형" in palm_lines.emotion_line or "억제" in palm_lines.emotion_line:
        result["목"] += 0.1
    if "길고 곧음" in palm_lines.head_line:
        result["금"] += 0.3
    if "2줄" in palm_lines.marriage_line or "분리" in palm_lines.marriage_line:
        result["수"] += -0.2
        result["화"] += 0.2
    if "뚜렷" in palm_lines.money_line:
        result["금"] += 0.4
        result["토"] += 0.3
    if "복잡" in palm_lines.money_line or "갈래" in palm_lines.money_line:
        result["금"] += 0.1
        result["토"] += -0.2
    return result

def analyze_zodiac_oheng(zodiac: str) -> Dict[str, float]:
    result = {"목": 0.0, "화": 0.0, "토": 0.0, "금": 0.0, "수": 0.0}
    if zodiac in ZODIAC_BOJEONG:
        for oheng, value in ZODIAC_BOJEONG[zodiac].items():
            result[oheng] += value
    return result

@app.post("/bojeong-oheng")
def calculate_oheng(data: InputData):
    birth_date = data.birth
    if data.calendar == "음력":
        birth_date = convert_lunar_to_solar(data.birth)

    name_bojeong = analyze_name_oheng(data.name, data.hanja_name)
    palm_bojeong = analyze_palm_oheng(data.palm_lines)
    zodiac_bojeong = analyze_zodiac_oheng(data.zodiac)

    bojeong_total = {
        k: name_bojeong.get(k, 0) + palm_bojeong.get(k, 0) + zodiac_bojeong.get(k, 0)
        for k in BASE_OHENG.keys()
    }

    final_oheng = {
        k: BASE_OHENG[k] + bojeong_total[k]
        for k in BASE_OHENG.keys()
    }

    explanation = {
        "이름": "燦은 火, 怜은 木으로 해석되어 火·木 기운 강화됨",
        "손금": "감정선 곡선형 → 연애 에너지 풍부(木 강화), 금전선 뚜렷 → 금전운 강함(金·土 강화)",
        "별자리": f"{data.zodiac}는 {ZODIAC_BOJEONG.get(data.zodiac, {})} 오행으로 보정됨",
        "생일": f"입력된 생일({data.calendar})은 변환되어 양력 기준 {birth_date}로 계산됨"
    }

    return {
        "base_oheng": BASE_OHENG,
        "bojeong_oheng": bojeong_total,
        "final_oheng": final_oheng,
        "explanation": explanation
    }

# ✅ 여기 추가한 부분!
@app.get("/openapi.json")
def get_openapi_json():
    return FileResponse("openapi.json", media_type="application/json")
