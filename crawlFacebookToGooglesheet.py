'''
Demo fetch Facebook FanPage data

Created on 2018年3月19日
@author: rocky.wang
'''
from googleService import GooglesheetService
import time

'''
Created on 2018年3月13日
@author: rocky.wang
'''
import json, os, requests

sheetService = GooglesheetService("1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk")


def main():
    
    rowList = sheetService.getValues("粉絲頁列表")
    for row in rowList:
        fanPageId = row[1]
        rangeName = row[2]
        fetchFanPage(fanPageId, rangeName)
        time.sleep(1) # 不睡似乎也不會怎麼樣，但反正一小時一次而已，睡一下比較安全

def fetchFanPage(fanPageId, rangeName):
    
    # 取已經寫入過的 post id
    existPostIds = getExistPostIds(rangeName)
    # 取前 25 筆貼文
    rowList = crawlFanpageData(fanPageId)
    # 過濾剩下沒寫入過的貼文
    rowList = [row for row in rowList if not row[2] in existPostIds]
    
    # 因為排序是由新往舊的抓，我想排序改為新的在上面
    rowList.reverse()
    
    print("New Post to write amount ", len(rowList))

    # 寫入 google sheet
    sheetService.appendSheet(rangeName, rowList)
    

'''
permalink_url 為粉絲頁文章原始連結
link 為文章張貼的連結 (因為後來才加上去，放在最後面)
'''
def crawlFanpageData(fanPageId):
    
    print(os.environ["FACEBOOK_ACCESS_TOKEN"])
    
    token = os.environ["FACEBOOK_ACCESS_TOKEN"]
    
    token = "EAACEdEose0cBAA8J07eM5k8Gz70oSOJl3YZB5fmdBI4VZA4ImudEPXLTp1ty33L8xocpPGZA0LenWbLoZCWkaU5HOIbKVKngZBHUxwa3iSOlTP5gCWZBxCHh2S69ylArjZB1JUEVAzhIqrPtqyvQ2hVZCAA7vLj66bjxSnr38Iaiv7tYD3wRC7KwBsAPZB4NvE2gjvp2n3t9ygAZDZD"
    
#     token = "EAACEdEose0cBAEtuXs1XZB0G46eVx6Bu58B3taQxrWGOWnZA41rkA8WRkRLQZBntPwhFBckERRFbWRYvlra5OZCJeCduBnQ9FO5D2nSuqmrZA4UTgzAfAarC5pXzhsz4r24ZCiEy46ZAMfaKaok6AX1HTs7ZAlKgvnIElKO0pZBrqUCAnlAN1wOZCEvgPKnD8Q420ZD"
    fields = "id, name, posts{id,name,message,created_time,link,permalink_url}"
    url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(fanPageId, fields, token)
    print("GET %s" %(url))
    js = json.loads(requests.get(url).text)
    print(js)
    
    rowList = []
    for data in js["posts"]["data"]:
        if data.get("message", "") == "":
#             data["message"] =  "分享了 " + data["name"] + " 的資料" 
            data["message"] =  "分享了資料"
            
        rowList.append(["N", data["created_time"], data["id"], data['message'], data["permalink_url"], data.get("link", "")])
        
    return rowList


def getExistPostIds(rangeName):
    sheetRows = sheetService.getValues(rangeName)
    existPostIds = []
    for row in sheetRows:
        existPostIds.append(row[2])
    return existPostIds



if __name__ == "__main__":
    main()
