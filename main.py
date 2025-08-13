from src.category import Category
from src.product import Product


p1 = Product("Яблоко", "Красное яблоко", 80, 15)
p2 = Product("Банан", "Желтый банан", 50, 20)

category = Category("Фрукты", "Свежие фрукты", [p1, p2])

print(category.products)

products = [
    Product("Яблоко", "Красное яблоко", 80, 15)
]
#_______________________________________________________________________________________
# Создаем новый товар через класс-метод
new_data = {"name": "Яблоко", "description": "Свежее яблоко", "price": 85, "quantity": 10}
Product.new_product(new_data, products)

# Создаем новый товар, которого нет
banana_data = {"name": "Банан", "description": "Желтый банан", "price": 50, "quantity": 20}
Product.new_product(banana_data, products)

print(products)
#__________________________________________________________________________________________
p = Product("Яблоко", "Красное яблоко", 80, 15)

print(p.price)  # 80

p.price = 0     # ❌ Цена не должна быть нулевая или отрицательная
p.price = 90    # ✅ Цена повысилась
p.price = 70    # ⏳ Спросит подтверждение: y/n