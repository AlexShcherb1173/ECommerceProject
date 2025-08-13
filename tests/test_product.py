# Что проверяют тесты:
# test_add_new_product — добавление нового товара в пустой список.
# test_update_existing_product_quantity_and_price — увеличение количества и выбор более высокой цены.
# test_update_existing_product_lower_price_keeps_old — цена не меняется, если новая ниже.
# test_add_multiple_products — можно добавить несколько разных товаров.

import pytest
from src.product import Product


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
