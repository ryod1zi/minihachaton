from decimal import Decimal, ROUND_HALF_UP

import json

class Cars:
    def __init__(self, brand, model, year, engine_volume, color, body_type, mileage, price):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_volume = Decimal(str(engine_volume)).quantize(Decimal('0.0'), rounding=ROUND_HALF_UP)
        self.color = color
        self.body_type = body_type
        self.mileage = mileage
        self.price = Decimal(str(price)).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)

class CreateMixin:
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance

class ListingMixin:
    @classmethod
    def listing(cls, car_list):
        return car_list

class RetrieveMixin:
    @classmethod
    def retrieve(cls, car_list, brand, model):
        for car in car_list:
            if car.brand == brand and car.model == model:
                return car
        return None

class UpdateMixin:
    @classmethod
    def update(cls, car_list, brand, model, **kwargs):
        car = cls.retrieve(car_list, brand, model)
        if car:
            for key, value in kwargs.items():
                setattr(car, key, value)
            return car
        return None

class DeleteMixin:
    @classmethod
    def delete(cls, car_list, brand, model):
        car = cls.retrieve(car_list, brand, model)
        if car:
            car_list.remove(car)
            return True
        return False

class CarsWithCRUD(CreateMixin, ListingMixin, RetrieveMixin, UpdateMixin, DeleteMixin, Cars):
    car_list = []

    def __init__(self, brand, model, year, engine_volume, color, body_type, mileage, price):
        super().__init__(brand, model, year, engine_volume, color, body_type, mileage, price)
        CarsWithCRUD.car_list.append(self)

    @classmethod
    def save_to_file(cls, filename='cars_data.json'):
        data = []
        for car in cls.car_list:
            data.append({
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'engine_volume': float(car.engine_volume),
                'color': car.color,
                'body_type': car.body_type,
                'mileage': int(car.mileage),
                'price': float(car.price)
            })

        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load_from_file(cls, filename='cars_data.json'):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)

            cls.car_list = []
            for car_data in data:
                cls.car_list.append(cls.create(**car_data))

        except FileNotFoundError:
            cls.car_list = []

def print_menu():
    print("\n==== Меню ====")
    print("1. Добавить машину")
    print("2. Список машин")
    print("3. Обновить информацию о машине")
    print("4. Удалить машину")
    print("5. Сохранить данные в файл")
    print("6. Загрузить данные из файла")
    print("7. Выйти")

def display_car_details(car):
    print("\n==== Информация о машине ====")
    print(f"Марка: {car.brand}")
    print(f"Модель: {car.model}")
    print(f"Год выпуска: {car.year}")
    print(f"Объем двигателя: {car.engine_volume}")
    print(f"Цвет: {car.color}")
    print(f"Тип кузова: {car.body_type}")
    print(f"Пробег: {car.mileage}")
    print(f"Цена: {car.price}")

def get_user_input(prompt):
    return input(prompt)

def add_car():
    brand = get_user_input("Введите марку: ")
    model = get_user_input("Введите модель: ")
    year = int(get_user_input("Введите год выпуска: "))
    engine_volume = float(get_user_input("Введите объем двигателя: "))
    color = get_user_input("Введите цвет: ")
    body_type = get_user_input("Введите тип кузова: ")
    mileage = int(get_user_input("Введите пробег: "))
    price = float(get_user_input("Введите цену: "))

    CarsWithCRUD.create(
        brand=brand,
        model=model,
        year=year,
        engine_volume=engine_volume,
        color=color,
        body_type=body_type,
        mileage=mileage,
        price=price
    )
    print("Машина добавлена успешно!")

def list_cars():
    cars_list = CarsWithCRUD.listing(CarsWithCRUD.car_list)
    if not cars_list:
        print("Список машин пуст.")
        return

    print("\n==== Список машин ====")
    for index, car in enumerate(cars_list, start=1):
        print(f"{index}. {car.brand} {car.model}")

    choice = get_user_input("Выберите номер машины для просмотра подробной информации (или Enter для возврата): ")
    if choice:
        try:
            index = int(choice)
            selected_car = cars_list[index - 1]
            display_car_details(selected_car)
        except (ValueError, IndexError):
            print("Неверный выбор. Пожалуйста, введите корректный номер.")

def update_car():
    brand = get_user_input("Введите марку машины для обновления: ")
    model = get_user_input("Введите модель машины для обновления: ")

    car = CarsWithCRUD.retrieve(CarsWithCRUD.car_list, brand, model)
    if not car:
        print("Машина не найдена.")
        return

    print("\n==== Текущая информация о машине ====")
    print(f"Марка: {car.brand}")
    print(f"Модель: {car.model}")
    print(f"Год выпуска: {car.year}")
    print(f"Объем двигателя: {car.engine_volume}")
    print(f"Цвет: {car.color}")
    print(f"Тип кузова: {car.body_type}")
    print(f"Пробег: {car.mileage}")
    print(f"Цена: {car.price}")

    update_fields = ['year', 'engine_volume', 'color', 'body_type', 'mileage', 'price']
    for field in update_fields:
        value = get_user_input(f"Введите новое значение {field.capitalize()} (нажмите Enter, чтобы пропустить): ")
        if value:
            setattr(car, field, type(getattr(car, field))(value))

    print("Информация о машине обновлена успешно!")

def delete_car():
    brand = get_user_input("Введите марку машины для удаления: ")
    model = get_user_input("Введите модель машины для удаления: ")

    deleted = CarsWithCRUD.delete(CarsWithCRUD.car_list, brand, model)
    if deleted:
        print("Машина удалена успешно!")
    else:
        print("Машина не найдена.")

def main():
    while True:
        print_menu()
        choice = get_user_input("Введите ваш выбор (1-7): ")

        if choice == '1':
            add_car()
        elif choice == '2':
            list_cars()
        elif choice == '3':
            update_car()
        elif choice == '4':
            delete_car()
        elif choice == '5':
            CarsWithCRUD.save_to_file()
            print("Данные сохранены в файл.")
        elif choice == '6':
            CarsWithCRUD.load_from_file()
            print("Данные загружены из файла.")
        elif choice == '7':
            print("Выход из программы. До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 7.")

if __name__ == "__main__":
    main()







