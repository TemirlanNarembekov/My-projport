# import csv

# # Задайте путь к CSV файлу
# file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\data.csv'

# # Создаем пустой список для хранения цен и дат
# prices = []
# logarithmic_returns = []
# # Открываем CSV файл и считываем данные
# try:
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Пропускаем заголовок
#         for row in reader:
#             if row[1]:  # Проверяем, есть ли данные о цене
#                 date = row[0]  # Дата
#                 price = float(row[1].replace(',', '.'))  # Цена (преобразуем в число и меняем запятую на точку)
#                 prices.append((date, price))  # Добавляем дату и цену в список //
# except FileNotFoundError:
#     print("Файл не найден.")
# except Exception as e:
#     print("Произошла ошибка:", e)

# # Сортируем цены по датам
# sorted_prices = sorted(prices, key=lambda x: x[0])

# # Выводим список отсортированных цен
# #for price in sorted_prices:
# #    print(price)
# quantity = 0
# for i in sorted_prices:
#     print(i)
#     quantity+=1
# print(quantity)

##############################################################################################################################################

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats

# import csv
# import math
# # Задайте путь к CSV файлу
# file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\data.csv'

# # Создаем пустой список для хранения цен и дат
# prices = []

# # Открываем CSV файл и считываем данные
# try:
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Пропускаем заголовок
#         for row in reader:
#             if row[1]:  # Проверяем, есть ли данные о цене
#                 date = row[0]  # Дата
#                 price = float(row[1].replace(',', '.'))  # Цена (преобразуем в число и меняем запятую на точку)
#                 prices.append((date, price))  # Добавляем дату и цену в список
# except FileNotFoundError:
#     print("Файл не найден.")
# except Exception as e:
#     print("Произошла ошибка:", e)

# # Сортируем цены по датам
# sorted_prices = sorted(prices, key=lambda x: x[0])

# # Создаем список только с ценами
# prices_only = [price for date, price in sorted_prices]

# # Выводим список отсортированных цен
# quantity = len(prices_only)
# logarithmic_returns=[]
# h_values = []
# for i in range(1,quantity):
#     log_return = math.log(prices_only[i] / prices_only[i-1])
#     logarithmic_returns.append(log_return)

# quantity_1 = len(logarithmic_returns)
# for j in range(1,quantity_1):
#     value = logarithmic_returns[j] - logarithmic_returns[j-1]
#     h_values.append(value)
# ##print(logarithmic_returns)
# ##print(h_values)

# # Вычисляем квантили нормального распределения
# observed_quantiles = np.percentile(logarithmic_returns, np.linspace(0, 100, num = quantity_1))
# normal_quantiles = stats.norm.ppf(np.linspace(0, 100, num = quantity_1))


# # Строим QQ-график
# plt.figure(figsize=(8, 6))
# plt.scatter(normal_quantiles, observed_quantiles)
# plt.plot([-3, 3], [-3, 3], linestyle='--', color='red')  # Прямая линия для нормального распределения
# plt.xlabel('Квантили нормального распределения')
# plt.ylabel('Квантили наблюдаемого распределения')
# plt.title('QQ-график')
# plt.grid(True)
# plt.show()
# # Для вычисления квантилей
# #data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # Пример данных
# # quantile_25 = stats.scoreatpercentile(logarithmic_returns, 25)  # 25-й квантиль
# # quantile_50 = stats.scoreatpercentile(logarithmic_returns, 50)  # 50-й квантиль (медиана)
# # quantile_75 = stats.scoreatpercentile(logarithmic_returns, 75)  # 75-й квантиль
# # quantile_5 = stats.scoreatpercentile(logarithmic_returns, 5)
# # quantile_10 = stats.scoreatpercentile(logarithmic_returns, 10)
# # quantile_90 = stats.scoreatpercentile(logarithmic_returns, 90)
# # quantile_95 = stats.scoreatpercentile(logarithmic_returns, 95)


# #####################################################################################################################

# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats

# import csv
# import math

# # Задайте путь к CSV файлу
# file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\data.csv'

# # Создаем пустой список для хранения цен и дат
# prices = []

# # Открываем CSV файл и считываем данные
# try:
#     with open(file_path, newline='', encoding='utf-8') as csvfile:
#         reader = csv.reader(csvfile)
#         next(reader)  # Пропускаем заголовок
#         for row in reader:
#             if row[1]:  # Проверяем, есть ли данные о цене
#                 date = row[0]  # Дата
#                 price = float(row[1].replace(',', '.'))  # Цена (преобразуем в число и меняем запятую на точку)
#                 prices.append((date, price))  # Добавляем дату и цену в список
# except FileNotFoundError:
#     print("Файл не найден.")
# except Exception as e:
#     print("Произошла ошибка:", e)

# # Сортируем цены по датам
# sorted_prices = sorted(prices, key=lambda x: x[0])

# # Создаем список только с ценами
# prices_only = [price for date, price in sorted_prices]

# # Выводим список отсортированных цен
# quantity = len(prices_only)
# logarithmic_returns=[]
# h_values = []
# for i in range(1,quantity):
#     log_return = math.log(prices_only[i] / prices_only[i-1])
#     logarithmic_returns.append(log_return)

# # Вычисляем квантили наблюдаемого распределения с бОльшим количеством точек
# num_quantiles = 1000  # Увеличиваем количество точек
# np.random.seed(0)
# observed_data = np.random.normal(loc=0, scale=1, size=1000)
# observed_quantiles = np.percentile(logarithmic_returns, np.linspace(0, 100, num=num_quantiles))

# # Строим QQ-график, используя квантили наблюдаемого распределения для обеих осей
# plt.figure(figsize=(8, 6))
# plt.scatter(observed_quantiles, observed_quantiles)  # Используем квантили наблюдаемого распределения для обеих осей
# plt.plot([-3, 3], [-3, 3], linestyle='--', color='red')  # Прямая линия для нормального распределения
# plt.xlabel('Квантили наблюдаемого распределения')
# plt.ylabel('Квантили наблюдаемого распределения')
# plt.title('QQ-график')
# plt.grid(True)
# plt.show()

######################################################################################################################


import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime

# Задайте путь к CSV файлу
file_path = 'C:\\Users\\user\\Desktop\\КУРСОВАЯ\\data_2009-2024.csv'

# Создаем пустой список для хранения цен и дат
prices = []

# Открываем CSV файл и считываем данные
try:
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Пропускаем заголовок
        for row in reader:
            if row[1]:  # Проверяем, есть ли данные о цене
                date = datetime.strptime(row[0], '%d.%m.%Y')  # Преобразуем дату в формат datetime
                price = float(row[1].replace(',', '.'))  # Цена (преобразуем в число и меняем запятую на точку)
                prices.append((date, price))  # Добавляем дату и цену в список
except FileNotFoundError:
    print("Файл не найден.")
except Exception as e:
    print("Произошла ошибка:", e)

# Сортируем цены по датам
sorted_prices = sorted(prices, key=lambda x: x[0])
prices_only = [price for date, price in sorted_prices]

quantity = len(sorted_prices)
logarithmic_returns=[]
for i in range(1,quantity):
    log_return = math.log(prices_only[i] / prices_only[i-1])
    logarithmic_returns.append(log_return)
logarithmic_returns_array = np.array(logarithmic_returns)
length = len(logarithmic_returns_array)
# Генерируем набор случайных чисел из стандартного нормального распределения


def calculate_statistics(sample):
    # Расчет математического ожидания (среднего значения)
    mean = np.mean(sample)
    
    # Расчет дисперсии
    variance = np.var(sample, ddof=1)  # Используем ddof=1 для выборочной дисперсии
    
    return mean, variance

# Пример использования:
sample = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])  # Замените на ваш массив данных
mean, variance = calculate_statistics(logarithmic_returns_array)

print(f"Математическое ожидание (среднее значение): {mean}")
print(f"Дисперсия: {variance}")


np.random.seed(0)
normal_data = np.random.normal(loc=0.00607391656991618, scale=0.001212346094874496, size=length)
#uniform_data = np.random.uniform(0,1, length)
# Вычисляем квантили нормального распределения
normal_quantiles = np.percentile(normal_data, np.linspace(0, 100, num = length))
#uniform_quantiles = np.percentile(uniform_data, np.linspace(0, 100, num=h_length))

# Вычисляем квантили наблюдаемого распределения
observed_quantiles = np.percentile(logarithmic_returns_array, np.linspace(0, 100, num = length))

# Строим QQ-график
plt.figure(figsize=(8, 6))
plt.scatter(normal_quantiles, observed_quantiles)  # Используем квантили наблюдаемого распределения для одной оси
plt.plot([-3, 3], [-3, 3], linestyle='--', color='red')  # Прямая линия для нормального распределения
plt.xlabel('Квантили теоретического распределения')
plt.ylabel('Квантили наблюдаемого распределения')
plt.title('QQ-график')
plt.grid(True)
plt.show()
