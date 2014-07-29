PyGod
=====

Console monitor for godville.net written on Python with curses library usage.


Features
--------

 - Minimalistic design
 - Hero status parsing and pop-up windows for the following situations
    - hero's health is low
    - there is an inventory item that can be activated
    - session is expired


Requirements
------------

1. Linux/Unix/MacOS
2. Python3 installed


Usage
-----

Regular usage:

`$python3 pygod.py god_name`

If you want more information about usage:

`$python3 pygod.py -h`



Support
-------

In case of any issues with this program please create an issue on GitHub, or
describe it at [forum](http://godville.net/forums/show_topic/3148).

Also, it is recommended to attach the `pygod.log` file, automatically written
in application root directory, and run the application in DEBUG mode in order
to provide more informative log file:

`python3 pygod.py god_name -D`
