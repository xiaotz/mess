import json
import re
from urllib.parse import quote
import html
from utils.crawl_video_list import crawl_video_handler
from utils.crawler import crawl, advanced_crawl


class weiqitv_handler(crawl_video_handler):
    def get_video_url_list(self) -> list:
        resp = crawl(self.base_url)
        try:
            p = re.compile(r'var videos = (?P<data>[^;]+);')
            m = p.search(resp)
            all_data = m.group('data')
            json_data = json.loads(all_data)
            l = list()
            for data in json_data:
                l.append('http://weiqitv.com/index/video_play?videoId=' + data['_id'])
            return l
        except Exception as e:
            print("error to parse html response: %s" % resp)
            print(str(e))
            return None

    def get_video_name(self, url:str) -> str:
        # get file name
        try:
            resp = crawl(url)
            p = re.compile(r'<title>(?P<name>[^<]+)</title>')
            m = p.search(resp)
            name = m.group('name')
            return name
        except Exception as e:
            print("error to parse html response: %s" % resp)
            print(str(e))
            return None

    def get_video_source_url(self, url:str) -> str:
        # get download url
        try:
            # normal super real
            query_url = 'http://www.flvcd.com/parse.php?kw=%s&format=super' % quote(url.replace('http://', ''))
            resp = advanced_crawl(query_url, use_proxy=True)
            p = re.compile(r' href="(?P<data>http://play.g3proxy.lecloud.com[^"]+)"')
            m = p.search(resp)
            if m is None:
                print(resp)
            download_url = html.unescape(m.group('data'))
            return download_url
        except Exception as e:
            print("error to parse html response: %s" % resp)
            print(str(e))
            return None
