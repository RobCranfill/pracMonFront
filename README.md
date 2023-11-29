# pracMonFront
Front-end for PracticeMonitor

Using PHP, Apache EChart, Python 3.11


## Goal
A MVP GUI for Practice Monitor that can run on my web host, for demo purposes.


## Dev environment

Desktop Ubuntu, MS VS Code, Python 3.11 venv, PHP built-in web server


# Architecture
This is OK for now, but maybe isn't scalable

* RPi Zero, USB to keyboard
  * Python script watching keyboard
  * At end of each session, uploads session data to cloud (see data format below)

* Web page on server
  * Uses PHP to run Python code:
    * Query IOT, update local DB
    * Present HTML page to slice and dice data
      * Apache ECharts


# IOT Data
Store: 
 * {start time (ISO format date & time)}
 * {session length (seconds)}
 * {keypress count}
* A feed for each user?
  * TODO: And/or a feed for test data!

# App front end
* PHP on server
  * Request like http://localhost:8000/pmf_front.php?api_key=12345&start=1/12/2001
    * This is insecure w/r/t the API key!
* Runs python code 
  * OK on Ionos
  * Code retrieve ALL RECORDS ?
    * TODO: can i just recall some records???
  * Updates local DB
  * Formats & displays chart data
 * TODO: UI framework? Or just one GET: handler?


## Notes
 * Use phone as hotspot???
 * GUI option to show gaps in sessions (non-stacked data) - shows practice patterns

## Problems, Questions
* How to install needed Python libs on Ionos?
  * And so PHP will see them

  
## code
* generate_test_data.py - As it says, generates test data to send to AIO. Limit 30 records in 10 minutes???
* get_session_data.py - Retrieve all records from AIO, save news ones (if any) to local DB, output JS.
* ionos_test.php/py
* pmf_front.php - symlink to pmf?.html
* server.sh - starts PHP server; run in separate console


## Feed names
Do I want/need to use a Group?
<pre>
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
</pre>