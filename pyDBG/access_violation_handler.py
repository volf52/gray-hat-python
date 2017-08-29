'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''


from pydbg import *
from pydbg.defines import *

import utils

def check_accessv(dbg):
    if dbg.dbg.u.Exception.dwFirstChance:
        return DBG_EXCEPTION_NOT_HANDLED
    
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print crash_bin.crash_synopsis()
    
    dbg.terminate_process()
    return DBG_EXCEPTION_NOT_HANDLED

pid = raw_input("Enter the process ID: ")
dbg = pydbg()
dbg.attach(int(pid))
dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, check_accessv)
dbg.run()

