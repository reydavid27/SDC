import csv
import json
import requests
import datetime

#These are the arrays and variables declared for use
youtube_id = []
already_stored = set()
date = []
user_id = []
user_info = {}
data = {}
user_dict = []
sdc_data = []
keepTrackofUsers = [[], [], [], [], [], [], []]
numofVidsWatched = [0, 0, 0, 0, 0, 0, 0]
AvgforDay = [0,0,0,0,0,0,0]
mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count = 0, 0, 0, 0, 0, 0, 0
mon_total, tues_total, wed_total, thurs_total, fri_total, sat_total, sun_total = 0, 0, 0, 0, 0, 0, 0


#These are used for the url building to make the API call
base_url = "https://www.googleapis.com/youtube/v3/"
video_url = base_url + "videos?part=snippet%2C+contentDetails%2C+statistics&id="
rest_vid_url = "&fields=items(contentDetails(caption%2Cdefinition%2Cduration)%2Cetag%2Cid%2Ckind%2Csnippet(categoryId%2CchannelId%2CchannelTitle%2Ctags%2Ctitle)%2Cstatistics(dislikeCount%2CviewCount))%2Ckind&key="
youtube_key = "AIzaSyBhfhYQkrMlAOPlCw_F4QNnT6SBRCmAvc8"
youtube_key2 = "AIzaSyAeurFNNLzBvFr3XRoGbGALTxq0wkT-w4Y"

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
            yt_id = url_link[32:] #fixing the url string to grab the Youtube ID
            date_fix = date_row[:10] #fixing the date string to delete the time stamp
            #print date_fix
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
    '''
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
    '''

#A function used to convert the date into a weekday string
#and appends the User ID and Weekday into a dictionary
def user_day(x, y, z):
    full_url = video_url + y + "&key=" + youtube_key
    result = requests.get(full_url, verify=True)
    json_contents = json.loads(result.content, object_hook=BlankDict)
    for item in json_contents["items"]:
        if item["kind"]:
            #month = int(z[5:7])
            #day = int(z[8:])
            #year = int(z[:4])
            month = int(z[:1])
            day = int(z[2:4])
            year = int(z[5:])
            date_together = (month, day, year)
            weekday = datetime.date(year, month, day).strftime("%A")
            key = x
            count_total_days(key, date_together, weekday)
            user_info.setdefault(key,[])
            user_info[key].append(weekday)
        else:
            pass
'''
A function used to gather the info needed to calculate the average number of videos watched.
It takes three parameters: x = key/User ID , y = date_together , z = weekday
KeepTrackofUsers is an array of an array size 7 (for the days of the week)
NumOfVidsWatched is an array for also keeping count of the days of the week
'''
def count_total_days(x, y, z):
    global mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count
    global mon_total, tues_total, wed_total, thurs_total, fri_total, sat_total, sun_total
    user = x

    if z == "Monday":
        mon_count += 1
        if user not in keepTrackofUsers[0]:
            keepTrackofUsers[0].append(user)
            numofVidsWatched[0] = numofVidsWatched[0] + 1

    elif z == "Tuesday":
        tues_count += 1
        if user not in keepTrackofUsers[1]:
            keepTrackofUsers[1].append(user)
            numofVidsWatched[1] = numofVidsWatched[1] + 1

    elif z == "Wednesday":
        wed_count += 1
        if user not in keepTrackofUsers[2]:
            keepTrackofUsers[2].append(user)
            numofVidsWatched[2] = numofVidsWatched[2] + 1

    elif z == "Thursday":
        thurs_count += 1
        if user not in keepTrackofUsers[3]:
            keepTrackofUsers[3].append(user)
            numofVidsWatched[3] = numofVidsWatched[3] + 1

    elif z == "Friday":
        fri_count += 1
        if user not in keepTrackofUsers[4]:
            keepTrackofUsers[4].append(user)
            numofVidsWatched[4] = numofVidsWatched[4] + 1

    elif z == "Saturday":
        sat_count += 1
        if user not in keepTrackofUsers[5]:
            keepTrackofUsers[5].append(user)
            numofVidsWatched[5] = numofVidsWatched[5] + 1

    elif z == "Sunday":
        sun_count += 1
        if user not in keepTrackofUsers[6]:
            keepTrackofUsers[6].append(user)
            numofVidsWatched[6] = numofVidsWatched[6] + 1

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
'''
This function calculates the average, using the info from
the Count_Total_days function
'''
def calculate_avg():
    if numofVidsWatched[0] == 0 or mon_total == 0:
        pass
    else:
        AvgforDay[0] = (mon_count / (numofVidsWatched[0] * mon_total))
    if numofVidsWatched[1] == 0 or tues_total == 0:
        pass
    else:
        #print "videos watched tues: ", numofVidsWatched[1]
        AvgforDay[1] = (tues_count / (numofVidsWatched[1] * tues_total))
        #print "avg for tues ", AvgforDay[1]
    if numofVidsWatched[2] == 0 or wed_total == 0:
        pass
    else:
        AvgforDay[2] = (wed_count / (numofVidsWatched[2] * wed_total))
    if numofVidsWatched[3] == 0 or thurs_total == 0:
        pass
    else:
        AvgforDay[3] = (thurs_count / (numofVidsWatched[3] * thurs_total))
    if numofVidsWatched[4] == 0 or fri_total == 0:
        pass
    else:
        AvgforDay[4] = (fri_count / (numofVidsWatched[4] * fri_total))
    if numofVidsWatched[5] == 0 or sat_total == 0:
        pass
    else:
        AvgforDay[5] = (sat_count / (numofVidsWatched[5] * sat_total))
    if numofVidsWatched[6] == 0 or sun_total == 0:
        pass
    else:
        AvgforDay[6] = (tues_count / (numofVidsWatched[6] * sun_total))
        
    '''
    print 'avg m: ', AvgforDay[0]
    print 'avg t: ', AvgforDay[1]
    print 'avg w: ', AvgforDay[2]
    print 'avg th:', AvgforDay[3]
    print 'avg f:', AvgforDay[4]
    print 'avg s:', AvgforDay[5]
    print 'avg sn:', AvgforDay[6]
    '''
'''
Function to count the number of a videos an individual user watches.
It also calculates the average of this total.
'''
def count_days():
    read_file()
    global mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count

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
                   
        total_vids_count = mon_count + tues_count + wed_count + thurs_count + fri_count + sat_count + sun_count  
        total_days = mon_total + tues_total + wed_total + thurs_total + fri_total + sat_total + sun_total
        
        final_avg_value = total_vids_count / total_days
        print "User: ", key
        print "total videos: ", total_vids_count
        print "total days: ", total_days
        print "final avg value: ", final_avg_value
        
        user_dict.append((key, final_avg_value))
                
        '''
        if mon_total != 0:
            mon_count = mon_count / mon_total
        if tues_total != 0:
            tues_count = tues_count / tues_total
        if wed_total != 0:
            wed_count = wed_count / wed_total
        if thurs_total != 0:
            thurs_count = thurs_count / thurs_total
        if fri_total != 0:
            fri_count = fri_count / fri_total
        if sat_total != 0:
            sat_count = sat_count / sat_total
        if sun_total != 0:
            sun_count = sun_count / sun_total

        user_dict.append((key, mon_count, tues_count,
                         wed_count, thurs_count,
                         fri_count, sat_count, sun_count))
        '''
        
        mon_count, tues_count, wed_count, thurs_count, fri_count, sat_count, sun_count = 0,0,0,0,0,0,0

#Function to output the data into a json text file
def json_file():
    count_days()
    
    for i in range(len(user_dict)):
        sdc_data.append({
            user_dict[i][0]: {
                "AverageVids": user_dict[i][1]
            }
        })
    
    '''
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
        
    '''
    with open("UserAvgDays.txt", "w") as f:
        json.dump(sdc_data, f, sort_keys = True, indent = 4, ensure_ascii=True)

    sdc_data2 = []
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
    json_file()
    print "success"
























                        
