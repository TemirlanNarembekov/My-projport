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
# Сгенерируем случайную выборку данных
np.random.seed(0)
data = [2, 2, 3, 5, 6, 6, 7, 8, 9, 10, 12, 12, 13, 15, 16]
x = np.random.normal(size = 1000) 
# Оценим плотность распределения данных с помощью ядерной оценки
kde = gaussian_kde(logarithmic_returns_array)
kde = gaussian_kde(x)
# Генерируем значения по оси X для построения графика
x_values = np.linspace(-1.5, 1.5, 1000)

# Вычисляем значения PDF для каждого значения по оси X
pdf_values = kde(x_values)

# Построим график функции плотности распределения
#sns.kdeplot(logarithmic_returns_array)
sns.kdeplot(x)
plt.title("Kernel Density Estimation")
plt.xlabel("Value")
plt.ylabel("Density")
plt.show()

