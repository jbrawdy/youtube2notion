from youtubesearchpython import VideosSearch
import json
import requests
from datetime import date

token = '<>'

databaseId = '<>'

headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-05-13"
}

def youtubeSearch(title):
    videosSearch = VideosSearch(title, limit = 1)
    results = videosSearch.result()

    for result in results["result"]:
        print(result["title"])
        title = result["title"]
        print(result["channel"]["name"])
        name = result["channel"]["name"]
        print(result["link"])
        link = result["link"]

    return title, name, link


def printYoutubeSearch(result):
    print(json.dumps(VideosSearch.result(), indent=4))

def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    # print(res.text)

    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)

def createPage(databaseId, headers, name, who, format, link, status, date=date.today()):

    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId },
        "properties": {
            "Name": {
                "title": [
                    {
                        "text": {
                            "content": name
                        }
                    }
                ]
            },
            "Who": {
                "rich_text": [
                    {
                        "text": {
                            "content": who
                        }
                    }
                ]
            },
            "Format": {
                "select": 
                    {
                        "name": format
                    }
            },
            "Link": {
                "url": link
            },
            "Status": {
                "select":
                    {
                        "name": status
                    }
            },
            "Date Completed": {
                "date":
                    {
                        "start": str(date)
                    }
            }
        }
    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    #print(res.text)


video = youtubeSearch('If youve got Natural Law Do you still Need or Want Jesus? ')
createPage(databaseId, headers, video[0], video[1], "YouTube", video[2],"In Progress")


