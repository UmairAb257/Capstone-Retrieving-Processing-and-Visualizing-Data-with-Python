import json
import sqlite3

sqlconnect = sqlite3.connect('rosterdata.sqlite')
sqlcursor = sqlconnect.cursor()

sqlcursor.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;

CREATE TABLE User (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name  TEXT UNIQUE
);

CREATE TABLE Course (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);

CREATE TABLE Member (
    user_id  INTEGER,
    course_id  INTEGER,
    role  INTEGER,
    PRIMARY KEY (user_id, course_id)
);
''')

filein = input('Enter filename: ')
if len(filein) < 1: filein = 'roster_data.json'

opfile = open(filein).read()
loadfile = json.loads(opfile)

for line in loadfile:
    name = line[0];
    title = line[1];
    role = line[2]

    sqlcursor.execute('''INSERT OR IGNORE INTO User (name)
              VALUES ( ? )''', (name, ) )
    sqlcursor.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = sqlcursor.fetchone()[0]

    sqlcursor.execute('''INSERT OR IGNORE INTO Course (title)
              VALUES ( ? )''', (title, ) )
    sqlcursor.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = sqlcursor.fetchone()[0]

    sqlcursor.execute('''INSERT OR REPLACE INTO Member
            (user_id, course_id, role) VALUES ( ?, ?, ? )''',
            ( user_id, course_id, role ) )

    sqlconnect.commit()
