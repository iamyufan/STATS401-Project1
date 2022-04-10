import time
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

def get_html(url):
    head = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',

        }
    req = requests.get(url,headers=head,verify=False)   # close ssl
    req.encoding = req.apparent_encoding                # set encoding
    return req.text

def get_urls():
    url = 'https://ugstudies.dukekunshan.edu.cn/academics/majors/'
    
    # Get and Parse HTML
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    # Filter the HTML to get only the table rows
    urls_all = soup.find_all('h2', attrs='elementor-heading-title elementor-size-default')
    
    urls_list=[]
    for item in urls_all:
        # print(item)
        try:
            urls=re.findall('<a href="(.*?)">', str(item))[0]
            urls_list.append(urls)
        except Exception as e:
            continue
    return urls_list

def query(url):

    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    div_all=soup.find_all('div',attrs='elementor-container elementor-column-gap-default')
    for item in div_all:
        # print(item)

        # Get course_id, credit, title, description
        try:
            mid = item.find('h6',attrs='elementor-heading-title elementor-size-default').string     # course_id
            print(mid)
        except Exception as e:
            continue

        branch=item.find_all('h6',attrs='elementor-heading-title elementor-size-default')           # credits
        if len(branch) >=3 :
            continue

        print(branch[-1].string)

        title=item.find('a',attrs='elementor-accordion-title').string                               # title
        title=str(title).strip('•   ')
        print(title)

        text=item.find_all('div',attrs='elementor-widget-container')[-1].string                     # description
        text=str(text).strip('\t').strip('\n')
        print(text)

        # Save
        dic={
            'MID':mid,
            'Credit': branch[-1].string,
            'Title': title,
            'Description': text,
        }
        L.append(dic)
        L_all.append(dic)
        
        
if __name__ == '__main__':
    L_all = []
    urls = get_urls()
    for url in urls:
        L = []
        query(url)
        df = pd.DataFrame(L)
        df.drop_duplicates(inplace=True)

        name=re.sub('https://ugstudies.dukekunshan.edu.cn/majors/','',url)
        name=re.sub('/','',name)
        df.to_csv(f'../data/course_description/{name}.csv',index=False)
        time.sleep(1)

    df0 = pd.DataFrame(L_all)
    df0.drop_duplicates(inplace=True)
    df0.to_csv('all.csv', index=False)

