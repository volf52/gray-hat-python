'''
Created on 28 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''
from ctypes import *
from my_debugger_defines import *

kernel32 = windll.kernel32


class debugger():
    def __init__(self):
        self.h_process = None
        self.pid= None
        self.debugger_active = False
    
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
            
            self.h_process = self.open_process(process_information.dwProcessId)
        
        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError()
        
    def open_process(self, pid):
        return kernel32.OpenProcess(PROCESS_ALL_ACCESS, pid, False)
    
    def attach(self, pid):
        
        self.h_process = self.open_process(pid)
        
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active = True
            self.pid = int(pid)
            self.run()
        else:
            print "[*] Unable to attach to the process."
    
    def run(self):
        
        while self.debugger_active:
            self.get_debug_event()
    
    def get_debug_event(self):
        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE
        
        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            raw_input("Press a key to continue...")
            self.debugger_active = False
            kernel32.ContinueDebugEvent(debug_event.dwProcessId, debug_event.dwThreadId, continue_status)
    
    def detach(self):
        
        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "There was an error."
            return False
    
        
             
        
        