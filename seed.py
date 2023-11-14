#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect("instance/urls.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS links (
                id INTEGER PRIMARY KEY,
                long_url TEXT,
                short_url TEXT,
                views INTEGER,
                created_at DATETIME
                );""")
