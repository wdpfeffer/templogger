import os, machine, esp, utime


def logger(lgstr):
    f = open('log.txt','a+')
    f.write(lgstr+"\n")
    f.close()

# Loop count
n = 0

if machine.reset_cause()==machine.DEEPSLEEP_RESET:
    logger("Deepsleep Reset Count")
    utime.sleep(1)
    rtc=machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0, 60000)
    machine.deepsleep()
    
else:
    logger("Normal Reset")
