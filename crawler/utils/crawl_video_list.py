import os
from utils.crawler import crawl_big_file


class crawl_video_handler(object):

    def __init__(self):
        self.base_url = None

    def set_base_url(self, url:str):
        self.base_url = url

    def get_video_url_list(self) -> list: pass

    def get_video_name(self, url:str) -> str: pass

    def get_video_source_url(self, url:str) -> str: pass


def start_crawl(handler:crawl_video_handler, url:str, base_dir:str):
    handler.set_base_url(url)
    url_list = handler.get_video_url_list()
    if url_list is None:
        exit(-1)
    i = 0
    for url in url_list:
        i += 1
        file_name = handler.get_video_name(url)
        if file_name is None:
            exit(-1)
        target_file_name = os.path.join(base_dir, str(i).zfill(3) + '.' + file_name + '.mp4')
        if os.path.exists(target_file_name):
            continue
        else:
            source_url = handler.get_video_source_url(url)
            if source_url is None:
                exit(-1)
            print('downloading ' + target_file_name)
            crawl_big_file(source_url, target_file_name)