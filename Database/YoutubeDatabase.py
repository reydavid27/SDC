import json
import sqlite3 as lite

data = ""
value = []
con = lite.connect('sdctest.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Youtube")
    cur.execute("CREATE TABLE Youtube(ID TEXT, Title TEXT)")
    value = []
    with open("newData.txt", "r") as f:
        data = json.loads(f.read())
    for i in range(len(data)):
        for key in data[i]:
            value.append(key)
    for i in range(len(value)):
        youtube_id = value[i]
        title = data[i][str(value[i])]["Title"]
        cur.execute("INSERT INTO Youtube(ID, Title) VALUES(?, ?)", (youtube_id , title,))        
    
