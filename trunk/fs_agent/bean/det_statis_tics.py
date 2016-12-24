# -*- coding: utf-8 -*-

# project: fshell
# author: s0nnet
# time: 2016-12-13
# desc: detection statistics 
# the kernel algorithm are learning
# from neopi.py and thanks for @Neohapsis.


import sys
import os
import re
import csv
import zlib
import math
from collections import defaultdict

if __name__ == "__main__":
    sys.path.append("../base")

from fs_base_cfg import *
from fsa_task import *
from fsa_task_type import *
   




class LanguageIC:
    def __init__(self):
        self.char_count = defaultdict(int)
        self.total_char_count = 0
        self.results = []
        self.ic_total_results = ""

    def calculate(self, data, filename):
        if not data: return 0
        char_count = 0
        total_char_count = 0

        for x in range(256):
            char = chr(x)
            charcount = data.count(char)
            char_count += charcount * (charcount - 1)
            total_char_count += charcount

        ic = float(char_count)/(total_char_count * (total_char_count - 1))
        return ic


class Entropy:
    def __init__(self):
        self.results = []

    def calculate(self, data, filename):
        if not data: return 0
        entropy = 0
        self.stripped_data = data.replace(' ', '')
        for x in range(256):
            p_x = float(self.stripped_data.count(chr(x)))/len(self.stripped_data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy


class LongestWord:
    def __init__(self):
        self.results = []

    def calculate(self, data, filename):
        if not data:
            return "", 0
        longest = 0
        longest_word = ""
        words = re.split("[\s,\n,\r]", data)
        if words:
            for word in words:
                length = len(word)
                if length > longest:
                    longest = length
                    longest_word = word
        return longest


class Compression:
    def __init__(self):
        self.results = []

    def calculate(self, data, filename):
        if not data:
            return "", 0
        compressed = zlib.compress(data)
        ratio = float(len(compressed)) / float(len(data))
        return ratio






class SearchFile:
    
    def search_file_path(self, web_dir, regex):
        for root, dirs, files in os.walk(web_dir):
            for file in files:
                filename = os.path.join(root, file)

                if (re.search(regex, filename)) and (os.path.getsize(filename) > BaseConf.SMALLEST_FILESIZE):
                    try:
                        data = open(root + "/" + file, 'rb').read()
                    except:
                        data = False
                        print "Could not read file :: %s/%s" % (root, file)
                    yield data, filename


class FsaTaskStatics:
    
    def __init__(self):
        self.web_dir = BaseConf.WEB_DIR
        self.out_file = BaseConf.CACHE_DIR + "/" + BaseConf.STATICS_RESULT
        scan_file_ext = BaseConf.SCAN_FILE_EXT
        ext_regex = scan_file_ext.replace(".", "\.")
        self.regex = re.compile("(%s)$" % (ext_regex))

    tests = []
    tests.append(LanguageIC())
    tests.append(Entropy())
    tests.append(LongestWord())
    tests.append(Compression())

    locator = SearchFile()

    # CSV file output array
    csv_array = []

    # Grab the file and calculate each test against file
    for data, filename in locator.search_file_path(web_dir, regex):
        if not data: continue
        
        # a row array for the CSV
        csv_row = []
        csv_row.append(filename)

        for test in tests:
            calculated_value = test.calculate(data, filename)
            csv_row.append(calculated_value)
        csv_array.append(csv_row)
    
    fileOutput = csv.writer(open(out_file, "wb"))
    fileOutput.writerows(csv_array)





