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

# This works for a feed in the "Default" group
FEED_NAME = "perfdata"
# How is this name supposed to be formatted? netier "/" nor "." work.
# FEED_NAME = "PracticeMonitor.perfdata"

try:
    aio = Client("robcranfill", aio_key)
    print("client OK")

    # Send the value 100 to a feed called "perfdata".
    aio.send(FEED_NAME, DATA_BLORT)
    print("send OK")

    # Retrieve the most recent value from the feed "Foo".
    # Access the value by reading the `value` property on the returned Data object.
    # Note that all values retrieved from IO are strings so you might need to convert
    # them to an int or numeric type if you expect a number.

    data = aio.receive("perfdata")
    print(f"Received value: '{data}'")

except Exception as e:
    print(e)
    print("Ouch!")
