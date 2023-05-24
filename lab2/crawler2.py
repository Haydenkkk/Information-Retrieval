from bs4 import BeautifulSoup
import requests
import re
import selenium
from selenium import webdriver
import os
import time
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36', 
    "Cookie": 'first_visit_datetime_pc=2023-04-03+20:05:21; p_ab_id=6; p_ab_id_2=4; p_ab_d_id=1639917103; yuid_b=J4OFEVE; _fbp=fb.1.1680519923390.2095052467; PHPSESSID=71354849_ImIU8T760AzZaIuigmucF7bfvSy0Hjg8; device_token=a7eaec54414b62037030260d34dff8a1; privacy_policy_agreement=5; c_type=22; privacy_policy_notification=0; a_type=0; b_type=0; QSI_S_ZN_5hF4My7Ad6VNNAi=v:0:0; p_b_type=1; tag_view_ranking=0xsDLqCEW6~Lt-oEicbBr~r_Jjn6Ua2V~HY55MqmzzQ~uvBGOtCzqF~_vCZ2RLsY2~5oPIfUbtd6~68luzZqFS0~-7RnTas_L3~jk9IzfjZ6n~tLEo7GtjcE~iRFlj3p1GG~ctjJwbmssT~uW5495Nhg-~O4zMr8hRGP~EYYBFpYNJp~98FF78f4J0~bYn3xr0RaN~zqe8dqUBGC~ckoqr0bPHv~5oHuFQXax5~rOnsP2Q5UN~_EOd7bsGyl~6n5sWl9nNm~tJaVY8ie4B~qG6ZMBxhkE~QaiOjmwQnI~ZTBAtZUDtQ~zaEtI28sYq~qXzcci65nj~TWrozby2UO~ncUG68iRRJ~PwDMGzD6xn~-LwvviyTfq~faHcYIP1U0~Ie2c51_4Sp~uK-xlAOB9q~0r_Dr-UWZa~wmxKAirQ_H~vrf3o5XcIa~pNtQi6YIt-~NGpDowiVmM~gCB7z_XWkp~vzTU7cI86f~azESOjmQSV~zyKU3Q5L4C~nIjJS15KLN~qkC-JF_MXY~4QveACRzn3~cnS1oIcWKc~aKhT3n4RHZ~HZk-7ZdqP6~w8ffkPoJ_S~HBlflqJjBZ~T40wdiG5yy~CEYqcod4iE~D4hLr_YmAD~_C6hhzFNWQ~gnmsbf1SSR~LX3_ayvQX4~r6jbYbwfYK~OgLi_QXWK2~fW51ff7RoH~DDIrgPa5XM~eVxus64GZU~KhhTM1zuNN~rI4MmDPPTp~FdBF-J6Pun~PnFukw__z_~LiGJo4dg8B~BtH0Tl8o51; _gid=GA1.2.812029370.1680713774; __cf_bm=jJRIu1fs568CGkJIsX1_hJBVI.9EAvWTv.DMD.20ExE-1680714712-0-AdhsU2aHwsmfFW8X25KWbCE4Yclwr8ddzk0ynWxWq3q4Atv1jx+4NN8YYAeC0zyxnEz3UC8QgiQLrZY68YpSPyj0BmhnfxTeZiF3HdTnqWcpTG8h6aXRsJ+AtrDMnGU7Nmi9hB55m3Q2bn1NNTANGXYWFgVkd0JtHxC6mK8vBnuw0X6gObB0jC4XYQbld0nt8w==; _ga=GA1.1.900687260.1680519923; _ga_75BBYNYN9J=GS1.1.1680713769.5.1.1680715263.0.0.0',
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
}



 