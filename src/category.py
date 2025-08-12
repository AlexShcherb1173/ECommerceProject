from __future__ import annotations

from typing import List

from src.product import Product


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

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products={len(self.products)})"
