#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = "Eric Rochow"
SITENAME = "Eric Rochow"
SITEURL = ""

PATH = "content"

TIMEZONE = "America/Detroit"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
THEME = (
    "/home/erochow/Scripts/landing-page/env/lib/python3.6/site-packages"
    "/pelican/themes/Flex"
)

# Blogroll
LINKS = (
    # ("Pelican", "http://getpelican.com/"),
    # ("Python.org", "http://python.org/"),
    # ("Jinja2", "http://jinja.pocoo.org/"),
    # ("You can modify those links in your config file", "#"),
    # ("Find Me on the Tubes!", "#"),
)

# Social widget
SOCIAL = (
    ("globe fa-lg", "#"),
    ("envelope-o fa-lg", "mailto:ericrochow@gmail.com"),
    ("rss fa-lg", "#"),
    ("linkedin fa-lg", "https://www.linkedin.com/in/erochow/"),
    ("github fa-lg", "https://github.com/ericrochow"),
    ("reddit fa-lg", "#"),
    ("twitter fa-lg", "https://twitter.com/eric_rochow"),
    ("lastfm fa-lg", "https://www.last.fm/user/ericrochow"),
    (
        "spotify fa-lg",
        "https://open.spotify.com/user/ericrochow?si=KEmxAAk8QZy31L82MMge4g",
    ),
    ("book fa-lg", "https://www.goodreads.com/user/show/18841479-eric-rochow"),
)

GOOGLE_ANALYTICS = "UA-135617138-1"
GITHUB_URL = "https://github.com/ericrochow"

DEFAULT_PAGINATION = False

IGNORE_FILES = [".#*", ".swp", ".tmpl"]
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
