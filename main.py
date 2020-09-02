import smbus
import time

bus = smbus.SMBus(1)


def read_double(addr):
    A = bus.read_byte_data(addr)