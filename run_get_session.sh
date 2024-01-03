#!/bin/bash
# get data from AIO, save new to DB, generate JS
# arg: start date like "2023-10-01"

python get_session_data.py `cat aio_secret.text` test-data-1 $1

