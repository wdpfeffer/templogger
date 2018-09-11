# This file is executed on every boot (including wake-boot from deepsleep)

import esp, network, gc, time, webrepl, machine
esp.osdebug(None)
gc.collect()


# print instructions for how to prevent webrepl form loading
print("To prevent Webrepl load, press ctrl-c in next 20 seconds")
n = 0
while n < 20:
  print(n)
  n += 1
  time.sleep(1)


#Attach to network
def getKey(item):
  return item[3]

sta=network.WLAN(network.STA_IF)
# ap=network.WLAN(network.AP_IF)
sta.active(True)
stations=sta.scan()
stations=sorted(stations,key=getKey)
pw=""
staName=""

for station in stations:
  staName=station[0].decode('utf-8')
  if (staName=="RMBio2_EXT"):
    pw="Lipid123"
    break
  if (staName=="RMBioPrivate"):
    pw="Lipid123!"
    break
  if (staName=="1-FBIsurveillance"):
    pw="tInKtHEGoAt06"
    break

if pw != "":
  sta.ifconfig(('10.211.224.200','255.255.255.0','10.211.224.1','8.8.8.8'))
  sta.connect(staName,pw)
else:
  print("pw not set")

# set a counter and reboot if connection takes longer than 30s
n=0
while pw !='' and not sta.isconnected():
  print("Connecting")
  time.sleep(1)
  n+=1
  if n>30:
    machine.reset()

# start webrepl
if sta.isconnected():
  print("Connected")
  time.sleep(5)
  webrepl.start()

