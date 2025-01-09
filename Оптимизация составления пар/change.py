# Исходные массивы
keys_array = ["apple", "banana", "cherry"]
values_array = [5, 3, 7]

# Создание словаря из массивов
created_dict = dict(zip(keys_array, values_array))

# Заранее заданный словарь
predefined_dict = {
    "apple": 5,
    "banana": 7,
    "cherry": 6,
    "date": 8
}

# Нахождение количества совпадений
matches = 0
for key in created_dict:
    if key in predefined_dict and created_dict[key] == predefined_dict[key]:
        matches += 1

print(f"Количество совпадений: {matches}")

