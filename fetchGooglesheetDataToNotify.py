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

        # 因為時間看起來是美國時間，還要再自己加 8，先拿掉時間顯示
#         dt = row[1][0:10] + " " + row[1][11:16]
#         message = "------------------------------------------\n[%s] [%s]\n------------------------------------------\n" %(rangeName, dt)

        message = "  文章來自 [%s]\n------------------------------------------\n" %(rangeName)
        message += row[3] + "\n\n" + row[5] + "\n\n原文連結: " + row[4] + "\n\n"

        lineTool.lineNotify(os.environ["LINE_FANS_TOKEN"], message)
        time.sleep(5)
        lineTool.lineNotify(os.environ["LINE_FANS_TOKEN2"], message)
        time.sleep(5)

#         lineTool.lineNotify(os.environ["LINE_TEST_TOKEN"], message)
        

if __name__ == "__main__":
    main()
