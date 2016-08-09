import requests
import json
import csv
from collections import Counter


user_info = {}
user_avg = {}
users_total_vids = Counter()
users_total_days = Counter()

base_url = "https://www.googleapis.com/youtube/v3/"
video_url = base_url + "videos?part=snippet%2C+contentDetails%2C+statistics&id="
youtube_key = "AIzaSyBhfhYQkrMlAOPlCw_F4QNnT6SBRCmAvc8"

class BlankDict(dict):
    def __missing__(self, key):
        return None

def read_file():
    already_stored = set()
    with open("sampletest.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url_link = row['url']
            youtube_id = url_link[32:].encode(encoding='UTF-8')  # fixing the url string to grab the Youtube ID
            user_id = row['user_id']
            date = row['timestamp']
            date_fix = date[:10] #fixing the date string to delete the time stamp
            if "youtube.com/watch" in url_link:
                if len(youtube_id) > 11:
                    pass
                else:
                    if youtube_id not in already_stored:
                        already_stored.add(youtube_id)
                        user_day(user_id, youtube_id, date_fix)

def user_day(user_id, youtube_id, date_fix):
    full_url = video_url + youtube_id + "&key=" + youtube_key
    result = requests.get(full_url, verify=True)
    json_contents = json.loads(result.content, object_hook=BlankDict)
    for item in json_contents["items"]:
        if item["kind"]:
            key = user_id
            users_total_vids[key] += 1
            user_info.setdefault(key, [])
            user_info[key].append(date_fix)
        else:
            pass

def count_total_days_user():
    read_file()
    already_user = set()
    count = 0
    for key, value in user_info.iteritems():
        for val in value:
            if val not in already_user:
                already_user.add(val)
                count += 1
        users_total_days[key] = count
        already_user = set()
        count = 0

def calculate_avg():
    count_total_days_user()
    for key, value in users_total_vids.iteritems() and users_total_days.iteritems():
        var = users_total_vids[key]/users_total_days[key]
        user_avg[key] = var

def output_json():
    calculate_avg()
    sdc_data = []
    for avg in user_avg:
        sdc_data.append({
            avg: user_avg[avg]
        })
    with open("SDCuserdata.txt", "w") as f:
        json.dump(sdc_data, f, sort_keys=True, indent=4, ensure_ascii=True)


if __name__ == '__main__':
    output_json()
    print "success"