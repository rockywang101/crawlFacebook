'''
fetch fanPageData on google sheet and notify

Created on 2018年3月19日
@author: rocky.wang
'''
from googleService import GooglesheetService
import requests
import json, os
import lineTool
import time

sheetService = GooglesheetService("1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk")


def main():
    
    for rangeName in sheetService.getRangeNameList():
        
        if rangeName == "粉絲頁列表":
            continue

        print("process notify step in rangeName: ", rangeName)
        
        rowList = sheetService.getValues(rangeName)
        
        # get not notify topics
        notifyRowList = [row for row in rowList if row[0] == "N"]
        
        rowListToMessageAndNotify(notifyRowList, rangeName)
        
        # update notify status
        for row in rowList:
            if row[0] == "N":
                row[0] = "Y"
        
        rowList = sheetService.updateSheet(rangeName, rowList)
    

def rowListToMessageAndNotify(rowList, rangeName):
    
    for row in rowList:
        print(row)
        dt = row[1][0:10] + " " + row[1][11:16]
        message = "------------------------------------------\n[%s] [%s]\n------------------------------------------\n" %(rangeName, dt)
        message += row[3] + "\n\n原文連結: " + row[4] + "\n\n"

        print("Notify message-----\n", message)
        lineTool.lineNotify(os.environ["LINE_FANS_TOKEN"], message)
        time.sleep(5)

#     html = message.replace("\n", "<br/>")
#     print(html)
#     GmailService.sendMail(html)
    

if __name__ == "__main__":
    main()
