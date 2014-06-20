#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import PyRSS2Gen
from os import path

app_dir = path.abspath(path.dirname(__file__) + '/..')

rss = PyRSS2Gen.RSS2(
    title = "No Agenda Show 16kbps Opus",
    link = "http://itm.im/noagendalite",
    description = "Low-bandwidth mirror of the No Agenda Show in 16 kilobits per second Opus Audio format",

    lastBuildDate = datetime.datetime.now(),

    items = [
        PyRSS2Gen.RSSItem(
            title = "title 1",
            link = "http://noagendalite.glump.net/assets/2014/NA-lofi-625-2014-06-12-Final.opus",
            description = "Description",
            guid = PyRSS2Gen.Guid("http://noagendalite.glump.net/assets/2014/NA-lofi-625-2014-06-12-Final.opus"),
            pubDate = datetime.datetime(2014, 6, 12, 19, 0),
            enclosure = PyRSS2Gen.Enclosure(
                "http://noagendalite.glump.net/assets/2014/NA-lofi-625-2014-06-12-Final.opus",
                1234,
                'audio/ogg'
            )
        ),
        PyRSS2Gen.RSSItem(
            title = "title 1",
            link = "http://noagendalite.glump.net/assets/2014/NA-lofi-627-2014-06-19-Final.opus",
            description = "Description",
            guid = PyRSS2Gen.Guid("http://noagendalite.glump.net/assets/2014/NA-lofi-627-2014-06-19-Final.opus"),
            pubDate = datetime.datetime(2014, 6, 19, 19, 0),
            enclosure = PyRSS2Gen.Enclosure(
                "http://noagendalite.glump.net/assets/2014/NA-lofi-627-2014-06-19-Final.opus",
                1234,
                'audio/ogg'
            )

        ),
    ])

rss.write_xml(open(app_dir + "/output/pyrss2gen.xml", "w"))

"""
 PyRSS2Gen.RSSItem(
       enclosure = PyRSS2Gen.Enclosure(
                                        "http://www.example.com/url",
                                        17176948, # file size
                                        "mime-type"))
"""