'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''
from pydbg import *
from pydbg.defines import *

import struct
import random

def printf_randomizer(dbg):
    parameter_addr = dbg.context.Esp + 0x8
    counter = dbg.read_process_memory(parameter_addr, 4)
    
    counter = struct.unpack("L", counter)[0]
    print "Counter %d" % int(counter)
    
    random_counter = random.randint(1, 100)
    random_counter = struct.pack("L", random_counter)[0]
    
    dbg.write_process_memory(parameter_addr, random_counter)
    
    return DBG_CONTINUE

dbg = pydbg()

pid = raw_input("Enter the printf_loop.py PID: ")

dbg.attach(int(pid))

printf_address = dbg.func_resolve("msvcrt", "printf")
dbg.bp_set(printf_address, description="printf__address", handler=printf_randomizer)

dbg.run()