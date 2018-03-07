import json
import datetime
import csv
import requests
import os.path
import operator
import sys


def writeJsonToFile(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


user = 'torvalds'
repo = 'linux'
if len(sys.argv) == 3:
    user = sys.argv[1]
    repo = sys.argv[2]
elif len(sys.argv) != 1:
    print 'please provide both user and repo or leave them empty'
    exit

# first vis
if os.path.isfile('json/'+user+'_'+repo+'_participation.json'):
    data = json.load(open('json/'+user+'_'+repo+'_participation.json'))
else:
    data = requests.get(
        "https://api.github.com/repos/"+user+"/"+repo+"/stats/participation").json()
    writeJsonToFile('json/'+user+'_'+repo+'_participation.json', data)
result = [data["owner"], [x-y for x, y in zip(data["all"], data["owner"])]]
with open('participation.csv', 'w') as file:
    wr = csv.writer(file, lineterminator='\n')
    wr.writerow(['owner', 'others'])
    for x in reversed(range(0, len(result[0]))):
        wr.writerow([result[0][x], result[1][x]])

# second vis
if os.path.isfile('json/'+user+'_'+repo+'_workinghour.json'):
    data = json.load(open('json/'+user+'_'+repo+'_workinghour.json'))
else:
    data = requests.get(
        "https://api.github.com/repos/"+user+"/"+repo+"/stats/punch_card").json()
    writeJsonToFile('json/'+user+'_'+repo+'_workinghour.json', data)
with open('workinghour.csv', 'w') as file:
    wr = csv.writer(file, lineterminator='\n')
    wr.writerow(['sunday', 'monday', 'tuesday', 'wendnesday',
                 'thursday', 'friday', 'saturday'])
    for x in range(8, 19):
        hour = []
        for y in [a for a in data if a[1] == x]:
            hour.append(y[2])
        wr.writerow(hour)

# third vis
languagesBytesTopandOthers = {"Others": 0}
languagesBytesOthers = {}
languagesBytesAll = {}


def mergeToLanguagesBytes(input):
    for propertyName in input:
        if propertyName in languagesBytesAll:
            languagesBytesAll[propertyName] += input[propertyName]
        else:
            languagesBytesAll[propertyName] = 0
            languagesBytesAll[propertyName] += input[propertyName]


def split():
    largest = max(languagesBytesAll.iteritems(), key=operator.itemgetter(1))[0]
    languagesBytesTopandOthers[largest] = languagesBytesAll[largest]
    for x in languagesBytesAll:
        if x != largest:
            languagesBytesTopandOthers["Others"] += languagesBytesAll[x]
            languagesBytesOthers[x] = languagesBytesAll[x]


def getLanguages(repos, index):
    if(index >= len(repos)):
        split()
        writeJsonToFile('languages.json', languagesBytesOthers)
        writeJsonToFile('languagesTopAndOthers.json',
                        languagesBytesTopandOthers)
        with open('languages.csv', 'w') as file:
            wr = csv.writer(file, lineterminator='\n')
            wr.writerow(['language', 'bytes'])
            for x in languagesBytesAll:
                wr.writerow([x, languagesBytesAll[x]])
        return
    if os.path.isfile('json/'+user+'_'+repo+'_'+repos[index]["name"]+'.json'):
        languages = json.load(
            open('json/'+user+'_'+repo+'_'+repos[index]["name"]+'.json'))
    else:
        languages = requests.get(
            "https://api.github.com/repos/"+user+"/" + repos[index]["name"] + "/languages").json()
        writeJsonToFile('json/'+user+'_'+repo+'_' +
                        repos[index]["name"]+'.json', languages)
    mergeToLanguagesBytes(languages)
    getLanguages(repos, index+1)
    return


if os.path.isfile('json/'+user+'_'+repo+'_repos.json'):
    repos = json.load(open('json/'+user+'_'+repo+'_repos.json'))
else:
    repos = requests.get("https://api.github.com/users/"+user+"/repos").json()
    writeJsonToFile('json/'+user+'_'+repo+'_repos.json', repos)
getLanguages(repos, 0)
