#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from os.path import dirname, exists
from os import makedirs

db_file = None
conn = None
app_dir = None

def init(p):
    global db_file, app_dir
    app_dir = p
    db_file = app_dir + '/state/history.sqlite'
    get_db()

def get_db():
    global conn
    if conn: return conn

    if(not exists(dirname(db_file))):
        makedirs(dirname(db_file))
    e = exists(db_file)
    conn = sqlite3.connect(db_file)
    if not e:
        conn.cursor().executescript("""
            CREATE TABLE history (
                orig_filename TEXT NOT NULL,
                folder TEXT NOT NULL,
                time_utc TEXT NOT NULL,
                opus TEXT NOT NULL,
                thumbnail TEXT NOT NULL,
                date_text TEXT NOT NULL,
                episode_num_text TEXT NOT NULL,
                post_title TEXT NOT NULL,
                desc TEXT NOT NULL
            );
            CREATE UNIQUE INDEX i_orig_filename on history (orig_filename ASC);
            CREATE INDEX i_time_utc on history (time_utc ASC);
        """)
        conn.commit()
    return conn

def is_new(f):
    c = conn.cursor()
    count = c.execute("""
        SELECT count(*) FROM history WHERE orig_filename = ?
    """, (f,)).fetchone()[0]
    return count == 0

def save(
    orig_filename, folder, opus, tumbnail, date_text,
    episode_num_text, post_title, desc
):
    c = conn.cursor()
    c.execute("""
        INSERT INTO history (
            orig_filename, time_utc,
            folder, opus, thumbnail,
            date_text, episode_num_text, post_title, desc
        ) VALUES (
            ?, datetime('now'),
            ?, ?, ?,
            ?, ?, ?, ?
        )
    """, (
        orig_filename, folder, opus, tumbnail, date_text,
        episode_num_text, post_title, desc
    ))
    conn.commit()
