import requests
from my_token import TOKEN

def fetch_category_ids():
    url = "https://api.lzt.market/category"
    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    categories = []
    for category in data.get("categories", []):
        category_info = {
            "category_id": category["category_id"],
            "category_title": category.get("category_title", ""),
            "category_name": category.get("category_name", ""),
            "category_url": category.get("category_url", "")
        }
        categories.append(category_info)

    return categories
