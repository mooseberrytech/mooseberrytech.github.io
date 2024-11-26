#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Adriana Vasiu'
SITENAME = ''
SITEURL = ''

THEME = 'themes/attila'
PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

MENUITEMS = (('Home', '/'),
             ('Author', '/author/adriana-vasiu/'),
             ('Testing', '/category/testing/'),
             ('Development', '/category/development/'),
             ('Instrumentation', '/category/instrumentation/'),
             ('Automation', '/category/automation/'),
             ('Ways of Working', '/category/ways-of-working/'),)

# Blogroll
LINKS = ()

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

# Pagination
DEFAULT_PAGINATION = 3
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Post and Pages path
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}.html'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Tags and Category path
CATEGORY_URL = 'category/{slug}'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_SAVE_AS = 'catgegories.html'
TAG_URL = 'tag/{slug}'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_SAVE_AS = 'tags.html'

# Author
AUTHOR_URL = 'author/{slug}'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_SAVE_AS = 'authors.html'

AUTHOR_META = {
  "adriana vasiu": {
    "name": "Adriana Vasiu",
    "image": "images/mooseberry_tech-512x512-NO-TEXT.png",
    "linkedin": "adrianavasiu",
    "bio": "I currently work as a consultant on software development."
  }
}

HOME_COVER = 'images/mooseberry_tech-BACKGOURND.jpg'
