from machine import Pin, I2C
# I2C Configuration
# for KC868-A16 Rev.: 1.6 
# 0x24(36 1----8) 0x25(37 9----16) OUT
# 0x21(33 9----16) 0x22(34 1----8) IN
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=100000)
pcf8574_address = 36

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

