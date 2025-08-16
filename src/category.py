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

from abc import ABC, abstractmethod
from typing import List

from src.product import Product


class BaseItem(ABC):
    @abstractmethod
    def total_quantity(self) -> int:
        """Возвращает общее количество товаров"""
        pass

    @abstractmethod
    def total_price(self) -> float:
        """Возвращает общую стоимость товаров"""
        pass


class Category(BaseItem):
    """Класс, представляющий категорию товаров."""

    category_count: int = 0
    product_count: int = 0  # общий счетчик всех продуктов всех категорий
    __products: List[Product]  # <— добавили явную аннотацию

    def __init__(self, name: str, description: str, products: List[Product]):
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой")
        if not isinstance(description, str):
            raise TypeError("description должен быть строкой")
        if not isinstance(products, list) or not all(isinstance(p, Product) for p in products):
            raise TypeError("products должны быть Product или их наследниками")

        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = products  # приватный список товаров

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию и увеличивает счетчик продуктов."""
        if not isinstance(product, Product):
            raise TypeError("Можно добавить только Product или наследников")
        self.__products.append(product)
        Category.product_count += 1

    def get_products(self) -> List[Product]:
        """Возвращает копию списка товаров (чтение без возможности изменить напрямую)."""
        return list(self.__products)

    @property
    def products(self) -> str:
        """Возвращает строку со списком всех продуктов, используя __str__ каждого продукта."""
        return "\n".join(str(p) for p in self.__products) + ("\n" if self.__products else "")

    def total_quantity(self) -> int:
        return sum(p.quantity for p in self.__products)

    def total_price(self) -> float:
        return sum(p.price * p.quantity for p in self.__products)

    def __repr__(self) -> str:
        return f"Category(name={self.name!r}, products={len(self.__products)})"

    def __str__(self) -> str:
        """Возвращает строку: Название категории, количество продуктов на складе: X шт."""
        return f"{self.name}, количество продуктов на складе: {self.total_quantity()} шт."

    class Order(BaseItem):
        def __init__(self, product: Product, quantity: int):
            if not isinstance(product, Product):
                raise TypeError("В заказе может быть указан только объект Product или его наследник")
            if not isinstance(quantity, int) or quantity <= 0:
                raise ValueError("Количество товара в заказе должно быть положительным целым числом")
            if quantity > product.quantity:
                raise ValueError("Недостаточно товара на складе для заказа")

            self.product = product
            self.quantity = quantity
            self._total_price = product.price * quantity

            # уменьшаем количество товара на складе
            self.product.quantity -= quantity

        def total_quantity(self) -> int:
            return self.quantity

        def total_price(self) -> float:
            return self._total_price

        def __repr__(self) -> str:
            return f"Order(product={self.product.name!r}, quantity={self.quantity}, total_price={self._total_price})"

        def __str__(self) -> str:
            return f"Заказ: {self.product.name}, количество: {self.quantity}, сумма: {self._total_price} руб."
