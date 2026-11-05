import requests

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
            "title": item["name"],
            "image": item.get("tiny_image"),
        })
    return results