from __future__ import annotations

import json
from typing import List

from src.category import Category
from src.product import Product


def load_categories_from_json(file_path: str) -> List[Category]:
    """
    Загружает категории и товары из JSON-файла.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    categories: List[Category] = []
    for cat in data:
        products = [Product(p["name"], p["description"], p["price"], p["quantity"]) for p in cat["products"]]
        categories.append(Category(cat["name"], cat["description"], products))

    return categories
