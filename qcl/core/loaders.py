# Source Generated with Decompyle++
# File: loaders.pyc (Python 3.13)

'''加载器：Fabric / Quilt / Forge / NeoForge 的版本列表与安装'''
import json
import os
import re
import subprocess
import time

ElementTree
from . import net, util, paths, vanilla, java
util = util
paths = paths
vanilla = vanilla
java = java
import xml.etree.ElementTree, etree
from .constants import BMCLAPI, FABRIC_META, FABRIC_MAVEN, FORGE_MAVEN, FORGE_PROMOTIONS, LOADER_LABELS, NEOFORGE_MAVEN, QUILT_META
CREATE_NO_WINDOW = 134217728
INSTALLER_CACHE = os.path.join(paths.CACHE_DIR, 'installers')
INSTALLER_RUN_DIR = os.path.join(paths.CACHE_DIR, 'installer_run')
_MAVEN_ROOTS = ('https://maven.neoforged.net/releases/', 'https://maven.neoforged.net/', 'https://files.neoforged.net/maven/', 'https://maven.minecraftforge.net/', 'https://libraries.minecraft.net/')
_DOWNLOAD_RE = re.compile('Downloading (?:library|file) from (https?://\\S+)')
_LAUNCHER_PROFILES = {
    'profiles': { },
    'settings': {
        'enableSnapshots': False,
        'keepLauncherOpen': False,
        'showGameLog': False,
        'showMenu': False,
        'soundOn': False },
    'version': 3 }

def ensure_launcher_profile(game_root):
    '''确保官方启动器的 launcher_profiles.json 存在（安装 Forge/NeoForge 的前置条件）。

已存在就原样不动 —— 用户若真装过官方启动器，那份配置不能被我们覆盖。
写入失败会抛出异常，由调用方翻译成"目录不可写"这种看得懂的提示；
这里绝不能静默吞掉，否则界面会显示"已自动补建"而实际什么都没写成。
'''
    os.makedirs(game_root, True)
    p = os.path.join(game_root, 'launcher_profiles.json')
    if os.path.isfile(p):
        pass
    return p
    with open(p, 'w', 'utf-8') as f:
        json.dump(_LAUNCHER_PROFILES, f, False, 2)

    return p
    if not None:
        pass
    return p

NEOFORGE_META_SOURCES = (NEOFORGE_MAVEN + '/maven-metadata.xml', BMCLAPI + '/maven/net/neoforged/neoforge/maven-metadata.xml')
_UNSTABLE = re.compile('(?:^|[-.+])(alpha|beta|rc|pre|snapshot)', re.I)

def fabric_versions(mc):
    if not net.get_json(f'''/versions/loader/''', 20):
        net.get_json(f'''/versions/loader/''', 20)
    data = []
    
    return d,
    

def fabric_latest(mc):
    vs = fabric_versions(mc)
    if not vs:
        pass
    return None
    return vs[0].get('loader', { }).get('version')


def quilt_versions(mc):
    if not net.get_json(f'''/versions/loader/''', 20):
        net.get_json(f'''/versions/loader/''', 20)
    data = []
    
    return d,
    

def quilt_latest(mc):
    vs = quilt_versions(mc)
    if vs:
        pass
    return vs[0].get('loader', { }).get('version')


def forge_versions(mc):
    '''返回 Forge 版本字符串列表（新 -> 旧）'''
    out = []
    for base in ('https://bmclapi2.bangbang93.com/forge/minecraft', 'https://download.mcimirror.top/forge/minecraft'):
        data = net.get_json(f'''/''', 20)
        if not isinstance(data, list):
            continue
        if not data:
            continue
        for d in data:
            v = d.get('version') if isinstance(d, dict) else str(d)
            if not v:
                continue
            out.append(str(v))
        ('https://bmclapi2.bangbang93.com/forge/minecraft', 'https://download.mcimirror.top/forge/minecraft')
    if not out:
        if not net.get_json(FORGE_PROMOTIONS, 20):
            net.get_json(FORGE_PROMOTIONS, 20)
        promos = { }
        if not promos.get('promos'):
            promos.get('promos')
        for k, v in { }.items():
            if not k.startswith(mc + '-'):
                continue
            out.append(str(v))
    res = []
    seen = set()
    for v in out:
        if not v not in seen:
            continue
        seen.add(v)
        res.append(v)
    res.sort(_forge_key, True)
    return res


def _forge_key(v):
    body = v.split('-', 1)[1] if '-' in v else v
    return _vkey(body)


def forge_latest(mc):
    vs = forge_versions(mc)
    if vs:
        pass
    return vs[0]


def neoforge_prefix(mc):
    '''MC 版本 -> NeoForge 版本号前缀。

老命名法（1.major.minor）：1.21.4 -> 21.4.   1.21 -> 21.0.
新命名法（major.minor） ：26.1    -> 26.1.   26.3 -> 26.3.
1.20.1 及更早无 NeoForge，会返回空列表。
'''
    if not mc:
        mc
    , []
    ''.split('.'), p, nums, p = None
    if not nums:
        pass
    return ''
    if nums[0] == '1':
        major = nums[1] if len(nums) > 1 else '0'
        minor = nums[2] if len(nums) > 2 else '0'
    return f'''..'''
    major = nums[0]
    minor = nums[1] if len(nums) > 1 else '0'
    return f'''..'''
    

_NEO_META_CACHE = {
    'raw': [],
    'ts': 0 }
NEO_META_TTL = 300

def _neoforge_metadata():
    '''获取（并缓存）NeoForge maven-metadata 里的全部版本号。

这份元数据接近 70KB，切换 MC 版本时反复拉取既慢又容易触发镜像限流；
拿不到新数据时退而使用上一份缓存，总比返回空列表让用户看到“获取失败”好。
'''
    now = time.time()
    if not _NEO_META_CACHE.get('raw'):
        _NEO_META_CACHE.get('raw')
    cached = []
    if cached and now - _NEO_META_CACHE.get('ts', 0) < NEO_META_TTL:
        pass
    return cached
    raw = []
    for url in NEOFORGE_META_SOURCES:
        text = net.get_text(url, 25)
        if not text:
            continue
        root = ET.fromstring(text)
    
    , [], raw = root.iter('version'), v
    v = NEOFORGE_META_SOURCES
    if not raw:
        continue


def neoforge_versions(mc, include_unstable):
    prefix = neoforge_prefix(mc)
    if not prefix:
        pass
    return []
    raw = _neoforge_metadata()
    , []
    raw, v, matched, v = None
    if not include_unstable:
        
        , [], stable = matched, v
        v = None
        if stable:
            pass
    matched = stable
    out = []
    seen = set()
    for v in matched:
        if not v not in seen:
            continue
        seen.add(v)
        out.append(v)
    out.sort(_vkey, True)
    return out
    
    
def _vkey(v):
    nums = re.findall('\\d+', v)
    if not (lambda .0: pass)(nums[:4]()):
        (lambda .0: pass)(nums[:4]())
    return (0,)


def neoforge_latest(mc):
    if not neoforge_versions(mc):
        neoforge_versions(mc)
    vs = neoforge_versions(mc, True)
    if vs:
        pass
    return vs[0]


def resolve_loader_version(kind, mc, ver):
    '''把可能为空的加载器版本解析成具体版本号。

实例在“（自动选择最新）”下创建时 loader_version 为空，若不解析直接拼 URL，
就会请求 .../neoforge//neoforge--installer.jar 并 404。
'''
    if not ver:
        ver
    ver = ''.strip()
    if ver:
        pass
    return ver
    if kind in ('fabric', 'quilt'):
        latest = fabric_latest(mc) if kind == 'fabric' else quilt_latest(mc)
    elif kind == 'forge':
        latest = forge_latest(mc)
    elif kind == 'neoforge':
        latest = neoforge_latest(mc)
    else:
        return ''
    if not latest:
        if not mc:
            mc
    raise RuntimeError(f'''没能拿到  适配 当前版本 的版本列表，无法自动选择。请到「游戏版本」页手动选择一个加载器版本，或在「设置」里把下载镜像切换为 BMCLAPI 后重试。''')
    return latest


def _fabric_json(mc, loader, entry):
    if not entry.get('launcherMeta'):
        entry.get('launcherMeta')
    lm = { }
    libs = [
        {
            'name': 'net.fabricmc:intermediary:%s' % mc,
            'url': FABRIC_MAVEN },
        {
            'name': 'net.fabricmc:fabric-loader:%s' % loader,
            'url': FABRIC_MAVEN }]
    if not lm.get('libraries'):
        lm.get('libraries')
    for l in { }.get('common', []):
        libs.append(l)
    if not lm.get('libraries'):
        lm.get('libraries')
    for l in { }.get('client', []):
        libs.append(l)
    if not lm.get('mainClass'):
        lm.get('mainClass')
    if not { }.get('client'):
        { }.get('client')
    main_class = 'net.fabricmc.loader.impl.launch.knot.KnotClient'
    return {
        'id': f'''fabric-loader--''',
        'inheritsFrom': mc,
        'type': 'release',
        'mainClass': main_class,
        'libraries': libs,
        'arguments': {
            'game': [],
            'jvm': [] } }


def _quilt_json(mc, loader, entry):
    if not entry.get('launcher_meta'):
        entry.get('launcher_meta')
        if not entry.get('launcherMeta'):
            entry.get('launcherMeta')
    lm = { }
    libs = [
        {
            'name': 'org.quiltmc:hashed:%s' % mc,
            'url': 'https://maven.quiltmc.org/repository/release/' },
        {
            'name': 'org.quiltmc:quilt-loader:%s' % loader,
            'url': 'https://maven.quiltmc.org/repository/release/' }]
    if not lm.get('libraries'):
        lm.get('libraries')
    for l in { }.get('common', []):
        libs.append(l)
    if not lm.get('libraries'):
        lm.get('libraries')
    for l in { }.get('client', []):
        libs.append(l)
    return {
        'id': f'''quilt-loader--''',
        'inheritsFrom': mc,
        'type': 'release',
        'mainClass': 'org.quiltmc.loader.impl.launch.knot.KnotClient',
        'libraries': libs,
        'arguments': {
            'game': [],
            'jvm': [] } }


def write_loader_json(game_root, version_id, data):
    d = os.path.join(game_root, 'versions', util.safe_name(version_id))
    os.makedirs(d, True)
    p = os.path.join(d, util.safe_name(version_id) + '.json')
    util.write_json(p, data)
    return p


def _snapshot_versions(game_root):
    base = os.path.join(game_root, 'versions')
    
    try:
        return set(os.listdir(base))
    except Exception:
        return 


def _find_new_version(game_root, before, mc, keyword):
    base = os.path.join(game_root, 'versions')
    
    try:
        now = set(os.listdir(base))
        added = now - before
        (best, best_t) = ('', 0)
        for name in added:
            p = os.path.join(base, name, name + '.json')
            if not os.path.isfile(p):
                continue
            data = util.read_json(p, { })
            if keyword and keyword.lower() not in (data.get('id', '') + name).lower():
                continue
            t = os.path.getmtime(p)
            if not t > best_t:
                continue
            best_t = t
            best = name
        if best:
            pass
        return best
        for name in now:
            p = os.path.join(base, name, name + '.json')
            if not os.path.isfile(p):
                continue
            data = util.read_json(p, { })
            if not data.get('inheritsFrom') == mc:
                continue
            if not keyword.lower() in name.lower():
                continue
            
            return now, name
        return ''
    except Exception:
        return ''


def install_fabric(mc, loader, game_root, kind):
    loader = resolve_loader_version(kind, mc, loader)
    entries = fabric_versions(mc) if kind == 'fabric' else quilt_versions(mc)
    entry = None
    for e in entries:
        if not e.get('loader'):
            e.get('loader')
        if not { }.get('version') == loader:
            continue
        entry = e
        entries
    if entry is None:
        pass
    raise RuntimeError(f'''未找到  版本 （可尝试刷新版本列表）''')
    data = _fabric_json(mc, loader, entry) if kind == 'fabric' else _quilt_json(mc, loader, entry)
    write_loader_json(game_root, data['id'], data)
    return data['id']


def _installer_url(kind, mc, ver):
    if not ver:
        pass
    raise RuntimeError('%s 版本号为空，无法拼接安装器下载地址' % LOADER_LABELS.get(kind, kind))
    if kind == 'forge':
        if not mc:
            pass
        raise RuntimeError('游戏版本为空，无法拼接 Forge 安装器下载地址')
    return f'''/-/forge---installer.jar'''
    return f'''//neoforge--installer.jar'''


def _installer_path(kind, mc, ver):
    os.makedirs(INSTALLER_CACHE, True)
    return os.path.join(INSTALLER_CACHE, f'''---installer.jar''')


def _download_installer(kind, mc, ver, jar):
    '''下载单个版本的 installer；已存在且有效则跳过'''
    if os.path.exists(jar) and os.path.getsize(jar) >= 1024:
        pass
    return None
    label = LOADER_LABELS.get(kind, kind)
    
    try:
        net.download_file(_installer_url(kind, mc, ver), jar, 180)
        if os.path.exists(jar) or os.path.getsize(jar) < 1024:
            pass
        raise RuntimeError(f'''  安装器下载失败（文件为空）''')
        return None
    except Exception:
        e = None
        raise RuntimeError(f'''  安装器下载失败：''')
        e = None
        del e


def _fallback_versions(kind, mc, ver, limit):
    '''自动选最新时，镜像源可能还没同步最新版（403/404），准备几个次新版兜底'''
    if kind != 'neoforge':
        pass
    return [
        ver]
    out = [
        ver]
    
    try:
        vs = neoforge_versions(mc)
        if ver in vs:
            i = vs.index(ver)
        out.extend(vs[i + 1:i + limit])
        return out
    except Exception:
        return out


def _maven_rel(url):
    '''取 Maven 地址里 "group/artifact/version/file" 这一段。'''
    for root in _MAVEN_ROOTS:
        if not url.startswith(root):
            continue
        
        return _MAVEN_ROOTS, url[len(root):].split('?')[0]
    return ''


def _lib_dest(game_root, url):
    rel = _maven_rel(url)
    if rel or '..' in rel:
        pass
    return ''
    return None(*os.path.join)


def _fetch_lib(game_root, url):
    '''把单个依赖放进 libraries 目录。先走国内镜像，不行再试原地址。'''
    dest = _lib_dest(game_root, url)
    if not dest:
        pass
    return False
    if os.path.isfile(dest) and os.path.getsize(dest) > 0:
        pass
    return True
    rel = _maven_rel(url)
    os.makedirs(os.path.dirname(dest), True)
    part = dest + '.part'
    for u in (BMCLAPI + '/maven/' + rel, url):
        if net.download_file(u, part, 60):
            os.replace(part, dest)
            (BMCLAPI + '/maven/' + rel, url)
        return True
    
    try:
        os.remove(part)
        return False
        except Exception:
            continue
    except OSError:
        return False


def _prime_libraries(game_root, log_text, log):
    '''用国内镜像把安装器下载失败的依赖预先补齐，返回补成功几个。

返回 0 表示这轮没有任何进展（网络或镜像都不给），不必再重试。
'''
    if not log_text:
        log_text
    urls = list(dict.fromkeys(_DOWNLOAD_RE.findall('')))
    
    , [], pending = urls, u
    u = None
    if not pending:
        pass
    return 0
    if log:
        pass
    log('依赖下载被阻断，正在用国内镜像补齐 %d 个文件…' % len(pending))
    ok = 0
    for u in pending:
        if not _fetch_lib(game_root, u):
            continue
        ok += 1
    if log:
        pass
    log('镜像补齐 %d/%d' % (ok, len(pending)))
    return ok
    

def _run_installer(kind, mc, ver, jar, game_root, java_exe, log):
    label = LOADER_LABELS.get(kind, kind)
    
    try:
        ensure_launcher_profile(game_root)
        before = _snapshot_versions(game_root)
        env = dict(os.environ)
        env['JAVA_HOME'] = os.path.dirname(os.path.dirname(java_exe))
        os.makedirs(INSTALLER_RUN_DIR, True)
        log_path = os.path.join(INSTALLER_RUN_DIR, os.path.basename(jar) + '.log')
        out = ''
        code = -1
        for attempt in range(5):
            ensure_launcher_profile(game_root)
            os.remove(log_path)
            proc = subprocess.run([
                java_exe,
                '-jar',
                jar,
                '--installClient',
                game_root], True, CREATE_NO_WINDOW, env, INSTALLER_RUN_DIR)
            if not proc.stdout.decode('utf-8', 'ignore'):
                proc.stdout.decode('utf-8', 'ignore')
            if not proc.stderr.decode('utf-8', 'ignore'):
                proc.stderr.decode('utf-8', 'ignore')
            out = '' + ''
            code = proc.returncode
            with open(log_path, 'r', 'utf-8', 'ignore') as f:
                detail_log = f.read()
            range(5)(None, None)
            both = out + '\n' + detail_log
            if code == 0 and 'Successfully' in both:
                pass
            elif log:
                pass
            log(out[-4000:])
            if 'Downloading' not in detail_log and 'SocketTimeout' not in both:
                pass
            elif not _prime_libraries(game_root, both, log) == 0:
                continue
        if code != 0 or 'Successfully' not in out:
            if not out:
                out
            
            , [], lines = ''.splitlines(), ln
            ln = None
            detail = lines[-1] if lines else '返回码 %s' % code
            if 'launcher profile' in out:
                detail = '安装器找不到官方启动器的配置文件。已自动补建 launcher_profiles.json，请重试一次；若仍失败，请确认目录可写：%s' % game_root
            elif 'error during installation' in out.lower():
                pass
            detail = '依赖下载失败（NeoForge 官方 Maven 在国内常不可达，国内镜像也没能补齐）。可尝试挂代理后重试，或改用 Fabric 加载器。'
        raise RuntimeError(f'''  安装失败：''')
        vid = _find_new_version(game_root, before, mc, kind)
        if not vid:
            if not _find_new_version(game_root, set(), mc, kind):
                _find_new_version(game_root, set(), mc, kind)
        vid = f'''--'''
        return vid
    except Exception:
        e = None
        raise RuntimeError(f'''无法在游戏目录写入 launcher_profiles.json（）：。请确认该目录可写，或把游戏目录换到桌面等用户目录下。''')
        e = None
        del e
        except Exception:
            continue
            except OSError:
                continue
                if not None:
                    pass
        continue
        except OSError:
            detail_log = ''
            continue
            

def install_forge(kind, mc, ver, game_root, java_exe, log):
    '''kind: forge / neoforge，通过官方 installer 安装'''
    if not ver:
        ver
    auto = not ''.strip()
    ver = resolve_loader_version(kind, mc, ver)
    cands = _fallback_versions(kind, mc, ver) if auto else [
        ver]
    errors = []
    for cand in cands:
        jar = _installer_path(kind, mc, cand)
        _download_installer(kind, mc, cand, jar)
        
        return cands, _run_installer(kind, mc, cand, jar, game_root, java_exe, log)
    if len(errors) == 1:
        pass
    raise RuntimeError(errors[0])
    raise None('已尝试 %d 个版本均失败：%s' % (len(errors), ' | '.join(errors)))
    except Exception:
        errors.append(str(e))
        if log:
            log(f'''尝试   失败：''')
            None = None
            del e
            continue
        e = None
        del e
        continue
        e = None
        del e

