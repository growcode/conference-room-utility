# Grow Conference Room Utility

# About
Give all your conference rooms a digital dashboard tied to your Google Apps account!

- Display a room's upcoming scheduled meetings
- Quickly join Hangouts for each meeting -- no login necessary

This project is a utility (powered by the Google Calendar API) that creates a website to
display the schedules of each of your conference rooms, including links for upcoming hangouts.

- Users can browse room usage via an internal URL.
- Each conference room has its own landing page that can be used as a homepage for conference room computers/TVs. Employees and visitors can easily see who has resevered a given room and quickly access Hangouts via the app's account login.

# Setup and Configuration
To get the utility up and running you will have to do the following (detailed below):

1. Add your conference rooms to your Google Apps account as resources
1. Configure the app in Google Cloud Console and your Google Apps account
1. Install this codeset on a Python-powered web server
1. Configure URLs to point to web service and deploy within conference rooms.

## Creating and Adding Resources to Google Apps
This utility requires setting up each of your conference rooms as a resource within Google Apps.
Add resources from the [Google Apps admin panel](http://admin.google.com) under
Apps -> Calendar -> Resources. See [Google's documentation on resources](https://support.google.com/a/answer/1686462?hl=en&ref_topic=1034362)
to learn more.

## Google Cloud and Apps Configuration
(Note that as Google frequently changes their administration pages, this
documentation may be out of date.)

1. Go to the [Google Developers Console](https://console.developers.google.com/project) and create a new project. You may use whatever information you desire on this screen.
2. Go to the APIs & Auth > APIs and activate the Calendar API and the Google+ Hangouts API.
3. Go to APIs & Auth > Credentials registered apps and register a new service account.
4. Click on the application, select certificate, and click generate new key.
5. Download the private key, taking note of the password.
6. Put the key generated in the previous step on the server in a secure place.
7. In the [Google Apps Admin panel](http://admin.google.com), go to Google Apps -> Calendar -> General Settings
8. Under "External Sharing" select "Share all information, but outsiders cannot change calendars."
9. Share the desired resource calendars with the generated service account.
    Be sure to select "See all event details" as the permission setting.

## Server Setup

### Requirements
- Python
- flask
- pytz
- httplib2
- google-api-python-client
- python-dateutil

### Setup Steps
1. Clone this project

        git clone git@bitbucket.org:thisisgrow/grow-conference-room-utility.git

2. Install pip

        sudo easy_install pip

3. Install required packages

        sudo pip install --upgrade flask pytz httplib2 google-api-python-client python-dateutil


4. On some platforms, you may also have to install Python headers and pyopenssl

        sudo apt-get install python-dev
        sudo pip install pyopenssl

5. Edit the configuration file.  See crweb/config.py for configuration options.
To use a custom logo, replace the current logo located here: crweb/static/img/logo.png
with another 60px square PNG. To use another size or format, edit the
properties of the logo class in crweb/static/css/styles.css.

6. Test configuration and Google setup by running the calendar resource test.
Fix any errors that will appear. A successful test will return a dump of all
events for the room specified in the configuration variable `test_room_id`.

        python crweb/cal_resource.py

7. To test that the app is functioning and that configuration values are correct, run
with the Flask test server. The rooms that were added in the configuration should be
present. As the cron is not yet set, no data will appear. To force reload, click the
reload link in the bottom right corner of the resource pane.

        python crweb/crweb.py

8. A cron (scheduled task) will need to be setup to periodically update the data for
each room. You can set this cron to repeat as often as you like, but you will need to
be sure not to go over the daily Google Calendar API usage limit (currently 100,000.)
To determine how often you can run the cron, use the following formula where `f` is
the frequency in minutes and `r` is the number of rooms in the configuration file.

        f = (60 * 24 * r) / 100,000

    Be sure to leave some overhead for expansion and forced reloads. If you have frequent
    updates to the calendar, then quicker updates may be necessary. If the calendar is
    not frequently changed, than setting the utility to update once or twice a day
    will be sufficient. The following cron will run every five minutes. Replace the
    path to the utility with your own path.

        */5	*	*	*	*	cd <PATH-TO-UTILITY> && python crweb/reload.py

9. Run the app either manually or with WSGI middleware.

## Deployment
Point a domain at the web service you just installed. For instance, you could use rooms.YourDomain.com. We recommend either password-protecting this site, or hosting it on an internal network.

Now employees should be able to use this new URL to browse the status of all configured rooms.

For each conference room that is equipped with a computer and primary display (either TV or a monitor), do the following:

1. Open the web browser and log into gmail with your resource's account. Close the window. (Note, by logging in this first time, clicking on Join Hangout links within the utility in the future will join the given Hangout as this resource account.)
2. Navigate to TheDomainYouConfiguredAbove.com and click on the room that you are currently in. Make this page the browser's home screen.

# Author
Created by [Grow](http://thisisgrow.com)

# License
This project is licensed under the MIT License. (See LICENSE)
