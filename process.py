import json
import datetime
import csv
import requests
import os.path


def writeJsonToFile(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


# first vis
if os.path.isfile('json/participation.json'):
    data = json.load(open('json/participation.json'))
else:
    data = requests.get(
        "https://api.github.com/repos/torvalds/linux/stats/participation").json()
    writeJsonToFile('json/participation.json', data)
result = [data["owner"], [x-y for x, y in zip(data["all"], data["owner"])]]
with open('participation.csv', 'w') as file:
    wr = csv.writer(file, lineterminator='\n')
    wr.writerow(['owner', 'others'])
    for x in reversed(range(0, len(result[0]))):
        wr.writerow([result[0][x], result[1][x]])

# second vis
if os.path.isfile('json/workinghour.json'):
    data = json.load(open('json/workinghour.json'))
else:
    data = requests.get(
        "https://api.github.com/repos/torvalds/linux/stats/punch_card").json()
    writeJsonToFile('json/workinghour.json', data)
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
languagesBytesCandOthers = {"C": 0, "Others": 0}
languagesBytesOthers = {}
languagesBytesAll = {}


def mergeToLanguagesBytes(input):
    for propertyName in input:
        if propertyName in languagesBytesAll:
            languagesBytesAll[propertyName] += input[propertyName]
        else:
            languagesBytesAll[propertyName] = 0
            languagesBytesAll[propertyName] += input[propertyName]

    for propertyName in input:
        if propertyName == 'C':
            languagesBytesCandOthers["C"] += input[propertyName]
        else:
            languagesBytesCandOthers["Others"] += input[propertyName]
    for propertyName in input:
        if propertyName == 'C':
            continue
        if propertyName in languagesBytesOthers:
            languagesBytesOthers[propertyName] += input[propertyName]
        else:
            languagesBytesOthers[propertyName] = 0
            languagesBytesOthers[propertyName] += input[propertyName]


def getLanguages(repos, index):
    if(index >= len(repos)):
        writeJsonToFile('languages.json', languagesBytesOthers)
        writeJsonToFile('languagesC.json', languagesBytesCandOthers)
        with open('languages.csv', 'w') as file:
            wr = csv.writer(file, lineterminator='\n')
            wr.writerow(['language', 'bytes'])
            # print(languagesBytesAll)
            for x in languagesBytesAll:
                wr.writerow([x, languagesBytesAll[x]])
        return
    if os.path.isfile('json/'+repos[index]["name"]+'.json'):
        languages = json.load(open('json/'+repos[index]["name"]+'.json'))
    else:
        languages = requests.get(
            "https://api.github.com/repos/torvalds/" + repos[index]["name"] + "/languages").json()
        writeJsonToFile('json/'+repos[index]["name"]+'.json', languages)
    # print(repos[index]["name"])
    mergeToLanguagesBytes(languages)
    getLanguages(repos, index+1)
    return


if os.path.isfile('json/repos.json'):
    repos = json.load(open('json/repos.json'))
else:
    repos = requests.get("https://api.github.com/users/torvalds/repos").json()
    writeJsonToFile('json/repos.json', repos)
getLanguages(repos, 0)
