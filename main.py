'''
Created on 2018年3月20日
@author: rocky.wang
'''
import createGooglesheetTab
import crawlFacebookToGooglesheet
import fetchGooglesheetDataToNotify

if __name__ == "__main__":
   
    # 檢查是否有新分頁需要建立
    createGooglesheetTab.main()

    # 爬粉絲頁資料到存放節 google sheet
    crawlFacebookToGooglesheet.main()
    
    # 進行通知
    fetchGooglesheetDataToNotify.main()
