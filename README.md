# Product & Category Management

## Описание
Проект реализует систему управления товарами и категориями на Python.  
Поддерживается:
- Создание объектов **товаров** (`Product`) с валидацией типов.
- Создание объектов **категорий** (`Category`), содержащих список товаров.
- Автоматический подсчёт количества категорий и товаров.
- Загрузка данных о категориях и товарах из **JSON**-файла.
- Модульные тесты с использованием `pytest`.

---
## Структура проекта
main.py # Основная логика классов и функций  
tests/ # Папка с тестами  
test_main.py # Тесты для классов и функции  
data.json # Пример входных данных  
README.md # Документация  


---

## Классы

### `Product`
Класс, представляющий товар.

**Атрибуты:**
- `name: str` — название товара.
- `description: str` — описание товара.
- `price: float` — цена (не может быть отрицательной).
- `quantity: int` — количество на складе (не может быть отрицательным).

**Пример:**
```python
from main import Product

p = Product(
    name="Samsung Galaxy S23 Ultra",
    description="256GB, Серый цвет, 200MP камера",
    price=180000.0,
    quantity=5
)
print(p)
Category
Класс, представляющий категорию товаров.

Атрибуты экземпляра:

name: str — название категории.

description: str — описание категории.

products: list[Product] — список товаров (только объекты класса Product).

Атрибуты класса:

category_count: int — количество созданных категорий.

product_count: int — общее количество товаров во всех категориях.  
```  

 **Пример**:
```python
from main import Product, Category

p1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
p2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

cat = Category(
    name="Смартфоны",
    description="Смартфоны, как средство не только коммуникации, но и удобства жизни",
    products=[p1, p2]
)

print(cat.name)  # "Смартфоны"
print(Category.category_count)  # 1
print(Category.product_count)   # 2
Функции
load_categories_from_json(file_path: str) -> list[Category]
Загружает список категорий с товарами из JSON-файла.
При этом автоматически создаются объекты Product и Category.
```  

 **Пример**:
```python

from main import load_categories_from_json

categories = load_categories_from_json("data.json")

for c in categories:
    print(c.name, "—", len(c.products), "товаров")
```  

 **Пример(data.json**:
```python

[
  {
    "name": "Смартфоны",
    "description": "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
    "products": [
      {
        "name": "Samsung Galaxy C23 Ultra",
        "description": "256GB, Серый цвет, 200MP камера",
        "price": 180000.0,
        "quantity": 5
      }
    ]
  }
]
```
## Запуск тестов
#### Для тестирования используется библиотека pytest.

## Установка:

#### pip install pytest
### Запуск:

#### pytest  
### Возможности валидации  
##### При передаче неверного типа данных (name не строка, price не число и т.д.) выбрасывается TypeError.

##### При отрицательных значениях price или quantity выбрасывается ValueError.

##### В Category.products можно передавать только список объектов Product.

