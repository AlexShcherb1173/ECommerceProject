from __future__ import annotations


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

    def __repr__(self) -> str:
        return f"Product(name={self.name!r}, price={self.price}, quantity={self.quantity})"
