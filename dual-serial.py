import os
import random
import string
import threading

import serial
from serial.tools.list_ports import comports

bytes = 10000
speed = 115200
timeout = 4
good = 'OK'
bad = 'FAIL:'

def testAworker(com, data):
    received = com.read(bytes)

    if received == data:
        print good
    else:
        print bad, str(len(received)) + 'B received'

def testA(port, com1, com2):
    data = os.urandom(bytes)
    worker = threading.Thread(target=testAworker, args=(com2, data))
    worker.start()
    print '    Writing data to ' + port + '...',
    com1.write(data)
    worker.join()

def testB(port, com1, com2):
    print '    Enabling DTR on ' + port + '...',
    com1.setDTR(True)
    cd = com2.getCD()
    dsr = com2.getDSR()

    if cd and dsr:
        print good
    else:
        print bad, 'no',
        if not cd:
            print 'CD',
        if not dsr:
            print 'DSR',
        print

    com1.setDTR(False)

def testC(port, com1, com2):
    print '    Enabling RTS on ' + port + '...',
    com1.setRTS(True)
    cts = com2.getCTS()
    ri = com2.getRI()

    if cts and ri:
        print good
    else:
        print bad, 'no',
        if not cts:
            print 'CTS',
        if not ri:
            print 'RI',
        print

    com1.setRTS(False)

def test(port1, port2):
    print 'Testing ' + port1 + ' and ' + port2 + ':'

    com1 = serial.Serial('\\\\.\\' + port1, speed, timeout=timeout)
    com2 = serial.Serial('\\\\.\\' + port2, speed, timeout=timeout)

    testA(port1, com1, com2)
    testA(port2, com2, com1)
    testB(port1, com1, com2)
    testB(port2, com2, com1)
    testC(port1, com1, com2)
    testC(port2, com2, com1)

    com1.close()
    com2.close()

    print 'DONE\n'

print (
    'Data length is ' + str(bytes) + 'B, baud rate is ' + str(speed) +
    'bps and timeout is ' + str(timeout) + 's.\n'
)
ports = {}

for port in comports():
    if (
        port[2] in ports and 
        abs(int(ports[port[2]][0][3:]) - int(port[0][3:])) == 1
    ):
        test(ports[port[2]][0], port[0])
        del ports[port[2]]
    else:
        ports[port[2]] = port

print 'Press Enter to continue'
raw_input()
