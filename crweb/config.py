#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration for the conference room application.
"""

# The path to the key generated in registering this app in the Google Cloud
# Console. The client email is display on that page as well.
client_key_path = ''
client_email = ''

# Leave the scopes the same, unless you are extending the codebase.
scope = 'https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.readonly'

# Test room id. Used in testing connectivity in cal_resource.py
test_room_id = ''

# Dictionary of all rooms. Key is the the URL slug. Name is the friendly name
# of the room. Id can be found under resources in the Google Apps admin
# panel (as email address x@resource.calendar.google.com. The key and name do
# not have to match the values in the Google Apps admin panel.
rooms = {
    'room-1': {
        'id': 'room-1@resource.calendar.google.com',
        'name': 'Room 1'
    },
    'room-2': {
        'id': 'room-2@resource.calendar.google.com',
        'name': 'Room 2'
    }
}

# Valid timezone provided to pytz http://pytz.sourceforge.net/
timezone = 'US/Eastern'

# Support email address. Shows at the bottom of each page.
# If you want to disable this, make support_email = None.
support_email = 'admin@example.com'

# If running in directory, need to go up directory to get data files
data_dir_prefix = '<ABSOLUTE_PATH_TO_PKG_DIR>/rooms.grow/'
