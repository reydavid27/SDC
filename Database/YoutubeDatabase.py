#This Python script loads a text file containing JSON data and outputs it to a database
#Programmers: David Acuqui & Carol Chau
#Created for Social Data Collective

import json
import sqlite3 as lite
import isodate


data = ""
value = []
con = lite.connect('SDCdatabase.db')

with con:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Youtube")
    cur.execute("CREATE TABLE Youtube(ID TEXT, Title TEXT, VideoViewCount INT, VideoLength INT, "
                "ChannelName TEXT, ChannelSubscriberCount INT, Categories TEXT, Tags TEXT)")
    value = []
    data_dict = []
    with open("newData.txt", "r") as f:
        data = json.loads(f.read())
    for i in range(len(data)):
        for key in data[i]:
            value.append(key)
    for i in range(len(value)):
        youtube_id = value[i]
        title = data[i][value[i]]["Title"]
        video_length = data[i][value[i]]["VideoLength"]
        video_views = data[i][value[i]]["ViewCount"]
        channel_name = data[i][value[i]]["ChannelName"]
        channel_sub_count = data[i][value[i]]["SubCount"]
        categories = data[i][value[i]]["Categories"]
        tags = data[i][(value[i])]["Tags"]
        #print tags

        cur.execute("INSERT INTO Youtube(ID, Title, VideoViewCount, VideoLength, ChannelName, ChannelSubscriberCount, Categories) "
            "VALUES (?,?,?,?,?,?,?)",
            (youtube_id, title, video_views, video_length, channel_name, channel_sub_count, categories,))
'''
    for i in range(len(value)):
        data_dict = [value[i],
                    data[i][value[i]]["Title"],
                    data[i][value[i]]["VideoLength"],
                    data[i][value[i]]["ViewCount"],
                    data[i][value[i]]["ChannelName"],
                    data[i][value[i]]["SubCount"],
                    data[i][value[i]]["Categories"]
        data.append(zip(youtube_id, title, video_length, video_views, channel_name, channel_sub_count, categories))

    print data
    #cur.executemany("INSERT INTO Youtube(ID, Title, VideoViewCount, VideoLength, ChannelName, ChannelSubscriberCount, Categories) "
    #    "VALUES (?,?,?,?,?,?,?)", data)


'''