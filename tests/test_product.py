# Что проверяют тесты:
# test_add_new_product — добавление нового товара в пустой список.
# test_update_existing_product_quantity_and_price — увеличение количества и выбор более высокой цены.
# test_update_existing_product_lower_price_keeps_old — цена не меняется, если новая ниже.
# test_add_multiple_products — можно добавить несколько разных товаров.
# test_set_price_positive_increase — повышение цены всегда проходит.
# test_set_price_zero_or_negative — цена не меняется, если ≤ 0, и выводится сообщение.
# test_price_decrease_confirm_yes — при понижении цены и ответе y цена меняется.
# test_price_decrease_confirm_no — при ответе n цена остаётся прежней и выводится предупреждение.

from typing import List
from unittest.mock import patch

import pytest

from src.product import Product


def test_product_valid_initialization() -> None:
    p = Product("Test", "Description", 100.0, 10)
    assert p.name == "Test"
    assert p.description == "Description"
    assert p.price == 100.0
    assert p.quantity == 10


@pytest.mark.parametrize("name", [123, None, 45.6])
def test_product_invalid_name_type(name: str) -> None:
    with pytest.raises(TypeError):
        Product(name, "Desc", 100.0, 1)


@pytest.mark.parametrize("desc", [123, None, ["list"]])
def test_product_invalid_description_type(desc: str) -> None:
    with pytest.raises(TypeError):
        Product("Name", desc, 100.0, 1)


@pytest.mark.parametrize("price", ["100", None, []])
def test_product_invalid_price_type(price: str) -> None:
    with pytest.raises(TypeError):
        Product("Name", "Desc", price, 1)  # type: ignore[arg-type]


def test_product_negative_price() -> None:
    with pytest.raises(ValueError):
        Product("Name", "Desc", -50.0, 1)


@pytest.mark.parametrize("quantity", ["5", 3.5, None])
def test_product_invalid_quantity_type(quantity: str) -> None:
    with pytest.raises(TypeError):
        Product("Name", "Desc", 100.0, quantity)  # type: ignore[arg-type]


def test_product_negative_quantity() -> None:
    with pytest.raises(ValueError):
        Product("Name", "Desc", 100.0, -1)


def test_add_new_product() -> None:
    products: List[Product] = []
    data = {"name": "Яблоко", "description": "Красное яблоко", "price": 80, "quantity": 15}

    product = Product.new_product(data, products)

    assert len(products) == 1
    assert product.name == "Яблоко"
    assert product.price == 80
    assert product.quantity == 15


def test_update_existing_product_quantity_and_price() -> None:
    products = [Product("Яблоко", "Красное яблоко", 80, 15)]
    data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 85, "quantity": 10}

    updated_product = Product.new_product(data, products)

    assert len(products) == 1  # не создается новый объект
    assert updated_product.quantity == 25  # количество сложено
    assert updated_product.price == 85  # цена обновлена на более высокую


def test_update_existing_product_lower_price_keeps_old(monkeypatch: pytest.MonkeyPatch) -> None:
    products = [Product("Яблоко", "Красное яблоко", 80, 15)]
    data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 70, "quantity": 5}

    # Автоматически подтверждаем отказ (n)
    monkeypatch.setattr("builtins.input", lambda _: "n")
    updated_product = Product.new_product(data, products)

    # количество увеличилось
    assert updated_product.quantity == 20
    # цена осталась прежней
    assert updated_product.price == 80


def test_add_multiple_products() -> None:
    products: List[Product] = []

    data1 = {"name": "Яблоко", "description": "Красное яблоко", "price": 80, "quantity": 15}
    data2 = {"name": "Банан", "description": "Желтый банан", "price": 50, "quantity": 20}

    Product.new_product(data1, products)
    Product.new_product(data2, products)

    assert len(products) == 2
    assert products[0].name == "Яблоко"
    assert products[1].name == "Банан"


def test_set_price_positive_increase() -> None:
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    p.price = 100  # повышаем цену
    assert p.price == 100


def test_set_price_zero_or_negative(capsys: "pytest.CaptureFixture[str]") -> None:
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    p.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 80  # цена не изменилась

    p.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 80


def test_price_decrease_confirm_yes() -> None:
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    with patch("builtins.input", return_value="y"):
        p.price = 70  # согласие на понижение
    assert p.price == 70


def test_price_decrease_confirm_no(capsys: "pytest.CaptureFixture[str]") -> None:
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    with patch("builtins.input", return_value="n"):
        p.price = 70  # отказ от понижения
    captured = capsys.readouterr()
    assert "Изменение цены отменено" in captured.out
    assert p.price == 80  # цена не изменилась


def test_product_init_valid() -> None:
    p = Product("Test", "Desc", 100.0, 5)
    assert p.name == "Test"
    assert p.description == "Desc"
    assert p.price == 100.0
    assert p.quantity == 5


@pytest.mark.parametrize(
    "name, description, price, quantity, exc_type",
    [
        (123, "desc", 100.0, 1, TypeError),
        ("Name", 123, 100.0, 1, TypeError),
        ("Name", "Desc", "price", 1, TypeError),
        ("Name", "Desc", -5, 1, ValueError),
        ("Name", "Desc", 0, 1, ValueError),
        ("Name", "Desc", 100.0, 1.5, TypeError),
        ("Name", "Desc", 100.0, -1, ValueError),
    ],
)
def test_product_init_invalid(
    name: str,
    description: str,
    price: float,
    quantity: int,
    exc_type: type,
) -> None:
    with pytest.raises(exc_type):
        Product(name, description, price, quantity)


def test_product_str() -> None:
    p = Product("Test", "Desc", 100.0, 5)
    assert str(p) == "Test, 100.0 руб. Остаток: 5 шт."


def test_product_repr() -> None:
    p = Product("Test", "Desc", 100.0, 5)
    assert repr(p) == "Product(name='Test', price=100.0, quantity=5)"


def test_price_setter_input_scenarios(monkeypatch: pytest.MonkeyPatch, capsys: "pytest.CaptureFixture[str]") -> None:
    p = Product("Test", "Desc", 100.0, 5)

    # цена <= 0
    p.price = -1
    captured = capsys.readouterr()
    assert "не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 100.0

    # снижение цены, отказ
    monkeypatch.setattr("builtins.input", lambda _: "n")
    p.price = 50
    captured = capsys.readouterr()
    assert "Изменение цены отменено" in captured.out
    assert p.price == 100.0

    # снижение цены, согласие
    monkeypatch.setattr("builtins.input", lambda _: "y")
    p.price = 50
    assert p.price == 50.0


def test_product_add() -> None:
    p1 = Product("A", "Desc", 100, 10)
    p2 = Product("B", "Desc", 200, 2)
    assert p1 + p2 == 1400  # 100×10 + 200×2


def test_new_product_creates() -> None:
    products: list[Product] = []
    data = {"name": "Test", "description": "Desc", "price": 100, "quantity": 5}
    p = Product.new_product(data, products)
    assert len(products) == 1
    assert p.name == "Test"


def test_new_product_updates_existing(monkeypatch: pytest.MonkeyPatch) -> None:
    products = [Product("Test", "Desc", 100, 5)]
    data = {"name": "Test", "description": "Desc", "price": 200, "quantity": 3}

    # цена выше — обновляется без вопросов
    updated = Product.new_product(data, products)
    assert updated.quantity == 8
    assert updated.price == 200

    # цена ниже — подтверждаем через mock
    data_lower_price = {"name": "Test", "description": "Desc", "price": 150, "quantity": 2}
    monkeypatch.setattr("builtins.input", lambda _: "y")
    updated_lower = Product.new_product(data_lower_price, products)
    assert updated_lower.price == 150
