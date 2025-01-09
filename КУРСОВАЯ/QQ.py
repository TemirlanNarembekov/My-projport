import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
from scipy.optimize import minimize
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
np.random.seed(0)

normal_data = np.random.normal(loc=0, scale=1, size=length)

# Квантили нормального распределения
normal_quantiles = np.percentile(normal_data, np.linspace(0, 100, num=length))

# Функция для минимизации
def objective(params):
    mu, sigma = params
    observed_quantiles = np.percentile(np.random.normal(loc=mu, scale=sigma, size=length), np.linspace(0, 100, num=length))
    return np.sum((observed_quantiles - normal_quantiles)**2)

# Начальное приближение для mu и sigma
initial_guess = [0, 1]

# Минимизация с использованием метода Нелдера-Мида
result = minimize(objective, initial_guess, method='Nelder-Mead')

# Получение оптимальных значений mu и sigma
mu_optimal, sigma_optimal = result.x

print("Оптимальное значение математического ожидания:", mu_optimal)
print("Оптимальное значение дисперсии:", sigma_optimal)

# Визуализация результатов
plt.figure(figsize=(8, 6))
plt.scatter(normal_quantiles, np.percentile(np.random.normal(loc=mu_optimal, scale=sigma_optimal, size=length), np.linspace(0, 100, num=length)))
plt.plot([-3, 3], [-3, 3], linestyle='--', color='red')
plt.xlabel('Квантили теоретического распределения')
plt.ylabel('Квантили наблюдаемого распределения')
plt.title('QQ-график')
plt.grid(True)
plt.show()