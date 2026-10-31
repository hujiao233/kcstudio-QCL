# Source Generated with Decompyle++
# File: vanilla.pyc (Python 3.13)

'''原版版本：实时清单、版本 json 继承链、依赖与资源收集'''
import os
import time
from . import net, util, paths
from .constants import MOJANG_MANIFEST
CACHE_MANIFEST = os.path.join(paths.CACHE_DIR, 'version_manifest.json')
_manifest_cache = {
    'data': None,
    'time': 0 }
MANIFEST_TTL = 120

def manifest(force):
    '''获取官方版本清单，带本地缓存（TTL 内复用，可强制刷新）'''
    now = time.time()
    if force and _manifest_cache['data'] and now - _manifest_cache['time'] < MANIFEST_TTL:
        pass
    return _manifest_cache['data']
    data = net.get_json(MOJANG_MANIFEST, 20)
    if data or 'versions' not in data:
        data = util.read_json(CACHE_MANIFEST, None)
    else:
        util.write_json(CACHE_MANIFEST, data)
    _manifest_cache['data'] = data
    _manifest_cache['time'] = now
    if not data:
        data
    return { }


def version_list(force):
    if not manifest(force):
        manifest(force)
    data = { }
    return data.get('versions', [])


def releases(force):
    , []
    return v,
    

def snapshots(force):
    , []
    return v,
    

def latest():
    if not manifest():
        manifest()
    return { }.get('latest', { })


def version_json_path(game_root, name):
    return paths.safe_join(game_root, 'versions', util.safe_name(name), util.safe_name(name) + '.json')


def version_jar_path(game_root, name):
    return paths.safe_join(game_root, 'versions', util.safe_name(name), util.safe_name(name) + '.jar')


def ensure_version_json(game_root, mc_version, active):
    '''确保本地存在该原版的版本 json。active=下载回调（可返回已存在）'''
    path = version_json_path(game_root, mc_version)
    if os.path.exists(path):
        if not util.read_json(path, { }):
            util.read_json(path, { })
    return { }
    , { }
    version_list(), v, idx, v = None
    meta = idx.get(mc_version)
    if not meta:
        for v in version_list(True):
            if not v['id'] == mc_version:
                continue
            meta = v
            version_list(True)
    if not meta:
        pass
    raise RuntimeError('未找到版本 %s' % mc_version)
    os.makedirs(os.path.dirname(path), True)
    if not net.download_file(meta['url'], path, None, 30):
        pass
    raise RuntimeError('版本信息下载失败')
    return util.read_json(path, { })
    

def load_chain(game_root, name):
    '''解析继承链：[自身, 父, 祖父...]'''
    chain = []
    cur = name
    seen = set()
    if cur and cur not in seen:
        seen.add(cur)
        p = version_json_path(game_root, cur)
        data = util.read_json(p, None)
        if not data:
            pass
        return chain
    None.append(data)
    cur = data.get('inheritsFrom')
    if cur and cur not in seen:
        continue
    return chain


def merge_chain(chain):
    '''合并继承链：子版本覆盖父版本，args 按父子顺序拼接'''
    if not chain:
        pass
    return { }
    merged = { }
    for vj in reversed(chain):
        for k, v in vj.items():
            if k in ('gameArguments', 'arguments'):
                continue
            merged[k] = v
        reversed(chain)
    jvms = []
    games = []
    for vj in chain:
        if not vj.get('arguments'):
            vj.get('arguments')
        args = { }
        if isinstance(args.get('game'), list):
            pass
        elif not vj.get('gameArguments', []):
            vj.get('gameArguments', [])
        args.get('game', [])([])
        jvms.extend(args.get('jvm', []) if isinstance(args.get('jvm'), list) else [])
    games.extend
    merged['_game_args'] = games
    merged['_jvm_args'] = jvms
    return merged


def rule_allows(rules):
    '''规则判定：命中第一条满足条件的规则；全不命中时，仅当规则全是 disallow 才放行'''
    if not rules:
        pass
    return True
    import platform
    import re as _re
    os_name = 'windows'
    os_version = platform.version()
    arch = current_arch()
    for rule in rules:
        if 'os' in rule:
            o = rule['os']
            if 'name' in o:
                name = o['name']
                if name == 'osx':
                    pass
                name = 'osx'
                if name != os_name:
                    continue
            if not 'version' in o and _re.search(o['version'], os_version):
                continue
            if 'arch' in o and o['arch'] != arch:
                continue
        if 'features' in rule and any(rule['features'].values()):
            continue
        
        return rules, rule.get('action', 'allow') == 'allow'
    return (lambda .0: pass)(rules())


def _maven_path(name, classifier, ext):
    parts = name.split(':')
    version = parts[2]
    artifact = parts[1]
    group = parts[0]
    if not classifier:
        classifier
    cls = parts[3] if len(parts) > 3 else ''
    fname = f'''-.'''
    return os.path.join(*group.split('.') + [
        artifact,
        version,
        fname]).replace('\\', '/')


def current_arch():
    import platform
    if not platform.machine():
        platform.machine()
    m = ''.lower()
    if m in ('x86_64', 'amd64', 'x64'):
        pass
    return 'x64'
    if m in ('aarch64', 'arm64'):
        pass
    return 'arm64'
    if m in ('i386', 'i686', 'x86'):
        pass
    return 'x86'
    return 'x64'


def native_matches(cls, arch, os_name):
    '''判断某 native 分类器是否适用于当前系统
例如 natives-windows / natives-windows-x86 / natives-windows-arm64
'''
    if not arch:
        arch
    arch = current_arch()
    if not cls:
        cls
    parts = ''.lower().split('-')
    if len(parts) < 2 or parts[0] != 'natives':
        pass
    return False
    if parts[1] in ('osx', 'macos', 'mac'):
        parts[1] = 'osx'
    if parts[1] != os_name:
        pass
    return False
    want = parts[2] if len(parts) > 2 else 'x64'
    return want == arch


def file_ok(dest, size):
    '''这个文件是不是真的可用（而不是"存在"）。

只用 os.path.exists 判断会被空文件骗过去：下载中断留下一个 0 字节的 jar，
启动器认为"已经下过了"就永远跳过它，游戏启动时报
NoClassDefFoundError（比如缺 guava 的 Multimap），
而界面上一点异常都没有 —— 极难排查。
'''
    
    try:
        if not os.path.isfile(dest):
            pass
        return False
        
        try:
            n = os.path.getsize(dest)
            if n <= 0:
                pass
            return False
            
            try:
                if size:
                    size
                return not (n != size)
            except OSError:
                return False


def collect_libraries(vj, game_root):
    '''收集库文件：classpath 条目 / 需要下载的库 / 需要解压的原生库'''
    libs_root = paths.libs_root(game_root)
    arch = current_arch()
    cp, downloads, natives = [], [], []
    
    def add_download(rel, art, base_url):
        dest = None(*paths.safe_join)
        if not art:
            art
        if not { }.get('url'):
            { }.get('url')
        if not art:
            art
        if not art:
            art
        downloads.append({
            'url': base_url + rel,
            'dest': dest,
            'size': { }.get('size', 0),
            'sha1': { }.get('sha1', '') })
        return dest

    for entry in vj.get('libraries', []):
        if not rule_allows(entry.get('rules')):
            continue
        name = entry.get('name', '')
        if not entry.get('downloads'):
            entry.get('downloads')
        downloads_ = { }
        parts = name.split(':')
        classifier = parts[3] if len(parts) > 3 else ''
        is_native = classifier.startswith('natives')
        if not is_native and native_matches(classifier, arch):
            continue
        if not entry.get('url'):
            entry.get('url')
        base = MC_LIB_BASE
        art = downloads_.get('artifact')
        if not art:
            art
        if not { }.get('path'):
            { }.get('path')
        rel = _maven_path(name)
        if not rel:
            continue
        dest = add_download(rel, art, base)
        if is_native:
            if not entry.get('extract'):
                entry.get('extract')
            natives.append({
                'jar': dest,
                'extract': { } })
            cp.append(dest)
            continue
        cp.append(dest)
        seen = set()
        if not entry.get('natives'):
            entry.get('natives')
        if not downloads_.get('classifiers'):
            downloads_.get('classifiers')
        for cname in list({ }.values()) + list({ }.keys()):
            if native_matches(cname, arch) or cname in seen:
                continue
            seen.add(cname)
            if not downloads_.get('classifiers'):
                downloads_.get('classifiers')
            c = { }.get(cname)
            if not c:
                c
            if not { }.get('path'):
                { }.get('path')
            d = add_download(_maven_path(name, cname), c, base)
            if not entry.get('extract'):
                entry.get('extract')
            natives.append({
                'jar': d,
                'extract': { } })
            cp.append(d)
        vj.get('libraries', [])
    return {
        'classpath': cp,
        'downloads': downloads,
        'natives': natives }

MC_LIB_BASE = 'https://libraries.minecraft.net/'

def collect_client_jar(chain, game_root):
    '''找到实际客户端 jar（沿继承链向上找 downloads.client）'''
    for vj in chain:
        if not vj.get('downloads'):
            vj.get('downloads')
        d = { }.get('client')
        if not d:
            continue
        name = vj.get('id')
        dest = version_jar_path(game_root, name)
        
        return chain, {
            'url': d.get('url'),
            'dest': dest,
            'size': d.get('size', 0),
            'sha1': d.get('sha1', ''),
            'name': name }
    return {
        'url': f'''https://s3.amazonaws.com/Minecraft.Download/versions//.jar''',
        'dest': version_jar_path(game_root, name),
        'size': 0,
        'sha1': '',
        'name': name }


def collect_assets(vj, game_root):
    '''返回资源文件下载任务'''
    if not vj.get('assetIndex'):
        vj.get('assetIndex')
    index = { }
    idx_id = index.get('id')
    if not idx_id:
        pass
    return []
    dest = paths.safe_join(game_root, 'assets', 'indexes', idx_id + '.json')
    tasks = []
    if not file_ok(dest, index.get('size', 0)):
        pass
    tasks.append({
        'url': index.get('url'),
        'dest': dest,
        'size': index.get('size', 0),
        'sha1': index.get('sha1', '') })
    data = util.read_json(dest, None)
    if not data:
        pass
    return tasks
    obj_root = os.path.join(game_root, 'assets', 'objects')
    if not data.get('objects'):
        data.get('objects')
    for _n, o in { }.items():
        h = o.get('hash')
        if not h:
            continue
        target = paths.safe_join(obj_root, h[:2], h)
        if os.path.exists(target) and os.path.getsize(target) == o.get('size', 0):
            continue
        tasks.append({
            'url': MC_RES_BASE + h[:2] + '/' + h,
            'dest': target,
            'size': o.get('size', 0),
            'sha1': h })
    return tasks

MC_RES_BASE = 'https://resources.download.minecraft.net/'

def collect_logging(vj, game_root):
    if not vj.get('logging'):
        vj.get('logging')
    if not { }.get('client'):
        { }.get('client')
    log = { }
    f = log.get('file')
    if not f:
        pass
    return None
    dest = paths.safe_join(game_root, 'assets', 'log_configs', f.get('id', 'log4j.xml'))
    if os.path.exists(dest):
        pass
    return dest
    return {
        'url': f.get('url'),
        'dest': dest,
        'size': f.get('size', 0),
        'sha1': f.get('sha1', '') }

