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
# Product.__str__ — теперь возвращает "Название, X руб. Остаток: Y шт.".
# Product.__add__ — реализовано сложение стоимости товаров на складе.
# Создадим два новых класса Smartphone и LawnGrass, наследников от Product.
# В __add__ добавим проверку type(self) is type(other) — это гарантирует, что смартфон не сложится с травой.

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

    def __str__(self) -> str:
        return f"{self.name}, {self.__price} руб. Остаток: {self.quantity} шт."

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

        # обновляем цену как при повышении, так и при снижении после подтверждения
        self.__price = float(new_price)

    def __add__(self, other: Product) -> float:
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только с другим Product")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, Any], products_list: List[Product]) -> Product:
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        for existing_product in products_list:
            if existing_product.name == name:  # можно добавить .lower() для игнорирования регистра
                existing_product.quantity += quantity
                existing_product.price = price  # сеттер сам спросит или обновит
                return existing_product

        new_prod = cls(name, description, price, quantity)
        products_list.append(new_prod)
        return new_prod


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        if not isinstance(efficiency, (int, float)):
            raise TypeError("efficiency должен быть числом")
        if not isinstance(model, str):
            raise TypeError("model должен быть строкой")
        if not isinstance(memory, int):
            raise TypeError("memory должен быть целым числом")
        if not isinstance(color, str):
            raise TypeError("color должен быть строкой")

        self.efficiency = float(efficiency)
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other: Product) -> float:
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return super().__add__(other)


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        if not isinstance(country, str):
            raise TypeError("country должен быть строкой")
        if not isinstance(germination_period, str):
            raise TypeError("germination_period должен быть строкой")
        if not isinstance(color, str):
            raise TypeError("color должен быть строкой")

        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other: Product) -> float:
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return super().__add__(other)
