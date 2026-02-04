from machine import ADC, Pin
from time import sleep

# Инициализация АЦП на GPIO36 (ADC1_CH0)
adc = ADC(Pin(39))

# Настройка диапазона измерений (по умолчанию 0-1.1В)
# Доступные диапазоны: ADC.ATTN_0DB (0-1.1V), ADC.ATTN_2_5DB (0-1.5V), 
# ADC.ATTN_6DB (0-2.2V), ADC.ATTN_11DB (0-3.9V)
adc.atten(ADC.ATTN_11DB)  # Устанавливаем максимальный диапазон 0-3.9V

# Настройка ширины бита (по умолчанию 12 бит)
# Доступные значения: ADC.WIDTH_9BIT, ADC.WIDTH_10BIT, ADC.WIDTH_11BIT, ADC.WIDTH_12BIT
adc.width(ADC.WIDTH_12BIT)

def read_adc():
    while True:
        value = adc.read()  # Чтение сырого значения (0-4095 для 12 бит)
        voltage = value * 3.9 / 4095  # Преобразование в напряжение (при atten=11DB)
        print("ADC value: {}, Voltage: {:.2f}V".format(value, voltage))
        sleep(1)

# Запуск чтения
read_adc()