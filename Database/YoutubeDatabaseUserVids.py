import json
import sqlite3 as lite

con = lite.connect('SDCdatabase.db')

with con:
    key_array = []

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS UserAvg")
    cur.execute("CREATE TABLE UserAvg (UserID TEXT, AvgVidsWatched INT)")

    with open("SDCuserdata.txt", "r") as f:
        data = json.loads(f.read())
    
    for i in range(len(data)):
        for key in data[i]:
            key_array.append(key)
    
    for i in range(len(data)):
        userid = key_array[i]
        avgvids = data[i][key_array[i]]

        cur.execute("INSERT INTO UserAvg(UserID, AvgVidsWatched) VALUES (?,?)",
                    (userid, avgvids, ))
        
