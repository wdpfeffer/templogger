import time
import machine
import network
import socket
import logger_cfg as lcfg
import OneWire as ow


def go_deep_sleep(sleeptime):
    st = sleeptime * 1000  # must be in milliseconds
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, st)
    machine.deepsleep()


# connect to socket
def connect_socket(addr):
    s = socket.socket()
    print("Socket created")
    s.connect(addr)
    time.sleep(1)
    print("Socket connected")

    return s

def send_to_server(sAddr):
	print(sAddr)
	#get address info
	_, _, host, path = sAddr.split('/', 3)
	print("host", host)
	print("path", path)
	addr = socket.getaddrinfo(host, 5000)[0][-1]
	print("addr", addr)
	first_run = True
	s = connect_socket(addr)
	s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
	#msg = s.recv(100).decode('utf-8')
	while True:
            data = s.recv(100)
            if "ready" in data:
                print("ready")
            else:
                break
        
        s.close()
 
def start_data(sAddr, sEvent, sDuration):
    print(sAddr)
    # set socket address
    addr = socket.getaddrinfo(sAddr, 5000)[0][-1]
    try:
        s = connect_socket(addr)
        first_run = True
        while True:
            # make sure server is ready
            msg = s.recv(100).decode('utf-8')
            if msg == "ready":
                ts = str(sEvent)+","
                temps = os.get_temps()
                for temp in temps:
                    ts += temp[0] + "," + str(temp[1]) + ","

                # send the temperatures
                if not first_run:
                    # do not send first run
                    s.send(ts.encode('utf-8'))
                s.close()
                if not first_run:
                    # do a normal sleep
                    time.sleep(sDuration)
                else:
                    # first run, only sleep 5 seconds before next read
                    time.sleep(5)
                if first_run:
                    first_run = False
                s = connect_socket(addr)
                time.sleep(1)
                # GoDeepSleep(60) #shut off for 1 minutes

    except:
        print('exception occured')
        # GoDeepSleep(5)


def start():
    # get previous address

    ans = input("Previous addr was %s, keep(k) or change(c): " % lcfg.addr)
    print(ans)
    if ans == ('c' or 'C'):
        lcfg.addr = input('What is new address? ')
        cans = False
        while not cans:
            reply = input('Is %s this the correct address (y or n): ' % lcfg.addr)
            if reply == ('n' or 'N'):
                lcfg.addr = input('What is the addr? ')
            else:
                cans = True

                # get previous collection

    ans = input("Previous collection time was %s, keep(k) or change(c): " % lcfg.collect_time)
    print(ans)
    if ans == ('c' or 'C'):
        lcfg.collect_time = int(input('What is new collect time? '))
        cans = False
        while not cans:
            reply = input('Is %s this the correct collection time (y or n): ' % lcfg.collect_time)
            if reply == ('n' or 'N'):
                lcfg.collect_time = int(input('What is the collection time? '))
            else:
                cans = True

            # get previous event number

    ans = input("Previous event number was %s, keep(k) or change(c): " % lcfg.event_no)
    print(ans)
    if ans == ('c' or 'C'):
        lcfg.event_no = int(input('What is new event number? '))
        cans = False
        while not cans:
            reply = input('Is %s this the correct event number (y or n): ' % lcfg.event_no)
            if reply == ('n' or 'N'):
                lcfg.event_no = int(input('What is the event number? '))
            else:
                cans = True

    f = open('logger_cfg.py', 'w')
    f.write('collect_time = %i' % lcfg.collect_time)
    f.write('\n')
    f.write('addr = \'%s\'' % lcfg.addr)
    f.write('\n')
    f.write('event_no = %i' % lcfg.event_no)
    f.close()

    start_data(lcfg.addr, lcfg.event_no, lcfg.collect_time)
