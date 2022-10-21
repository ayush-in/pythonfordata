import pyodbc
import sqlite3

connection = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=GGKU5DELL1915;'
                      'Database=scrappingdb;'
                      'Trusted_Connection=yes;')

odbc_cur = connection.cursor()

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()

# name = "db.sqlite3"
album_tracks = """
CREATE TABLE album_tracks(
    id int PRIMARY KEY,
    album_name varchar(100),
    title varchar(100),
    length varchar(100) 
    );               
"""
join = """
SELECT s.id,a.name, s.title, s.length from album a INNER JOIN songs s on a.id = s.album_id;
"""
insert = """
insert into album_tracks(id, album_name, title, length) values(?,?,?,?);
"""

if not odbc_cur.tables(table='album_tracks', tableType='TABLE').fetchone():
    odbc_cur.execute(album_tracks)
data  = cur.execute(join)
for i in data:
    odbc_cur.execute(insert,i)


conn.commit()

cur.close()

connection.commit()
connection.close()
