# Тесты для нового поведения Category с приватным списком товаров и методом add_product().
# Тесты будут проверять:
# Что при инициализации категории товары сохраняются в приватный атрибут.
# Что к приватному списку нельзя обратиться напрямую.
# Что метод add_product() корректно добавляет Product и увеличивает счётчик product_count.
# Что при попытке добавить не-Product выбрасывается TypeError.
# Что метод get_products() возвращает копию списка.
# автоматический подсчёт категорий (category_count)
# автоматический подсчёт продуктов (product_count)
# Тесты для нового поведения Category с приватным списком товаров и методом add_product().
# Тесты будут проверять:
# Что при инициализации категории товары сохраняются в приватный атрибут.
# Что к приватному списку нельзя обратиться напрямую.
# Что метод add_product() корректно добавляет Product и увеличивает счётчик product_count.
# Что при попытке добавить не-Product выбрасывается TypeError.
# Что метод get_products() возвращает копию списка.
# автоматический подсчёт категорий (category_count)
# автоматический подсчёт продуктов (product_count)
# Что здесь важно:
# # type: ignore[arg-type] в тесте с неправильным типом нужен, чтобы mypy не ругался.
# В test_category_initial_products_and_privacy мы прямо проверяем, что приватный атрибут реально приватный.
# Сброс Category.product_count в начале теста test_add_product_increases_count нужен,
# чтобы тест не зависел от других тестов.
#
# В conftest.py фикстура с autouse=True запускается автоматически перед каждым тестом,
# сбрасывая product_count и category_count без явного вызова в тестах.
# Теперь в тестах можно не сбрасывать счётчики вручную — они всегда начинаются с 0.

# capsys проверяет, что CreationLoggerMixin реально выводит сообщение при создании.
# Проверяется валидация цены и количества.
# Тестируется правильная работа Product.new_product (и обновление, и добавление).
# Наследники Smartphone и LawnGrass тестируются на наличие всех полей.
# Category тестируется на корректные счётчики и защиту от неправильных типов.
# Order тестируется на правильный расчёт и защиту от некорректных данных.

# Category.add_product — если добавить товар с quantity=0, то ошибка ловится, выводится сообщение,
# и всегда выводится "Обработка добавления товара завершена".
# Category.add_product успешный сценарий — товар добавляется и выводятся оба сообщения (успешно и завершена).
# Order — при заказе с quantity=0 выбрасывается исключение и выводится сообщение о завершении.
# Order успешный сценарий — заказ создаётся, количество товара уменьшается, выводятся сообщения.


from typing import Any

import pytest

from src.category import Category
from src.product import Product, ZeroQuantityError


@pytest.fixture(autouse=True)
def reset_category_counters() -> None:
    """
    Сбрасывает счётчики категорий и товаров перед каждым тестом.
    """
    Category.category_count = 0
    Category.product_count = 0


def test_category_valid_initialization() -> None:
    p1 = Product("P1", "D1", 10.0, 1)
    p2 = Product("P2", "D2", 20.0, 2)
    c = Category("Cat", "Desc", [p1, p2])
    assert c.name == "Cat"
    assert c.description == "Desc"
    assert len(c.products.strip().split("\n")) == 2
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
        Category("Name", "Desc", "Not a list")  # type: ignore[arg-type]


def test_category_products_not_product_objects() -> None:
    with pytest.raises(TypeError):
        Category("Name", "Desc", ["string", 123])  # type: ignore[list-item]


def test_category_initial_products_and_privacy() -> None:
    p1 = Product("Prod1", "Desc1", 10.0, 5)
    category = Category("Cat1", "DescCat", [p1])

    # Проверка, что приватный атрибут напрямую не доступен
    with pytest.raises(AttributeError):
        _ = category.__products  # type: ignore[attr-defined]

    # Проверка, что get_products возвращает копию, а не оригинал
    products_copy = category.get_products()
    assert products_copy == [p1]
    assert products_copy is not category.get_products()


def test_add_product_increases_count() -> None:
    Category.product_count = 0  # Сброс перед тестом

    p1 = Product("Prod1", "Desc1", 10.0, 5)
    category = Category("Cat1", "DescCat", [p1])

    p2 = Product("Prod2", "Desc2", 20.0, 3)
    category.add_product(p2)

    assert p2 in category.get_products()
    assert Category.product_count == 2


def test_add_non_product_raises_type_error() -> None:
    p1 = Product("Prod1", "Desc1", 10.0, 5)
    category = Category("Cat1", "DescCat", [p1])

    with pytest.raises(TypeError):
        category.add_product("not a product")  # type: ignore[arg-type]


def test_get_products_returns_copy() -> None:
    p1 = Product("Prod1", "Desc1", 10.0, 5)
    category = Category("Cat1", "DescCat", [p1])

    products_copy = category.get_products()
    products_copy.append(Product("Prod2", "Desc2", 20.0, 3))

    assert len(category.get_products()) == 1


def test_category_count_increments_on_creation() -> None:
    Category.category_count = 0  # Сброс перед тестом

    p1 = Product("Prod1", "Desc1", 10.0, 5)
    Category("Cat1", "DescCat", [p1])
    Category("Cat2", "DescCat2", [])

    assert Category.category_count == 2


def test_product_count_increments_on_creation() -> None:
    Category.product_count = 0  # Сброс перед тестом

    p1 = Product("Prod1", "Desc1", 10.0, 5)
    p2 = Product("Prod2", "Desc2", 20.0, 3)
    Category("Cat1", "DescCat", [p1, p2])

    assert Category.product_count == 2


def test_products_getter_returns_correct_string() -> None:
    # Создаем тестовые продукты
    p1 = Product("Яблоко", "Красное яблоко", 80, 15)
    p2 = Product("Банан", "Желтый банан", 50, 20)

    # Создаем категорию с этими продуктами
    category = Category("Фрукты", "Свежие фрукты", [p1, p2])

    # Ожидаемая строка
    expected = "Яблоко, 80.0 руб. Остаток: 15 шт.\n" "Банан, 50.0 руб. Остаток: 20 шт.\n"

    # Проверяем геттер
    assert category.products == expected


def test_products_getter_empty_list() -> None:
    # Категория без продуктов
    category = Category("Пустая категория", "Нет товаров", [])

    # Проверяем, что геттер возвращает пустую строку
    assert category.products == ""


def test_products_privacy() -> None:
    # Проверка, что напрямую получить __products нельзя
    p1 = Product("Яблоко", "Красное яблоко", 80, 15)
    category = Category("Фрукты", "Свежие фрукты", [p1])

    with pytest.raises(AttributeError):
        _ = category.__products  # напрямую доступ запрещен


def test_category_init_and_str() -> None:
    p1 = Product("A", "Desc", 100, 2)
    p2 = Product("B", "Desc", 200, 3)
    cat = Category("TestCat", "DescCat", [p1, p2])
    assert "TestCat" in str(cat)
    assert "5 шт" in str(cat)  # общее количество


def test_category_add_product() -> None:
    cat = Category("Cat", "Desc", [])
    p = Product("A", "Desc", 100, 2)
    cat.add_product(p)
    assert p in cat.get_products()


def test_category_products_property() -> None:
    p1 = Product("Prod1", "Desc", 10, 1)
    p2 = Product("Prod2", "Desc", 20, 2)
    cat = Category("Cat", "Desc", [p1, p2])
    products_str = cat.products
    assert "Prod1, 10.0 руб. Остаток: 1 шт." in products_str
    assert "Prod2, 20.0 руб. Остаток: 2 шт." in products_str


def test_order_valid_creation_and_stock_update() -> None:
    p = Product("Prod1", "Desc1", 10.0, 5)
    order = Category.Order(p, 3)

    # заказ создан
    assert isinstance(order, Category.Order)
    assert order.total_quantity() == 3
    assert order.total_price() == 30.0

    # остаток на складе уменьшился
    assert p.quantity == 2


def test_order_invalid_product_type() -> None:
    with pytest.raises(TypeError):
        Category.Order("not a product", 1)  # type: ignore[arg-type]


@pytest.mark.parametrize("bad_qty", [-1, "3", None])
def test_order_invalid_quantity_type_or_value(bad_qty: Any) -> None:
    p = Product("Prod1", "Desc1", 10.0, 5)
    with pytest.raises(ValueError):
        Category.Order(p, bad_qty)  # type: ignore[arg-type]


def test_order_quantity_exceeds_stock() -> None:
    p = Product("Prod1", "Desc1", 10.0, 2)
    with pytest.raises(ValueError, match="Недостаточно товара"):
        Category.Order(p, 5)


def test_order_str_and_repr() -> None:
    p = Product("Prod1", "Desc1", 10.0, 5)
    order = Category.Order(p, 2)

    s = str(order)
    r = repr(order)

    assert "Заказ: Prod1" in s
    assert "сумма: 20.0 руб." in s
    assert "Order(product='Prod1'" in r
    assert "quantity=2" in r
    assert "total_price=20.0" in r


def test_average_price_normal_case() -> None:
    p1 = Product("P1", "Desc", 100, 2)
    p2 = Product("P2", "Desc", 200, 3)
    category = Category("TestCat", "Desc", [p1, p2])

    avg = category.average_price()
    assert avg == (100 + 200) / 2  # 150.0


def test_average_price_one_product() -> None:
    p1 = Product("P1", "Desc", 300, 5)
    category = Category("TestCat", "Desc", [p1])

    avg = category.average_price()
    assert avg == 300


def test_average_price_empty_category_returns_zero() -> None:
    category = Category("EmptyCat", "Desc", [])
    assert category.average_price() == 0


def test_category_add_product_zero_quantity(capsys: "pytest.CaptureFixture[str]") -> None:
    cat = Category("Phones", "Smartphones", [])
    p = Product("iPhone", "Desc", 1000, 0)  # вызовет ZeroQuantityError в __init__

    # здесь проверяем именно add_product
    with pytest.raises(ZeroQuantityError):
        cat.add_product(p)

    captured = capsys.readouterr()
    assert "Обработка добавления товара завершена" in captured.out


def test_category_add_product_success(capsys: "pytest.CaptureFixture[str]") -> None:
    cat = Category("Phones", "Smartphones", [])
    p = Product("iPhone", "Desc", 1000, 1)

    cat.add_product(p)

    captured = capsys.readouterr()
    assert "Товар 'iPhone' добавлен" in captured.out
    assert "Обработка добавления товара завершена" in captured.out


def test_order_with_zero_quantity_raises(capsys: "pytest.CaptureFixture[str]") -> None:
    p = Product("Samsung", "Phone", 500, 10)
    with pytest.raises(ZeroQuantityError, match="Нельзя заказать нулевое количество товара"):
        Category.Order(p, 0)

    captured = capsys.readouterr()
    assert "Обработка заказа завершена" in captured.out


def test_order_success(capsys: "pytest.CaptureFixture[str]") -> None:
    p = Product("Xiaomi", "Phone", 300, 5)
    order = Category.Order(p, 2)

    assert order.total_quantity() == 2
    assert order.total_price() == 600
    assert p.quantity == 3  # склад уменьшился

    captured = capsys.readouterr()
    assert "Заказ на товар 'Xiaomi' успешно создан" in captured.out
    assert "Обработка заказа завершена" in captured.out
