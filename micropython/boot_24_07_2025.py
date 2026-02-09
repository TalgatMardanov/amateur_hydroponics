#port 0 out авто регулятор pH
#port 1 out авто регулятор TDS
#port 2 out авто регулятор перемешивание
#port 3 out вкл/выкл помпы
#port 4 out вкл/выкл освещение
#port 5 out вкл/выкл вентиляции
#port 6 out вкл/выкл влажность только включение увлажнителя
#port 7 out вкл/выкл полив
#********************
#port 0 in датчик бака
import onewire, ds18x20
import bmp280
import network
from umqtt.simple import MQTTClient
from time import sleep, ticks_ms, ticks_diff
from machine import Pin, WDT, reset, I2C, ADC
import time
# Инициализация АЦП на GPIO35 (CH3), GPIO39 (CH4)
adc_ch3 = ADC(Pin(35))
adc_ch4 = ADC(Pin(39))

adc_ht1 = ADC(Pin(32))
adc_ht2 = ADC(Pin(33))

# Настройка диапазона измерений (по умолчанию 0-1.1В)
# Доступные диапазоны: ADC.ATTN_0DB (0-1.1V), ADC.ATTN_2_5DB (0-1.5V), 
# ADC.ATTN_6DB (0-2.2V), ADC.ATTN_11DB (0-3.9V)
adc_ch3.atten(ADC.ATTN_11DB)  # Устанавливаем максимальный диапазон 0-3.9V
adc_ch4.atten(ADC.ATTN_11DB)  # Устанавливаем максимальный диапазон 0-3.9V

adc_ht1.atten(ADC.ATTN_11DB)
adc_ht2.atten(ADC.ATTN_11DB)
# Настройка ширины бита (по умолчанию 12 бит)
# Доступные значения: ADC.WIDTH_9BIT, ADC.WIDTH_10BIT, ADC.WIDTH_11BIT, ADC.WIDTH_12BIT
adc_ch3.width(ADC.WIDTH_12BIT)
adc_ch4.width(ADC.WIDTH_12BIT)

adc_ht1.width(ADC.WIDTH_12BIT)
adc_ht2.width(ADC.WIDTH_12BIT)



# I2C Configuration
# for KC868-A16 Rev.: 1.6 
# 0x24(36 1----8) 0x25(37 9----16) OUT
# 0x21(33 9----16) 0x22(34 1----8) IN
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
pcf8574_address = 36

bmp = bmp280.BMP280(i2c)

# Настройка 1-Wire на GPIO9 (SD2)
ow = onewire.OneWire(Pin(14, Pin.OPEN_DRAIN))  # OPEN_DRAIN важно для ESP32!
ds = ds18x20.DS18X20(ow)

# Конфигурация
port_states = {f'p{i}': False for i in range(16)}
wdt = WDT(timeout=60000)

WIFI_SSID = "HOmE_2G"
WIFI_PASSWORD = "220319840"

MQTT_BROKER = "46.8.210.247"
MQTT_PORT = 1883
MQTT_USER = "Riki"
MQTT_PASSWORD = "2203"
MQTT_CLIENT_ID = "esp32_client"

MQTT_TOPICS = [
    b"ph", b"tds", b"setpoint_ph", b"setpoint_tds",
    b"ph_regulator", b"tds_regulator", b"mixing",
    b"outside_temperature", b"internal_temperature",
    b"humidity", b"tank_sensor", b"reg_pump",
    b"reg_lighting", b"reg_ventilation", b"reg_humidity",
    b"watering", b"outdoor_lighting", b"interior_lighting",
    b"connect",b"resout_0",b"resout_1",b"resout_2",b"resout_3",
    b"resout_4",b"resout_5",b"resout_6",b"resout_7"
]
# Функция для считывания состояния портов
def read_ports_ch0():
    # Считываем текущее состояние всех портов
    pcf8574_address = 34
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    return current_state
def read_ports_ch1():
    # Считываем текущее состояние всех портов
    pcf8574_address = 33
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    return current_state

# функции включения и отключения портов
def set_p0(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111110 if state else current_state | 0b00000001
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p1(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p1'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111101 if state else current_state | 0b00000010
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p2(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p2'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111011 if state else current_state | 0b00000100
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p3(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p3'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11110111 if state else current_state | 0b00001000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p4(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p4'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11101111 if state else current_state | 0b00010000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p5(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p5'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11011111 if state else current_state | 0b00100000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p6(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p6'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b10111111 if state else current_state | 0b01000000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p7(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p7'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b01111111 if state else current_state | 0b10000000
    i2c.writeto(pcf8574_address, bytes([new_state]))
# ****************************************Резервные порты
def set_p8(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p8'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111110 if state else current_state | 0b00000001
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p9(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111101 if state else current_state | 0b00000010
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p10(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p10'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111011 if state else current_state | 0b00000100
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p11(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p11'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11110111 if state else current_state | 0b00001000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p12(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p12'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11101111 if state else current_state | 0b00010000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p13(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p13'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11011111 if state else current_state | 0b00100000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p14(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p14'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b10111111 if state else current_state | 0b01000000
    i2c.writeto(pcf8574_address, bytes([new_state]))

def set_p15(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p15'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b01111111 if state else current_state | 0b10000000
    i2c.writeto(pcf8574_address, bytes([new_state]))

# Глобальные переменные
mqtt_client = None
last_publish_time = 0
publish_interval = 2000  # 1 секунд в миллисекундах

def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    
    if not wifi.isconnected():
        print("Connecting to Wi-Fi...")
        wifi.connect(WIFI_SSID, WIFI_PASSWORD)
        
        for retry in range(20):
            if wifi.isconnected():
                break
            print(f"Attempt {retry + 1}/20")
            sleep(1)
            wdt.feed()
        
        if not wifi.isconnected():
            print("Wi-Fi connection failed!")
            wdt.feed()
            reset()
    
    print("Wi-Fi connected! IP:", wifi.ifconfig()[0])

def on_message(topic, msg):
    global mqtt_client
    wdt.feed()
    topic = topic.decode()
    msg = msg.decode()
    print(f"Message on '{topic}': {msg}")
    
    # Обработка команд
    if topic == "reg_pump":
        port_states['p3'] = (msg == '1')
        print('reg_pump')
        set_p3(msg == '1')
    elif topic == "reg_lighting":
        port_states['p4'] = (msg == '1')
        print('reg_lighting')
        set_p4(msg == '1')
    elif topic == "reg_ventilation":
        port_states['p5'] = (msg == '1')
        print('reg_ventilation')
        set_p5(msg == '1')
    elif topic == "watering":
        port_states['p7'] = (msg == '1')
        print('watering')
        set_p7(msg == '1')
    elif topic == "reg_humidity":
        port_states['p6'] = (msg == '1')
        print('reg_humidity')
        set_p6(msg == '1')
    #только для pH и TDS
    elif topic == "ph_regulator":
        port_states['p0'] = (msg == '1')
        print('reg_humidity')
        set_p0(msg == '1')
    elif topic == "tds_regulator":
        port_states['p1'] = (msg == '1')
        print('tds_humidity')
        set_p1(msg == '1')
    elif topic == "mixing":
        port_states['p2'] = (msg == '1')
        print('mixing')
        set_p2(msg == '1')
    # резервные порты
    elif topic == "resout_0":
        port_states['p8'] = (msg == '1')
        print('resout_0')
        set_p8(msg == '1')
    elif topic == "resout_1":
        port_states['p9'] = (msg == '1')
        print('resout_1')
        set_p9(msg == '1')
    elif topic == "resout_2":
        port_states['p10'] = (msg == '1')
        print('resout_2')
        set_p10(msg == '1')
    elif topic == "resout_3":
        port_states['p11'] = (msg == '1')
        print('resout_3')
        set_p11(msg == '1')
    elif topic == "resout_4":
        port_states['p12'] = (msg == '1')
        print('resout_4')
        set_p12(msg == '1')
    elif topic == "resout_5":
        port_states['p13'] = (msg == '1')
        print('resout_5')
        set_p13(msg == '1')
    elif topic == "resout_6":
        port_states['p14'] = (msg == '1')
        print('resout_6')
        set_p14(msg == '1')
    elif topic == "resout_7":
        port_states['p15'] = (msg == '1')
        print('resout_7')
        set_p15(msg == '1')


def init_mqtt():
    global mqtt_client
    try:
        mqtt_client = MQTTClient(
            client_id=MQTT_CLIENT_ID,
            server=MQTT_BROKER,
            port=MQTT_PORT,
            user=MQTT_USER,
            password=MQTT_PASSWORD
        )
        mqtt_client.set_callback(on_message)
        mqtt_client.connect()
        
        for topic in MQTT_TOPICS:
            mqtt_client.subscribe(topic)
            print(f"Subscribed to: {topic.decode()}")
            
        return True
    except Exception as e:
        print("MQTT Error:", e)
        mqtt_client = None
        return False

def mqtt_check_message():
    global mqtt_client
    if mqtt_client:
        try:
            mqtt_client.check_msg()  # Неблокирующая проверка сообщений
            return True
        except Exception as e:
            print("MQTT Check Error:", e)
            mqtt_client = None
    return False

def mqtt_publish(topic, message, retain=True):
    global mqtt_client
    if mqtt_client is None:
        if not init_mqtt():
            return False
    
    try:
        topic = topic.encode() if isinstance(topic, str) else topic
        message = str(message).encode() if not isinstance(message, bytes) else message
        mqtt_client.publish(topic, message, retain=retain)
        print(f"Published to {topic.decode()}: {message.decode()}")
        return True
    except Exception as e:
        print("Publish Error:", e)
        mqtt_client = None
        return False

def publish_sensor_data():
    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
    pcf8574_address = 36
    # Здесь реализуйте сбор и публикацию данных с датчиков
    #mqtt_publish("internal_temperature", 25.4)
    #mqtt_publish("humidity", 65)
    #mqtt_publish("tank_sensor", 1)
    mqtt_publish("connect", 1)
    # ЧТЕНИЕ ПОРТОВ CH0 и CH1
    status_ch0 = read_ports_ch0()  # Считываем состояние портов
    #print("BIN:", bin(status_ch0))  # Выводим состояние в двоичном формате
    status_ch1 = read_ports_ch1()  # Считываем состояние портов
    #print("BIN:", bin(status_ch1))  # Выводим состояние в двоичном формате

    bit_position = 0  # Например, проверяем 3-й бит (нумерация с 0)
    if status_ch0 & (1 << bit_position):
        #print(f"BIT {bit_position} install (1)")
        mqtt_publish("tank_sensor", 1)
    else:
        #print(f"BIT {bit_position} NOT install (0)")
        mqtt_publish("tank_sensor", 0)

    # Поиск датчиков
    ow = onewire.OneWire(Pin(14, Pin.OPEN_DRAIN))
    roms = ds.scan()
    ds.convert_temp()
    temp = ds.read_temp(roms[0])  
    #print(f"t: {temp:.2f}C")
    mqtt_publish("internal_temperature", temp)

    i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
    # Инициализация BMP280
    bmp = bmp280.BMP280(i2c)

    temp_bmp = bmp.temperature  # Чтение температуры
    pres_bmp = bmp.pressure    # Чтение давления
    pres_bmp = int((pres_bmp/100)-254)
    
    value_outdoor_lighting = adc_ch3.read() # наружнее освещение
    value_interior_lighting = adc_ch4.read()# внутренее освещение

    value_ph = adc_ht1.read()# ph измерение
    value_tds= adc_ht2.read()# tds измерение
    #print("ADC value: {}".format(value_interior_lighting))
    #print("ADC value: {}".format(value_outdoor_lighting))
    #print("ADC ph: {}".format(value_ph))
    #print("ADC tds: {}".format(value_tds))
    mqtt_publish("interior_lighting",value_interior_lighting)
    mqtt_publish("outdoor_lighting",value_outdoor_lighting)
    mqtt_publish("ph",value_ph)
    mqtt_publish("tds",value_tds)
    mqtt_publish("outside_temperature", temp_bmp)  
    mqtt_publish("humidity", pres_bmp)
    
def main_loop():
    global last_publish_time, mqtt_client
    
    connect_wifi()
    init_mqtt()
    
    
    
    while True:
        current_time = ticks_ms()
        
        # Периодическая публикация данных
        if ticks_diff(current_time, last_publish_time) >= publish_interval:
            publish_sensor_data()
            last_publish_time = current_time
        
        # Проверка входящих сообщений
        mqtt_check_message()
        
        
        # Сброс watchdog
        wdt.feed()
        
        # Короткая пауза для снижения нагрузки
        sleep(0.1)

if __name__ == "__main__":
    main_loop()