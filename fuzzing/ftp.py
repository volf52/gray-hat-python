'''
Created on 30 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

from sulley import *

s_initialize("user")
s_static("USER")
s_delim(" ")
s_string("volf")
s_static("\r\n")

s_initialize("pass")
s_static("PASS")
s_delim(" ")
s_string("volf")
s_static("\r\n")

s_initialize("cwd")
s_static("CWD")
s_delim(" ")
s_string("c: ")
s_static("\r\n")

s_initialize("dele")
s_static("DELE")
s_delim(" ")
s_string("c:\\test.txt")
s_static("\r\n")

s_initialize("mdtm")
s_static("MDTM")
s_delim(" ")
s_string("C:\\boot.ini")
s_static("\r\n")

s_initialize("mkd")
s_static("MKD")
s_delim(" ")
s_string("C:\\TESTDIR")
s_static("\r\n")