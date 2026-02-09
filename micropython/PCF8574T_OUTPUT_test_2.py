from machine import Pin, WDT, reset, I2C, ADC
import time

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


set_p1(0)
set_p2(0)
set_p3(0)
set_p4(0)
set_p5(0)
set_p6(0)
set_p7(0)
set_p8(0)
"""set next port"""
set_p9(1)
set_p10(0)
set_p11(0)
set_p12(0)
set_p13(0)
set_p14(0)
set_p15(0)
set_p16(0)
