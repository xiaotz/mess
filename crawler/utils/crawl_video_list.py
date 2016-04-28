import os
from utils.crawler import crawl_big_file, crawl_multiple_url_into_file
import concurrent.futures

class crawl_video_handler(object):
    def __init__(self):
        self.base_url = None

    def set_base_url(self, base_rul):
        self.base_url = base_rul

    def get_video_url_list(self): pass

    def get_video_name(self, video_url): pass

    def get_video_source_url(self, video_url): pass


def start_crawl(handler, url, base_dir, concurrent_num):
    handler.set_base_url(url)
    url_list = handler.get_video_url_list()
    if url_list is None:
        exit(-1)
    i = 0

    downloading_list = []
    for url in url_list:
        i += 1
        file_name = handler.get_video_name(url)
        if file_name is None:
            exit(-1)
        target_file_name = os.path.join(base_dir, str(i).zfill(3) + '.' + file_name + '.mp4')
        if os.path.exists(target_file_name):
            continue
        else:
            downloading_list.append({'file_name': target_file_name, 'handler': handler, 'url': url})
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_num)
    executor.map(start_crawl_one, downloading_list)


def start_crawl_one(dict):
    print('downloading ' + dict['file_name'])
    source_url = dict['handler'].get_video_source_url(dict['url'])
    if source_url is None:
        return None
    elif type(source_url) is str:
        crawl_big_file(source_url, dict['file_name'])
    elif type(source_url) is list:
        crawl_multiple_url_into_file(source_url, dict['file_name'])
    else:
        raise Exception("unknown download type")