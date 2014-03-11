#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Calendar resource handling functions.
"""

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
import time
from datetime import datetime, date, timedelta
import dateutil.parser
import pytz
import json
import config


def get_service():
    """
    Authorizes with Google and returns an API service for making requests
    against the Calendar API v3.
    """

    # Read key in from file
    f = file(config.client_key_path, "rb")
    key = f.read()
    f.close()

    # Create credentials
    credentials = SignedJwtAssertionCredentials(config.client_email, key,
                                                config.scope)

    # Authorize with credentials and return service
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('calendar', 'v3', http=http)

    return service


def get_room_filename(room_name):
    """ Returns the complete path for the JSON data file for a given room.  """
    return config.data_dir_prefix + 'data/' + room_name + '.json'


def load_room_data(room_name):
    """ Attempts to load the event data for a given room.  """
    try:
        f = open(get_room_filename(room_name), 'rb')
        data = json.loads(f.read())
        f.close()
    except:
        data = None
    return data


def save_room_data(room_name, data):
    """ Attempts to save the event data for a given room.  """
    try:
        f = open(get_room_filename(room_name), 'w')
        f.write(json.dumps(data))
        f.close()
        return True
    except:
        print "Save failed"
        return False


def get_cal_feed(resource_email):
    """
    Given a client and a user id (in this case the id of a Google Calendar
    resource), fetch the events for today.
    """
    events = []
    feed = None
    service = get_service()

    try:
        feed = service.events().list(calendarId=resource_email,
                                     timeMin=get_start_time(),
                                     timeMax=get_end_time()).execute()
    except:
        pass

    # If valid data is returned, loop over the data
    # to build out the event data array.
    if feed is not None:
        for event in feed['items']:

            start_ts = get_timestamp(event['start']['dateTime'])
            end_ts = get_timestamp(event['end']['dateTime'])

            try:
                hangoutLink = event['hangoutLink']
            except KeyError:
                hangoutLink = ''

            try:
                name = event['summary']
            except KeyError:
                name = ''

            events.append({
                'name': name,
                'start': get_time(start_ts),
                'end': get_time(end_ts),
                'start_ts': start_ts,
                'end_ts': end_ts,
                'hangout': hangoutLink
            })
    else:
        pass

    events = sorted(events, key=lambda event: event['start_ts'])
    return events


"""
Generic functions. Not tied to Google APIs
"""


def get_time(ts):
    """ Get a data from a Unix timestamp.  """
    tz = pytz.timezone(config.timezone)
    return datetime.fromtimestamp(ts, tz).strftime('%I:%M%p').lower().lstrip('0')


def get_timestamp(dt):
    """ Get a Unix timestamp from a date """
    tz = pytz.timezone(config.timezone)
    return time.mktime(dateutil.parser.parse(dt).astimezone(tz).timetuple())


def get_start_time():
    """ Get start time for Google Calendar queries.  """
    tz = pytz.timezone(config.timezone)
    return (date.today().isoformat()) + "T00:00:00Z"


def get_end_time():
    """ Get end time for Google Calendar queries.  """
    tz = pytz.timezone(config.timezone)
    return ((date.today() + timedelta(days=1)).isoformat()) + "T00:00:00Z"


def run_test():
    """
    Test function to make sure everything is configured correctly. Attempts to
    connect to the Google Calendar API and return event data for one room
    (specified in config.test_room_id.)
    """
    service = get_service()
    events = service.events().list(calendarId=config.test_room_id).execute()
    print events


if __name__ == '__main__':
    """ If run by itself, run the connection test.  """
    run_test()
