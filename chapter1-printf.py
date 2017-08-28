'''
Created on Aug 27, 2017

@author: Muhammad Arslan<rslnkrmt2552@gmail.com>
'''

from ctypes import *

libc = CDLL("libc.so.6")
message_string = "Hello World!"
libc.printf("Testing %s", message_string)