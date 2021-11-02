import gc
import time
import machine
import urequests as requests

import onewire
import ds18x20
import bmp280 as bmp
from max6675 import MAX6675
import uartworker0


# max6675 K-type thermocouple
def ktype():
  so = machine.Pin(12, machine.Pin.IN)
  sck = machine.Pin(14, machine.Pin.OUT)
  cs = machine.Pin(15, machine.Pin.OUT)
  max6675 = MAX6675(sck, cs, so)
  result = {'KTYPE': max6675.read()}
  return result


# BMP280
def bosh():
  i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4), freq=10000)

  try:
    b = bmp.BMP280(i2c)
    b.use_case(bmp.BMP280_CASE_WEATHER)
    b.oversample(bmp.BMP280_OS_HIGH)
    b.temp_os = bmp.BMP280_TEMP_OS_8
    b.press_os = bmp.BMP280_PRES_OS_4
    result = {'TBMP': round(b.temperature, 2), 'PBMP': (b.pressure/100)}

  except OSError:
    return {'TBMP': 0, 'PBMP': 0}

  return result


# ds18s20
def ow():
  ds_Pin = machine.Pin(0)
  ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_Pin))
  roms = ds_sensor.scan()
  ds_sensor.convert_temp()
  time.sleep_ms(750)
  result = {'TDS18': round(ds_sensor.read_temp(roms[0]), 2)}
  return result

try:
  while True:

    returning_watter = ow()
    exhaust_gases = ktype()
    external_wheather = bosh()
    rb20 = uartworker0.run()

    result = returning_watter.copy()
    result.update(exhaust_gases)
    result.update(external_wheather)
    result.update(rb20)
    print(result)

    try:
      r = requests.post('http://172.16.1.1:8089/post', json=result)

    except:
      print("The host is unreachable")

    result = {}
    gc.collect()

    time.sleep(30)

except Exception as e:
  err = e
