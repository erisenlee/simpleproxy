import sys
sys.path.append('/root/workspace/Flask/ProxyPool/env/lib/python3.5/site-packages')
from proxypool.scheduler import Scheduler


if __name__ == '__main__':

    s=Scheduler()

    s.run()