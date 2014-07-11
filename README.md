PyGod
=====

Console monitor for godville.net written on Python with curses library usage.


Requirements
============

1. Python 3 installed

Windows Specific
----------------

1. Curses module installed: http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
   (due to unofficial support of curses on windows, it will probably have issues
   with UTF-8 encoding in strings


Usage
=====

Regular usage:

`python3 pygod.py god_name`

If you want more information about usage:

`python3 pygod.py -h`



Support
=======

In case of any issues with this script please create an issue on GitHub, or
describe it at [forum](http://godville.net/forums/show_topic/3148).

Also, it is recommended to attach the `pygod.log` file, automatically written
in application root directory, and run the application in DEBUG mode in order
to provide more informative log file:

`python3 pygod.py god_name -D`
