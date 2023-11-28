# test code to figure this all out.
# download all data (?) from cloud service, update local db
# most of this code now used in get_session_data


import datetime
import json
import sqlite3
import sys

# Import library and create instance of REST client.
from Adafruit_IO import Client

JSON_KEY_START  = "SeshStart"
JSON_KEY_LENGTH = "SeshLength"
JSON_KEY_NOTES  = "SeshNotes"


DB_NAME = "pm.db"


def query_for_date(date_str):

    session_lengths = []

    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()
    res = cur.execute(f"SELECT * FROM perfdata WHERE startdate LIKE '{date_str}%'")
    got = res.fetchall()
    # print(f"\n------------ matching {date_str}")
    i = 0
    for g in got:
        i += 1
        # print(f" #{i} - {g} (sess: {g[1]})")
        session_lengths.append(g[1])
    # print()
    con.close()

    return session_lengths




# # return list of dict of date, session data
# #
# def get_date_range(start_date, number_of_days):
#     result = []
#     result.append({"startdate": "2023-10-01", "sessions":[10]})
#     result.append({"startdate": "2023-10-02", "sessions":[10, 20]})
#     result.append({"startdate": "2023-10-03", "sessions":[10, 20, 30]})
#     result.append({"startdate": "2023-10-04", "sessions":[10, 20, 30, 40]})
#     result.append({"startdate": "2023-10-05", "sessions":[10, 20, 30]})
#     result.append({"startdate": "2023-10-06", "sessions":[10, 20]})
#     result.append({"startdate": "2023-10-07", "sessions":[10]})
#     return result


def save_to_db(data_dict_list):

    print("Attempting to save ALL records; FIXME:")

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
            # print(f" (duplicate record {sesh_start})")

    con.commit()    
    con.close()
    print(f"Records skipped: {skipped}")


def list_of_ints_from_str(str):
    l = eval(str) # tricky!
    return l


def output_js_for_chart(dataset):

    # the data is rotated, so to speak :-/
    # we have 
    #       day1: s1, s2, s3
    #       day2: s4, s5
    #       day3: s6
    #       day4: s7, s8
    # but need
    #       row1: s1, s4, s6, s7
    #       row2: s2, s5, s8,  0
    #       row3: s3,  0,  0,  0



    # make a list of lists of data for the days
    day_data = []
    longest = 0
    for d in dataset:
        # d['sessions'] is actually one string!
        this_day = list_of_ints_from_str(d['sessions'])
        # print(f" appending {d['sessions']} which is a {type(d['sessions'])}")
        day_data.append(this_day)
        # print(f"session list: {day_data}")
        if len(this_day) > longest:
            longest = len(this_day)

    print(f"\nsession list: {day_data}")
    print(f"\n longest: {longest}")

    # pad to longest
    for d in day_data:
        # print(f"   pad {d} ?")
        if len(d) < longest:
            for i in range(longest -(len(d))):
                d.append(0)
        # print(f" = pad {d}")
    print(f"padded session list:\n{day_data}")

    # rotate
    # thanks to https://stackoverflow.com/questions/8421337/rotating-a-two-dimensional-array-in-python
    rotated_days = list(zip(*day_data[::-1]))
    # print(f"rotated session list: {rotated_days}")

    # for some reason each new row is reversed. fix.
    i = 0
    for r in rotated_days:

        print( "]]]] {")
        print(f"]]]] data: {str(list(reversed(r)))}")
        print( "]]]]  type: 'bar',")
        print( "]]]]  stack: 'x'")

        i += 1
        if i == longest:
            print("]]]] }")
        else:
            print("]]]] },")


    oldCode = False
    if oldCode:
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



# return list of dict of date, session data
#
def get_date_range(start_date, number_of_days):

    result = []
    for i in range(number_of_days):
        day = datetime.datetime.fromisoformat(start_date) + datetime.timedelta(days=i)

        # just match the date part. FIXME: ok to just use substring?
        just_date = day.isoformat()[0:10]
        day_sessions = query_for_date(just_date)
        result.append({"startdate": just_date, "sessions":str(day_sessions)})

    return result


# query_date is like "2023-10-02"
#
def main(aio_key, feed_key, query_date):

    print(f"get_session_data: XXX {query_date}")

# first, update the database

    # try:
    aio = Client("robcranfill", aio_key)
    print("client OK")

    # FIXME: this gets *all* the data.
    data = aio.data(feed_key)

    # save new records to local db
    # FIXME: attempts to save all
    save_to_db(data)

# next, query the db for the data and output it

    range_data = get_date_range(query_date, 7)
    print(f"range_data: {range_data}")
    output_js_for_chart(range_data)

    # except Exception as e:
        # print("Error:")
        # print(e.with_traceback)


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print(f"Run with: {sys.argv[0]}  {{API_KEY}}  {{FEED_KEY}}  {{QUERY_DATE}}")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])

