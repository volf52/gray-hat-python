'''
Created on 28 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

import my_debugger

debugger = my_debugger.debugger()

pid = raw_input("Enter the PID of the process to attach to: ")
debugger.attach(int(pid))
debugger.detach()