from bs4 import BeautifulSoup
import requests
import re
import os
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 
    # "Cookie": 'first_visit_datetime_pc=2023-04-03+20:05:21; p_ab_id=6; p_ab_id_2=4; p_ab_d_id=1639917103; yuid_b=J4OFEVE; _fbp=fb.1.1680519923390.2095052467; PHPSESSID=71354849_ImIU8T760AzZaIuigmucF7bfvSy0Hjg8; device_token=a7eaec54414b62037030260d34dff8a1; privacy_policy_agreement=5; c_type=22; privacy_policy_notification=0; a_type=0; b_type=0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; p_b_type=1; tag_view_ranking=0xsDLqCEW6~Lt-oEicbBr~r_Jjn6Ua2V~HY55MqmzzQ~uvBGOtCzqF~_vCZ2RLsY2~5oPIfUbtd6~68luzZqFS0~-7RnTas_L3~jk9IzfjZ6n~tLEo7GtjcE~iRFlj3p1GG~ctjJwbmssT~uW5495Nhg-~O4zMr8hRGP~EYYBFpYNJp~98FF78f4J0~bYn3xr0RaN~zqe8dqUBGC~ckoqr0bPHv~5oHuFQXax5~rOnsP2Q5UN~_EOd7bsGyl~6n5sWl9nNm~tJaVY8ie4B~qG6ZMBxhkE~QaiOjmwQnI~ZTBAtZUDtQ~zaEtI28sYq~qXzcci65nj~TWrozby2UO~ncUG68iRRJ~PwDMGzD6xn~-LwvviyTfq~faHcYIP1U0~Ie2c51_4Sp~uK-xlAOB9q~0r_Dr-UWZa~wmxKAirQ_H~vrf3o5XcIa~pNtQi6YIt-~NGpDowiVmM~gCB7z_XWkp~vzTU7cI86f~azESOjmQSV~zyKU3Q5L4C~nIjJS15KLN~qkC-JF_MXY~4QveACRzn3~cnS1oIcWKc~aKhT3n4RHZ~HZk-7ZdqP6~w8ffkPoJ_S~HBlflqJjBZ~T40wdiG5yy~CEYqcod4iE~D4hLr_YmAD~_C6hhzFNWQ~gnmsbf1SSR~LX3_ayvQX4~r6jbYbwfYK~OgLi_QXWK2~fW51ff7RoH~DDIrgPa5XM~eVxus64GZU~KhhTM1zuNN~rI4MmDPPTp~FdBF-J6Pun~PnFukw__z_~LiGJo4dg8B~BtH0Tl8o51; _gid=GA1.2.812029370.1680713774; __cf_bm=jJRIu1fs568CGkJIsX1_hJBVI.9EAvWTv.DMD.20ExE-1680714712-0-AdhsU2aHwsmfFW8X25KWbCE4Yclwr8ddzk0ynWxWq3q4Atv1jx+4NN8YYAeC0zyxnEz3UC8QgiQLrZY68YpSPyj0BmhnfxTeZiF3HdTnqWcpTG8h6aXRsJ+AtrDMnGU7Nmi9hB55m3Q2bn1NNTANGXYWFgVkd0JtHxC6mK8vBnuw0X6gObB0jC4XYQbld0nt8w==; _ga=GA1.1.900687260.1680519923; _ga_75BBYNYN9J=GS1.1.1680713769.5.1.1680715263.0.0.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}

# ===== 爬取红楼梦 =====
# def crawl(path, url, depth=1): # 定义爬取函数
#     if not os.path.exists(path):
#         os.mkdir(path)
#     if depth == 0: # 如果爬取深度为0
#         return # 返回
#     # try: # 尝试执行以下代码
#     print('-' * 30) # 打印分割线'
#     print('Crawling:', url) # 打印爬取的网页地址
#     response = requests.get(url, headers=headers) # 发送GET请求
#     if response.status_code == 200: # 如果请求成功
#         print('Status code:', response.status_code) # 打印状态码
#         print('Content type:', response.headers['Content-Type']) # 打印内容类型
#         print('Encoding:', response.encoding) # 打印编码方式
#         print('-' * 30) # 打印分割线
#         #ISO-8859-1 转 gnk
#         text = response.text.encode(response.encoding).decode('gbk', errors='ignore') # 忽略编码错误
#         soup = BeautifulSoup(text, 'lxml') # 使用BeautifulSoup解析网页
#         for link in soup.find_all('a'): # 遍历网页中的每个链接
#             if link.has_attr('href'): # 如果链接有href属性
#                 if link['href'].startswith('http'): # 如果链接以http开头
#                     crawl(path, link['href'], depth-1) # 递归调用爬取函数，爬取深度减1
#                 else:
#                     crawl(path, url + link['href'], depth-1) # 递归调用爬取函数，爬取深度减1
#         text = soup.get_text() # 获取网页中的文本
#         text = re.sub(r'\s+', ' ', text) # 将文本中的多个空格替换为一个空格
#         text = re.sub(r'\n', ' ', text) # 将文本中的换行符替换为空格
#         text = re.sub(r'\t', ' ', text) # 将文本中的制表符替换为空格
#         text = re.sub(r'\xa0', ' ', text) # 将文本中的不间断空格替换为空格
#         text = re.sub(r'\u3000', ' ', text) # 将文本中的全角空格替换为空格
#         text = re.sub(r'[^\w\s]', ' ', text) # 将文本中的非单词和非空格字符替换为空格
#         text = re.sub(r'\s+', ' ', text) # 将文本中的多个空格替换为一个空格
#         text = text.strip() # 去掉文本两端的空格
#         if len(text): # 如果文本不为空
#             print('Text length:', len(text)) # 打印文本长度
#             with open(os.path.join(path, url.replace('/', '_')), 'w+', encoding='utf-8') as f: # 打开文档
#                 f.write(text) # 写入文本
#                 print('Saved to:', os.path.join(path, url.replace('/', '_'))) # 打印文档保存路径
#     else:
#         print('Error:', response.status_code)
    # except: # 如果发生异常
    #     print('Exception!')

# ======================


# ====== 爬取nt大陆 ======
def crawl(path, url, depth=1): # 定义爬取函数
    if not os.path.exists(path):
        os.mkdir(path)
    if depth == 0: # 如果爬取深度为0
        return # 返回
    # try: # 尝试执行以下代码
    print('-' * 30) # 打印分割线'
    print('Crawling:', url) # 打印爬取的网页地址
    response = requests.get(url, headers=headers) # 发送GET请求
    if response.status_code == 200: # 如果请求成功
        print('Status code:', response.status_code) # 打印状态码
        print('Content type:', response.headers['Content-Type']) # 打印内容类型
        print('Encoding:', response.encoding) # 打印编码方式
        print('-' * 30) # 打印分割线
        #ISO-8859-1 转 gnk
        text = response.text.encode(response.encoding, errors='ignore').decode('gbk', errors='ignore')# 忽略编码错误
        soup = BeautifulSoup(text, 'lxml') # 使用BeautifulSoup解析网页
        #找到所有dd下的a标签
        for link in soup.find_all('dd'):
            for a in link.find_all('a'):
                if a.has_attr('href'):
                    if a['href'].startswith('http'):
                        crawl(path, a['href'], depth-1)
                    else:
                        crawl(path, url + a['href'], depth-1)
        text = soup.get_text() # 获取网页中的文本
        # text = re.sub(r'\s+', ' ', text) # 将文本中的多个空格替换为一个空格
        # text = re.sub(r'\n', ' ', text) # 将文本中的换行符替换为空格
        # text = re.sub(r'\t', ' ', text) # 将文本中的制表符替换为空格
        # text = re.sub(r'\xa0', ' ', text) # 将文本中的不间断空格替换为空格
        # text = re.sub(r'\u3000', ' ', text) # 将文本中的全角空格替换为空格
        # text = re.sub(r'[^\w\s]', ' ', text) # 将文本中的非单词和非空格字符替换为空格
        # text = re.sub(r'\s+', ' ', text) # 将文本中的多个空格替换为一个空格
        # text = text.strip() # 去掉文本两端的空格
        if len(text): # 如果文本不为空
            print('Text length:', len(text)) # 打印文本长度
            with open(os.path.join(path, url.replace('/', '_')), 'w+', encoding='utf-8') as f: # 打开文档
                f.write(text) # 写入文本
                print('Saved to:', os.path.join(path, url.replace('/', '_'))) # 打印文档保存路径
    else:
        print('Error:', response.status_code)
    # except: # 如果发生异常
    #     print('Exception!')

# ======================


# crawl('HongLouMeng', 'http://www.purepen.com/hlm/', depth=2) # 红楼梦(分词抽象)
crawl('DouLuoDaLu', 'https://www.qb5.tw/book_518/', depth=2) # nt大陆

