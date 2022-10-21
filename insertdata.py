import csv
import sqlite3
from pathlib import Path

name = "db.sqlite3"
path = Path("E:\\Maroon5").resolve()

sql_create_album = """
CREATE TABLE IF NOT EXISTS album (id INTEGER PRIMARY KEY AUTOINCREMENT, name text);
"""

sql_create_songs = """
CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    album_id INTEGER,
    title TEXT,
    length TEXT
);
"""
insert_album = "INSERT INTO album (name) VALUES (?);"
insert_track = "INSERT INTO songs (album_id, title, length) VALUES (?, ?, ?);"


with sqlite3.connect(name) as conn:
    cur = conn.cursor()
    cur.execute(sql_create_album)
    cur.execute(sql_create_songs)
    conn.commit()
    filenames = path.glob("*.csv")
    for filename in filenames:
        cur.execute(insert_album, (filename.stem,))
        album_id = cur.lastrowid
        with open(filename, "r") as fp:
            for row in csv.DictReader(fp):
                if not row:
                    continue
                cur.execute(insert_track, (album_id, row["title"], row["duration"]))
        conn.commit()
    cur.close()
