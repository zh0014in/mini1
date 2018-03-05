import json
import datetime
import csv
from pprint import pprint

#first vis
data = json.load(open('participation.json'))

result = [data["owner"], [x-y for x,y in zip(data["all"], data["owner"])]]

with open('participation.csv','w') as file:
    wr = csv.writer(file)
    wr.writerow(['owner', 'others'])
    for x in reversed(range(0, len(result[0]))):
        wr.writerow([result[0][x], result[1][x]])

#second vis
data = json.load(open('workinghour.json'))
with open('workinghour.csv', 'w') as file:
    wr = csv.writer(file)
    wr.writerow(['sunday', 'monday', 'tuesday', 'wendsday', 'thirsday', 'friday', 'saturday'])
    for x in range(8, 19):
        hour = []
        for y in [a for a in data if a[1] == x]:
            hour.append(y[2])
        wr.writerow(hour)




# owner =  [a for a in data if a["author"]["login"]=="torvalds"]
# pprint(owner)

# weeks = []
# ownerCommits = []
# othersCommits = [0 for i in range(52)]

# for x in owner:
#     for week in reversed(x["weeks"][-52:]):
#         date =datetime.datetime.fromtimestamp(week["w"]).strftime('%Y-%m-%d') 
#         print date + " " + str(week["c"])
#         weeks.append(date)
#         ownerCommits.append(week["c"])

# others = [a for a in data if a["author"]["login"]!="torvalds"]

# for x in others:
#     commits = []
#     for week in reversed(x["weeks"][-52:]):
#         commits.append(week["c"])
#     othersCommits = [x+y for x,y in zip(othersCommits, commits)]

# print othersCommits