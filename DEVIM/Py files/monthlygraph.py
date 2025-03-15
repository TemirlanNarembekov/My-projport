from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pymannkendall import original_test
import statsmodels.sandbox.stats.runs as runs
import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
path = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\new_plan2.csv'
plan = pd.read_csv(path)

# Преобразуем даты
plan["plan_at"] = pd.to_datetime(plan["plan_at"])

# Агрегируем данные по месяцам с учетом года
plan["month"] = plan["plan_at"].dt.strftime("%Y-%m")  # Формат "ГГГГ-ММ"
monthly_late_sum = plan.groupby("month")["late"].sum().reset_index()
monthly_payment_count = plan.groupby("month").size().reset_index(name="count")

# Объединяем и считаем долю просрочек(частота)
monthly_stats = monthly_late_sum.merge(monthly_payment_count, on="month")
monthly_stats["overdue_ratio"] = monthly_stats["late"] / monthly_stats["count"]

# plt.figure(figsize=(10, 5))
# plt.plot(monthly_stats["month"], monthly_stats["late"], marker='o', linestyle='-', color='r', label="Число просрочек")
# plt.title("Число просрочек в месяц")
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid()
# # plt.show()

# # 2. Общее число платежей в месяц
# plt.figure(figsize=(10, 5))
# plt.plot(monthly_stats["month"], monthly_stats["count"], marker='o', linestyle='-', color='b', label="Число платежей")
# plt.title("Число платежей в месяц")
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid()
# plt.show()

# 3. Доля просрочек в месяц
plt.figure(figsize=(10, 5))
plt.plot(monthly_stats["month"], monthly_stats["overdue_ratio"], marker='o', linestyle='-', color='g', label="Доля просрочек")
plt.title("Доля просрочек в месяц")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()

result1 = original_test(monthly_stats["late"])
# print("Число просрочек в месяц:",result1)
result2 = original_test(monthly_stats["overdue_ratio"])
# print("доля просрочек в месяц:",result2)

median = np.median(monthly_stats["overdue_ratio"])
binary_sequence = np.where(monthly_stats["overdue_ratio"] > median, 1, 0)
# Запускаем тест Вальда-Вольфовица
z_stat, p_value = runs.runstest_1samp(binary_sequence, correction=True)

# Вывод результатов
print(f"Статистика Z: {z_stat}")
print(f"P-value: {p_value}")

# Интерпретация
alpha = 0.01
if p_value < alpha:
    print("Гипотеза о случайности отвергается: имеется тренд.")
else:
    print("Нет оснований отвергать гипотезу о случайности:отсутствует тренд.")

