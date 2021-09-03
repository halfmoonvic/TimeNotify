# -*- coding: utf-8 -*-

import sublime
import sublime_plugin
from datetime import datetime

STATUSBARTIME_SETTING_FILE = 'TimeNotify.sublime-settings'
SETTINGS = {}


def get_settings():
    settings = sublime.load_settings(STATUSBARTIME_SETTING_FILE)
    SETTINGS['format'] = settings.get('format', '%H:%M:%S')
    SETTINGS['interval'] = settings.get('interval', 1000) * 1000
    SETTINGS['delay'] = settings.get('delay', 300)
    SETTINGS['onlyinview'] = settings.get('onlyinview', False)
    SETTINGS['lefty'] = settings.get('lefty', True)

    events = settings.get('events', [])
    now = datetime.now()
    for event in events:
        if event.get('time') and len(event.get('week')):
            notify_time = now.strftime("%Y-%m-%d") + ' ' + event.get('time')
            event['time'] = int(datetime.strptime(
                notify_time, '%Y-%m-%d %H:%M:%S').timestamp())

    SETTINGS['events'] = events


def plugin_loaded():
    get_settings()


class StatusBarTime(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        Timer().displayTime(view, SETTINGS['interval'], SETTINGS['onlyinview'])


class Timer():
    def __init__(self):
        self.status_key = '0__statusclock'
        self._format = SETTINGS['format']
        self._events = SETTINGS['events']
        self._delay = SETTINGS['delay']

    def displayTime(self, view, interval, onlyinview):
        now = datetime.now()

        view.set_status(self.status_key, now.strftime(self._format))

        if len(self._events):
            self.notify(view, now)

        actwin = sublime.active_window()

        if not actwin:
            view.set_status(self.status_key, '')
            return
        if not onlyinview or (actwin.active_view() and actwin.active_view().id() == view.id()):
            sublime.set_timeout(lambda: self.displayTime(
                view, interval, onlyinview), interval)

    def notify(self, view, time):
        actwin = sublime.active_window()
        if not actwin or actwin.active_view().id() != view.id():
            return

        for event in self._events:
            if time.weekday() + 1 in event.get('week') and event['time'] == int(time.timestamp()):

                if sublime.ok_cancel_dialog(
                        event.get('message'),
                        'Delay %(delay)s M' % {'delay': int(
                            event.get('delay', self._delay) / 60)}
                ):
                    event['time'] = event['time'] + \
                        event.get('delay', self._delay)
