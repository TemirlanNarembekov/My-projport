from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
path = 'C:\\Users\\user\\Desktop\\TEST-CHALLENGES\\DEVIM\\task_2_data\\new_plan2.csv'
plan = pd.read_csv(path)

dates = Counter(plan['plan_at'])

daily_late_sum = plan.groupby("plan_at")["late"].sum().reset_index()


daily_overdues = daily_late_sum['late']

indices = list(range(1, len(daily_overdues) + 1))

# Создание графика
plt.figure(figsize=(10, 6))
plt.plot(indices, daily_overdues, marker='o', linestyle='-', color='b', label='daily_overdues')

# Добавление заголовков и подписей
plt.title('Количество просрочек на временной шкале', fontsize=14)
plt.xlabel('Дни', fontsize=12)  # Или "Месяцы", если это месячные данные
plt.ylabel('Количество просрочек', fontsize=12)
plt.grid(True)
plt.legend()

# Отображение графика
# plt.tight_layout()
# plt.show()

