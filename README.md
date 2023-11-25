# pracMonFront
Front-end for PracticeMonitor
Using PHP, Apache EChart, Python 3.11


## Goal
A MVP GUI for Practice Monitor that can run on my web host, for demo purposes.


## Dev environment

Desktop Ubuntu, Python 3.11 venv, PHP built-in web server

# Architecture
This is OK for now, but isn't scalable

* RPi Zero, USB to keyboard
  * Python script watching keyboard
  * At end of each session, uploads session data to cloud (see data format below)

# IOT Data
Store: 
 * {start time (readable string)}
 * {session length (seconds)}
 * {keypress count}

# App front end
* PHP on server
  * Request like http://localhost:8000/pmf_front.php?api_key=12345&start=1/12/2001
    * This is insecure w/r/t the API key!
* Runs python code 
  * TODO: can I do that on Ionos????
  * Code retrieve ALL RECORDS ?
    * TODO: can i just recall some records???
  * Updates local DB of data
  * Formats & displays chart data
 * TODO: UI framework? Or just one GET: handler?

## Notes
 * Use phone as hotspot???

* Option to show gaps in sessions (non-stacked data) - shows practice patterns

