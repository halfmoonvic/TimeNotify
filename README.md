# TimeNotify

TimeNotify is a Sublime Text plugin that displays the current time in the status bar and allows you to set events to be notified at specific times.

it is inspired by [Status Bar Time](https://packagecontrol.io/packages/Status%20Bar%20Time)

## How to install

* Clone or [download](https://github.com/halfmoonvic/TimeNotify/archive/master.zip) git repo into your packages folder

* Using [Package Control](http://wbond.net/sublime_packages/package_control):

    Run “Package Control: Install Package” command, and find `TimeNotify` package

---

## Settings

**`interval: 1`:**

The clock update interval is in seconds. The default is 1.

**`format: "%H:%M:%S`:**

The time format is to display in the status bar. Default is `%H:%M:%S | %j | %m-%d | %A`. [refer document](http://docs.python.org/2/library/time.html#time.strftime)

**`lefty: true`:**

Stick the clock on the left side of the status bar, if you change this option, a restart is required

**`delay: 300`:**

The time to delay notifications in seconds. Default is 300

**`events`:**

An array of events is to be notified at specific times.  
By setting the "events" configuration item, you can create reminders at specific times or dates.
These reminders are set to any form of time, such as any second of a certain minute, a certain hour, a certain day, a certain week, a certain month, or any time of a certain year.
Note that the settings of minute, hour, day, week, month, and year are all optional,
and you can freely combine them according to your needs.
When these specific settings are not used, you need to specify the "time" option format as "%Y-%m-%d %H:%M:%S",
such as "2022-11-10 18:20:00".
In this configuration item, you can also set the message content and the delay or advance time of the reminder.

* `event.delay`:

    The message is to display in the notification. Required.

* `event.delay`:

    The time to delay the notification is in seconds. Optional.

* `event.advance`:

    The time in seconds to notify before the actual time. Optional.

* `event.time`:

    The time to notify in the format as below:

    - `%S`format, it will be interpreted as any second of the current minute.
    - `%M:%S` format, it will be interpreted as any time of the current hour.
    - `%H:%M:%S` format, it will be interpreted as any time of the current day.
    - `%d %H:%M:%S` format, it will be interpreted as any time of the current month.
    - `%m-%d %H:%M:%S` format, it will be interpreted as any time of year.
    - `%Y-%m-%d %H:%M:%S` format, it will be a certain time.

    As the code below, It will remind you at 2023-06-06 08:10:10.

    ```
    "time": "2023-06-06 08:10:10", // %Y-%m-%d %H:%M:%S
    "message": "certain time msg"
    ```

* `event.minute`:
    An array of minutes to notify on (0-59). Optional.

    As the code below, the full-time should be "%Y-%m-%d %H:10:20"、"%Y-%m-%d %H:10:30".  
     It will remind you at 10 seconds of the 20th and 30th minute of every hour.

    ```
    "minute": [20, 30],
    "time": "10", // %S
    "message": "minute msg"
    ```

* event.hour:
    An array of hours to notify on (0-23). Optional.

    As code below, the full-time should be "%Y-%m-%d 08:10:10"、"%Y-%m-%d 09:10:10".  
     it will remind you at 08:10:10 and 09:10:10 every day.

    ```
    "hour": [08, 09],
    "time": "10:10", // %M:%S
    "message": "hour msg"
    ```

* event.day:
    An array of days of the month to notify on (1-31). Optional.

    As code below, the full-time should be "%Y-%m-06 08:10:10".  
     it will remind you at 08:10:10 on the 6th day of every month.

    ```
    "day": [6],
    "time": "08:10:10", // `%H:%M:%S`
    "message": "day msg"
    ```

* event.week:

    An array of weekdays to notify on (1-7, where 1 is Monday and 7 is Sunday). Optional.  
     As the code below, it will remind you at 08:10:10 on every Monday, Tuesday, and Wednesday.

    ```
    "week": [1, 2, 3],
    "time": "08:10:10", // %H:%M:%S
    "message": "week msg"
    ```

* event.month:

    An array of months to notify on (1-12, where 1 is January and 12 is December). Optional.

    As code below, the full-time should be "%Y-06-06 08:10:10" "%Y-10-06 08:10:10".  
     it will remind you at 08:10:10 in June and October every year.

    ```
    "month": [06, 10],
    "time": "06 08:10:10", // %d %H:%M:%S
    "message": "month msg"
    ```

* event.year:
    An array of years to notify on. Optional.

    As code below, the full-time should be "2023-06-06 08:10:10" "2024-06-06 08:10:10",  
     it will remind you at 2023-06-06 08:10:10 and 2024-06-06 08:10:10.

    ```
    "year": [2023, 2024],
    "time": "06-06 08:10:10", // %m-%d %H:%M:%S
    "message": "year msg"
    ```

----------

The following code is an example of events configuration items
