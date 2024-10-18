import sqlite3
from datetime import datetime, timedelta
import pandas as pd
import numpy as np


# กำหนดช่วงวันที่
start_date = datetime(2024, 10, 11)
end_date = datetime(2024, 10, 18)

# สร้างคอลัมน์วันที่และเวลา โดยมีช่วงห่างทุก 3 ชั่วโมง
dates = pd.date_range(start=start_date, end=end_date, freq='D')
times = pd.date_range('00:00:00', '23:00:00', freq='3H').time
date_time = [(d, t) for d in dates for t in times]

# สุ่มค่าสำหรับ MQ-7, MQ-135, Temp, และ Humidity และ NodeID
id_values = np.random.randint(low =1 , high = 4, size = len(date_time))
print(f"{id_values}")
mq7_values = np.round(np.random.uniform(25, 1000, len(date_time)), 2)
mq135_values = np.round(np.random.uniform(400, 42000, len(date_time)), 2)
temp_values = np.round(np.random.uniform(25, 89, len(date_time)), 2)
humidity_values = np.round(np.random.uniform(59, 89, len(date_time)), 2)

# สร้างฐานข้อมูล SQLite
conn = sqlite3.connect('sensor_data.db')
cursor = conn.cursor()

# สร้างตารางสำหรับข้อมูล
cursor.execute('''
    CREATE TABLE sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Node_ID INTEGER,
        Date TEXT,
        Time TEXT,
        MQ7 REAL,
        MQ135 REAL,
        Temperature REAL,
        Humidity REAL
    )
''')

# ใส่ข้อมูลเข้าในตาราง
for i, (d, t) in enumerate(date_time):
    cursor.execute(f'''
        INSERT INTO sensor_data (Node_ID, date, time, mq7, mq135, temperature, humidity)
        VALUES ({id_values[i]}, ?, ?, ?, ?, ?, ?)
    ''', (d.strftime('%d/%m/%Y'), t.strftime('%H:%M:%S'), mq7_values[i], mq135_values[i], temp_values[i], humidity_values[i]))
    print(id_values[i])

# บันทึกข้อมูลและปิดการเชื่อมต่อ
conn.commit()
conn.close()

print("สร้างไฟล์ SQLite เรียบร้อยแล้ว")
