# Source Generated with Decompyle++
# File: net.pyc (Python 3.13)

'''网络层：会话、镜像、HTTP 请求、流式下载（不依赖 Qt，服务端可用）'''
import json
import os
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .constants import APP_VERSION, MIRRORS
from . import util
UA = 'QCL-Launcher/%s' % APP_VERSION
CONNECT_TIMEOUT = 6
RATELIMIT_CODES = (403, 429)
RATELIMIT_WAIT = 2.5

class MirrorManager:
    
    def __init__(self):
        self.mirrors = MIRRORS
        self.current = MIRRORS[0]
        self._down = { }

    
    def set_mirror(self, name):
        for m in self.mirrors:
            if not m.name == name:
                continue
            self.current = m
            self.mirrors
            return True
        return False

    
    def map(self, url):
        return self.current.map(url)

    
    def candidates(self, url):
        '''返回候选 URL 列表：当前镜像 -> 其他镜像 -> 官方原址'''
        out = []
        primary = self.map(url)
        out.append(primary)
        for m in self.mirrors:
            v = m.map(url)
            if not v not in out:
                continue
            out.append(v)
        if url not in out:
            pass
        out.append(url)
        return out

    
    def ordered_candidates(self, url):
        '''按健康度排序的候选列表：近期失败的排到最后。

否则每次请求都要先等官方源（国内常不可达）超时，才轮到可用镜像。
'''
        now = time.time()
        cands = self.candidates(url)
        good = [u for u in cands if self._down.get(u, 0) <= now]
        bad = [u for u in cands if self._down.get(u, 0) > now]
        return good + bad
        
        
    def pick(self, url):
        now = time.time()
        cands = self.ordered_candidates(url)
        , []
        cands, u, healthy, u = None
        if not healthy:
            self._down.clear()
        healthy = cands
        return healthy[0]
        

    def mark_down(self, url, seconds):
        self._down[url] = time.time() + seconds


mirrors = MirrorManager()

def session(pool):
    s = requests.Session()
    s.headers.update({
        'User-Agent': UA,
        'Accept': 'application/json' })
    retry = Retry(2, 0, 1, 0.3, [
        429,
        500,
        502,
        503,
        504], frozenset([
        'GET',
        'HEAD']))
    ad = HTTPAdapter(retry, pool, pool)
    s.mount('https://', ad)
    s.mount('http://', ad)
    return s

_SESSIONS = { }

def get_session():
    import threading
    tid = threading.get_ident()
    if tid not in _SESSIONS:
        _SESSIONS[tid] = session()
    return _SESSIONS[tid]


def _timeout_pair(timeout):
    '''把标量超时拆成 (连接, 读取)。

连接超时单独收紧：连不上的源应尽快放弃并回落到镜像，
而读取大文件时仍保留调用方给的完整时间。
'''
    
    try:
        t = float(timeout)
        return (min(CONNECT_TIMEOUT, t), t)
    except (TypeError, ValueError):
        return 


def request(method, url, timeout, **kw):
    '''带镜像回落的请求'''
    cands = mirrors.ordered_candidates(url)
    to = _timeout_pair(timeout)
    last = None
    for u in cands:
        for attempt in (0, 1):
            r = get_session().request(*(method, u), **{
                'timeout': to })
            if r.status_code in RATELIMIT_CODES and attempt == 0:
                time.sleep(RATELIMIT_WAIT)
                continue
            if r.status_code < 400:
                
                
            return cands, (0, 1), r
            if r.status_code >= 500:
                pass
            mirrors.mark_down(u, 60)
            RuntimeError(f'''HTTP  ''')
    if not last:
        last
    raise RuntimeError('请求失败: %s' % url)
    except Exception:
        None = None
        last = e
        mirrors.mark_down(u, 60)
        e = None
        del e
        continue
        e = None
        del e


def get_json(url, timeout, default, **kw):
    
    try:
        r = request(*('GET', url), **{
            'timeout': timeout })
        return r.json()
    except Exception:
        return 


def get_text(url, timeout, default, **kw):
    
    try:
        r = request(*('GET', url), **{
            'timeout': timeout })
        if not r.encoding:
            r.encoding
        r.encoding = 'utf-8'
        return r.text
    except Exception:
        return 


def get_bytes(url, timeout, **kw):
    return request(*('GET', url), **{
        'timeout': timeout }).content


def head_size(url, timeout):
    
    try:
        r = get_session().head(mirrors.pick(url), timeout, True)
        if not r.headers.get('Content-Length', 0):
            r.headers.get('Content-Length', 0)
        return int(0)
    except Exception:
        return 0


def friendly_error(url, e):
    '''把 requests 的原始异常翻译成用户能看懂的中文提示'''
    
    try:
        import requests
        if isinstance(e, requests.HTTPError):
            code = getattr(getattr(e, 'response', None), 'status_code', 0)
            if code == 404:
                pass
            return RuntimeError('文件不存在（HTTP 404）：%s' % url)
        if None == 403:
            pass
        return RuntimeError('下载被拒绝（HTTP 403，通常是镜像限流，请稍后重试）：%s' % url)
        
        try:
            if code == 429:
                pass
            return RuntimeError('请求过于频繁（HTTP 429），请稍后重试：%s' % url)
            
            try:
                if code:
                    pass
                return RuntimeError(f'''下载失败（HTTP ）：''')
                
                try:
                    if isinstance(e, requests.Timeout):
                        pass
                    return RuntimeError('下载超时：%s' % url)
                    
                    try:
                        if isinstance(e, requests.ConnectionError):
                            pass
                        return RuntimeError('无法连接服务器：%s' % url)
                        return e
                    except Exception:
                        return e


def download_file(url, dest, size, sha1, progress, timeout, chunk):
    '''流式下载（支持断点续传 + 校验），供服务端/命令行使用。
progress(done, total) 可选回调。'''
    os.makedirs(os.path.dirname(dest), True)
    cands = mirrors.ordered_candidates(url)
    to = _timeout_pair(timeout)
    last = None
    for u in cands:
        for attempt in (0, 1):
            got = 0
            mode = 'wb'
            headers = { }
            if mode == 'ab' and got:
                headers['Range'] = 'bytes=%d-' % got
            if not headers:
                headers
            r = get_session().get(u, True, to, None)
            if r.status_code == 416:
                r = get_session().get(u, True, to)
                mode = 'wb'
            got = 0
            if r.status_code in RATELIMIT_CODES and attempt == 0:
                time.sleep(RATELIMIT_WAIT)
                continue
            r.raise_for_status()
            if r.status_code == 200 and mode == 'ab':
                mode = 'wb'
            got = 0
            if not size:
                size
                if not r.headers.get('Content-Length', 0):
                    r.headers.get('Content-Length', 0)
            total = int(0)
            with open(dest, mode) as f:
                for data in r.iter_content(chunk):
                    if not data:
                        continue
                    f.write(data)
                    got += len(data)
                    if not progress:
                        continue
                    progress(got, total)
                None if os.path.exists(dest) and size else cands

                if sha1 and util.sha1_file(dest) != sha1:
                    os.remove(dest)
                    last = ValueError('校验失败 %s' % u)
                    continue
            return True
    if last:
        pass
    raise last
    return False
    if not None:
        pass
    continue
    continue
    except Exception:
        e = None
        last = friendly_error(u, e)
        mirrors.mark_down(u, 60)
        e = None
        del e
        continue
        e = None
        del e


def fetch_manifest():
    '''获取原版版本清单（带镜像回落）'''
    from .constants import MOJANG_MANIFEST
    if not get_json(MOJANG_MANIFEST, 20):
        get_json(MOJANG_MANIFEST, 20)
    return { }

