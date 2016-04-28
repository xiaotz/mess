from utils.crawler import set_proxy
from utils.crawl_video_list import start_crawl
from handler.weiqitv import weiqitv_handler
import sys

if __name__ == "__main__":
    w = weiqitv_handler('super')
    proxy = None
    if len(sys.argv) == 3:
        set_proxy(sys.argv[1], sys.argv[2])
    start_url = 'http://weiqitv.com/index/video_play?videoId=53c744f09874f0e76a8b481a'
    store_dir = '/home/xiaotz/Videos/ge'
    start_crawl(w, start_url, store_dir)

