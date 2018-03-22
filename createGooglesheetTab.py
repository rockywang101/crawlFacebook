'''
檢查粉絲頁列表，建立尚未建立的 sheet

https://docs.google.com/spreadsheets/d/1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk/edit#gid=1244591370

Created on 2018年3月19日
@author: rocky.wang
'''
from googleService import GooglesheetService
import json, os, requests


googlesheetService = GooglesheetService("1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk") # init service by spreadsheetId

def main():
    
    # 抓取 
    rowList = googlesheetService.getValues("粉絲頁列表")
     
    cnt = createSheetIfNotExist(rowList)
     
    if cnt > 0: 
        googlesheetService.updateSheet("粉絲頁列表", rowList)
        print("update sheet rows amount %s" %(cnt))
    else:
        print("no sheet need to create")
        
def createSheetIfNotExist(rowList):
    
    # 抓取 spredsheet 所有分頁名稱
    rangeNameList = googlesheetService.getRangeNameList()
    
    cnt = 0
    for row in rowList:
        # 已經有後續的資料，代表處理過，不需再處理
        if len(row) > 1:
            continue
        
        # 由網址取得粉絲頁 ID
        fanPageId = row[0].split("/")[-2]
        # 處理像是「XXXX-OOOO-1616764821902568」，很搞怪的前面有中文，只有後面的「1616764821902568」是 id
        if "-" in fanPageId:
            fanPageId = fanPageId.split("-")[-1]

        fields = "id, name"
        url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(fanPageId, fields, os.environ["FACEBOOK_ACCESS_TOKEN"])
 
        response = requests.get(url)
        js = json.loads(response.text)
        
        if not js["name"] in rangeNameList:
            print("create sheet named %s" %(js["name"]))
            googlesheetService.addSheet(js["name"])
            
            googlesheetService.appendSheet(js["name"], [["已通知", "建立時間", "文章ID", "內容", "原始連結"]])
        
        row.append(fanPageId)
        row.append(js["name"])
        cnt += 1
    
    return cnt
        
if __name__ == "__main__":
    main()