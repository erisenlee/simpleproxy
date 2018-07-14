import requests
import json
url='http://47.100.61.172/api/proxy/3'

re=requests.get(url)
proxy=json.loads(re.content)
print(type(proxy))