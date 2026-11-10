import requests, json

_cache = {}

def SearchSteam(term):
    responce = requests.get(
        "https://store.steampowered.com/api/storesearch/",
        params={"term": term, "cc": "pl", "l": "polish"},
        timeout=10,
    )
    responce.raise_for_status()
    data = responce.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "steam_appid": item["id"],
            "tytul": item["name"],
            "image": item.get("tiny_image"),
        })
    return results

def GetSteamDetails(appId):
    if appId in _cache:
        return _cache[appId]
    
    resp = requests.get(
        "https://store.steampowered.com/api/appdetails",
        params={"appids": appId, "cc": "pl", "l": "polish"},
        timeout=10,
    )
    resp.raise_for_status()
    data = resp.json()[str(appId)].get("data", {})

    summary = {}
    try:
        resp = requests.get(
            "https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/",
            params={"input_json": json.dumps({
                "appid": appId,
                "languages": ["all"],
                "num_per_page": 1,
                "review_type": 0,
                "purchase_type": 1,
            })},
            timeout=10,
        )
        resp.raise_for_status()
        summary = resp.json().get("response", {}).get("query_summary", {})
    except Exception as e:
        print("BLAD RECENZJI:", repr(e))

    wynik = {
        "opis": data.get("short_description"),
        "metacritic": data.get("metacritic", {}).get("score"),
        "steam_ocena": summary.get("review_score_desc"),
        "pozytywne": summary.get("total_positive"),
        "negatywne": summary.get("total_negative"),
    }
    if summary:
        _cache[appId] = wynik
    return wynik
