# -*- coding: utf-8 -*-

from datetime import datetime

import sublime
import sublime_plugin

STATUSBARTIME_SETTING_FILE = 'TimeNotify.sublime-settings'
SETTINGS = {}

TIMEFORMAT = {
    '%S': 2,
    '%M:%S': 5,
    '%H:%M:%S': 8,
    '%d %H:%M:%S': 11,
    '%m-%d %H:%M:%S': 14,
    '%Y-%m-%d %H:%M:%S': 19,
}


def get_settings():
    settings = sublime.load_settings(STATUSBARTIME_SETTING_FILE)
    SETTINGS['format'] = settings.get('format', '%H:%M:%S')
    SETTINGS['interval'] = settings.get('interval', 1000) * 1000
    SETTINGS['delay'] = settings.get('delay', 300)
    SETTINGS['onlyinview'] = settings.get('onlyinview', False)
    SETTINGS['lefty'] = settings.get('lefty', True)
    SETTINGS['eventdict'] = {}

    now = datetime.now()
    events = settings.get('events', [])
    events = [event for event in events if event.get('time')]

    for event in events:
        notify_time = event['time']
        formatter = len(event.get('time', ''))

        if formatter == TIMEFORMAT['%S']:  # 01
            notify_time = now.strftime('%Y-%m-%d %H:%M:') + event['time']

        if formatter == TIMEFORMAT['%M:%S']:  # 20:00
            notify_time = now.strftime('%Y-%m-%d %H:') + event['time']

        if formatter == TIMEFORMAT['%H:%M:%S']:  # 18:20:00
            notify_time = now.strftime('%Y-%m-%d ') + event['time']

        if formatter == TIMEFORMAT['%d %H:%M:%S']:  # 10 18:20:00
            notify_time = now.strftime('%Y-%m-') + event['time']

        if formatter == TIMEFORMAT['%m-%d %H:%M:%S']:  # 11-10 18:20:00
            notify_time = now.strftime('%Y-') + event['time']

        if formatter == TIMEFORMAT['%Y-%m-%d %H:%M:%S']:  # 2022-11-10 18:20:00
            notify_time = event['time']

        timestamp = int(
            datetime.strptime(notify_time, '%Y-%m-%d %H:%M:%S').timestamp())

        event['time'] = timestamp
        SETTINGS['eventdict'][timestamp] = event
        if event.get('advance'):
            SETTINGS['eventdict'][timestamp - event['advance']] = event

    SETTINGS['events'] = events


def get_duration(duration):
    if duration < 60:
        return duration, 'seconds'

    if duration < 3600:
        return int(duration / 60), 'minutes'

    if duration < 86400:
        return int(duration / 60 / 60), 'hours'

    return int(duration / 60 / 60 / 24), 'days'


def plugin_loaded():
    get_settings()
    sublime.load_settings('TimeNotify.sublime-settings').add_on_change(
        'get_settings', get_settings)


class StatusBarTime(sublime_plugin.ViewEventListener):

    def __init__(self, view):
        Timer().displayTime(view)


class Timer():

    def __init__(self):
        self.status_key = '0__statusclock' if SETTINGS[
            'lefty'] else 'statusclock'

    def displayTime(self, view):
        now = datetime.now()
        view.set_status(self.status_key, now.strftime(SETTINGS['format']))

        actwin = sublime.active_window()
        same_active_view_id = actwin.active_view() and actwin.active_view().id(
        ) == view.id()

        if not actwin:
            view.set_status(self.status_key, '')
            return

        if SETTINGS.get('events') and len(
                SETTINGS['events']) and same_active_view_id:
            self.notify(now)

        if not SETTINGS['onlyinview'] or same_active_view_id:
            sublime.set_timeout(lambda: self.displayTime(view),
                                SETTINGS['interval'])

    def notify(self, time):
        nowtimestamp = int(time.timestamp())
        event = SETTINGS['eventdict'].get(nowtimestamp)

        if not event or (
                event.get('minute') and time.minute not in event['minute']
        ) or (event.get('hour') and time.hour not in event['hour']) or (
                event.get('week') and time.weekday() + 1 not in event['week']
        ) or (event.get('day') and time.day not in event['day']) or (
                event.get('month') and time.month not in event['month']) or (
                    event.get('year') and time.year not in event['year']):
            return

        if event.get('advance'
                     ) and nowtimestamp == event['time'] - event['advance']:
            self.advance(event['message'], event['advance'])
            return

        if nowtimestamp == event['time']:
            self.delay(event['message'], event.get('delay', SETTINGS['delay']),
                       event)
            return

    def advance(self, message, duration):
        duration, unit = get_duration(duration)
        sublime.message_dialog('advance %(duration)s %(unit)s: %(message)s' % {
            'duration': duration,
            'unit': unit,
            'message': message,
        })

    def delay(self, message, duration, event):
        duration, unit = get_duration(duration)
        if sublime.ok_cancel_dialog(
                message, 'Delay %(delay)s %(unit)s' % {
                    'delay': duration,
                    'unit': unit
                }):
            del SETTINGS['eventdict'][event['time']]
            delaytime = event['time'] + duration
            event['time'] = delaytime
            SETTINGS['eventdict'][delaytime] = event
