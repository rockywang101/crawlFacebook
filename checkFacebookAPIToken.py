'''
檢查 Facebook API Token 是否過期，並更換ㄌ


Created on 2018年3月19日
@author: rocky.wang
'''
import requests
import json

token = "EAABb6vxMesIBAISKgjO7L9kVIqESpB5B4ZCIKdlz7DBSSit2E09FkL9NIf6bUx5GsO7tXDFobtC4YfZAZCNldDZANJ7SsEPFEClEB5RlEie7hvvLymjVgzxXgwqbx7MZBfNZCeycTTK0zZB6sWMrbtIx0IQPbevQhAI6Y0c1xorqgZDZD"

def main():
    
    id = "ezlifeInstructor"
    fields = "id, name"
    url = 'https://graph.facebook.com/v2.10/{}?fields={}&access_token={}'.format(id, fields, token)

    response = requests.get(url)
    js = json.loads(response.text)
    print(js)
    print(js["error"]["code"])
    print(js["error"]["error_subcode"])
    print(js["error"]["message"])

    appId = "101064813345474"
    appSecret = ""
    shortlivedAccessToken = ""
    url = "https://graph.facebook.com/oauth/access_token?client_id={}&client_secret={}&fb_exchange_token={}&grant_type=fb_exchange_token".format(appId, appSecret, shortlivedAccessToken)
        
if __name__ == "__main__":
    main()