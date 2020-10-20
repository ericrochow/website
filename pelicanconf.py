#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import math
from datetime import datetime

import arrow

AUTHOR = "Eric Rochow"
SITEURL = "https://www.ericroc.how"
SITENAME = AUTHOR
SITETITLE = AUTHOR
# SITESUBTITLE = ""
# SITEDESCRIPTION = ""
SITELOGO = SITEURL + "/images/face.png"
# FAVICON = SITEURL + ""
COPYRIGHT_NAME = AUTHOR
COPYRIGHT_YEAR = datetime.now().year


class Career(object):
    def __init__(self):
        self.career_start = arrow.get("2011-10-25T09:00:00.00-4:00")
        self.todayh_date = arrow.utcnow()

    def career_years(self):
        """
        """
        tdelta = self.career_start - self.today_date
        ydelta = math.ceil(tdelta.days / 365.25)
        return ydelta


PATH = "content"

TIMEZONE = "America/Detroit"

DEFAULT_LANG = "en"
OG_LOCALE = "en_US"
LOCALE = "en_US.utf8"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
THEME = "themes/Flex"
USE_LESS = True
SUMMARY_MAX_LENGTH = 20

PLUGIN_PATHS = ["plugins/"]
PLUGINS = [
    "liquid_tags",
    "pin_to_top",
    # "related_posts",
    "similar_posts",
    # "pelican-githubprojects",
    # "video_privacy_enhancer",
    # "jinja2.ext.i18n",
    # "goodreads_activity",
]
# JINJA_ENVIRONMENT = []

ROBOTS = "index, follow"
STATIC_PATHS = ["images", "extra/robots.txt", "extra/favicon.ico"]
EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
    "extra/favicon.ico": {"path": "favicon.ico"},
}

# Blogroll
LINKS = (
    # ("Pelican", "http://getpelican.com/"),
    # ("Python.org", "http://python.org/"),
    # ("Jinja2", "http://jinja.pocoo.org/"),
    # ("You can modify those links in your config file", "#"),
    # ("Find Me on the Tubes!", "#"),
    ("Resume", "http://resume.ericroc.how"),
)

# Social widget
SOCIAL = (
    ("globe", "https://www.ericroc.how"),
    ("envelope", "mailto:ericrochow@gmail.com"),
    ("rss", "https://www.ericroc.how"),
    ("linkedin", "https://www.linkedin.com/in/erochow/"),
    ("github", "https://github.com/ericrochow"),
    # ("reddit", "#"),
    ("twitter", "https://twitter.com/eric_rochow"),
    ("lastfm", "https://www.last.fm/user/ericrochow"),
    ("spotify", "https://open.spotify.com/user/ericrochow?si=KEmxAAk8QZy31L82MMge4g",),
    ("book", "https://www.goodreads.com/user/show/18841479-eric-rochow"),
)

MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

GOOGLE_ANALYTICS = "UA-135617138-1"
GITHUB_URL = "https://github.com/ericrochow"
GITHUB_USERNAME = "ericrochow"
TWITTER_USERNAME = "eric_rochow"
# GOODREADS_ACTIVITY_FEED = (
# "https://www.goodreads.com/review/list_rss/18841479?key="
# "KyT3ziOY47qSj-aDbM-SDOa3uJn9UkKP6osSP-O42Dd1G4RL&shelf=read"
# )

# TEMPLATE_PAGES = {"templates/goodreads.html": "pages/read-with-me.html"}
TEMPLATE_EXTENSIONS = [".html", ".j2"]
THEME_TEMPLATES_OVERRIDES = ["content/templates/"]
READERS = {"html": None}

DEFAULT_PAGINATION = 10

IGNORE_FILES = [".#*", ".swp", ".tmpl", ".pre"]
# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
