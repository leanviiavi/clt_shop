import pandas as pd

# Загрузка Excel-файла
df = pd.read_excel("parts.xlsx")

desired_columns = df.columns.tolist()
# Преобразование DataFrame в список словарей
parts_list = df.to_dict(orient="records")

# Вывод результата
for part in parts_list:
    print(part)


# desired_columns = [
#     'Партномер запчасти', 'Марка авто', 'Модель авто', 'Название запчасти',
#     'Категория', 'Подкатегория', 'Качество', 'Состояние',
#     'Поколение', 'Единица изм', 'Винкод', 'Цена', 'Количество'
# ]

df = pd.read_excel("parts.xlsx", usecols=desired_columns)
parts_list = df.to_dict(orient="records") 
for part in parts_list:
    print(part)

print(len(parts_list))

from products.models import Product

