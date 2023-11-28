# generate some good-looking data!
# robcranfill
# sys.arg[1] must be Adafruit AIO API key

import datetime
import json
import random
import sys
import time

from Adafruit_IO import Client



# This works for a feed in the "Default" group
# FEED_NAME = "test_data_1"


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


def send_data(api_key, feed, data):
    try:
        aio = Client("robcranfill", api_key)
        print("client OK")
    except Exception as e:
        print(e)
        print("Bummer!")

    throttle = 1.0
    print(f"* Sending {len(data)} session records to feed '{feed}', throttled by {throttle} seconds....")
    i = 0
    for d in data:
        i += 1
        print(f"sending data record {i}")
        aio.send(feed, d)
        time.sleep(throttle)
    print("send OK")


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Must provide API key & feed key!")
        sys.exit(1)
    api_key = sys.argv[1]
    feed_key = sys.argv[2] # note: feed "key", not "name"!

    all_days = []
    for d_gen in range(1, 31):
        day_data = generate_json_test_data(year=2023, month=10, day=d_gen, hour=8)
        # print(f"Generated {len(day_data)} data points:\n{day_data}")
        all_days += day_data

    # print(f"* All days: {len(all_days)} sessions:\n{all_days}")

    send_data(api_key, feed_key, all_days)

    print("done!")
