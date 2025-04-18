from pymannkendall import original_test
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import statsmodels.sandbox.stats.runs as runs
from dailygraph import daily_overdues,daily_late_sum,plan


daily_payment_count = plan.groupby("plan_at").size().reset_index(name="count")
counts = daily_payment_count["count"].tolist()  # Количество платежей
daily_stats = daily_late_sum.merge(daily_payment_count, on="plan_at")
daily_stats["overdue_ratio"] = daily_stats["late"] / daily_stats["count"]

counts = daily_payment_count["count"].tolist()  # Количество платежей
indices = list(range(1, len(daily_stats) + 1))

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(indices, daily_stats["overdue_ratio"], marker='o', linestyle='-', color='b', label='Daily Payments')
plt.xlabel("Дни")
plt.ylabel("Доля просрочек в день")
plt.title("Ежедневное доля просрочек")
plt.xticks(rotation=45)  # Поворачиваем подписи оси X для читаемости
plt.legend()
plt.grid()
plt.show()

result = original_test(daily_stats["overdue_ratio"])
print(result)