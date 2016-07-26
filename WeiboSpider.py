import sqlite3
import time
import json

conn = sqlite3.connect('./data.db')

conn.execute('''CREATE TABLE IF NOT EXISTS weibo(
                id   INTEGER PRIMARY KEY NOT NULL,
                text TEXT                NOT NULL
             )''')

since_id = 0
while 1:
    import httplib, urllib
    headers = {"Cache-Control": "no-cache"}
    c = httplib.HTTPSConnection("api.weibo.com")
    c.request("GET", "/2/statuses/home_timeline.json?access_token=2.00G7FZADTeJdZD019667c1a6VD5t5D&count=100&since_id=" + str(since_id) + "&feature=1", headers = headers)
    response = c.getresponse()
    print response.status, response.reason
    # data = response.read()
    data = json.loads(response.read(), 'utf8')
    # print data
    # print data['statuses']
    for statuse in data['statuses']:
        mid = statuse['id']
        # print statuse['text'].replace("'", "''")
        # print statuse['text']
        since_id = max(since_id, mid)
        try:
            conn.execute("INSERT INTO weibo VALUES (" + str(mid) + ", '" + statuse['text'].replace("'", "''") + "')")
            conn.commit()
        except sqlite3.IntegrityError:
            print str(mid) + " already exists"
    print since_id
    time.sleep(5 * 60)
