import db
from bs4 import BeautifulSoup
import requests
import csv


csvpath = '/Users/brucez/Desktop/Brucez/DKU/DKU_courses/3/STATS401/Project1/data/'

def writeToCSV(data):
    f = open(csvpath, 'a+', newline='',encoding='utf-8')
    writer = csv.writer(f)
    for i in data:
        writer.writerow(i)
    f.close()
    
def getScholarList():
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'scholars.duke.edu',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'
    }
    for page in range(76, 243):
        print(page)
        pdata = []
        resp = requests.get(url='https://scholars.duke.edu/individuallist?page='+str(page)+'&vclassId=http%3A%2F%2Fvivoweb.org%2Fontology%2Fcore%23FacultyMember', headers=headers)
        soup = BeautifulSoup(resp.content, 'lxml')
        lst = soup.find_all(title = 'individual name')
        for one in lst:
            data = []
            data.append(one.contents[0])
            data.append(one.attrs['href'])
            pdata.append(data)
        writeToCSV(pdata)
    print("done")

if __name__=='__main__':
    getScholarList()