'''
Created on 2018年3月20日
@author: rocky.wang
'''
import json, os, requests

def main():
    
    fanPageId = "teacherwarrenc"
    rowList = crawlFanpageData(fanPageId)
    
    for row in rowList:
        print(row)


def crawlFanpageData(fanPageId):
    
    fields = "id, name, posts{id,name,message,created_time,permalink_url}"
    url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(fanPageId, fields, os.environ["FACEBOOK_ACCESS_TOKEN"])
    print("GET %s" %(url))
    js = json.loads(requests.get(url).text)
    print(js)
    
    rowList = [["ID", "Message", "Time", "Notify", "PostUrl"]]
    
    for data in js["posts"]["data"]:
 
#         if data.get("message", "") == "":
#             data["message"] =  "分享了 " + data["name"] + " 的資料" 
            
        rowList.append([data["id"], data['message'], data["created_time"], "Not Yet", data["permalink_url"]])    
    return rowList

if __name__ == "__main__":
    main()
