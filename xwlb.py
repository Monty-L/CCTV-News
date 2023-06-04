"""
@author: Monty
@project: XWLB
"""

import os
import requests
from bs4 import BeautifulSoup
import datetime
import time

def get_range_date(s_y,s_m,s_d,e_y,e_m,e_d):
    """
    获取一段日期，并得到列表
    :para s_y,s_m,s_d分别是开始的年月日  e_y,e_m,e_d分别是结束日期的年月日
    """
    start_time = datetime.date(s_y,s_m,s_d)
    end_time = datetime.date(e_y,e_m,e_d)
    day_range = list()
    for i in range((end_time - start_time).days+1):
        day = start_time + datetime.timedelta(days=i)
        day_range.append(str(day))

    return day_range


#在当前文件下生成目录存放东西
current_directory = os.getcwd()
output_directory = "wxlb"
output_path = os.path.join(current_directory, output_directory)
if not os.path.exists(output_path):
    os.mkdir(output_path)


for cur_date_ in get_range_date(2023,5,1,2023,5,4):
    cur_date=cur_date_.replace("-","")
    subdir_path = os.path.join(output_path, cur_date)
    if not os.path.exists(subdir_path):
        os.mkdir(subdir_path)
    
    url=f"https://tv.cctv.com/lm/xwlb/day/{cur_date}.shtml"
    resp=requests.get(url)

    resp.encoding="utf-8"#解码

    #打印并保存resp.text
    # file_path ='output.txt'
    # with open(file_path, 'w', encoding="utf-8") as f:
    #     f.write(resp.text, )

    soup = BeautifulSoup(resp.text,"html.parser")#把resp对象的texe传给bs4用于解析
    links=soup.find_all('a')

    visited = set()  
    for link in links:
        href = link.get('href')
        title = link.get('alt').strip("\[视频\]")
        drop="《新闻联播》"
        if drop in title:  #去掉每天的第一个新闻
            continue

        if href not in visited:
            visited.add(href)


    final_link=list(visited)
    
    for child_link in final_link:
        child_page_resp = requests.get(child_link, stream=True)
        time.sleep(1)#防止爬取过频繁影响网站正常运行
        child_page_resp.encoding = 'utf-8 '
        child_page = BeautifulSoup(child_page_resp.text, "html.parser")

        child_cont=child_page.find("div",class_="content_area").text
        tit=child_page.find("div",class_="ph_title_l").text.strip("\[视频\]")


        ##写入文件
        save_title=tit.replace(":", "").replace("?", "").replace("<", "").replace(">", "")
        filename = save_title + ".txt"

        save_path = os.path.join(subdir_path,filename)
        with open(save_path, 'w', encoding="utf-8") as f:
            f.write(child_cont, )

