# from __future__ import annotations
# from src.loading import load_categories_from_json
# from src.category import Category
#
#
# if __name__ == "__main__":
#     categories = load_categories_from_json("data/products.json")
#
#     for cat in categories:
#         print(cat.name, cat.description)
#         for prod in cat.products:
#             print("  ", prod.name, "-", prod.price)
#
#     print("Всего категорий:", Category.category_count)
#     print("Всего товаров:", Category.product_count)

from typing import List
from src.category import Category
from src.product import Product


p1 = Product("Яблоко", "Красное яблоко", 80, 15)
p2 = Product("Банан", "Желтый банан", 50, 20)

category = Category("Фрукты", "Свежие фрукты", [p1, p2])

print(category.products)

products = [
    Product("Яблоко", "Красное яблоко", 80, 15)
]

# Создаем новый товар через класс-метод
new_data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 85, "quantity": 10}
Product.new_product(new_data, products)

# Создаем новый товар, которого нет
banana_data = {"name": "Банан", "description": "Желтый банан", "price": 50, "quantity": 20}
Product.new_product(banana_data, products)

print(products)