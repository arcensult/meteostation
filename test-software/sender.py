import requests
import time
import random

# ВАЖНО: Убедись, что порт совпадает с server.py (5001)
URL = "http://127.0.0.1:5001/api/update"

print("📡 Эмулятор Wemos D1 Mini запущен...")
print(f"Цель: {URL}\n")

# Создаем сессию и отключаем прокси
session = requests.Session()
session.trust_env = False  # <-- ЭТО ГЛАВНАЯ СТРОКА, она отключает системные прокси

try:
    while True:
        # Генерируем случайные данные
        temp = round(random.uniform(20.0, 25.0), 1)
        press = round(random.uniform(755.0, 765.0), 1)
        uv = round(random.uniform(0, 5), 1)

        payload = {
            "temperature": temp,
            "pressure": press,
            "uv_index": uv
        }

        try:
            # Используем созданную сессию вместо requests.post
            r = session.post(URL, json=payload)
            
            if r.status_code == 200:
                print(f"✅ [OK] Отправлено: {payload}")
            else:
                print(f"❌ Ошибка {r.status_code}: {r.text}")
        except Exception as e:
            print(f"⚠️ Ошибка соединения: {e}")

        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Эмулятор остановлен.")

