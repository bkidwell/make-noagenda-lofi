#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: graceful error handling
# TODO: use imagemagick to convert covert art from whatever format it is to 256x256 (?) jpeg
# TODO: remove font and script tags from description
# TODO: output path: files/$year/$month/filename
# TODO: get post_date from filesystem date of input files

import db
import re
from os import path, listdir, makedirs
from mutagenx.id3 import ID3
from mutagenx.oggopus import OggOpus
from subprocess import Popen, PIPE

app_dir = path.abspath(path.dirname(__file__) + '/..')
db.init(app_dir)

def get_input_files():
    dirlist = listdir(app_dir + '/input')
    f = []
    for item in dirlist:
        if item[-4:].lower() == '.mp3':
            f.append(item)
    return f

# -----

files = [f for f in get_input_files() if db.is_new(f)]
for f in files:
    m = re.match(r'.*?(\d{4}-\d{2}-\d{2}).*?', f)
    date_text = m.group(1) if m is not None else ''
    year = date_text[:4]
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
    t_num = str(tags.get('TRCK', ''))
    t_title = str(tags.get('TIT2', ''))
    t_artist = str(tags.get('TPE1', ''))
    t_album = str(tags.get('TALB', ''))
    t_desc = str(tags.get("COMM::'eng'", '')).strip()

    if not path.exists(new_folder): makedirs(new_folder)
    cover_file = open(new_folder + '/' + base_filename + '.png', 'wb')
    cover_file.write(t_cover.data)
    cover_file.close()

    post_title = [a for a in t_desc.splitlines(False) if len(a.strip())][0]

    print(f)
    print(date_text)
    print(episode_num_text)
    print(new_filename)
    print(post_title)
    #print(t_num, t_title, t_artist, t_album)
    #print(t_desc)

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

    db.save(
        orig_filename=f,
        folder=year,
        opus=new_filename,
        tumbnail=base_filename + '.png',
        date_text=date_text,
        episode_num_text=episode_num_text,
        post_title=post_title,
        desc=t_desc
    )

