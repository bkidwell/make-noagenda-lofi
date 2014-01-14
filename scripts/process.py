#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: graceful error handling

import sqlite3
import re
import json
from datetime import datetime
from os import path, listdir, makedirs
from mutagen.id3 import ID3
from mutagen.oggopus import OggOpus
from base64 import b64encode
from subprocess import Popen, PIPE

app_dir = path.abspath(path.dirname(__file__) + '/..')
db_file = app_dir + '/state/history.sqlite'

def get_db():
    e = path.exists(db_file)
    conn = sqlite3.connect(db_file)
    if not e:
        conn.cursor().executescript("""
            CREATE TABLE history (
                filename TEXT NOT NULL,
                time_utc TEXT NOT NULL
            );
            CREATE UNIQUE INDEX i_filename on history (filename ASC);
            CREATE INDEX i_time_utc on history (time_utc ASC);
        """)
    return conn

def get_input_files():
    dirlist = listdir(app_dir + '/input')
    f = []
    for item in dirlist:
        if item[-4:].lower() == '.mp3':
            f.append(item)
    return f

def is_new(f):
    c = conn.cursor()
    count = c.execute("""
        SELECT count(*) FROM history WHERE filename = ?
    """, (f,)).fetchone()[0]
    if count == 0:
        # TODO: don't write file into history until it is successfully processed
        c.execute("""
            INSERT INTO history (filename, time_utc) VALUES (?, datetime('now'))
        """, (f,))
        conn.commit()
    return count == 0

# -----

conn = get_db()
files = [f for f in get_input_files() if is_new(f) or True]
year = unicode(datetime.now().year)
for f in files:
    m = re.match(r'.*?(\d{4}-\d{2}-\d{2}).*?', f)
    date_text = m.group(1) if m is not None else ''
    m = re.match(r'NA-([\d\.]{3,6})-.*?', f)
    episode_num_text = m.group(1) if m is not None else ''

    src_filepath = app_dir + '/input/' + f

    new_filename = re.sub(r'^NA-', r'NA-lofi-', f)
    base_filename = new_filename[:-4] 
    new_filename = base_filename + '.opus'
    new_folder = app_dir + '/output/' + year
    new_filepath = new_folder + '/' + new_filename

    tags = ID3(app_dir + '/input/' + f)
    t_cover = tags.get('APIC:', None)
    t_num = unicode(tags.get('TRCK', ''))
    t_title = unicode(tags.get('TIT2', ''))
    t_artist = unicode(tags.get('TPE1', ''))
    t_album = unicode(tags.get('TALB', ''))
    t_desc = unicode(tags.get("USLT::'eng'", '')).strip()

    if not path.exists(new_folder): makedirs(new_folder)
    cover_file = open(new_folder + '/' + base_filename + '.jpg', 'wb')
    cover_file.write(t_cover.data)
    cover_file.close()

    title2 = [a for a in unicode(t_desc).splitlines(False) if len(a.strip())][1]
    post_title = unicode(t_title) + u' – ' + title2

    print(f)
    print(date_text)
    print(episode_num_text)
    print(new_filename)
    print(post_title)
    print(t_num, t_title, t_artist, t_album)
    #print(t_desc)

    if False:
        p1 = Popen([
            'lame', '--decode', src_filepath, '-'
        ], stdout=PIPE)
        p2 = Popen([
            'opusenc', '--bitrate', '16', '--downmix-mono', '-', new_filepath
        ], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output = p2.communicate()[0]
        print(output)

    tagsout = OggOpus(new_filepath)
    tagsout['TITLE'] = t_title
    tagsout['ALBUM'] = t_album
    tagsout['TRACKNUMBER'] = t_num
    tagsout['ARTIST'] = t_artist
    tagsout['DESCRIPTION'] = t_desc
    tagsout.save()

    q_folder = app_dir + '/output/queue'
    q_filepath = q_folder + '/' + base_filename + '.data'
    if not path.exists(q_folder): makedirs(q_folder)
    data = {
        'year': year,
        'opusfile': base_filename + '.opus',
        'jpgfile': base_filename + '.jpg',
        'date_text': date_text,
        'episode_num_text': episode_num_text,
        'post_title': post_title
    }
    queue_file = open(q_filepath, 'w')
    queue_file.write(json.dumps(data))
    queue_file.close()
