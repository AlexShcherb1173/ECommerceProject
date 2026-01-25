import pytest

from src.category import Category


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """Автоматически сбрасывает счётчики Category перед каждым тестом."""
    Category.product_count = 0
    Category.category_count = 0
