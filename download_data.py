# test code to figure this all out.
# download all data (?) from cloud service, update local db
# robcranfill

import datetime
import json
import sqlite3
import sys

# Import library and create instance of REST client.
from Adafruit_IO import Client

FEED_NAME = "perfdata"

JSON_KEY_START  = "SeshStart"
JSON_KEY_LENGTH = "SeshLength"
JSON_KEY_NOTES  = "SeshNotes"


DB_NAME = "pm.db"


# TODO: not working yet
def output_jscript_data(data_dict_list):

    # FIXME: can't do this in the final output unless I make it a comment somehow
    print(f"Processing {len(data_dict_list)} items:")

    n_last = len(data_dict_list)
    n = 0
    for d in data_dict_list:

        json_record = d.value
        # print(f" - json: '{json_str}'")

        record_dict = json.loads(json_record)[0]
        # print(f"  = dict: {record_dict}")

        sesh_start  = record_dict[JSON_KEY_START]
        sesh_start_date = datetime.datetime.fromisoformat(sesh_start)

        sesh_len    = int(record_dict[JSON_KEY_LENGTH])
        sesh_notes  = int(record_dict[JSON_KEY_NOTES])

        print(f" == {sesh_start_date}")
        # print(f" == {sesh_start}, {sesh_len}, {sesh_notes}")


def show_db():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    res = cur.execute("SELECT * FROM perfdata")
    got = res.fetchall()
    print("\n------------ database contents")
    i = 0
    for g in got:
        i += 1
        print(f" #{i} - {g}")
    print()
    con.close()


def query_for_date(date_str):
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM perfdata WHERE startdate LIKE '{date_str}%'")
    got = res.fetchall()
    print(f"\n------------ matching {date_str}")
    i = 0
    for g in got:
        i += 1
        print(f" #{i} - {g} (sess: {g[1]})")
    print()
    con.close()


# return list of dict of date, session data
#
def get_date_range(start_date, number_of_days):

    result = []

    result.append({"startdate": "2023-10-01", "sessions":[10]})
    result.append({"startdate": "2023-10-02", "sessions":[10, 20]})
    result.append({"startdate": "2023-10-03", "sessions":[10, 20, 30]})
    result.append({"startdate": "2023-10-04", "sessions":[10, 20, 30, 40]})
    result.append({"startdate": "2023-10-05", "sessions":[10, 20, 30]})
    result.append({"startdate": "2023-10-06", "sessions":[10, 20]})
    result.append({"startdate": "2023-10-07", "sessions":[10]})
    
    return result


def save_to_db(data_dict_list):

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    try:
        # error on create is OK, generally
        try: 
            cur.execute("CREATE TABLE perfdata(startdate STRING PRIMARY KEY, duration, keypresses)")
        except:
            print("Table exists? OK, continuing....")
    except Exception as e:
        print(e)
        return

    skipped = 0
    for d in data_dict_list:

        # for some reason json returns a 1-item tuple.
        record = json.loads(d.value)[0]

        sesh_start  =     record[JSON_KEY_START]
        sesh_len    = int(record[JSON_KEY_LENGTH])
        sesh_notes  = int(record[JSON_KEY_NOTES])
    
        sesh_start_date = datetime.datetime.fromisoformat(sesh_start)

        try:
            cur.execute(f"INSERT INTO perfdata VALUES ('{sesh_start}', {sesh_len}, {sesh_notes})")
        except:
            skipped += 1
            print(f" (duplicate record {sesh_start})")

    con.commit()    
    con.close()
    print(f"Records skipped: {skipped}")


def output_js_for_chart(dataset):

    # for each day
    n = 0
    for d in dataset:
        date_str = d["startdate"]
        session_list = d["sessions"]

        # print(f"startdate = {date_str}, sess = {session_list}")

        print( " {")
        print(f"  data: {str(session_list)},")
        print( "  type: 'bar',")
        print( "  stack: 'x'")

        n += 1
        if n != len(dataset):
            print(" },")
        else:
            print(" }")


def main(aio_key):

    # try:
    aio = Client("robcranfill", aio_key)
    print("client OK")

    # this gets *all* the data. :-(
    # the items we want are the .value members of each item
    data = aio.data("perfdata")

    # output_jscript_data(data)
    
    save_to_db(data)

    # these two fail if db doesn't exist; call save_to_db once to fix that.
    show_db()
    query_for_date("2023-10-02")

    range_data = get_date_range('x', 7)
    print(f"range_data: {range_data}")
    output_js_for_chart(range_data)


    # except Exception as e:
        # print("Error:")
        # print(e.with_traceback)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(f"Run with: {sys.argv[0]} API_KEY")
        sys.exit(1)

    main(sys.argv[1])

