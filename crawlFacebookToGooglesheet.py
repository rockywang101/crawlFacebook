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
    
    token = "EAACEdEose0cBAMFOfQ3lTTH3ByrbzuNuHa9XIfnZCZB0ZAH6ZBaUM3QKWwJ8mzaI02En0LG0wga01CpRJ8k23vXOVFQuqd9tZAPoPEvAqHZCs7XMAYxBZAxqLuDFNlWw6fZAzW0eicbMy4j2lLRQe5kZCOj0eJ2LRDntFZAAZAA87Aa3qmCguTuAUSxHdgZAF1kTgX74ceykaKVZBCQZDZD"
    
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
