# Класс-метод new_product, который:
# Принимает словарь с параметрами товара.
# Создает объект Product через конструктор __init__.
# Проверяет, нет ли товара с таким же name в переданном списке товаров.
# Если есть:
# увеличивает quantity существующего товара,
# выбирает более высокую цену.
# Возвращает созданный объект (или обновленный существующий).
# Цена приватная (__price), а доступ к ней реализован через @property и @price.setter с проверками:
# Запрет на ноль и отрицательные значения с выводом "Цена не должна быть нулевая или отрицательная".
# Если цена понижается — спрашивать у пользователя подтверждение через input("...").

from __future__ import annotations

from typing import Any, Dict, List


class Product:
    """Класс, представляющий товар."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Проверка типов
        if not isinstance(name, str):
            raise TypeError("name должен быть строкой")
        if not isinstance(description, str):
            raise TypeError("description должен быть строкой")
        if not isinstance(price, (int, float)):
            raise TypeError("price должен быть числом")
        if price <= 0:
            raise ValueError("price не может быть нулевым или отрицательным")
        if not isinstance(quantity, int):
            raise TypeError("quantity должен быть целым числом")
        if quantity < 0:
            raise ValueError("quantity не может быть отрицательным")

        self.name: str = name
        self.description: str = description
        self.__price: float = float(price)  # приватный атрибут
        self.quantity: int = quantity

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.__price}, quantity={self.quantity})"

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута __price"""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для приватного атрибута __price"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirm = input(f"Цена снижается с {self.__price} до {new_price}. Подтвердите (y/n): ").strip().lower()
            if confirm != "y":
                print("Изменение цены отменено")
                return

        self.__price = float(new_price)

    @classmethod
    def new_product(cls, product_data: Dict[str, Any], products_list: List[Product]) -> Product:
        """
        Создает новый продукт из словаря.
        Если продукт с таким именем уже есть — обновляет количество и цену.
        """
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        for existing_product in products_list:
            if existing_product.name == name:
                existing_product.quantity += quantity
                if price > existing_product.price:
                    existing_product.price = price
                return existing_product

        new_prod = cls(name, description, price, quantity)
        products_list.append(new_prod)
        return new_prod
