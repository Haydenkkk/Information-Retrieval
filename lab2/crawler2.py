import os
import requests
import jieba
import time
from bs4 import BeautifulSoup
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57'
}

chapters = []  # 存储所有章节的数据
count = 1

def crawl(path, url, depth=1):
    global count
    if not os.path.exists(path):
        os.mkdir(path)
    if depth == 0:
        return

    print('-' * 30)
    print('Crawling:', url)
    if(count % 100 == 0): time.sleep(10)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Status code:', response.status_code)
        print('Content type:', response.headers['Content-Type'])
        print('Encoding:', response.encoding)
        print('-' * 30)
        text = response.text.encode(response.encoding, errors='ignore').decode('gb2312', errors='ignore')
        soup = BeautifulSoup(text, 'lxml')

        chapter_data = {}  # 存储当前章节的数据

        # 获取标题
        main_div = soup.find('div', {'id': 'main'})
        title_element = main_div.find('h1') if main_div else None
        title = title_element.text.strip() if title_element else ''
        chapter_data['headline'] = title

        # 获取URL
        chapter_data['url'] = url

        # 获取内容
        content = soup.get_text().strip()
        chapter_data['content'] = content
        chapter_data['content_seg'] = jieba.lcut(content)

        # 将当前章节的数据添加到列表中
        chapters.append(chapter_data)

        # 递归爬取下一级章节
        for link in soup.find_all('dd'):
            for a in link.find_all('a'):
                if a.has_attr('href'):
                    if a['href'].startswith('http'):
                        crawl(path, a['href'], depth-1)
                    else:
                        crawl(path, url + a['href'], depth-1)

        if len(content):
            print('Text length:', len(content))
            with open(os.path.join(path, 'chapter-'+str(count)+'.json'), 'w+', encoding='utf-8') as f:
                json.dump(chapter_data, f, ensure_ascii=False, indent=4)
                print('Saved to:', os.path.join(path, 'chapter-'+str(count)+'.json'))
                count += 1
    else:
        print('Error:', response.status_code)



crawl('../doucments/DouLuo_Json', 'https://www.qb5.tw/book_518/', depth=2)



 