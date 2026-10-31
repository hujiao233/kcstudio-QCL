# Source Generated with Decompyle++
# File: updater.pyc (Python 3.13)

'''自动更新：检测主机发布的新版本 -> 下载 -> 自替换重启；以及发布新版本'''
import os
import re
import subprocess
import sys
import time
from . import net, paths, util
from .constants import APP_NAME, APP_VERSION, DEFAULT_HOST
UPDATE_DIRNAME = 'updates'
CREATE_NO_WINDOW = 134217728

def version_key(v):
    if not v:
        v
    nums = re.findall('\\d+', '0')
    if not (lambda .0: pass)(nums[:4]()):
        (lambda .0: pass)(nums[:4]())
    return (0,)


def newer(a, b):
    return version_key(a) > version_key(b)


def applied_version():
    '''客户端已应用过的最新版本号。

为什么需要它：APP_VERSION 是编译时写死的，更新机制不碰它。
发布者填 1.0.1 打包，但包里代码仍是 1.0.0 —— 客户端更新完重启，
拿写死的 1.0.0 去和 manifest 的 1.0.1 比，永远"有更新"，弹窗无限循环。
所以更新成功后把 manifest 的版本记到这里（存在 data/settings.json，
更新时不覆盖 data 目录，能跨更新存活），比较时以它为准。
'''
    settings = settings
    # import  # [decompiler] module name lost
    if not settings.settings.get('applied_version', ''):
        settings.settings.get('applied_version', '')
    return ''.strip()


def effective_version():
    '''真正该拿来和主机比较的版本：写死版本 与 已应用版本 取较大者。'''
    av = applied_version()
    if av and newer(av, APP_VERSION):
        pass
    return av
    return APP_VERSION


def mark_applied(version):
    '''记录"已应用过这个版本"，防止更新后重复弹提示。'''
    if not version:
        pass
    return None
    settings = settings
    # import  # [decompiler] module name lost
    if newer(version, applied_version()):
        settings.settings.set('applied_version', version)
    return None


def update_dir():
    d = os.path.join(paths.APP_DIR, UPDATE_DIRNAME)
    os.makedirs(d, True)
    return d


def local_manifest():
    if not util.read_json(os.path.join(update_dir(), 'manifest.json'), None):
        util.read_json(os.path.join(update_dir(), 'manifest.json'), None)
    return { }


def check(progress):
    '''向主机查询是否有新版本；返回 manifest 或 {}'''
    settings = settings
    # import  # [decompiler] module name lost
    base = settings.settings.host_url
    if not (base or base == DEFAULT_HOST) and _self_host():
        pass
    return { }
    
    try:
        if not net.get_json(base + '/api/update/manifest', 6):
            net.get_json(base + '/api/update/manifest', 6)
        data = { }
        if data or 'version' not in data:
            pass
        return { }
        if not newer(data.get('version', '0'), effective_version()):
            pass
        return { }
        return data
    except Exception:
        return 


def _self_host():
    settings = settings
    # import  # [decompiler] module name lost
    return bool(settings.settings.get('is_host', False))


def download_update(manifest, dest, progress):
    settings = settings
    # import  # [decompiler] module name lost
    base = settings.settings.host_url
    if not manifest.get('url'):
        manifest.get('url')
    url = '/download/' + manifest.get('file', '')
    if url.startswith('/'):
        pass
    url = base + url
    return net.download_file(url, dest, manifest.get('size', 0), progress, 120)


def publish(version, notes, required, src_dir, progress):
    '''打包当前目录为新版本并写入 manifest（在发布者的电脑上执行）'''
    if not version:
        version
    version = ''.strip()
    if not version:
        pass
    raise ValueError('版本号不能为空')
    if not newer(version, APP_VERSION):
        pass
    raise ValueError('版本号需大于当前版本 %s' % APP_VERSION)
    if not src_dir:
        src_dir
    src_dir = paths.APP_DIR
    out_dir = update_dir()
    name = f'''-.zip'''
    out = os.path.join(out_dir, name)
    util.make_zip(src_dir, out, ('.minecraft', 'data', 'updates', '__pycache__', 'logs', '.git'))
    manifest = {
        'version': version,
        'file': name,
        'url': '/download/' + name,
        'sha256': util.sha256_file(out),
        'size': os.path.getsize(out),
        'notes': notes,
        'required': bool(required),
        'time': int(time.time()) }
    util.write_json(os.path.join(out_dir, 'manifest.json'), manifest)
    mark_applied(version)
    return manifest


def _bat_path():
    import tempfile
    return os.path.join(tempfile.gettempdir(), '%s_Updater.bat' % APP_NAME)


def write_updater_bat(stage, dst, app):
    bat = _bat_path()
    content = f'''@echo off\nchcp 65001 >nul\nset "SRC="\nset "DST="\nset "APP="\nping -n 3 127.0.0.1 >nul\nxcopy "%SRC%\\*" "%DST%\\" /E /Y /Q /I >nul\nstart "" "%APP%"\nrmdir /s /q "%SRC%"\ndel "%~f0"\n'''
    with open(bat, 'w', 'utf-8') as f:
        f.write(content)

    return bat
    if not None:
        pass
    return bat


def apply_update(manifest, zip_path):
    '''解压到暂存目录并准备替换脚本，返回 bat 路径'''
    stage = os.path.join(paths.TMP_DIR, 'update_%s' % manifest.get('version', '0'))
    util.rmtree(stage)
    os.makedirs(stage, True)
    util.unzip(zip_path, stage)
    app = os.path.join(paths.APP_DIR, APP_NAME + '.exe')
    entries = os.listdir(stage)
    inner = os.path.join(stage, entries[0]) if len(entries) == 1 and os.path.isdir(os.path.join(stage, entries[0])) and APP_NAME + '.exe' in os.listdir(os.path.join(stage, entries[0])) else stage
    return write_updater_bat(inner, paths.APP_DIR, app)


def run_updater(bat):
    subprocess.Popen([
        'cmd',
        '/c',
        bat], CREATE_NO_WINDOW, True, os.path.dirname(bat))


def do_update(manifest, progress):
    '''完整更新流程：下载 -> 校验 -> 生成脚本 -> 交给脚本替换'''
    if not manifest.get('file'):
        manifest.get('file')
    zip_path = os.path.join(paths.TMP_DIR, 'update.zip')
    os.makedirs(paths.TMP_DIR, True)
    if not download_update(manifest, zip_path, progress):
        pass
    return False
    if manifest.get('sha256') and util.sha256_file(zip_path) != manifest['sha256']:
        pass
    return False
    bat = apply_update(manifest, zip_path)
    run_updater(bat)
    mark_applied(manifest.get('version'))
    return True


def self_replace_and_restart(stage_in):
    '''（备用）直接自替换，供脚本缺失时使用'''
    app = sys.executable
    time.sleep(1)
    
    try:
        util.rmtree(os.path.join(paths.APP_DIR, '_internal'))
        for root, _dirs, files in os.walk(stage_in):
            rel = os.path.relpath(root, stage_in)
            target = paths.APP_DIR if rel == '.' else os.path.join(paths.APP_DIR, rel)
            os.makedirs(target, True)
            for f in files:
                with open(os.path.join(root, f), 'rb') as a:
                    with open(os.path.join(target, f), 'wb') as b:
                        b.write(a.read())
                    files(None, None)
                    os.walk(stage_in)(None, None)
                    continue
                    continue
                    subprocess.Popen([
                        app], paths.APP_DIR)
                    return None
                    except Exception:
                        continue
                        if not None:
                            pass

    continue
    if not None:
        pass
    continue
    except Exception:
        continue

