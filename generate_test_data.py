# generate some good-looking data!
# robcranfill
# sys.arg[1] must be Adafruit AIO API key

import datetime
import json
import random
import sys
import time

from Adafruit_IO import Client


if len(sys.argv) != 2:
    print("Must provide API key!")
    sys.exit(1)
api_key = sys.argv[1]

# This works for a feed in the "Default" group
FEED_NAME = "perfdata"

# How is this name supposed to be formatted? neither "/" nor "." work.
# FEED_NAME = "PracticeMonitor.perfdata"
# Perhaps all lower case would have worked. Not sure I want to use a group anyway.
#
# >>> from Adafruit_IO import Client
# >>> aio = Client("robcranfill", "XXX")
# >>> f = aio.feeds()
# >>> f
# [Feed(name='perfdata', key='perfdata', id=2660025, description='Feed for PerformanceMonitor project.', 
# unit_type=None, unit_symbol=None, history=True, visibility='private', license=None, status_notify=False, 
# status_timeout=4320), 
# Feed(name='perfdata', key='practicemonitor.perfdata', id=2660022, description='', 
# unit_type=None, unit_symbol=None, history=True, visibility='private', license=None, status_notify=False, 
# status_timeout=4320)]
#


JSON_KEY_START  = "SeshStart"
JSON_KEY_LENGTH = "SeshLength"
JSON_KEY_NOTES  = "SeshNotes"

def format_as_json(session_start_str, session_length_sec, session_notes):

    one_record = [{ 
                    JSON_KEY_START:  session_start_str,
                    JSON_KEY_LENGTH: session_length_sec,
                    JSON_KEY_NOTES:  session_notes
                    }]
    return json.dumps(one_record)


# create some semi-random session data
# return a list of JSON strings: the data

# generate data for one day, starting at indicated time
#
def generate_json_test_data(year=2023, month=1, day=1, hour=9):

    t_start = datetime.datetime(year, month, day, hour)
    # print(f"Generate data starting {t_start} = {t_start.strftime('%s')}")

    result = []
    for i in range(random.choice([0, 1, 2, 2, 2, 3, 3, 3, 4, 4])): # number of sessions

        gap_sec = random.randint(600, 60*60*2)
        t_start += datetime.timedelta(seconds=gap_sec)

        duration_sec = random.randint(600, 3600)
        keypresses = random.randint(1000, 10000)
        # print(f" - Session {i}: {t_start} for {datetime.timedelta(seconds=duration_sec)} "
        #       f"(gap {datetime.timedelta(seconds=gap_sec)})")

        json = format_as_json(t_start.isoformat(), duration_sec, keypresses)
        result.append(json)

        t_start += datetime.timedelta(seconds=duration_sec)

    return result


def send_data(api_key, data):
    try:
        aio = Client("robcranfill", api_key)
        print("client OK")

        for d in data:
            aio.send(FEED_NAME, d)
        print("send OK")

    except Exception as e:
        print(e)
        print("Bummer!")

all_days = []
for d_gen in range(1, 8):
    day_data = generate_json_test_data(year=2023, month=10, day=d_gen, hour=8)
    print(f"Generated {len(day_data)} data points:\n{day_data}")
    all_days += day_data

print(f"* All days: {len(all_days)} sessions:\n{all_days}")

print("NOT sending!")
send_data(api_key, all_days)
