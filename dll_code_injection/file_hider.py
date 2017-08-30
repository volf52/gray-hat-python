'''
Created on 30 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

import sys

try:
    fd = open(sys.argv[1], "rb")
    dll_contents = fd.read()
    fd.close()
    print "[*] Filesize: %d" % len(dll_contents)
    fd = open("%s:%s" (sys.argv[2], sys.argv[1]), "wb")
    fd.write(dll_contents)
    fd.close()
except:
    print "[***] Usage:\n[***] ./file_hider.py <DLL_Path> <File to hide in>"
    sys.exit(0)