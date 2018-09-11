import time
import ds18x20
import onewire
from machine import Pin


def get_probe_no(addr):
    s = str(addr)
    vs = s.split("\\x")
    ns = ""

    for x in range(1, len(vs)):
        ns += vs[x]

    ns = ns.replace("')", "")

    return ns


def print_all_temps():
    ds.convert_temp()
    roms = ds.scan()
    for rom in roms:
        probe_id = get_probe_no(rom)
        temp = ds.read_temp(rom)
        print('id', probe_id, 'temp', temp)


def get_temps():
    ds.convert_temp()
    roms = ds.scan()
    temps=[]
    for rom in roms:
        probe_id = get_probe_no(rom)
        temp = ds.read_temp(rom)
        temps.append((probe_id, temp))

    return temps


ow = onewire.OneWire(Pin(12))  # onewire device conneceted ot pin 12
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
time.sleep_ms(750)
