# This will be called by the PHP page to generate the chart data.
# robcranfill
# Simply outputs the Apache EChart JavaScript fragment to stdout.

import json
import sys

# Import library and create instance of REST client.
from Adafruit_IO import Client

FEED_NAME = "perfdata"

JSON_KEY_START  = "SeshStart"
JSON_KEY_LENGTH = "SeshLength"
JSON_KEY_NOTES  = "SeshNotes"


# super-simple initial test; this is what the output should look like.
def print_dummy_data():
    print("            {")
    print("              data: [10, 20, 20, 35, 45, 25, 0],")
    print("              type: 'bar',")
    print("              stack: 'x'")
    print("            },")
    print("            {")
    print("              data: [50, 40, 30, 50, 0, 15, 0],")
    print("              type: 'bar',")
    print("              stack: 'x'")
    print("            },")
    print("            {")
    print("              data: [10, 20, 30, 40, 0, 0, 0],")
    print("              type: 'bar',")
    print("              stack: 'x'")
    print("            }")


def output_jscript_data(data_dict_list):

    print(f"Got {len(data_dict_list)} items:")

    n_last = len(data_dict_list)
    n = 0
    for d in data_dict_list:

        json_str = d.value
        # print(f" - json: '{json_str}'")

        j_dict = json.loads(json_str)[0]
        # print(f"  = dict: {j_dict}")

        sesh_start  = j_dict[JSON_KEY_START]
        sesh_len    = int(j_dict[JSON_KEY_LENGTH])
        sesh_notes  = int(j_dict[JSON_KEY_NOTES])
        # print(f" == {sesh_start}, {sesh_len}, {sesh_notes}")

        print(" {")
        d_string = ""
        
        # FIXME: this isn't right, obviously
        print("  data: [10, 20, 20, 35, 45, 25, 0],")
        print("  type: 'bar',")
        print("  stack: 'x'")

        n += 1
        if n != n_last:
            print(" },")
        else:
            print(" }")


def main(aio_key):

    try:
        aio = Client("robcranfill", aio_key)
        print("client OK")

        # Retrieve the most recent value from the feed "Foo".
        # Access the value by reading the `value` property on the returned Data object.
        # Note that all values retrieved from IO are strings so you might need to convert
        # them to an int or numeric type if you expect a number.

        data = aio.data("perfdata")
        output_jscript_data(data)

    except Exception as e:
        print("Error:")
        print(e)


# does this work in PHP environment? yes.
if __name__ == "__main__":

    # print_dummy_data()

    if len(sys.argv) != 2:
        print(f"Run with: {sys.argv[0]} API_KEY")
        sys.exit(1)
    main(sys.argv[1])

