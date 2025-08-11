import pytest
import json
from pathlib import Path
from src.code import Product, Category, load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """
    Сбрасывает счётчики категорий и товаров перед каждым тестом.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_product_valid_initialization():
    p = Product("Test", "Description", 100.0, 10)
    assert p.name == "Test"
    assert p.description == "Description"
    assert p.price == 100.0
    assert p.quantity == 10


@pytest.mark.parametrize("name", [123, None, 45.6])
def test_product_invalid_name_type(name):
    with pytest.raises(TypeError):
        Product(name, "Desc", 100.0, 1)


@pytest.mark.parametrize("desc", [123, None, ["list"]])
def test_product_invalid_description_type(desc):
    with pytest.raises(TypeError):
        Product("Name", desc, 100.0, 1)


@pytest.mark.parametrize("price", ["100", None, []])
def test_product_invalid_price_type(price):
    with pytest.raises(TypeError):
        Product("Name", "Desc", price, 1)


def test_product_negative_price():
    with pytest.raises(ValueError):
        Product("Name", "Desc", -50.0, 1)


@pytest.mark.parametrize("quantity", ["5", 3.5, None])
def test_product_invalid_quantity_type(quantity):
    with pytest.raises(TypeError):
        Product("Name", "Desc", 100.0, quantity)


def test_product_negative_quantity():
    with pytest.raises(ValueError):
        Product("Name", "Desc", 100.0, -1)


def test_category_valid_initialization():
    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    c = Category("Cat", "Desc", [p1, p2])
    assert c.name == "Cat"
    assert c.description == "Desc"
    assert len(c.products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


@pytest.mark.parametrize("name", [123, None])
def test_category_invalid_name_type(name):
    with pytest.raises(TypeError):
        Category(name, "Desc", [])


@pytest.mark.parametrize("desc", [123, None])
def test_category_invalid_description_type(desc):
    with pytest.raises(TypeError):
        Category("Name", desc, [])


def test_category_invalid_products_type():
    with pytest.raises(TypeError):
        Category("Name", "Desc", "Not a list")


def test_category_products_not_product_objects():
    with pytest.raises(TypeError):
        Category("Name", "Desc", ["string", 123])


def test_load_categories_from_json(tmp_path: Path):
    data = [
        {
            "name": "Test Category",
            "description": "Test description",
            "products": [
                {
                    "name": "Prod1",
                    "description": "Desc1",
                    "price": 10.0,
                    "quantity": 1
                },
                {
                    "name": "Prod2",
                    "description": "Desc2",
                    "price": 20.0,
                    "quantity": 2
                }
            ]
        }
    ]
    json_path = tmp_path / "test_data.json"
    json_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    categories = load_categories_from_json(str(json_path))
    assert len(categories) == 1
    assert categories[0].name == "Test Category"
    assert len(categories[0].products) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2