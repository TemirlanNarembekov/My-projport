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
length = len(logarithmic_returns)
logarithmic_returns_array = np.array(logarithmic_returns)



data = logarithmic_returns_array[79:]
d = len(data)
# Вывод элементов массива logarithmic_returns_array


def calculate_DW_statistic(log_returns):
    # Вычисляем разности между последовательными значениями логарифмических доходностей
    diff_log_returns = np.diff(log_returns)
    
    # Вычисляем сумму квадратов разностей между последовательными значениями
    numerator = np.sum(diff_log_returns ** 2)
    
    # Вычисляем сумму квадратов всех значений логарифмических доходностей
    denominator = np.sum(log_returns ** 2)
    
    # Вычисляем статистику DW
    DW_statistic = numerator / denominator
    
    return DW_statistic

# Пример использования

if __name__ == "__main__":
    # Ваш временной ряд логарифмических доходностей (замените данными из вашего временного ряда)
   
    
    # Вычисляем статистику DW
    DW_statistic = calculate_DW_statistic(logarithmic_returns_array)
    
    print("Статистика DW:", DW_statistic)
    


print(length)