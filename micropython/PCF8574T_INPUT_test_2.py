from machine import Pin, I2C
import time

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


while True:
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
    bit_position = 3
    if state & (1 << bit_position):
        print("port4 ", 1)
    else:
        print("port4 ", 0)
    bit_position = 4
    if state & (1 << bit_position):
        print("port5 ", 1)
    else:
        print("port5 ", 0)
    bit_position = 5
    if state & (1 << bit_position):
        print("port6 ", 1)
    else:
        print("port6 ", 0)
    bit_position = 6
    if state & (1 << bit_position):
        print("port7 ", 1)
    else:
        print("port7 ", 0)
    bit_position = 7
    if state & (1 << bit_position):
        print("port8 ", 1)
    else:
        print("port8 ", 0)
    print("NEXT PORTS")
    """NEXT CHANNEL INPUT"""
    state = read_ports_ch1()
    bit_position = 0
    if state & (1 << bit_position):
        print("port9 ", 1)
    else:
        print("port9 ", 0)
    bit_position = 1
    if state & (1 << bit_position):
        print("port10 ", 1)
    else:
        print("port10 ", 0)
    bit_position = 2
    if state & (1 << bit_position):
        print("port11 ", 1)
    else:
        print("port11 ", 0)
    bit_position = 3
    if state & (1 << bit_position):
        print("port12 ", 1)
    else:
        print("port12 ", 0)
    bit_position = 4
    if state & (1 << bit_position):
        print("port13 ", 1)
    else:
        print("port13 ", 0)
    bit_position = 5
    if state & (1 << bit_position):
        print("port14 ", 1)
    else:
        print("port14 ", 0)
    bit_position = 6
    if state & (1 << bit_position):
        print("port15 ", 1)
    else:
        print("port15 ", 0)
    bit_position = 7
    if state & (1 << bit_position):
        print("port16 ", 1)
    else:
        print("port16 ", 0)
    print("*********************FINISH*********************")
    time.sleep(1)  # Ждем 1 секунду перед следующим считыванием