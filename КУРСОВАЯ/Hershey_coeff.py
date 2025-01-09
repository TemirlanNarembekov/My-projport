
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

#for item in logarithmic_returns_array:
 #   print(item)

sample = logarithmic_returns_array[169:]
# def calculate_hirsch_coefficient(logarithmic):
#     # Рассчитываем среднее значение логарифмических доходностей
#     total_log_return = np.sum(logarithmic)#done
    
#     # Рассчитываем количество периодов
#     num_periods = len(logarithmic)#done
    
#     # Рассчитываем среднюю логарифмическую доходность
#     mean_log_return = total_log_return / num_periods #done
 
#     # Рассчитываем разность между каждой логарифмической доходностью и средним значением
#     deviations = logarithmic - mean_log_return#done
    
#     # Возводим разности в куб и суммируем
#     sum_cubed_deviations = np.sum(deviations**3)/num_periods #done
    
#     # Возводим разности в квадрат и суммируем
#     sum_squared_deviations = np.sum(deviations**2)/(num_periods)#done
    
#     # Рассчитываем коэффициент Херша
#     hirsch_coefficient = sum_cubed_deviations / ((sum_squared_deviations)**(3/2))
#     return hirsch_coefficient

def calculate_hirsch_coefficient(logarithmic):
    # Рассчитываем среднее значение логарифмических доходностей
    mean_log_return = np.mean(logarithmic)
    
    # Рассчитываем разность между каждой логарифмической доходностью и средним значением
    deviations = logarithmic - mean_log_return
    
    # Возводим разности в куб и суммируем
    sum_cubed_deviations = np.sum(deviations**3)
    
    # Возводим разности в квадрат и суммируем
    sum_squared_deviations = np.sum(deviations**2)
    
    # Рассчитываем количество периодов
    num_periods = len(logarithmic)
    
    # Избегаем деления на ноль
    if sum_squared_deviations == 0:
        return 0
    
    # Печать промежуточных значений для отладки
    print(f"mean_log_return: {mean_log_return}")
    print(f"deviations: {deviations}")
    print(f"sum_cubed_deviations: {sum_cubed_deviations}")
    print(f"sum_squared_deviations: {sum_squared_deviations}")
    
    # Нормализуем суммы
    normalized_cubed_deviations = sum_cubed_deviations / num_periods
    normalized_squared_deviations = sum_squared_deviations / num_periods
    
    # Рассчитываем коэффициент Хирша
    hirsch_coefficient = normalized_cubed_deviations / (normalized_squared_deviations ** (3/2))
    
    # Печать окончательного значения коэффициента для отладки
    print(f"hirsch_coefficient: {hirsch_coefficient}")
    
    return hirsch_coefficient

# Вызываем функцию для расчета коэффициента Херша
hirsch_coefficient = calculate_hirsch_coefficient(logarithmic_returns_array)
print("Коэффициент Херша (H):", hirsch_coefficient)
