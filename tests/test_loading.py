import json
from pathlib import Path

import pytest

from src.category import Category
from src.loading import load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """
    Сбрасывает счётчики категорий и товаров перед каждым тестом.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_load_categories_from_json(tmp_path: Path) -> None:
    data = [
        {
            "name": "Test Category",
            "description": "Test description",
            "products": [
                {"name": "Prod1", "description": "Desc1", "price": 10.0, "quantity": 1},
                {"name": "Prod2", "description": "Desc2", "price": 20.0, "quantity": 2},
            ],
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
