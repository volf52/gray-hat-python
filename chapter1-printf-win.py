'''
Created on 27 Aug 2017

@author: volf
'''

from ctypes import *

msvcrt = cdll.msvcrt
message_string = "Hello World!\n"
msvcrt.printf("Testing: %s", message_string)