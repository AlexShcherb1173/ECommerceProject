from typing import Optional, Union

import pytest

from src.category import Category
from src.product import Product


def test_category_valid_initialization() -> None:
    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    c = Category("Cat", "Desc", [p1, p2])
    assert c.name == "Cat"
    assert c.description == "Desc"
    assert len(c.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


@pytest.mark.parametrize("name", [123, None])
def test_category_invalid_name_type(name: str) -> None:
    with pytest.raises(TypeError):
        Category(name, "Desc", [])


@pytest.mark.parametrize("desc", [123, None])
def test_category_invalid_description_type(desc: str) -> None:
    with pytest.raises(TypeError):
        Category("Name", desc, [])


def test_category_invalid_products_type() -> None:
    with pytest.raises(TypeError):
        Category("Name", "Desc", "Not a list") # type: ignore[arg-type]


def test_category_products_not_product_objects() -> None:
    with pytest.raises(TypeError):
        Category("Name", "Desc", ["string", 123])  # type: ignore[list-item]
