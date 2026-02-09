import network
import time

# Настройка WiFi в режиме станции
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

# Подключение к сети (замени на свои данные)
SSID = "ТВОЙ_SSID"
PASSWORD = "ТВОЙ_ПАРОЛЬ"

print("Подключаемся к WiFi...")
wifi.connect(SSID, PASSWORD)

# Ждём подключения (макс. 10 секунд)
timeout = 0
while not wifi.isconnected() and timeout < 10:
    print("Ожидание подключения...")
    time.sleep(1)
    timeout += 1

if wifi.isconnected():
    print("Успешно подключено к:", SSID)
    print("IP-адрес:", wifi.ifconfig()[0])
    
    # Бесконечный цикл вывода RSSI
    while True:
        rssi = wifi.status('rssi')  # Получаем уровень сигнала
        print("Уровень сигнала (RSSI):", rssi, "dBm")
        time.sleep(1)  # Пауза 1 секунда
else:
    print("Не удалось подключиться к WiFi!")