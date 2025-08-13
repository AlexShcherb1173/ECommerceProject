# Что проверяют тесты:
# test_add_new_product — добавление нового товара в пустой список.
# test_update_existing_product_quantity_and_price — увеличение количества и выбор более высокой цены.
# test_update_existing_product_lower_price_keeps_old — цена не меняется, если новая ниже.
# test_add_multiple_products — можно добавить несколько разных товаров.
# test_set_price_positive_increase — повышение цены всегда проходит.
# test_set_price_zero_or_negative — цена не меняется, если ≤ 0, и выводится сообщение.
# test_price_decrease_confirm_yes — при понижении цены и ответе y цена меняется.
# test_price_decrease_confirm_no — при ответе n цена остаётся прежней и выводится предупреждение.

import pytest
from src.product import Product
from unittest.mock import patch


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
        Product("Name", "Desc", price, 1) # type: ignore[arg-type]


def test_product_negative_price() -> None:
    with pytest.raises(ValueError):
        Product("Name", "Desc", -50.0, 1)


@pytest.mark.parametrize("quantity", ["5", 3.5, None])
def test_product_invalid_quantity_type(quantity: str) -> None:
    with pytest.raises(TypeError):
        Product("Name", "Desc", 100.0, quantity) # type: ignore[arg-type]


def test_product_negative_quantity() -> None:
    with pytest.raises(ValueError):
        Product("Name", "Desc", 100.0, -1)

        
def test_add_new_product():
    products = []
    data = {"name": "Яблоко", "description": "Красное яблоко", "price": 80, "quantity": 15}

    product = Product.new_product(data, products)

    assert len(products) == 1
    assert product.name == "Яблоко"
    assert product.price == 80
    assert product.quantity == 15


def test_update_existing_product_quantity_and_price():
    products = [Product("Яблоко", "Красное яблоко", 80, 15)]
    data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 85, "quantity": 10}

    updated_product = Product.new_product(data, products)

    assert len(products) == 1  # не создается новый объект
    assert updated_product.quantity == 25  # количество сложено
    assert updated_product.price == 85  # цена обновлена на более высокую


def test_update_existing_product_lower_price_keeps_old():
    products = [Product("Яблоко", "Красное яблоко", 80, 15)]
    data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 70, "quantity": 5}

    updated_product = Product.new_product(data, products)

    assert updated_product.quantity == 20
    assert updated_product.price == 80  # цена осталась прежней, т.к. новая ниже


def test_add_multiple_products():
    products = []

    data1 = {"name": "Яблоко", "description": "Красное яблоко", "price": 80, "quantity": 15}
    data2 = {"name": "Банан", "description": "Желтый банан", "price": 50, "quantity": 20}

    Product.new_product(data1, products)
    Product.new_product(data2, products)

    assert len(products) == 2
    assert products[0].name == "Яблоко"
    assert products[1].name == "Банан"

import pytest
from unittest.mock import patch
from src.product import Product


def test_set_price_positive_increase():
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    p.price = 100  # повышаем цену
    assert p.price == 100


def test_set_price_zero_or_negative(capsys):
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    p.price = 0
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 80  # цена не изменилась

    p.price = -50
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert p.price == 80


def test_price_decrease_confirm_yes():
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    with patch("builtins.input", return_value="y"):
        p.price = 70  # согласие на понижение
    assert p.price == 70


def test_price_decrease_confirm_no(capsys):
    p = Product("Яблоко", "Красное яблоко", 80, 15)
    with patch("builtins.input", return_value="n"):
        p.price = 70  # отказ от понижения
    captured = capsys.readouterr()
    assert "Изменение цены отменено" in captured.out
    assert p.price == 80  # цена не изменилась
