import gzip
import os
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from urllib.request import Request
import urllib.request as req

g_proxy_dict={}
g_adv_proxy_dict={'proxyType': ProxyType.MANUAL}
g_keys = {'http':'httpProxy'}
g_headers = {'Accept-Encoding': 'compress, gzip',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        #'Referer': 'http://www.flvcd.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }


def set_proxy(key, value):
    global g_proxy_dict
    global g_adv_proxy_dict
    g_proxy_dict[key] = value
    g_adv_proxy_dict[g_keys[key]] = value


def crawl(url, charset="utf-8", timeout=10, use_proxy=False):
    request = Request(url)
    try:
        if use_proxy:
            global g_proxy_dict
            proxy = req.ProxyHandler(g_proxy_dict)
            auth = req.HTTPBasicAuthHandler()
            opener = req.build_opener(proxy, auth, req.HTTPHandler)
            req.install_opener(opener)
        response = req.urlopen(request, timeout=timeout)
        if response.getheader("Content-Encoding") == "gzip":
            tmp = gzip.decompress(response.read()).decode(charset)
        else:
            tmp = response.read().decode(charset)
        if use_proxy:
            req.install_opener(None)
        return tmp
    except Exception as e:
        print("error for url %s" % url)
        print(str(e))
        return None
    finally:
        try:
            response.close()
        except Exception as e:
            print(str(e))
            return None


def advanced_crawl(url, charset="utf-8", timeout=10, use_proxy=False) -> str:
    try:
        global g_adv_proxy_dict
        proxy = None
        if use_proxy:
            proxy = Proxy(g_adv_proxy_dict)
        browser = webdriver.Firefox(proxy=proxy)
        browser.get(url)
        resp = browser.page_source
        browser.close()
        return resp
    except Exception as e:
        print("error for url %s" % url)
        print(str(e))
        return None


def crawl_big_file(url: str, local_file: str):
    # NOTE the stream=True parameter
    local_file_tmp = local_file + '.tmp'
    if os.path.exists(local_file_tmp):
        os.remove(local_file_tmp)
    try:
        req.urlretrieve(url, local_file_tmp)
    except Exception as e:
        print("error for url %s" % url)
        print(str(e))
        return None
    os.rename(local_file_tmp, local_file)

