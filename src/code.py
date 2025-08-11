from __future__ import annotations
from typing import List
import json


class Product:
    """
    Класс, представляющий товар.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Проверка типов
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой")
        if not isinstance(description, str):
            raise TypeError("description должен быть строкой")
        if not isinstance(price, (int, float)):
            raise TypeError("price должен быть числом")
        if price < 0:
            raise ValueError("price не может быть отрицательным")
        if not isinstance(quantity, int):
            raise TypeError("quantity должен быть целым числом")
        if quantity < 0:
            raise ValueError("quantity не может быть отрицательным")

        self.name: str = name
        self.description: str = description
        self.price: float = float(price)
        self.quantity: int = quantity

    def __repr__(self):
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"


class Category:
    """
    Класс, представляющий категорию товаров.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        # Проверка типов
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой")
        if not isinstance(description, str):
            raise TypeError("description должен быть строкой")
        if not isinstance(products, list):
            raise TypeError("products должен быть списком")
        if not all(isinstance(p, Product) for p in products):
            raise TypeError("в products должны быть только объекты класса Product")

        self.name: str = name
        self.description: str = description
        self.products: List[Product] = products

        # обновляем счетчики
        Category.category_count += 1
        Category.product_count += len(products)

    def __repr__(self):
        return f"Category(name={self.name!r}, products={len(self.products)})"


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


if __name__ == "__main__":
    categories = load_categories_from_json("../data/products.json")

    for cat in categories:
        print(cat.name, cat.description)
        for prod in cat.products:
            print("  ", prod.name, "-", prod.price)

    print("Всего категорий:", Category.category_count)
    print("Всего товаров:", Category.product_count)
