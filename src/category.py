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
# Category.products — вместо ручной сборки строки просто использует str(product) для каждого товара.
# Category.__str__ — считает общее количество всех единиц товара (quantity) и выводит "Название категории,
# количество продуктов: X шт.".

from __future__ import annotations

from typing import List

from src.product import Product


class Category:
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0  # общий счетчик всех продуктов всех категорий

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
        """Возвращает строку со списком всех продуктов, используя __str__ каждого продукта."""
        return "\n".join(str(p) for p in self.__products) + ("\n" if self.__products else "")

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products={len(self.__products)})"

    def __str__(self) -> str:
        """Возвращает строку: Название категории, количество продуктов на складе: X шт."""
        total_quantity = sum(p.quantity for p in self.__products)
        return f"{self.name}, количество продуктов на складе: {total_quantity} шт."
