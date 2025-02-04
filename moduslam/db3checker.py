import sqlite3
import pandas as pd

db3_path = "/home/lab/Desktop/rosbag2_2023_11_02-12_18_16/rosbag2_2023_11_02-12_18_16_0.db3"

conn = sqlite3.connect(db3_path)
cursor = conn.cursor()

query = "SELECT * FROM messages WHERE timestamp = ?"

# Ваш конкретный таймштамп
timestamp_to_find = 1698927496694033807

# Выполните запрос для получения данных
cursor.execute(query, (timestamp_to_find,))
rows = cursor.fetchall()

# Конвертируем в DataFrame для удобного просмотра (по желанию)
df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])

# Вывод результата
print(df)

# Закрываем соединение
conn.close()
