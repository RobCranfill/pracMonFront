# dunmp adafruit iot data to CSV file?
# robcranfill
# sys.arg[1] must be Adafruit AIO API key

import json
import random
import sys
import time

from Adafruit_IO import Client


if len(sys.argv) != 2:
    print("Must provide API key!")
    sys.exit(1)
api_key = sys.argv[1]

# This works for a feed in the "Default" group; fine
FEED_NAME = "perfdata"


# As per main code. Refactor?
JSON_KEY_TS     = "SeshNumber"
JSON_KEY_START  = "SeshStart"
JSON_KEY_END    = "SeshEnd"
JSON_KEY_NOTES  = "SeshNotes"

def format_as_json(total_sessions, session_start_sec, session_end_sec, session_notes):

    one_record = [{ JSON_KEY_TS:    total_sessions,
                    JSON_KEY_START: time.ctime(session_start_sec),
                    JSON_KEY_END:   time.ctime(session_end_sec),
                    JSON_KEY_NOTES: session_notes
                    }]
    return json.dumps(one_record)


def dump_data(api_key):
    try:
        aio = Client("robcranfill", api_key)
        print("client OK")

        # Get list of feeds and print the names, for fun.
        feeds = aio.feeds()
        for f in feeds:
            print(f"Feed: {f.name}")


        # Get an array of all data from feed 'Test'
        data = aio.data(FEED_NAME)
        print(f" ---- {len(data)} records ----")
        for d in data:

            json_str = d.value
            # print(f"Data: {json_str}")

            p_obj = json.loads(json_str)
            # print(f"Got: {p_obj}")
            
            dict_zero = p_obj[0] # should be only one - check?
            sesh_no     = dict_zero[JSON_KEY_TS]
            sesh_start  = dict_zero[JSON_KEY_START]
            sesh_end    = dict_zero[JSON_KEY_END]
            sesh_notes  = dict_zero[JSON_KEY_NOTES]

            print(f"{sesh_no},{sesh_start},{sesh_end},{sesh_notes}")

    except Exception as e:
        print(e)
        print("Ouch!")


dump_data(api_key)
