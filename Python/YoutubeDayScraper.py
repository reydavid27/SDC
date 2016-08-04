import csv
import json
import requests
import datetime


youtube_id = []
already_stored = set()
date = []
user_id = []
user_info = {}
data = {}
user_dict = []
sdc_data = []
keep_track_of_users = [[], [], [], [], [], [], []]
Num_of_Vids_Watched = [0, 0, 0, 0, 0, 0, 0]
AvgforDay = [0,0,0,0,0,0,0]
mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count = 0, 0, 0, 0, 0, 0, 0
mon_total, tues_total, wed_total, thurs_total, fri_total, sat_total, sun_total = 0, 0, 0, 0, 0, 0, 0

base_url = "https://www.googleapis.com/youtube/v3/"
video_url = base_url + "videos?part=snippet%2C+contentDetails%2C+statistics&id="
rest_vid_url = "&fields=items(contentDetails(caption%2Cdefinition%2Cduration)%2Cetag%2Cid%2Ckind%2Csnippet(categoryId%2CchannelId%2CchannelTitle%2Ctags%2Ctitle)%2Cstatistics(dislikeCount%2CviewCount))%2Ckind&key="
youtube_key = "AIzaSyBhfhYQkrMlAOPlCw_F4QNnT6SBRCmAvc8" #"AIzaSyAeurFNNLzBvFr3XRoGbGALTxq0wkT-w4Y"

class BlankDict(dict):
    def __missing__(self, key):
        return None

def read_file():
    with open("youtube_urls.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url_link = row['url']
            user_row = row['user_id']
            date_row = row['timestamp']
            yt_id = url_link[32:]
            date_fix = date_row[:10]
            if "youtube.com/watch" in url_link:
                if len(yt_id) > 11:
                    pass
                else:
                    if yt_id not in already_stored:
                        already_stored.add(yt_id)
                        youtube_id.append(yt_id.encode(encoding='UTF-8'))
                        date.append(date_fix)
                        user_day(user_row, yt_id, date_fix)
    calculate_avg()
    print "Mon count ", mon_count
    print "Tues count ", tues_count
    print "Wed count ", wed_count
    print "Thurs count ", thurs_count
    print "Fri count ", fri_count
    print "Sat count ", sun_count
    print "Sun count ", sun_count

    print "Mon total", mon_total
    print "Tues total", tues_total
    print "Wed total", wed_total
    print "Thurs total", thurs_total
    print "Fri total", fri_total
    print "Sat total", sat_total
    print "Sun total", sun_total

def user_day(x, y, z):
    full_url = video_url + y + "&key=" + youtube_key
    result = requests.get(full_url)
    json_contents = json.loads(result.content, object_hook=BlankDict)
    for item in json_contents["items"]:
        if item["kind"]:
            month = int(z[5:7])
            day = int(z[8:])
            year = int(z[:4])
            date_together = (month, day, year)
            weekday = datetime.date(year, month, day).strftime("%A")
            key = x
            count_total_days(key, date_together, weekday)
            user_info.setdefault(key,[])
            user_info[key].append(weekday)
        else:
            pass



def count_total_days(x, y, z):
    global mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count
    global mon_total, tues_total, wed_total, thurs_total, fri_total, sat_total, sun_total
    user = x

    if z == "Monday:":
        mon_count += 1
        if user not in keep_track_of_users[0]:
            keep_track_of_users[0].append(user)
            Num_of_Vids_Watched[0] = Num_of_Vids_Watched[0] + 1

    elif z == "Tuesday:":
        tues_count += 1
        if user not in keep_track_of_users[1]:
            keep_track_of_users[1].append(user)
            Num_of_Vids_Watched[1] = Num_of_Vids_Watched[1] + 1

    elif z == "Wednesday:":
        wed_count += 1
        if user not in keep_track_of_users[2]:
            keep_track_of_users[2].append(user)
            Num_of_Vids_Watched[2] = Num_of_Vids_Watched[2] + 1

    elif z == "Thursday:":
        thurs_count += 1
        if user not in keep_track_of_users[3]:
            keep_track_of_users[3].append(user)
            Num_of_Vids_Watched[3] = Num_of_Vids_Watched[3] + 1

    elif z == "Friday:":
        fri_count += 1
        if user not in keep_track_of_users[4]:
            keep_track_of_users[4].append(user)
            Num_of_Vids_Watched[4] = Num_of_Vids_Watched[4] + 1

    elif z == "Saturday:":
        sat_count += 1
        if user not in keep_track_of_users[5]:
            keep_track_of_users[5].append(user)
            Num_of_Vids_Watched[5] = Num_of_Vids_Watched[5] + 1

    elif z == "Sunday:":
        sun_count += 1
        if user not in keep_track_of_users[6]:
            keep_track_of_users[6].append(user)
            Num_of_Vids_Watched[6] = Num_of_Vids_Watched[6] + 1

    if y not in already_stored:
        already_stored.add(y)
        if z == "Monday":
            mon_total += 1
        elif z == "Tuesday":
            tues_total +=1
        elif z == "Wednesday":
            wed_total += 1
        elif z == "Thursday":
            thurs_total += 1
        elif z == "Friday":
            fri_total += 1
        elif z == "Saturday":
            sat_total += 1
        elif z == "Sunday":
            sun_total += 1
    else:
        pass

def calculate_avg():
    AvgforDay[0] = (mon_count / (Num_of_Vids_Watched[0] * mon_total))
    AvgforDay[1] = (tues_count / (Num_of_Vids_Watched[1] * tues_total))
    AvgforDay[2] = (wed_count / (Num_of_Vids_Watched[2] * wed_total))
    AvgforDay[3] = (thurs_count / (Num_of_Vids_Watched[3] * thurs_total))
    AvgforDay[4] = (fri_count / (Num_of_Vids_Watched[4] * fri_total))
    AvgforDay[5] = (sat_count / (Num_of_Vids_Watched[5] * sat_total))
    AvgforDay[6] = (tues_count / (Num_of_Vids_Watched[6] * sun_total))

def count_days():
    read_file()
    global mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count
    mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count = 0, 0, 0, 0, 0, 0, 0

    for key, value in user_info.iteritems():
        for val in value:
            if val == "Monday":
                mon_count += 1
            elif val == "Tuesday":
                tues_count += 1
            elif val == "Wednesday":
                wed_count += 1
            elif val == "Thursday":
                thurs_count += 1
            elif val == "Friday":
                fri_count += 1
            elif val == "Saturday":
                sat_count += 1
            elif val == "Sunday":
                sun_count += 1

        mon_count = mon_count / mon_total
        tues_count = tues_count / tues_total
        wed_count = wed_count / wed_total
        thurs_count = thurs_count / thurs_total
        fri_count = fri_count / fri_total
        sat_count = sat_count / sat_total
        sun_count = sun_count / sun_total

        user_dict.append((key, mon_count, tues_count,
                         wed_count, thurs_count,
                         fri_count, sat_count, sun_count))
        
        mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count = 0,0,0,0,0,0,0

def json_file():
    #read_file()
    count_days()


    for i in range(len(user_dict)):
        sdc_data.append({
            user_dict[i][0]:{
                "Monday": user_dict[i][1],
                "Tuesday": user_dict[i][2],
                "Wednesday": user_dict[i][3],
                "Thursday": user_dict[i][4],
                "Friday": user_dict[i][5],
                "Saturday": user_dict[i][6],
                "Sunday": user_dict[i][7]
                }
            })
        
    with open("UserAvgDays.txt", "w") as f:
        json.dump(sdc_data, f, sort_keys = True, indent = 4, ensure_ascii=True)



    sdc_data2 = []
    for i in range(len(AvgforDay)):
        sdc_data2.append({
            "Monday": AvgforDay[0],
            "Tuesday": AvgforDay[1],
            "Wednesday": AvgforDay[2],
            "Thursday": AvgforDay[3],
            "Friday": AvgforDay[4],
            "Saturday": AvgforDay[5],
            "Sunday": AvgforDay[6]
        })

    with open("TotalAvgDays.txt", "w") as n:
        json.dump(sdc_data2, n, indent= 4)

if __name__ == '__main__':
    #count_days()
    json_file()
    #read_file()
    print "success"
























                        
