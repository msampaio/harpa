#!/usr/bin/env python

import pandas
import os
import socket


def load_csv(filename='harp.csv'):
    hostname = socket.gethostname()
    if "webfaction.com" in hostname:
        f = os.path.join('/home/genos/webapps/harp/harp', 'csv', filename)

    else:
        f = os.path.join('csv', filename)
    return pandas.DataFrame.from_csv(f)
