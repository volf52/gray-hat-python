'''
Created on 28 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32


class debugger():
    def __init__(self):
        pass
    
    def load(self, path_to_exe):
        
        #set creation_flags = CREATE_NEW_CONSOLE to see GUI 
        creation_flags = DEBUG_PROCESS
        
        startupinfo = STARTUPINFO()
        process_information = PROCESS_INFORMATION()
        
        # Allow the started process to be shown as a seperate window
        startupinfo.dwFlags = 0x1
        startupinfo.wShowWindow = 0x0 
        startupinfo.cb = sizeof(startupinfo)
        
        if kernel32.CreateProcessA(path_to_exe, 
                                   None,
                                   None,
                                   None,
                                   None,
                                   creation_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] We have successfully launched the process!"
            print "[*] PID : %d" % process_information.dwProcessId
        
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError()
        