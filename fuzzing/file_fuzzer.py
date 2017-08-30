'''
Created on 30 Aug 2017

@author: Muhammad Arslan <rslnkrmt2552@gmail.com>
'''

from pydbg import *
from pydbg.defines import *

import utils
import random
import sys
import struct
import threading
import os
import shutil
import time
import getopt

class file_fuzzer:
    
    def __init__(self, exe_path, ext):
        
        self.exe_path = exe_path
        self.ext = ext
        self.orig_file = None
        self.mutated_file = None
        self.iteration = 0
        self.crash = None
        self.pid = None
        self.in_accessv_handler = False
        self.dbg = None
        self.running = False
        self.ready = False
        self.test_cases = ["%s%n%s%n%s%n", "\xff", "\x00", "A"]
    
    def file_picker(self):
        file_list = os.listdir("examples/")
        list_length = len(file_list)
        file = file_list[random.randint(0, list_length-1)]
        shutil.copy("examples\\%s" % file, "test.%s" % self.ext)
        
        return file
    
    def fuzz(self):
        
        while True:
            
            if not self.running:
                self.test_file = self.file_picker()
                self.mutate_file()
                
                pydbg_thread = threading.Thread(target=self.start_debugger)
                pydbg_thread.setDaemon(0)
                pydbg_thread.start()
                
                while self.pid == None:
                    time.sleep(1)
                
                moniter_thread = threading.Thread(target = self.moniter_debugger)
                moniter_thread.setDaemon(0)
                moniter_thread.start()
                
                self.iteration += 1
            
            else:
                time.sleep(0)
    
    def start_debugger(self):
        print "[*] Starting debugger for iteration: %d" % self.iteration
        self.running = True
        self.dbg = pydbg()
        
        self.dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, self.check_accessv)
        pid = self.dbg.load(self.exe_path, "test.%s" % self.ext)
        self.pid = self.dbg.pid
        self.dbg.run()
    
    
    def check_accessv(self, dbg):
        '''
        Access violation handler to trap crash info.
        '''
        if dbg.dbg.u.Exception.dwFirstChance:
            return DBG_CONTINUE
        
        print "[*] Woot! Handling an access violation!"
        self.in_accessv_handler = True
        crash_bin = utils.crash_binning.crash_binning()
        crash_bin.record_crash(dbg)
        self.crash = crash_bin.crash_synopsis()
        
        crash_fd = open("crashes\\crash-%d" % self.iteration, "w")
        crash_fd.write(self.crash)
        crash_fd.close()
        
        shutil.copy("test.%s" % self.ext, "crashes\\%d.%s" % (self.iteration, self.ext))
        shutil.copy("examples\\%s" % self.test_file, "crashes\\%d_orig.%s" % (self.iteration, self.ext))
        
        self.dbg.terminate_process()
        self.in_accessv_handler = False
        self.running = False
        
        return DBG_EXCEPTION_NOT_HANDLED
    
    def moniter_debugger(self):
        counter = 0
        print "[*] Moniter thread for pid: %d waiting." % self.pid
        while counter < 3:
            time.sleep(1)
            print counter
            counter += 1
        
        if self.in_accessv_handler != True:
            time.sleep(1)
            self.dbg.terminate_process()
            self.pid = None
            self.running = False
        else:
            print "[*] The access violation handler is doing it's bussiness. Waiting..."
            
            while self.running:
                time.sleep(1)
    
    def mutate_file(self):
        fd = open("test.%s" % self.ext, "rb")
        stream = fd.read()
        fd.close()
        
        test_case = self.test_cases[random.randint(0, len(self.test_cases) - 1)]
        stream_length  = len(stream)
        rand_offset = random.randint(0, stream_length - 1)
        rand_len = random.randint(0, 100)
        
        test_case = test_case * rand_len
        
        fuzz_file = stream[:rand_offset]
        fuzz_file += str(test_case)
        fuzz_file += stream[rand_offset:]
        
        fd = open("test.%s" % self.ext, "wb")
        fd.write(fuzz_file)
        fd.close()
    
        return
    
def print_usage():
    print "[*]"
    print "[*] file_fuzzer.py -e <Executable Path> -x <File Extension>"
    print "[*]"
        
    sys.exit(0)

if __name__ == "__main__":
    print "[*] Generic File Fuzzer."
    try:
        opts, argo = getopt.getopt(sys.argv[1:], "e:x")
    except getopt.GetoptError:
        print_usage()
    
    exe_path = None
    ext = None
    
    for o,a in opts:
        if o == "-e":
            exe_path = a
        elif o == "-x":
            ext = a
        
        if exe_path is not None and ext is not None:
            fuzzer = file_fuzzer(exe_path, ext)
        else:
            print_usage()
             
                    