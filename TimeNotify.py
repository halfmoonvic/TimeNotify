# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
from datetime import datetime
import re

STATUSBARTIME_SETTING_FILE = 'TimeNotify.sublime-settings'
SETTINGS = {}


def get_settings():
    settings = sublime.load_settings(STATUSBARTIME_SETTING_FILE)
    SETTINGS['format'] = settings.get('format', '%H:%M:%S')
    SETTINGS['interval'] = settings.get('interval', 1000) * 1000
    SETTINGS['delay'] = settings.get('delay', 300)
    SETTINGS['onlyinview'] = settings.get('onlyinview', False)
    SETTINGS['lefty'] = settings.get('lefty', True)

    now = datetime.now()
    events = settings.get('events', [])
    events = [event for event in events if event.get('time')]

    for event in events:
        dividing_lines = re.findall('-', event.get('time'))
        space_counts = re.findall(' ', event.get('time'))
        notify_time = event['time']
        if len(dividing_lines) == 0:
            if len(space_counts) == 0:
                notify_time = now.strftime('%Y-%m-%d') + ' ' + event['time']
            else:
                notify_time = now.strftime('%Y-%m') + '-' + event['time']
        if len(dividing_lines) == 1:
            notify_time = now.strftime('%Y') + '-' + event['time']
        if len(dividing_lines) == 2:
            notify_time = event['time']

        event['time'] = int(datetime.strptime(
            notify_time, '%Y-%m-%d %H:%M:%S').timestamp())

    SETTINGS['events'] = events


def plugin_loaded():
    get_settings()
    sublime.load_settings(
        'TimeNotify.sublime-settings').add_on_change('get_settings', get_settings)


class StatusBarTime(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        Timer().displayTime(view, SETTINGS['interval'], SETTINGS['onlyinview'])


class Timer():
    def __init__(self):
        self.status_key = '0__statusclock'

    def displayTime(self, view, interval, onlyinview):
        now = datetime.now()
        view.set_status(self.status_key, now.strftime(SETTINGS['format']))

        actwin = sublime.active_window()
        same_active_view_id = actwin.active_view(
        ) and actwin.active_view().id() == view.id()

        if not actwin:
            view.set_status(self.status_key, '')
            return

        if SETTINGS.get('events') and len(SETTINGS['events']) and same_active_view_id:
            self.notify(now)

        if not onlyinview or same_active_view_id:
            sublime.set_timeout(lambda: self.displayTime(
                view, interval, onlyinview), interval)

    def notify(self, time):
        nowtimestamp = int(time.timestamp())

        for event in SETTINGS['events']:
            if (event.get('week') and time.weekday() + 1 in event['week']) or not event.get('week'):
                if event.get('advance') and event['time'] - event['advance'] == nowtimestamp:
                    self.advance(event['message'], event['advance'])
                if event['time'] == nowtimestamp:
                    self.delay(event['message'], event.get(
                        'delay', SETTINGS['delay']), event)

    def advance(self, message, duration):
        sublime.message_dialog('advance %(duration)s Hours: %(message)s' % {
                               'duration': int(duration / 60 / 60), 'message': message})

    def delay(self, message, duration, event):
        if sublime.ok_cancel_dialog(
            message,
            'Delay %(delay)s Min' % {'delay': int(duration / 60)}
        ):
            event['time'] = event['time'] + duration
