'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

from ctypes import *

msvcrt = cdll.msvcrt

raw_input("Enter any key once debugger is attached.")

buffer = c_char_p("AAAAA")

overflow = "A" * 100

msvcrt.strcpy(buffer, overflow)
