'''
Created on 2018年3月20日
@author: rocky.wang
'''
import os, requests, json

# https://www.facebook.com/teacherwarrenc/posts/1000479993434136


def main():

    postId = "543892195759587_1023460234469445"
    
    picUrlList = fetchPostPictures(postId)
    
    picUrls = ""
    for picUrl in picUrlList:
        picUrls += picUrl + "\n"
    
    print(picUrls)


def fetchPostPictures(postId):
    url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(postId, "attachments", os.environ["FACEBOOK_ACCESS_TOKEN"])
    response = requests.get(url)
    js = json.loads(response.text)
    picUrlList = []
    
    for data in js["attachments"]["data"][0]["subattachments"]["data"]:
        picUrlList.append(data["media"]["image"]["src"])

#     try:
#         for data in js["attachments"]["data"][0]["subattachments"]["data"]:
#             picUrlList.append(data["media"]["image"]["src"])
#     except:
#         pass

    return picUrlList

if __name__ == "__main__":
    main()
