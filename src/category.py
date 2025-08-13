# Перепишем твой класс Category так, чтобы:
# список товаров стал приватным (self.__products);
# доступ к нему напрямую снаружи был невозможен;
# был метод add_product() для добавления объекта Product;
# при добавлении продукта увеличивался счётчик product_count.
# Что изменилось:
# self.__products — теперь приватный атрибут.
# Добавлен метод add_product() — безопасно добавляет продукт.
# Добавлен метод get_products() — позволяет получить копию списка товаров, но не менять его напрямую.
# Логика подсчёта product_count осталась, но теперь инкремент происходит и при добавлении через add_product().

from __future__ import annotations

from typing import List

from src.product import Product


class Category:
    """Класс, представляющий категорию товаров."""

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
        self.__products: List[Product] = products  # приватный список товаров

        # обновляем счетчики
        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию и увеличивает счетчик продуктов."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавить только объект класса Product")

        self.__products.append(product)
        Category.product_count += 1

    def get_products(self) -> List[Product]:
        """Возвращает копию списка товаров (чтение без возможности изменить напрямую)."""
        return list(self.__products)

    @property
    def products(self) -> str:
        """Возвращает строку со списком всех продуктов"""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products={len(self.__products)})"
