#!/usr/bin/env python3

import sys
import os
import glob
from datetime import datetime
import hashlib

class Z2scanner:
    def __init__(self, sig):
        self.sig = sig
        self.scan_dir = 0
        self.version = "0.0.1"

    def setopt(self, opt):
        if opt == '-d':
            self.scan_dir = 1
        else:
            print("invalid option %s" % opt)

    def scan(self, scan_path):
        if not os.path.exists(scan_path):
            print("%s: No such file or directory" % scan_path)
            return

        if self.scan_dir:
            if os.path.isdir(scan_path):
                file_list = [_ for _ in glob.glob(
                    "%s/**" % scan_path, recursive=True) if os.path.isfile(_)]
            else:
                print("%s is not directory" % scan_path)
                return
        else:
            if os.path.isfile(scan_path):
                file_list = [scan_path]
            else:
                print("%s is not regular file" % scan_path)
                return

        self.result = [self.match(_) for _ in file_list]

    def match(self, filename):
        output_format = "target_path:%s\tscanner_version:%s\tscan_date: %s\tis_malicious:%s\treason_method:%s"
        md5 = hashlib.md5()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(2048 * md5.block_size), b''):
                md5.update(chunk)
                checksum = md5.hexdigest()
            if self.sig == checksum:
                reason_method = "Embedded-Signatures"
            else:
                reason_method = ""
        return output_format % (filename, self.version, datetime.today().strftime("%Y-%m-%d_%H-%M-%S"), bool(reason_method), reason_method)

    def print(self):
        if hasattr(self, 'result'):
            [print(_) for _ in self.result]


def main(argv):
    scanner = Z2scanner('26cd7ef06f358bdb5bf20f109f41aead')

    for arg in argv:
        if arg[0] == '-':
            scanner.setopt(arg)
        else:
            scanner.scan(arg)
    scanner.print()


if __name__ == '__main__':
    main(sys.argv[1:])
