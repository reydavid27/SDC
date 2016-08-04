import csv
import json
import requests
import isodate

#arrays and dictionary
youtube_id = []
already_stored = set()
user_id = []
vid_title = []
data = {}
new_user_ids = []
sdc_data = []

#URL building for making the API calls
youtube_key = "AIzaSyAeurFNNLzBvFr3XRoGbGALTxq0wkT-w4Y"
base_url = "https://www.googleapis.com/youtube/v3/"
video_url = base_url + "videos?part=snippet%2C+contentDetails%2C+statistics&id="
rest_vid_url = "&fields=items(contentDetails(caption%2Cdefinition%2Cduration)%2Cetag%2Cid%2Ckind%2Csnippet(categoryId%2CchannelId%2CchannelTitle%2Ctags%2Ctitle)%2Cstatistics(dislikeCount%2CviewCount))%2Ckind&key="
channel_url = base_url + "channels?part=statistics&id="
category_url = base_url + "videoCategories?part=snippet&id="

class BlankDict(dict):
    def __missing__(self, key):
        return None

def read_file():
    with open("sampletest.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url_link = row['url']
            user_row = row['user_id']
            yt_id = url_link[32:] #only grab the ID from the url link
            if "youtube.com/watch" in url_link:
                if len(yt_id) > 11:
                    pass
                else:
                    if yt_id not in already_stored:
                        already_stored.add(yt_id)
                        youtube_id.append(yt_id.encode(encoding='UTF-8'))
                        user_id.append(user_row)

def get_category(x):
    full_url = category_url + x + "&fields=items(snippet)&key=" + youtube_key
    result = requests.get(full_url)
    json_contents = json.loads(result.content)
    for item in json_contents["items"]:
        var = item["snippet"]["title"]
        return var

def get_sub_count(x):
    full_url = channel_url + x + "&key=" + youtube_key
    result = requests.get(full_url)
    json_contents = json.loads(result.content, object_hook=BlankDict)
    for item in json_contents["items"]:
        var = item["statistics"]["subscriberCount"]
        return var

def youtube_data():
    read_file()

    for ids in youtube_id:
        full_url = video_url + ids + rest_vid_url + youtube_key
        result = requests.get(full_url)
        json_contents = json.loads(result.content, object_hook=BlankDict)
        for item in json_contents["items"]:
            if item["kind"]:
                data[ids] = []
                new_user_ids.append(ids)
                youtube_id.remove(ids)
                category = get_category(item["snippet"]["categoryId"])
                sub_count = get_sub_count(item["snippet"]["channelId"])
                datum = [item["snippet"]["title"],
                         item["snippet"]["channelTitle"],
                         item["snippet"]["channelId"],
                         isodate.parse_duration(item["contentDetails"]["duration"]),
                         item["statistics"]["viewCount"],
                         item["snippet"]["tags"],
                         category,
                         sub_count]
                data[ids].append(datum)
            else:
                pass

def json_file():
    youtube_data()

    for i in range(len(new_user_ids)):
        sdc_data.append({
            new_user_ids[i]: {
                "Title": data[new_user_ids[i]][0][0],
                "ViewCount": data[new_user_ids[i]][0][4],
                "VideoLength": str([new_user_ids[i]][0][3]),
                "ChannelName": data[new_user_ids[i]][0][1],
                "Categories": data[new_user_ids[i]][0][6],
                "SubCount": data[new_user_ids[i]][0][7],
                "Tags": data[new_user_ids[i]][0][5]
                }
             })

    with open("SDC_data.txt", "w") as f:
        json.dump(sdc_data, f, sort_keys = True, indent = 4, ensure_ascii=True)

if __name__ == '__main__':
    json_file()
    print "success"