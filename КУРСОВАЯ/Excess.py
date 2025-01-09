import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import pandas as pd
import csv
import math
from datetime import datetime
import scipy.stats
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

sample = [-0.05, 0.21, 0.005]

def calculate_hirsch_coefficient(logarithmic):
    # Рассчитываем среднее значение логарифмических доходностей
    total_log_return = np.sum(logarithmic)#done
    
    # Рассчитываем количество периодов
    num_periods = len(logarithmic)#done
    
    # Рассчитываем среднюю логарифмическую доходность
    mean_log_return = total_log_return / num_periods #done
 
    # Рассчитываем разность между каждой логарифмической доходностью и средним значением
    deviations = logarithmic - mean_log_return#done
    
    # Возводим разности в куб и суммируем
    sum_four_deviations = np.sum(deviations**4)/num_periods #done
    
    # Возводим разности в квадрат и суммируем
    sum_squared_deviations = np.sum(deviations**2)/num_periods#done
    sum_squared_deviations_2 = sum_squared_deviations**2
    
    # Рассчитываем коэффициент Херша
    hirsch_coefficient = sum_four_deviations / sum_squared_deviations_2
    overall = hirsch_coefficient - 3
    return overall
    

# Вызываем функцию для расчета коэффициента Херша
# hirsch_coefficient = calculate_hirsch_coefficient(logarithmic_returns_array)
# print("Коэффициент Херша (H):", hirsch_coefficient)

x = list(range(1,180))
r = scipy.stats.pearsonr(x, logarithmic_returns_array)

print(r)
result = scipy.stats.linregress(x, logarithmic_returns_array)
r_val = result.rvalue
print(r_val)
##гип0 не отклоняется так как p_val=0,84>0,01, correlation = -0.014