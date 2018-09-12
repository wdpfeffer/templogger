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


def printHeader():
    roms = ds.scan()
    headStr = ''
    for rom in roms:
        headStr += '{:15s}'.format(get_probe_no(rom))  # build a header
    print(headStr)


def print_all_temps():
    ds.convert_temp()
    roms = ds.scan()
    
    tmpStr = ''
    m = 0
    n = 0
    fs = ''
    for rom in roms:
        if m == 0:
            n = m
            fs='{:0.2f}'
            # print(fs)
        else:
            n = 20-len(tmpStr)
            fs = '{:' + str(n) + '.2f}'
            # print(fs)
        m += 1
        tmpStr += fs.format(ds.read_temp(rom))
        
    print(tmpStr)


def scrollTemps():
    n = 0
    while True:
        if n == 0:
            printHeader()
        n += 1
        if n > 20:
            n = 0
        print_all_temps()
        time.sleep(1)


def get_temps():
    ds.convert_temp()
    roms = ds.scan()
    temps=[]
    for rom in roms:
        probe_id = get_probe_no(rom)
        temp = ds.read_temp(rom)
        temps.append((probe_id, temp))

    return temps


# todo determine if these lines are needed for thaw temp probe to run
ow = onewire.OneWire(Pin(12))  # onewire device conneceted ot pin 12
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
time.sleep_ms(750)
