from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from src.product import Product, ZeroQuantityError


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
        try:
            if product.quantity == 0:
                raise ZeroQuantityError("Нельзя добавить товар с нулевым количеством")
            self.__products.append(product)
        except ZeroQuantityError as e:
            print(f"[ERROR] {e}")
        else:
            print(f"[INFO] Товар '{product.name}' добавлен в категорию '{self.name}'")
            Category.product_count += 1
        finally:
            print("[INFO] Обработка добавления товара завершена")

    def get_products(self) -> List[Product]:
        """Возвращает копию списка товаров (чтение без возможности изменить напрямую)."""
        return list(self.__products)

    def average_price(self) -> float:
        """Возвращает среднюю цену товаров в категории. Если товаров нет — возвращает 0 (обработка деления на ноль)."""
        try:
            total_price = sum(p.price for p in self.__products)
            count = len(self.__products)
            return total_price / count
        except ZeroDivisionError:
            return 0

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
            if not isinstance(quantity, int) or quantity < 0:
                raise ValueError("Количество товара в заказе должно быть целым числом")
            try:
                if quantity == 0:
                    raise ZeroQuantityError("Нельзя заказать нулевое количество товара")
                if quantity > product.quantity:
                    raise ValueError("Недостаточно товара на складе для заказа")

                self.product = product
                self.quantity = quantity
                self._total_price = product.price * quantity
                self.product.quantity -= quantity

            except ZeroQuantityError as e:
                print(f"[ERROR] {e}")
                raise
            else:
                print(f"[INFO] Заказ на товар '{product.name}' успешно создан")
            finally:
                print("[INFO] Обработка заказа завершена")

            # self.product = product
            # self.quantity = quantity
            # self._total_price = product.price * quantity
            #
            # # уменьшаем количество товара на складе
            # self.product.quantity -= quantity

        def total_quantity(self) -> int:
            return self.quantity

        def total_price(self) -> float:
            return self._total_price

        def __repr__(self) -> str:
            return f"Order(product={self.product.name!r}, quantity={self.quantity}, total_price={self._total_price})"

        def __str__(self) -> str:
            return f"Заказ: {self.product.name}, количество: {self.quantity}, сумма: {self._total_price} руб."

        class Order(BaseItem):
            def __init__(self, product: Product, quantity: int):
                try:
                    if quantity == 0:
                        raise ZeroQuantityError("Нельзя заказать нулевое количество товара")
                    if quantity > product.quantity:
                        raise ValueError("Недостаточно товара на складе для заказа")

                    self.product = product
                    self.quantity = quantity
                    self._total_price = product.price * quantity
                    self.product.quantity -= quantity

                except ZeroQuantityError as e:
                    print(f"[ERROR] {e}")
                    raise
                else:
                    print(f"[INFO] Заказ на товар '{product.name}' успешно создан")
                finally:
                    print("[INFO] Обработка заказа завершена")
