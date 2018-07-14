import redis
from proxypool.config import HOST, PORT, PASSWORD, KEY, INITSCORE,MAX_SCORE,MIN_SCORE,BATCH_NUMBER
from proxypool.utils import proxy_match
from random import choice

class RedisClient:
    def __init__(self):
        self.db = redis.StrictRedis(host=HOST, port=PORT,password=PASSWORD)

    def is_exists(self, proxy):
        return True if self.db.zscore(KEY, proxy) else False

    def add(self, proxy):
        if proxy_match(proxy):
            self.db.zadd(KEY, INITSCORE, proxy)

    @property
    def count(self):
        return self.db.zcard(KEY)

    @property
    def is_empty(self):
        return True if self.count == 0 else False

    def random(self):
        if not self.is_empty:
            proxies = self.db.zrangebyscore(KEY,MIN_SCORE,MAX_SCORE, start=0,num=5)
            if proxies:
                random=choice(proxies)
                self.remove(random)
                return random

    def decrease(self, proxy):
        if self.is_exists(proxy):
            score=self.db.zscore(KEY,proxy)
            if score>5:
                return self.db.zincrby(KEY,proxy,-1)
            else:
                self.remove(proxy)

    def batch(self):
        if not self.is_empty:
            if self.count <= BATCH_NUMBER:
                return self.db.zrange(KEY, 0, self.count)
            return self.db.zrevrangebyscore(KEY, 10, 0, start=0, num=10)

    def remove(self,proxy):
        if self.is_exists(proxy):
            self.db.zrem(KEY,proxy)



if __name__ == '__main__':
    redis = RedisClient()
    # for i in range(20):
    #     redis.add('{}11.11.11.11:22'.format(i))
    # for i in redis.batch():
    #     print(i.decode())
    r=redis.batch()
    print(r)