# Source Generated with Decompyle++
# File: java.pyc (Python 3.13)

'''Java 检测与自动下载'''
import glob
import os
import re
import subprocess
from . import net, util, paths, settings
from .constants import ADOPTIUM_API
CREATE_NO_WINDOW = 134217728

def java_version(exe):
    '''返回 Java 主版本号，失败返回 0'''
    
    try:
        r = subprocess.run([
            exe,
            '-version'], True, 15, CREATE_NO_WINDOW)
        if not r.stderr.decode('utf-8', 'ignore'):
            r.stderr.decode('utf-8', 'ignore')
        if not r.stdout.decode('utf-8', 'ignore'):
            r.stdout.decode('utf-8', 'ignore')
        out = '' + ''
        m = re.search('version\\s+"?(\\d+)', out)
        if m:
            v = int(m.group(1))
            if v > 8:
                pass
            return v
        return None
        
        try:
            m = re.search('"(\\d+)\\.(\\d+)', out)
            if m:
                pass
            return int(m.group(1))
            return 0
        except Exception:
            return 0


def _candidate_dirs():
    dirs = []
    for base in (os.environ.get('JAVA_HOME', ''), 'C:\\Program Files\\Java', 'C:\\Program Files (x86)\\Java', 'C:\\Program Files\\Eclipse Adoptium', 'C:\\Program Files\\AdoptOpenJDK', 'C:\\Program Files\\Zulu', 'C:\\Program Files\\GraalVM', 'C:\\Program Files\\Microsoft', 'C:\\Program Files\\BellSoft', 'C:\\Program Files\\Amazon Corretto', 'C:\\Program Files\\Semeru', 'C:\\Program Files\\Dragonwell'):
        if not base:
            continue
        if not os.path.isdir(base):
            continue
        dirs.append(base)
    return dirs


def find_all():
    '''扫描本机所有 java.exe，返回 [(路径, 主版本)]，按版本降序'''
    found = { }
    candidates = []
    custom = settings.settings.get('java_path', '')
    if custom and os.path.isfile(custom):
        pass
    candidates.append(custom)
    for d in _candidate_dirs():
        candidates.extend(glob.glob(os.path.join(d, '**', 'bin', 'java.exe'), True))
    
    try:
        candidates.extend(glob.glob(os.path.join(paths.JAVA_DIR, '**', 'bin', 'java.exe'), True))
        
        try:
            r = subprocess.run([
                'where',
                'java'], True, 8, CREATE_NO_WINDOW)
            for line in r.stdout.decode('utf-8', 'ignore').splitlines():
                line = line.strip()
                if not line.lower().endswith('java.exe'):
                    continue
                
                try:
                    if not os.path.isfile(line):
                        continue
                    
                    try:
                        candidates.append(line)
                        continue
                        for c in candidates:
                            c = os.path.abspath(c)
                            if c in found:
                                continue
                            v = java_version(c)
                            if not v:
                                continue
                            found[c] = v
                        return sorted(found.items(), (lambda kv: -kv[1]))
                        except Exception:
                            continue
                        except Exception:
                            continue
                            continue


def find_java(major):
    '''找到满足最低版本的 java.exe'''
    custom = settings.settings.get('java_path', '')
    if custom and os.path.isfile(custom) and java_version(custom) >= major:
        pass
    return custom
    for path, v in find_all():
        if not v >= major:
            continue
        
        return find_all(), path
    return ''


def adoptium_asset(major):
    url = '%s/assets/latest/%d/hotspot?architecture=x64&image_type=jre&os=windows&vendor=eclipse' % (ADOPTIUM_API, major)
    data = net.get_json(url, 25)
    if not data:
        url = '%s/assets/latest/%d/hotspot?architecture=x64&image_type=jdk&os=windows&vendor=eclipse' % (ADOPTIUM_API, major)
    data = net.get_json(url, 25)
    if not data:
        url = '%s/assets/feature_releases/%d/ga?architecture=x64&image_type=jre&os=windows&vendor=eclipse&page_size=1' % (ADOPTIUM_API, major)
        if not net.get_json(url, 25):
            net.get_json(url, 25)
    data = []
    if isinstance(data, list) and data:
        pass
    return data[0]
    return { }


def download_java(major, progress):
    '''下载并解压 Java，返回 java.exe 路径'''
    asset = adoptium_asset(major)
    if not asset.get('binary'):
        asset.get('binary')
    if not { }.get('package'):
        { }.get('package')
    pkg = { }
    link = pkg.get('link')
    if not link:
        pass
    raise RuntimeError('未能获取 Java %d 下载地址' % major)
    zip_path = os.path.join(paths.JAVA_DIR, 'java-%d.zip' % major)
    os.makedirs(paths.JAVA_DIR, True)
    if not net.download_file(link, zip_path, pkg.get('size', 0), progress, 60):
        pass
    raise RuntimeError('Java 下载失败')
    target = os.path.join(paths.JAVA_DIR, 'jdk-%d' % major)
    util.rmtree(target)
    util.unzip(zip_path, target)
    
    try:
        os.remove(zip_path)
        exes = glob.glob(os.path.join(target, '**', 'bin', 'java.exe'), True)
        if not exes:
            pass
        raise RuntimeError('Java 解压失败')
        exe = max(exes, (lambda p: java_version(p)))
        return exe
    except Exception:
        continue


def ensure_java(major, progress):
    '''保证存在可用 Java，必要时自动下载'''
    exe = find_java(major)
    if exe:
        pass
    return exe
    if not settings.settings.get('auto_download_java', True):
        pass
    raise RuntimeError('未找到 Java %d+，请在设置中指定或开启自动下载' % major)
    return download_java(major, progress)

