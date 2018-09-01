#!/usr/bin/python
import sys
import os
import aliaxer.cli.main as app

here = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    sys.exit(app.controller(here))
