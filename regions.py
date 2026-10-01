"""Canonical overseas-entity regions."""

REGIONS = [
    ("동북아시아", "Northeast Asia"),
    ("동남아시아", "Southeast Asia"),
    ("서남아시아", "Southwest Asia"),
    ("아메리카", "Americas"),
    ("오세아니아", "Oceania"),
    ("유럽", "Europe"),
]

KO_TO_EN = {ko: en for ko, en in REGIONS}
EN_TO_KO = {en.lower(): ko for ko, en in REGIONS}

ALIASES = {
    "미주": "아메리카",
    "동남아": "동남아시아",
    "중국": "동북아시아",
    "인도": "서남아시아",
    "중동아프리카": "서남아시아",
    "중동": "서남아시아",
    "일본": "동북아시아",
    "일본·오세아니아": "동북아시아",
    "일본.오세아니아": "동북아시아",
    "asean": "동남아시아",
    "china": "동북아시아",
    "india": "서남아시아",
    "mea": "서남아시아",
    "middle east": "서남아시아",
    "americas": "아메리카",
    "america": "아메리카",
    "europe": "유럽",
    "oceania": "오세아니아",
    "northeast asia": "동북아시아",
    "southeast asia": "동남아시아",
    "southwest asia": "서남아시아",
    "south west asia": "서남아시아",
    "japan & oceania": "동북아시아",
    "japan and oceania": "동북아시아",
}

COUNTRY_TO_REGION = {
    "china": "동북아시아",
    "japan": "동북아시아",
    "taiwan": "동북아시아",
    "hong kong": "동북아시아",
    "중국": "동북아시아",
    "일본": "동북아시아",
    "대만": "동북아시아",
    "홍콩": "동북아시아",
    "vietnam": "동남아시아",
    "indonesia": "동남아시아",
    "thailand": "동남아시아",
    "malaysia": "동남아시아",
    "myanmar": "동남아시아",
    "philippines": "동남아시아",
    "singapore": "동남아시아",
    "cambodia": "동남아시아",
    "베트남": "동남아시아",
    "인도네시아": "동남아시아",
    "태국": "동남아시아",
    "말레이시아": "동남아시아",
    "미얀마": "동남아시아",
    "필리핀": "동남아시아",
    "싱가포르": "동남아시아",
    "캄보디아": "동남아시아",
    "india": "서남아시아",
    "uae": "서남아시아",
    "saudi arabia": "서남아시아",
    "kuwait": "서남아시아",
    "egypt": "서남아시아",
    "south africa": "서남아시아",
    "morocco": "서남아시아",
    "인도": "서남아시아",
    "사우디": "서남아시아",
    "쿠웨이트": "서남아시아",
    "이집트": "서남아시아",
    "남아공": "서남아시아",
    "모로코": "서남아시아",
    "usa": "아메리카",
    "mexico": "아메리카",
    "brazil": "아메리카",
    "argentina": "아메리카",
    "canada": "아메리카",
    "peru": "아메리카",
    "chile": "아메리카",
    "미국": "아메리카",
    "멕시코": "아메리카",
    "브라질": "아메리카",
    "아르헨티나": "아메리카",
    "캐나다": "아메리카",
    "페루": "아메리카",
    "칠레": "아메리카",
    "australia": "오세아니아",
    "호주": "오세아니아",
    "poland": "유럽",
    "turkiye": "유럽",
    "turkey": "유럽",
    "germany": "유럽",
    "united kingdom": "유럽",
    "italy": "유럽",
    "spain": "유럽",
    "france": "유럽",
    "netherlands": "유럽",
    "czechia": "유럽",
    "hungary": "유럽",
    "폴란드": "유럽",
    "튀르키예": "유럽",
    "독일": "유럽",
    "영국": "유럽",
    "이탈리아": "유럽",
    "스페인": "유럽",
    "프랑스": "유럽",
    "네덜란드": "유럽",
    "체코": "유럽",
    "헝가리": "유럽",
}


def resolve_region(*values, country="", country_en=""):
    for raw in values:
        text = str(raw or "").strip()
        if not text:
            continue
        if text in KO_TO_EN:
            return text, KO_TO_EN[text]
        key = text.lower()
        if key in EN_TO_KO:
            ko = EN_TO_KO[key]
            return ko, KO_TO_EN[ko]
    for raw in (country_en, country):
        key = str(raw or "").strip().lower()
        if key in COUNTRY_TO_REGION:
            ko = COUNTRY_TO_REGION[key]
            return ko, KO_TO_EN[ko]
    for raw in values:
        text = str(raw or "").strip()
        if not text:
            continue
        alias = ALIASES.get(text) or ALIASES.get(text.lower())
        if alias:
            return alias, KO_TO_EN[alias]
    return "", ""


def apply_region(sub):
    ko, en = resolve_region(sub.region, sub.region_en, country=sub.country, country_en=sub.country_en)
    if ko:
        sub.region = ko
        sub.region_en = en
    return ko
