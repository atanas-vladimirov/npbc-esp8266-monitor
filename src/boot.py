# This file is executed on every boot (including wake-boot from deepsleep)

import gc
#import esp
import uos
import machine
import webrepl
import network
import ntptime

# Note:
# By default, UART0 outputs some printed information when the device is powered
# on and booting up.
# The baud rate of the printed information is relevant to the frequency of the
# external crystal oscillator. If the frequency of the crystal
# oscillator is 40 MHz, then the baud rate for printing is 115200;
# if the frequency of the crystal oscillator is 26 MHz,
# then the baud rate for printing is 74880.

gc.collect()
machine.freq(160000000)  # set the CPU frequency to 160 MHz
# uos.dupterm(None, 1)  # disable REPL on UART(0)
# uart1 = machine.UART(1, baudrate=74880) # 26 MHz crystal oscillator
# esp.osdebug(1)
# uos.dupterm(uart1, 1) # enable REPL on UART(1) as read-only (for debugging)
webrepl.start()


# helper function to view file contents from commandline
def cat(Filename):
    f = open(Filename)
    print(f.read())
    f.close()


# ls
def ls():
    d = uos.listdir()
    return d


# Start wifi
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('whitebox', 'nexus@home')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
do_connect()

# synchronize with ntp
ntptime.host = 'bg.pool.ntp.org'
ntptime.settime()  # set the rtc datetime from the remote server
