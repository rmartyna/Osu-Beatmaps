from __future__ import print_function
import sys
from init import *


def error_msg(msg, err):
    print(msg, file=sys.stderr)
    if err is not None:
        try:
            ERROR_LOG.write(msg + '\n' + str(err) + '\n\n')
        except Exception as e:
            print('CANNOT WRITE INTO ERROR LOG.', file=sys.stderr)
            print(str(e))