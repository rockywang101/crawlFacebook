'''
Demo fetch Facebook FanPage data

Created on 2018年3月19日
@author: rocky.wang
'''
import time, os, json, requests
from googleService import GooglesheetService
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import datetime

sheetService = GooglesheetService("1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk")


def main():
    print("執行時間 {}".format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')))
    
    token = fetchToken()
    
    rowList = sheetService.getValues("粉絲頁列表")
    for row in rowList:
        fanPageId = row[1]
        rangeName = row[2]
        fetchFanPage(fanPageId, rangeName, token)
        time.sleep(1) # 不睡似乎也不會怎麼樣，但反正一小時一次而已，睡一下比較安全


def fetchFanPage(fanPageId, rangeName, token):
    
    # 取已經寫入過的 post id
    existPostIds = getExistPostIds(rangeName)
    # 取前 25 筆貼文
    rowList = crawlFanpageData(fanPageId, token)
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
def crawlFanpageData(fanPageId, token):
    
#     print(os.environ["FACEBOOK_ACCESS_TOKEN"])
#     token = "EAACEdEose0cBAOBGwisffpqJznCSvW2qzLHruyTKYyrZB91NTmVVsUx0ALau7qcdqAxMPWLkCQg4bHFz2ZAONb3QwlaLl6BHwHjKSuvsiIWxOZAQ0JUQb8lis1IpO5fUb6IDoMQODPIiGCiGrjGOVkP9h3i96l8ScgHT5ZBZCf07igFpMcIibGqeTWysuTBfzkGqIvS8BdwZDZD"
    
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


def fetchToken():
        
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    
    print("開啟臉書")
    driver.get("https://www.facebook.com/")
    time.sleep(5)
    print("進行登入")
    elem = driver.find_element_by_id("email")
    elem.clear()
    elem.send_keys("rockywang101@gmail.com")
    elem = driver.find_element_by_id("pass")
    elem.clear()
    elem.send_keys(os.environ["MY_PASSWORD"])
    elem.send_keys(Keys.RETURN)
    time.sleep(5)
    
    print("進入 API 頁面")
    driver.get("https://developers.facebook.com/tools/explorer")
    time.sleep(5)
    print("取得權杖")
    elem = driver.find_element_by_link_text("取得權杖")
    elem.click()
    time.sleep(2)
    print("取得用戶存取權杖")
    elem2 = driver.find_element_by_link_text("取得用戶存取權杖")
    elem2.click()
    time.sleep(2)
    print("取得存取權杖")
    elem3 = driver.find_element(By.XPATH, '//button[text()="取得存取權杖"]')
    elem3.click()
    time.sleep(5)
    
    inputList = driver.find_elements_by_class_name("_58al")
    token = inputList[2].get_attribute('value')
    print("取得 API Token: " + token)
    
    driver.close()
    return token



if __name__ == "__main__":
    main()
