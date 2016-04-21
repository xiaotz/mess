# download big file
# http://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file

from utils.crawler import set_proxy
from utils.crawl_video_list import start_crawl
from handler.weiqitv import weiqitv_handler
import sys

if __name__ == "__main__":
    w = weiqitv_handler()
    proxy = None
    if len(sys.argv) == 3:
        set_proxy(sys.argv[1], sys.argv[2])
    start_url = 'http://weiqitv.com/index/video_play?type=2&videoId=53c744f09874f0e76a8b47b3'
    store_dir = '/home/xiaotz/Videos/mao'
    start_crawl(w, start_url, store_dir)

