#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import json
import sys
import re
import urllib2
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

conn = sqlite3.connect('./data.db')

conn.execute('''CREATE TABLE IF NOT EXISTS news_content(
                id   INTEGER PRIMARY KEY NOT NULL,
                text TEXT                NOT NULL
             )''')

conn.execute('''CREATE TABLE IF NOT EXISTS news(
                id   INTEGER PRIMARY KEY NOT NULL,
                text TEXT                NOT NULL
             )''')

conn.execute('''CREATE TABLE IF NOT EXISTS news_url(
                id   INTEGER PRIMARY KEY NOT NULL,
                text TEXT                NOT NULL UNIQUE
             )''')

def get_news_url():
    for row in conn.execute("SELECT * FROM weibo"):
        try:
            weibo_id = row[0]
            print weibo_id
            match = re.findall(u"(http://t.cn/.{7})", row[1])
            for url in match:
                print url
                conn.execute("INSERT INTO news_url (text) VALUES (?)", (url, ))
                conn.commit()
        except Exception as err:
            print err

def get_news_html():
    for row in conn.execute("SELECT * FROM news_url"):
        try:
            news_id = row[0]
            # print news_id
            url = row[1]
            print url
            request = urllib2.Request(url, headers={"Accept-Encoding": "utf-8", "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
            html = urllib2.urlopen(request).read().decode('utf-8')
            if html != "":
                conn.execute("INSERT INTO news_content (id, text) VALUES (?, ?)", (news_id, html))
                conn.commit()
        except Exception as err:
            print err

def parse_news_html():
    for row in conn.execute("SELECT * FROM news_content"):
        try:
            news_id = row[0]
            html = row[1]
            if html != "":
                soup = BeautifulSoup(html)
                contents = soup.find_all("p")
                news_content = ""
                for paragraph in contents:
                    text = paragraph.get_text()
                    if len(text) >= 20 and not paragraph.find('a'):
                        news_content += text
                if len(news_content) >= 50:
                    conn.execute("INSERT INTO news (id, text) VALUES (?, ?)", (news_id, news_content))
                    conn.commit()
            print news_id
        except Exception as err:
            print err

def solve_news_content():
    for row in conn.execute("SELECT * FROM news"):
        try:
            news_id = row[0]
            content = row[1]
            content = content.replace('\n', '')
            conn.execute("UPDATE news SET text=? WHERE id=?", (content, news_id))
            conn.commit()
            print news_id
        except Exception as err:
            print err

solve_news_content()

