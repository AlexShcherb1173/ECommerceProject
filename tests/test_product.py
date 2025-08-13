from typing import Optional, Union

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
