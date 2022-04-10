import csv
import db
from bs4 import BeautifulSoup
import requests
import re
import threading
from concurrent.futures import ThreadPoolExecutor

pattern = re.compile(r'Unique ID: \d+')
conn = db.duke()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '__utmz=76785792.1648770952.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _ga=GA1.2.1929483050.1648770952; _gid=GA1.2.597729008.1648770998; __utma=76785792.1929483050.1648770952.1648788553.1648812474.5; _shibsession_64656661756c7468747470733a2f2f69646d732d7765622d7075622e6f69742e64756b652e656475=_7a90d3a665eaeb6bfba5a20dca69caaa',
    'Host': 'directory.duke.edu',
    'Origin': 'https://directory.duke.edu',
    'Referer': 'https://directory.duke.edu/directory/search',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"MacOS"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (MacOS NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}

lock = threading.Lock()

def split_list_n_list(origin_list, n):
    if len(origin_list) % n == 0:
        cnt = len(origin_list) // n
    else:
        cnt = len(origin_list) // n + 1
 
    for i in range(0, n):
        yield origin_list[i*cnt:(i+1)*cnt]
        
def work(nameLst):
    nameLst.reverse()
    for name in nameLst:
        str = name.split(',')
        ss = str[1].lstrip().rstrip().split()
        if(len(ss)>1):
            searchName = ss[0]+' '+ss[1][0]
        else:
            searchName = ss[0]
        searchName = searchName+' '+str[0]
        data = {
            'search':searchName
        }
        try:
            resp = requests.post(url='https://directory.duke.edu/directory/search',headers=headers,data = data)
            if(resp.status_code!=200):
                print("cookie error")
                return
            tt = BeautifulSoup(resp.content, 'lxml')
            text = tt.find_all('table', 'display full-width')
            id = ''
            if(text[0].text=='\n'):
                continue
            try:
                id = pattern.findall(text[0].text)[0]
            except:
                id = text.text
            dd = []
            dd.append(name)
            dd.append(id)
            print(dd)
            lock.acquire()
            conn.insert(dd)
            lock.release()
        except:
            return
    print("done")
    
def getLstFromDB():
    lst = conn.readLst()
    rt = []
    for i in lst:
        rt.append(i[0])
    return rt

print("Reading sholars list")
nameList = getLstFromDB()
print("Done. Count: "+str(len(nameList)))
pool = ThreadPoolExecutor(max_workers=30)
l = split_list_n_list(nameList, 30)
for i in l:
    pool.submit(work,i)