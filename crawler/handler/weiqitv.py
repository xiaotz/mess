import json
import re
from urllib.parse import quote
import html
from utils.crawl_video_list import crawl_video_handler
from utils.crawler import crawl, firefox_crawl


class weiqitv_handler(crawl_video_handler):
    def __init__(self, video_format):
        self.format = video_format

    def get_video_url_list(self):
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
            print("error to get_video_url_list: %s" % resp)
            print(str(e))
            return None

    def get_video_name(self, url):
        try:
            resp = crawl(url)
            p = re.compile(r'<title>(?P<name>[^<]+)</title>')
            m = p.search(resp)
            name = m.group('name')
            return name
        except Exception as e:
            print("error to get_video_name: %s" % resp)
            print(str(e))
            return None

    def get_video_source_url(self, video_url):
        try:
            query_url = 'http://www.flvcd.com/parse.php?kw=%s&format=%s' % (quote(video_url.replace('http://', '')), self.format)
            resp = firefox_crawl(query_url, use_proxy=True)
            p = re.compile(r' href="(?P<data>http://play.g3proxy.lecloud.com[^"]+)"')
            m = p.search(resp)
            if m is None:
                # maybe this is not a letv
                resp = crawl(video_url)
                p = re.compile(r'\"url\":\"http:\\/\\/www\.yunsp\.com\.cn:8080\\/dispatch\\/video\\/get\\/(?P<vid>\d+)_(?P<sid>\d+)_0\.ovp\"')
                m = p.search(resp)
                if m is None:
                    return None
                else:
                    sid = m.group('sid')
                    # vid = m.group('vid')
                    info_url='http://www.yunsp.com.cn:8080/dispatch/videoPlay/getInfo?vid=%s&sid=%s&isList=0&ecode=notexist' % (m.group('vid'), m.group('sid'))
                    info_resp = crawl(info_url)
                    info_resp_json = json.loads(info_resp)
                    hint_url = info_resp_json[0]['posterUrl']
                    p = re.compile(r'(?P<video_id>video\d+)/video')
                    m = p.search(hint_url)
                    video_id = m.group('video_id')
                    m3u8_url = 'http://hlsat.upuday.com/vod/ovp/%s/mp4/800/%s.mp4/av-g.m3u8' % (sid, video_id)
                    download_url_resp = crawl(m3u8_url)
                    download_url = []
                    for url in download_url_resp.split('\n'):
                        if not url.startswith('#') and url:
                            download_url.append(url)
                    return download_url
            else:
                download_url = html.unescape(m.group('data'))
                return download_url
        except Exception as e:
            print('error occurs when get download url for %s, error = %s' % (url, str(e)))
            return None
