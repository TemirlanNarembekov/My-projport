import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.sandbox.stats.runs as runs
import numpy as np
import seaborn as sns
from pymannkendall import original_test
# Загружаем данные
path = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\new_plan2.csv'
path2 = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\payments.csv'
path3 = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\orders.csv'
plan = pd.read_csv(path)
payments = pd.read_csv(path2)


# Загружаем данные
plan_path = '/mnt/data/new_plan2.csv'
plan = pd.read_csv(path)
payments = pd.read_csv(path2)
orders = pd.read_csv(path3)
# Преобразуем даты
plan["plan_at"] = pd.to_datetime(plan["plan_at"])
payments["paid_at"] = pd.to_datetime(payments["paid_at"])
orders["put_at"] = pd.to_datetime(orders["put_at"])
# Агрегируем данные по месяцам

plan["month"] = plan["plan_at"].dt.strftime("%Y-%m")
payments["month"] = payments["paid_at"].dt.strftime("%Y-%m")
orders["month"] = orders["put_at"].dt.strftime("%Y-%m")

# Считаем сумму планируемых платежей и фактически оплаченных сумм по месяцам
monthly_required_sum = plan.groupby("month")["plan_sum_total"].sum().reset_index()
monthly_paid_sum = payments.groupby("month")["paid_sum"].sum().reset_index()
monthly_issued_sum = orders.groupby("month")["issued_sum"].sum().reset_index()

# Объединяем данные и считаем сумму просрочек и их долю
monthly_stats = pd.merge(monthly_required_sum, monthly_paid_sum, on="month", how="left")
monthly_stats = pd.merge(monthly_stats, monthly_issued_sum, on="month", how="left")
monthly_stats["late"] = monthly_stats["plan_sum_total"] - monthly_stats["paid_sum"]
monthly_stats["late"] = monthly_stats["late"].clip(lower=0)  # Исключаем отрицательные значения
monthly_stats["late_ratio"] = monthly_stats["late"] / monthly_stats["plan_sum_total"]

# Строим график
# # Строим график суммы просрочек
# plt.figure(figsize=(10, 5))
# plt.plot(monthly_stats["month"], monthly_stats["late"], marker='o', linestyle='-', color='r', label='Сумма просрочек')
# plt.xlabel("Месяц")
# plt.ylabel("Сумма просрочек")
# plt.title("Динамика суммы просрочек по месяцам")
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid()
# plt.show()

# Строим график доли просрочек
plt.figure(figsize=(10, 5))
plt.plot(monthly_stats["month"], monthly_stats["late_ratio"], marker='o', linestyle='-', color='b', label='Доля просрочек')
plt.xlabel("Месяц")
plt.ylabel("Доля просрочек")
plt.title("Динамика доли просрочек по месяцам")
plt.xticks(rotation=45)
plt.legend()
plt.grid()
plt.show()

# # Строим график выданных сумм (issued_sum)
# plt.figure(figsize=(10, 5))
# plt.plot(monthly_stats["month"], monthly_stats["issued_sum"], marker='o', linestyle='-', color='g', label='Выданные суммы')
# plt.xlabel("Месяц")
# plt.ylabel("Выданные суммы")
# plt.title("Динамика выданных сумм по месяцам")
# plt.xticks(rotation=45)
# plt.legend()
# plt.grid()
# plt.show()

# # Вывод результата
# print(monthly_stats)
threshold = monthly_stats["late_ratio"].mean()  # Среднее вместо медианы
binary_sequence = np.where(monthly_stats["late_ratio"] > threshold, 1, 0)
# Запускаем тест Вальда-Вольфовица
z_stat, p_value = runs.runstest_1samp(binary_sequence, correction=True)

# Вывод результатов
# print(f"Статистика Z: {z_stat}")
# print(f"P-value: {p_value}")

# Интерпретация
# alpha = 0.01
# if p_value < alpha:
#     print("Гипотеза о случайности отвергается: имеется тренд.")
# else:
#     print("Нет оснований отвергать гипотезу о случайности:отсутствует тренд.")

result = original_test(monthly_stats["late_ratio"])
# print(result)