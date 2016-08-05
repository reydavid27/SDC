#This Python script loads a text file containing JSON data and outputs it to a database
#Programmers: David Acuqui
#Created for Social Data Collective

import json
import sqlite3 as lite

con = lite.connect('SDCdatabase.db')

with con:
    key_array = [] #array to hold the dictionary keys

    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS Youtube")
    cur.execute("CREATE TABLE Youtube(ID TEXT, Title TEXT, VideoViewCount INT, VideoLength INT, "
                "ChannelName TEXT, ChannelSubscriberCount INT, Categories TEXT, Tags TEXT)")


    with open("YoutubeData.txt", "r") as f:
        data = json.loads(f.read())
    #loop through the data to append the keys to the array
    for i in range(len(data)):
        for key in data[i]:
            key_array.append(key)
    for i in range(len(key_array)):
        youtube_id = key_array[i]
        title = data[i][key_array[i]]["Title"]
        video_length = data[i][key_array[i]]["VideoLength"]
        video_views = data[i][key_array[i]]["ViewCount"]
        channel_name = data[i][key_array[i]]["ChannelName"]
        channel_sub_count = data[i][key_array[i]]["SubCount"]
        categories = data[i][key_array[i]]["Categories"]
        tags = data[i][(key_array[i])]["Tags"]

        #the following loop goes through each item in tags and stores it as a string
        var = " "
        if tags is not None:
            for tag in tags:
                var += tag + ", "
        else:
            var += tag
            var = "None"

        #put the above variables into the SQL table Youtube
        cur.execute("INSERT INTO Youtube(ID, Title, VideoViewCount, VideoLength, ChannelName, ChannelSubscriberCount, Categories, Tags) "
            "VALUES (?,?,?,?,?,?,?,?)",
            (youtube_id, title, video_views, video_length, channel_name, channel_sub_count, categories, var, ))