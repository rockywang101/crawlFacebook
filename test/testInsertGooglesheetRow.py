'''
測試 insert row 在特定行

Created on 2018年3月20日
@author: rocky.wang
'''
from googleService import GooglesheetService

#insertDataOption

def main():

    googlesheetService = GooglesheetService("1bydUUYVTxyyz2jxm3JRzIQkdElNthLHuQpzW6-DLVUk")

    rowList = [
            [1, 2, 3],
            [4, 5, 6],
        ]
    
    googlesheetService.appendSheet("華倫存股 穩中求勝", rowList, insertDataOption="INSERT_ROWS")

if __name__ == "__main__":
    main()

