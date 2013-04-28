# PyMention is an implementation of WebMention in Python

[WebMention](http://webmention.org/) is "A modern alternative to Pingback".

This implementation uses gunicorn and requests to provide a Python way
to achieve this.

At this early stage of the development, the code has only been released
for enthousiast hackers, do not use it for real until it reaches 1.0.


## Commands

To install dependencies:

    $ pip install -r requirements.txt

To launch the server:

    $ cd pymention && gunicorn server:app

To launch tests:

    $ python pymention/tests.py  


## Contributions

If you plan to contribute, do not forget to add tests for your pull-request :-)

*BSD licensed.*
