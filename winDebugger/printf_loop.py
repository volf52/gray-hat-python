'''
Created on 29 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

from ctypes import *
import time

msvcrt = cdll.msvcrt
counter = 0

while True:
    msvcrt.printf("Loop iteration %d!\n" % counter)
    time.sleep(2)
    counter += 1