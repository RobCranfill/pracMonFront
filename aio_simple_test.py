# test of adafruit iot lib
# robcranfill
# first arg must by AdafruitIO key
# like this: python aio_simple_test.py `cat aio_secret.text`

import sys

# Import library and create instance of REST client.
from Adafruit_IO import Client


if len(sys.argv) != 2:
    print(f"Run with: {sys.argv[0]} API_KEY")
    sys.exit(1)
aio_key = sys.argv[1]

DATA_BLORT = "1\t2\t12:34:00 11/10/2023\t12:35:00 11/10/2023"

# Should I use a "group?" Maybe not.
# How is this name supposed to be formatted? nethier "/" nor "." work.
# FEED_NAME = "PracticeMonitor.perfdata"

# This works for a feed in the "Default" group
FEED_NAME = "perfdata"

try:
    aio = Client("robcranfill", aio_key)
    print("client OK")

    # # Send some data to the feed .
    # no, don't
    # aio.send(FEED_NAME, DATA_BLORT)
    # print("send OK")

    data = aio.data("perfdata")
    for d in data:
        print(f" - '{d.value}'")

except Exception as e:
    print(e)
    print("Ouch!")
