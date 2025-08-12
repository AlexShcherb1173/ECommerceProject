from __future__ import annotations
from src.loading import load_categories_from_json
from src.category import Category


if __name__ == "__main__":
    categories = load_categories_from_json("data/products.json")

    for cat in categories:
        print(cat.name, cat.description)
        for prod in cat.products:
            print("  ", prod.name, "-", prod.price)

    print("Всего категорий:", Category.category_count)
    print("Всего товаров:", Category.product_count)
