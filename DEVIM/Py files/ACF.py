import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dailygraph import daily_overdues
import time
from monthlygraph import monthly_stats

# Настройка доступа
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:/Users/user/Desktop/КУРСОВАЯ/studious-karma-450113-s5-66bb1d03297d.json", scope)
client = gspread.authorize(creds)

# Открытие таблицы по ее ID
spreadsheet_id = '1DTDnuggglDMy6wF0NhHLlgxOmg1jmPM9ObqpUPPjg8Q'
spreadsheet = client.open_by_key(spreadsheet_id)

# Выбор листа по названию
worksheet = spreadsheet.worksheet('Лист2')
cell_range = f'B1:B{len(monthly_stats["overdue_ratio"])}'
worksheet.update(cell_range, [[val] for val in monthly_stats["overdue_ratio"]])
print("Данные успешно загружены в столбец B!")
# Ваш список данных
data_list = monthly_stats["overdue_ratio"]  # и т.д.


# Формирование списка формул для всего столбца C
for i in range(1, len(data_list)+1):
    formula = f'=КОРРЕЛ(B$1:ДВССЫЛ(АДРЕС(СЧЁТЗ(B{i}:B$50000);СТОЛБЕЦ(B{i});4));B{i}:ДВССЫЛ(АДРЕС(СЧЁТЗ(B$1:B$50000);СТОЛБЕЦ(B{i});4)))'
    worksheet.update_acell(f'C{i}', formula)  # Используем update_acell для добавления формулы в ячейку C
    time.sleep(1)  # Пауза в 1 секунду между запросами

print("Формулы успешно обновлены!")