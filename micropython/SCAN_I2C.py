from machine import Pin, I2C

# Инициализация I2C
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)  # Замените пины на ваши

# Сканирование устройств на шине I2C
devices = i2c.scan()
print("scans:", devices)