from proxypool.db import RedisClient
from proxypool.config import TEST_URL
import asyncio
import requests
# from urllib.parse import urlparse

class Filter:
    def __init__(self):
        self.db=RedisClient()

    async def check_one(self,proxy):

        proxies={'http':'http://'+proxy}
        try:
            print('正在测试: {}'.format(proxy))
            r=requests.get(TEST_URL,proxies=proxies)
        except requests.RequestException:
            print('检测失败',proxy)
            self.db.remove(proxy)
            return
        if r.status_code==200:
            print('代理可用',proxy)
            self.db.decrease(proxy)


    def run(self):
        print('===开始测试代理===')
        try:
            print('当前代理个数：{}'.format(self.db.count))
            tasks=[asyncio.ensure_future(self.check_one(proxy.decode())) for proxy in self.db.batch()]
            loop=asyncio.get_event_loop()
            loop.run_until_complete(asyncio.wait(tasks))

        except Exception as e:
            print('测试错误',e.args)

if __name__ == '__main__':
    f=Filter()
    proxy='103.242.45.68:8080'
    r=requests.get(TEST_URL,proxies={'http':'http://'+proxy})
    print(r.status_code)