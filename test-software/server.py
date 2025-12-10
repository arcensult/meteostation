from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime
import os

app = Flask(__name__)
DB_NAME = "weather_data.db"

# Создаем базу данных при старте
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            pressure REAL,
            uv_index REAL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ База данных {DB_NAME} готова.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/update', methods=['POST'])
def receive_data():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data"}), 400

    # Получаем данные (с защитой от пустых значений)
    temp = data.get('temperature', 0.0)
    press = data.get('pressure', 0.0)
    uv = data.get('uv_index', 0.0)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO readings (temperature, pressure, uv_index) VALUES (?, ?, ?)",
        (temp, press, uv)
    )
    conn.commit()
    conn.close()

    print(f"📥 Принято: Temp={temp}°C, Press={press}мм, UV={uv}")
    return jsonify({"status": "success"}), 200

@app.route('/api/history')
def get_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Берем последние 20 записей
    cursor.execute("SELECT timestamp, temperature, pressure, uv_index FROM readings ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    
    # Переворачиваем список (старые -> новые)
    rows = rows[::-1] 
    
    # Отрезаем секунды от времени (2023-10-25 14:30:05 -> 14:30:05)
    labels = [row[0].split(' ')[1] for row in rows]

    data = {
        "labels": labels,
        "temp": [row[1] for row in rows],
        "pressure": [row[2] for row in rows],
        "uv": [row[3] for row in rows]
    }
    return jsonify(data)

if __name__ == '__main__':
    init_db()
    print("🚀 Сервер запущен! Открой в браузере: http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5001)

