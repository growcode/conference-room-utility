#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cron to reload events from Google Calendar.
"""

import cal_resource
import config

if __name__ == '__main__':
    """
    Reload data for all rooms. Loop over each room.
    Get events from Google calendar and save to data file.
    """

    for room in config.rooms:
        print "Reloading events for", room
        events = cal_resource.get_cal_feed(config.rooms.get(room).get('id'))
        cal_resource.save_room_data(room, events)
