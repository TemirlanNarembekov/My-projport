
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np
import seaborn as sns
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
# Пример ряда доходностей

# Генерация индексов для оси X (например, номер месяца или периода)
indices = list(range(1, len(logarithmic_returns_array) + 1))

# Создание графика
plt.figure(figsize=(10, 6))
plt.plot(indices, logarithmic_returns_array, marker='o', linestyle='-', color='b', label='Logarithmic Returns')

# Добавление заголовков и подписей
plt.title('Доходности валюты на временной шкале', fontsize=14)
plt.xlabel('Периоды', fontsize=12)  # Или "Месяцы", если это месячные данные
plt.ylabel('Логарифмическая доходность', fontsize=12)
plt.grid(True)
plt.legend()

# Отображение графика
plt.tight_layout()
plt.show()
