import requests
import json
import csv
from collections import Counter

user_info = {} #Holds the key (user id) and value (day the user watched a vid)
user_avg = {} #Holds the key (user id) and value (avg vid watched)
users_total_vids = Counter() #Holds the number of videos a user has watched
users_total_days = Counter() #Holds the number of days the user spent watching vids

#building the url for the API call
base_url = "https://www.googleapis.com/youtube/v3/"
video_url = base_url + "videos?part=snippet%2C+contentDetails%2C+statistics&id="
youtube_key = "AIzaSyBhfhYQkrMlAOPlCw_F4QNnT6SBRCmAvc8"

class BlankDict(dict):
    def __missing__(self, key):
        return None

def read_file():
    already_stored = set()
    with open("youtube_urls.csv") as csvfile:
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
                        already_stored.add(youtube_id) #using this set so we don't take duplicates of the url
                        user_day(user_id, youtube_id, date_fix)
'''
This function does three things
1) Makes an API call
2) Counts the number of videos an individual user watches
3) Builds a dictionary that contains the user id with value of a date (when they watched the vid)
'''
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
'''
This function is used to count how many days the
user spent watching the videos
'''
def count_total_days_user():
    read_file()
    already_user = set() #set to keep track of dates.  Don't want to take duplicate dates
    count = 0
    for key, value in user_info.iteritems():
        for val in value:
            if val not in already_user:
                already_user.add(val)
                count += 1
        users_total_days[key] = count #add the total number of days to the Counter
        already_user = set() #set the set back to zero for the next user
        count = 0

#Function to calculate the average number of videos a user watched
def calculate_avg():
    count_total_days_user()
    for key, value in users_total_vids.iteritems() and users_total_days.iteritems():
        var = users_total_vids[key]/users_total_days[key]
        user_avg[key] = var #Pass the key and value to the dictionary

#Function to output the results into a json file
def output_json():
    calculate_avg()
    sdc_data = [] #list to hold the info to be dumped
    for avg in user_avg:
        sdc_data.append({
            avg: user_avg[avg]
        })
    with open("SDCuserdata.txt", "w") as f:
        json.dump(sdc_data, f, sort_keys=True, indent=4, ensure_ascii=True)

if __name__ == '__main__':
    output_json()
    print "success"