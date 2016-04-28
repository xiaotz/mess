import os
from utils.crawler import crawl_big_file, crawl_multiple_url_into_file


class crawl_video_handler(object):
    def __init__(self):
        self.base_url = None

    def set_base_url(self, base_rul):
        self.base_url = base_rul

    def get_video_url_list(self): pass

    def get_video_name(self, video_url): pass

    def get_video_source_url(self, video_url): pass


def start_crawl(handler, url, base_dir):
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
            print('downloading ' + target_file_name)
            source_url = handler.get_video_source_url(url)
            if source_url is None:
                exit(-1)
                # continue
            elif type(source_url) is str:
                crawl_big_file(source_url, target_file_name)
            elif type(source_url) is list:
                crawl_multiple_url_into_file(source_url, target_file_name)
            else:
                raise Exception("unknown download type")
