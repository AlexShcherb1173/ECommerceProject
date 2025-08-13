# Класс-метод new_product, который:
# Принимает словарь с параметрами товара.
# Создает объект Product через конструктор __init__.
# Проверяет, нет ли товара с таким же name в переданном списке товаров.
# Если есть:
# увеличивает quantity существующего товара,
# выбирает более высокую цену.
# Возвращает созданный объект (или обновленный существующий).

from __future__ import annotations
from typing import List, Dict, Any

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

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"

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

        # Проверка на дубликат
        for existing_product in products_list:
            if existing_product.name == name:
                # Обновляем количество
                existing_product.quantity += quantity
                # Устанавливаем более высокую цену
                if price > existing_product.price:
                    existing_product.price = price
                return existing_product  # возвращаем обновленный товар

        # Если дубликат не найден, создаем новый
        new_prod = cls(name, description, price, quantity)
        products_list.append(new_prod)
        return new_prod
