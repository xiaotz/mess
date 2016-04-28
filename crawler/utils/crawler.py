import gzip
import os
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import shutil
import urllib.request as request

g_proxy_dict = {}  # key: http, https, ...
g_firefox_keys = {'http': 'httpProxy'}
g_firefox_proxy_dict={'proxyType': ProxyType.MANUAL}

g_headers = {'Accept-Encoding': 'compress, gzip',
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
             # 'Referer': 'http://www.flvcd.com/',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            }


def set_proxy(key, value):
    global g_proxy_dict
    global g_firefox_proxy_dict
    g_proxy_dict[key] = value
    g_firefox_proxy_dict[g_firefox_keys[key]] = value


def crawl(url, charset="utf-8", timeout=10, use_proxy=False, retries=5):
    retry = 0
    while retry < retries:
        try:
            req = request.Request(url)
            if use_proxy:
                global g_proxy_dict
                proxy = request.ProxyHandler(g_proxy_dict)
                auth = request.HTTPBasicAuthHandler()
                opener = request.build_opener(proxy, auth, request.HTTPHandler)
                request.install_opener(opener)
            with request.urlopen(req, timeout=timeout) as response:
                if response.getheader("Content-Encoding") == "gzip":
                    tmp = gzip.decompress(response.read()).decode(charset)
                else:
                    tmp = response.read().decode(charset)
                if use_proxy:
                    request.install_opener(None)
                return tmp
        except Exception as expt:
            print("error occurs when crawling url %s, error= %s" % (url, str(expt)))
            retry += 1
    return None


def firefox_crawl(url, use_proxy=False, retries=3):
    retry = 0
    while retry < retries:
        try:
            global g_firefox_proxy_dict
            proxy = None
            if use_proxy:
                proxy = Proxy(g_firefox_proxy_dict)
            firefox_browser = webdriver.Firefox(proxy=proxy)
            firefox_browser.get(url)
            resp = firefox_browser.page_source
            firefox_browser.close()
            return resp
        except Exception as expt:
            print("error occurs when firefox_crawl url %s, error=%s" % (url, str(expt)))
            retry += 1
    return None


def chrome_craw(url, use_proxy=False, retries=3):
    retry = 0
    while retry < retries:
        try:
            ch_options = webdriver.ChromeOptions()
            if use_proxy:
                ch_options.add_argument('--proxy-server=http://%s' % g_keys['http'])
            browser = webdriver.Chrome(chrome_options=ch_options)
            browser.get(url)
            resp = browser.page_source
            browser.close()
            return resp
        except Exception as e:
            print("error occurs when chrome_craw url %s, error=%s" % (url, str(e)))
            retry += 1
    return None


def advanced_crawl_js_var(url, var, use_proxy=False, retries=5):
    retry = 0
    while retry < retries:
        try:
            global g_firefox_proxy_dict
            proxy = None
            if use_proxy:
                proxy = Proxy(g_firefox_proxy_dict)
            browser = webdriver.Firefox(proxy=proxy)
            browser.get(url)
            result = browser.execute_script("return %s;" % var)
            browser.close()
            return result
        except Exception as expt:
            print("error occurs when advanced_crawl_js_var url %s, error=%s" % (url, str(expt)))
            retry += 1
    return None


def crawl_big_file(url, local_file, retries=3):
    retry = 0
    while retry < retries:
        try:
            local_file_tmp = local_file + '.tmp'
            if os.path.exists(local_file_tmp):
                os.remove(local_file_tmp)
            request.urlretrieve(url, local_file_tmp)
            os.rename(local_file_tmp, local_file)
            return True
        except Exception as expt:
            print("error occurs when downloading %s to %s, retry = %d, error = %s" % (url, local_file, retry, str(expt)))
            retry += 1
    return False


def crawl_multiple_url_into_file(url_list, local_file):
    try:
        local_tmp_folder = local_file + '_tmp'
        local_tmp_file = local_file + '.tmp'
        if not os.path.exists(local_tmp_folder):
            os.mkdir(local_tmp_folder)
        if os.path.exists(local_tmp_file):
            os.remove(local_tmp_file)
        with open(local_tmp_file, "wb") as f:
            i = 0
            for url in url_list:
                i += 1
                tmp_file = os.path.join(local_tmp_folder, '%d.tmp' % i)
                if not os.path.exists(tmp_file):
                    crawl_big_file(url, tmp_file)
                with open(tmp_file, "rb") as tmp_f:
                    f.write(tmp_f.read())
        os.rename(local_tmp_file, local_file)
        shutil.rmtree(local_tmp_folder)
        return True
    except Exception as expt:
        print("error occurs when download multiple url to file:%s, error = %s" % (local_file, str(expt)))
    return False
