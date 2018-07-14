import re
import requests

BASE_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def proxy_match(proxy):
    pattern = re.compile('\d+\.\d+\.\d+\.\d+:\d+')
    if pattern.match(proxy):
        return True
    else:
        print('proxy format is incorrect', proxy)


def get_page(url,options={}):
    headers=dict(BASE_HEADERS,**options)
    try:
        response = requests.get(url, headers=headers)
    except requests.ConnectionError as e:
        print('Connection error', e)
        return None
    if response.status_code == 200:
        return response.text


