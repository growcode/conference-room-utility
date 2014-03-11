#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flask route definitions and implementation.
"""

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash

import cal_resource
import config
import time

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/')
def show_room_list():
    """ Homepage. Show the list of available rooms.  """
    title = 'Rooms'
    rooms = config.rooms

    return render_template('show_room_list.html', title=title, rooms=rooms,
                           support_email=config.support_email)


@app.route('/room/<room_name>')
def check_room_status(room_name):
    """ Get today's events for a specific room.  """

    events = cal_resource.load_room_data(room_name)

    if events is None:
        force_check_room_status(room_name, 1)
        events = cal_resource.load_room_data(room_name)

    try:
        event_count = len(events)
    except:
        events = []
        event_count = 0

    if room_name in config.rooms:
        title = config.rooms.get(room_name).get('name')
    else:
        title = room_name.replace('-', ' ').title()

    now = time.time()

    return render_template('check_room_status.html', title=title,
                           events=events, event_count=event_count,
                           now_ts=now, show_reload=True,
                           support_email=config.support_email)


@app.route('/room/<room_name>/reload/<force_reload>')
def force_check_room_status(room_name, force_reload):
    """ Reload event data from Google Calendar.  """

    if config.rooms.get(room_name):
        # print "000000", config.rooms.get(room_name).get('id')
        events = cal_resource.get_cal_feed(config.rooms.get(room_name).get('id'))
    else:
        events = []

    cal_resource.save_room_data(room_name, events)

    # print events

    return render_template('force_results.html', status=room_name)


if __name__ == '__main__':
    """ Run the app """
    app.debug = True
    app.run('0.0.0.0')
