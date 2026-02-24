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

# Конфигурация
port_states = {f'p{i}': False for i in range(16)}

# функции включения и отключения портов
def set_p1(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111110 if state else current_state | 0b00000001
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p2(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111101 if state else current_state | 0b00000010
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p3(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111011 if state else current_state | 0b00000100
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p4(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11110111 if state else current_state | 0b00001000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p5(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11101111 if state else current_state | 0b00010000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p6(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11011111 if state else current_state | 0b00100000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p7(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b10111111 if state else current_state | 0b01000000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p8(state, save_state=True):
    pcf8574_address = 36
    if save_state:
        port_states['p0'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b01111111 if state else current_state | 0b10000000
    i2c.writeto(pcf8574_address, bytes([new_state]))
"""port output"""
def set_p9(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111110 if state else current_state | 0b00000001
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p10(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111101 if state else current_state | 0b00000010
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p11(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11111011 if state else current_state | 0b00000100
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p12(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11110111 if state else current_state | 0b00001000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p13(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11101111 if state else current_state | 0b00010000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p14(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b11011111 if state else current_state | 0b00100000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p15(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b10111111 if state else current_state | 0b01000000
    i2c.writeto(pcf8574_address, bytes([new_state]))
def set_p16(state, save_state=True):
    pcf8574_address = 37
    if save_state:
        port_states['p9'] = state
    
    current_state = i2c.readfrom(pcf8574_address, 1)[0]
    new_state = current_state & 0b01111111 if state else current_state | 0b10000000
    i2c.writeto(pcf8574_address, bytes([new_state]))


#set_p1(0)
#set_p2(0)
#set_p3(0)
#set_p4(0)
#set_p5(0)
#set_p6(0)
#set_p7(0)
#set_p8(0)
"""set next port"""
#set_p9(0)
#set_p10(0)
#set_p11(0)
#set_p12(0)
#set_p13(0)
#set_p14(0)
#set_p15(1)
#set_p16(1)
#********************************************************************
WIFI_SSID = "XXXXX"
WIFI_PASSWORD = "XXXXX"

MQTT_BROKER = "XXX.XXX.XXX.XXX"
MQTT_PORT = 1883
MQTT_USER = "XXXXX"
MQTT_PASSWORD = "XXXXX"
MQTT_CLIENT_ID = "XXXXX"
#********************************************************************
MQTT_TOPICS = [
    b"g1_adc_ph", b"g1_adc_tds", b"g1_out_port_16", b"g1_out_port_15", b"g1_out_port_14"
]

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

"""порт 1-нижний, 2-средний, 3-верхний ср(0)"""
"""while True:
    state = read_ports_ch0()
    bit_position = 0
    if state & (1 << bit_position):
        print("port1 ", 1)
    else:
        print("port1 ", 0)
    bit_position = 1
    if state & (1 << bit_position):
        print("port2 ", 1)
    else:
        print("port2 ", 0)
    bit_position = 2
    if state & (1 << bit_position):
        print("port3 ", 1)
    else:
        print("port3 ", 0)
    time.sleep(1)  # Ждем 1 секунду перед следующим считыванием"""

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
            #wdt.feed()
        
        if not wifi.isconnected():
            print("Wi-Fi connection failed!")
            #wdt.feed()
            reset()
    
    print("Wi-Fi connected! IP:", wifi.ifconfig()[0])

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

def on_message(topic, msg):
    global mqtt_client
    #wdt.feed()
    topic = topic.decode()
    msg = msg.decode()
    print(f"Message on '{topic}': {msg}")
    
    # Обработка команд
    if topic == "g1_out_port_16":
        set_p16(msg == '1')
    if topic == "g1_out_port_15":
        set_p15(msg == '1')

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
    status_ch0 = read_ports_ch0()  # Считываем состояние портов
    status_ch1 = read_ports_ch1()  # Считываем состояние портов
    value_tds = adc_ch3.read() # считаем TDS датчик
    value_ph = adc_ch4.read() # считаем TDS датчик
    mqtt_publish("g1_adc_tds",value_tds)
    mqtt_publish("g1_adc_ph",value_ph)
    return 0

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
        #wdt.feed()
        
        # Короткая пауза для снижения нагрузки
        sleep(0.1)

if __name__ == "__main__":
    main_loop()