# TimeNotify

this package is inspired by [Status Bar Time](https://packagecontrol.io/packages/Status%20Bar%20Time)

## How to install

-   Clone or [download](https://github.com/halfmoonvic/TimeNotify/archive/master.zip) git repo into your packages folder

Using [Package Control](http://wbond.net/sublime_packages/package_control):

-   Run “Package Control: Install Package” command, and find `TimeNotify` package

---

## Settings

`"interval": 1`:

Clock update interval seconds.

`"format": "%H:%M:%S`:

Specifies date / time format, [refer document](http://docs.python.org/2/library/time.html#time.strftime)

`"lefty": true`:

Stick the clock on the left side of the status bar, if you change this option, restart is required

`"delay": 300`:

Time to delay notify, seconds

`events`:

By setting the "events" configuration item, you can create reminders at specific times or dates.
These reminders are set to any form of time, such as any second of a certain minute, a certain hour, a certain day, a certain week, a certain month, or any time of a certain year.
Note that the settings of minute, hour, day, week, month, and year are all optional,
and you can freely combine them according to your needs.
When these specific settings are not used, you need to specify the "time" option format as "%Y-%m-%d %H:%M:%S",
such as "2022-11-10 18:20:00".
In this configuration item, you can also set the message content and the delay or advance time of the reminder.

`events.delay`:

Set the delay duration for the reminder. it will override `delay` option.

`events.advance`:

Set the advance duration for the reminder.


```
events.time:
----------
"time": "2022-11-11 10:42:20",
"message": "special time"
```

it will remind you at "2022-11-11 10:42:20"


```
events.minute: value range 0 - 59
----------
"minute": [20, 30],
"time": "50",
"message": "minute msg"
```

the full time should be "%Y-%m-%d %H:50:20"、"%Y-%m-%d %H:50:30", it will remind you at 13 and 14 seconds past the 50th minute of every hour.


```
events.hour: value range 0 - 23
----------
"hour": [18, 19],
"time": "28:50",
"message": "hour msg"
```

the full time should be "%Y-%m-%d 18:28:50"、"%Y-%m-%d 19:28:50", it will remind you at 18:28:59 and 19:28:59 every day.


```
events.day: value range 1 - 28/29/30/31
----------
"day": [11],
"time": "10:31:10",
"message": "day msg"
```

the full time should be "%Y-%m-11 10:31:10", it will remind you at 10:31:10 on the 11th day of every month.


```
events.week: value range 1 - 7
----------
"week": [1, 2, 3],
"time": "10:31:10",
"message": "week msg"
```

it will remind you at 10:31:10 on Monday, Tuesday, and Wednesday.


```
events.month: value range 1 - 12
----------
"month": [10, 11],
"time": "11 10:35:50",
"message": "month msg"
```

the full time should be "%Y-10-11 10:35:50" "%Y-11-11 10:35:50", it will remind you at 10:35:50 in October and November every year.


```
events.year:
----------
"year": [2022, 2023],
"time": "11-11 10:38:40",
"message": "year msg"
```

the full time should be "2022-11-11 10:38:40" "2023-11-11 10:38:40", it will remind you at 2022-11-11 10:38:40 and 2023-11-11 10:38:40
