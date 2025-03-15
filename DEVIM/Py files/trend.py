from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import statsmodels.sandbox.stats.runs as runs
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.filters.hp_filter import hpfilter
import statsmodels.api as sm

path = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\new_plan2.csv'
plan = pd.read_csv(path)

daily_late_sum = plan.groupby("plan_at")["late"].sum().reset_index()
daily_overdues = daily_late_sum['late']

median = np.median(daily_overdues)
binary_sequence = np.where(daily_overdues > median, 1, 0)
# Запускаем тест Вальда-Вольфовица
z_stat, p_value = runs.runstest_1samp(binary_sequence, correction=True)

# # Вывод результатов
# print(f"Статистика Z: {z_stat}")
# print(f"P-value: {p_value}")

# # Интерпретация
# alpha = 0.01
# if p_value < alpha:
#     print("Гипотеза о случайности отвергается: имеется тренд.")
# else:
#     print("Нет оснований отвергать гипотезу о случайности:отсутсвует тренд.")



result = seasonal_decompose(daily_late_sum["late"], model="additive", period=7)
trend = result.trend

# Убираем NaN значения
trend_clean = trend.dropna()

# HP-фильтрация тренда
# trend_hp, _ = hpfilter(trend_clean, lamb=1600)

np.random.seed(42)
data = pd.Series(np.random.randn(300).cumsum())

# Применение фильтра Ходрика-Прескотта
trend_hp, _ = sm.tsa.filters.hpfilter(data, lamb=100)

# # Визуализация
# plt.figure(figsize=(12, 6))
# plt.plot(data, color='gray', alpha=0.5, label='Original Data')
# plt.plot(trend_hp, color='red', label='Long-term Trend')
# plt.legend()
# plt.grid()
# plt.show()
plt.figure(figsize=(10, 6))
sns.histplot(data, bins=10, kde=True)  # kde=True добавляет линию плотности

plt.xlabel("Доля просрочек")
plt.ylabel("Частота")
plt.title("Распределение доли просрочек")
plt.grid(True)
plt.show()