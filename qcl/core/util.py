# Source Generated with Decompyle++
# File: util.pyc (Python 3.13)

'''通用工具函数'''
import hashlib
import json
import os
import re
import shutil
import stat
import tempfile
import time
import zipfile
ILLEGAL = re.compile('[<>:"|?*\\x00-\\x1f]')

def oem_encoding():
    '''控制台（cmd）使用的代码页，用于生成批处理文件。
中文 Windows 一般为 cp936，英文为 cp437/850。'''
    enc = None
    
    try:
        import ctypes
        cp = ctypes.windll.kernel32.GetOEMCP()
        if cp:
            pass
        enc = 'cp%d' % cp
        if not enc:
            
            try:
                import locale
                enc = locale.getpreferredencoding(False)
                
                try:
                    if not enc:
                        enc
                    '测'.encode('')
                    if not enc:
                        
                        try:
                            '测'.encode('gbk')
                            enc = 'gbk'
                            return enc
                            return enc
                            except Exception:
                                enc = None
                            continue
                            except Exception:
                                enc = None
                            continue
                            except Exception:
                                enc = None
                            continue
                        except Exception:
                            enc = 'utf-8'
                            return enc


def write_text_oem(path, text):
    '''以控制台代码页写入文本文件（供批处理读取）'''
    
    try:
        enc = oem_encoding()
        with open(path, 'w', enc, 'replace', '\r\n') as f:
            f.write(text)
            
            try:
                None(None, None)
                return True
                if not None:
                    pass
                
                try:
                    return True
                    
                    try:
                        pass
                    except Exception:
                        return False


def normalize_crlf(text):
    '''统一换行符为 CRLF（cmd.exe 解析批处理文件必须使用 CRLF）'''
    return text.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')


def read_text_any(path):
    '''读取未知编码的文本（UTF-8 / GBK 自动判断）'''
    
    try:
        with open(path, 'rb') as f:
            raw = f.read()
            
            try:
                None(None, None)
                for enc in ('utf-8-sig', 'utf-8', oem_encoding(), 'gbk', 'cp1252'):
                    
                    return ('utf-8-sig', 'utf-8', oem_encoding(), 'gbk', 'cp1252'), raw.decode(enc)
                return raw.decode('utf-8', 'ignore')
                if not None:
                    pass
                
                try:
                    continue
                    
                    try:
                        pass
                    except Exception:
                        return ''
                        except Exception:
                            continue


def sha1_file(path):
    h = hashlib.sha1()
    with None:
        f = open(path, 'rb')
        for chunk in iter((lambda : f.read(1048576)), b''):
            h.update(chunk)
    None(None, None)
    return h.hexdigest()
    if not None:
        pass
    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with None:
        f = open(path, 'rb')
        for chunk in iter((lambda : f.read(1048576)), b''):
            h.update(chunk)
    None(None, None)
    return h.hexdigest()
    if not None:
        pass
    return h.hexdigest()


def human_size(n):
    
    try:
        n = float(n)
        for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
            if abs(n) < 1024:
                
            return ('B', 'KB', 'MB', 'GB', 'TB'), '%.1f %s' % (n, unit)
        return '%.1f PB' % n
    except Exception:
        return '-'


def safe_name(name, repl):
    name = ILLEGAL.sub(repl, str(name)).strip().rstrip('.')
    if not name:
        name
    return 'unnamed'


def read_json(path, default):
    
    try:
        with open(path, 'r', 'utf-8') as f:
            
            try:
                (None, None)
                return None, json.load(f)
                if not None:
                    pass
                
                try:
                    return None
                    
                    try:
                        pass
                    except Exception:
                        return 


def write_json(path, data):
    
    try:
        os.makedirs(os.path.dirname(path), True)
        tmp = path + '.tmp'
        with open(tmp, 'w', 'utf-8') as f:
            json.dump(data, f, False, 2)
            
            try:
                None(None, None)
                os.replace(tmp, path)
                return True
                if not None:
                    pass
                
                try:
                    continue
                except Exception:
                    return False


def _onerror(func, path, exc_info):
    
    try:
        os.chmod(path, stat.S_IWUSR)
        func(path)
        return None
    except Exception:
        return None


def rmtree(path, ignore_errors):
    if not path or os.path.exists(path):
        pass
    return None
    
    try:
        shutil.rmtree(path, _onerror if not ignore_errors else None)
        return None
    except Exception:
        if not ignore_errors:
            pass
        raise 
        return None


def unzip(src, dest, exclude_prefix, overwrite):
    """解压 zip，返回解压文件数。exclude_prefix 可跳过如 'META-INF/' 的条目"""
    n = 0
    os.makedirs(dest, True)
    with zipfile.ZipFile(src) as zf:
        for info in zf.infolist():
            name = info.filename
            if (lambda .0: pass)(exclude_prefix()):
                continue
            if name.endswith('/'):
                continue
            target = os.path.join(dest, name)
            os.makedirs(os.path.dirname(target), True)
            if not os.path.exists(target) and overwrite:
                continue
            with zf.open(info) as src_f:
                with open(target, 'wb') as dst_f:
                    shutil.copyfileobj(src_f, dst_f, 524288)
                None(None, None)
                any(None, None)
                n += 1
                continue
                None(None, None)
                return n
                if not None:
                    pass
    continue
    if not None:
        pass
    continue
    if not None:
        pass
    return n


def extract_natives(jar, dest, exclude_prefix):
    return unzip(jar, dest, exclude_prefix, True)


def make_zip(src_dir, out_file, skip_dirs):
    os.makedirs(os.path.dirname(out_file), True)
    with zipfile.ZipFile(out_file, 'w', zipfile.ZIP_DEFLATED, 6) as zf:
        for root, dirs, files in os.walk(src_dir):
            pass
        , []
        dirs[:] = d,
        for None in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, src_dir)
            zf.write(full, rel)
        continue
        None(None, None)
        return out_file
        
        if not d,:
            pass
    None, None, None
    return out_file


def list_zip(src):
    
    try:
        with zipfile.ZipFile(src) as zf:
            
            try:
                (None, None)
                return None, zf.namelist()
                if not None:
                    pass
                
                try:
                    return None
                    
                    try:
                        pass
                    except Exception:
                        return 


def now_ms():
    return int(time.time() * 1000)


def tmp_file(suffix):
    paths = paths
    # import  # [decompiler] module name lost
    os.makedirs(paths.TMP_DIR, True)
    (fd, p) = tempfile.mkstemp(suffix, paths.TMP_DIR)
    os.close(fd)
    return p


class Emitter:
    __doc__ = '极简事件总线'
    
    def __init__(self):
        self._handlers = { }

    
    def on(self, name, fn):
        self._handlers.setdefault(name, []).append(fn)
        return fn

    
    def off(self, name, fn):
        '''取消订阅。不传 fn 则清空该事件的全部订阅。

页面切换时如果不反注册，旧页面的绑定方法会一直被事件总线持有：
一来每切一次页面就多一份订阅（内存涨、回调重复触发），
二来回调会打到已经不可见的控件上。
'''
        if fn is None:
            self._handlers.pop(name, None)
        return None
        if not self._handlers.get(name):
            self._handlers.get(name)
        lst = []
        
        try:
            lst.remove(fn)
            if not lst:
                self._handlers.pop(name, None)
            return None
            return None
        except ValueError:
            continue


    def emit(self, name, *args, **kwargs):
        for fn in list(self._handlers.get(name, [])):
            fn(*args, **{ })
        return None
        except Exception:
            continue

