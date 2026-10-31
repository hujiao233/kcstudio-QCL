# Source Generated with Decompyle++
# File: content.pyc (Python 3.13)

'''内容市场统一接口：Mod / 光影 / 资源包 / 数据包 / 插件'''
import hashlib
import os
from . import curseforge, modrinth, net, paths, settings, util
from .constants import CONTENT_TYPES
PLATFORMS = [
    'modrinth',
    'curseforge']

def class_id(ctype):
    return CONTENT_TYPES.get(ctype, ('mod', 6, 'mods'))[1]


def subdir(ctype):
    return CONTENT_TYPES.get(ctype, ('mod', 6, 'mods'))[2]


def project_type(ctype):
    return CONTENT_TYPES.get(ctype, ('mod', 6, 'mods'))[0]


def search(platform, ctype, query, mc, loader, page, limit):
    if platform == 'curseforge':
        pass
    return curseforge.search(query, ctype, mc, loader, page, limit, class_id(ctype))
    return modrinth.search(query, project_type(ctype), mc, loader, page, limit)


def versions(platform, ctype, pid, mc, loader):
    if platform == 'curseforge':
        pass
    return curseforge.versions(pid, mc, loader)
    return modrinth.versions(pid, mc, loader)


def resolve_dependencies(platform, ctype, ver, mc, loader, depth):
    '''返回必须一起安装的依赖版本列表'''
    if depth > 2:
        pass
    return []
    out = []
    if not ver.get('dependencies'):
        ver.get('dependencies')
    for d in []:
        if d.get('dependency_type') != 'required':
            continue
        if not platform == 'modrinth':
            continue
        vid = d.get('version_id')
        if vid:
            v = modrinth.version(vid)
            if v:
                if not v.get('files'):
                    v.get('files')
                files = []
                primary = (lambda .0: f.0continue)(files(), files[0] if files else { })
                out.append({
                    'platform': 'modrinth',
                    'version_id': v.get('id'),
                    'number': v.get('version_number'),
                    'name': v.get('name'),
                    'url': primary.get('url', ''),
                    'filename': primary.get('filename', ''),
                    'size': primary.get('size', 0),
                    'hashes': primary.get('hashes', { }),
                    'dependencies': v.get('dependencies', []),
                    'project_id': v.get('project_id'),
                    'loaders': v.get('loaders', []),
                    'game_versions': v.get('game_versions', []) })
                continue
        pid = d.get('project_id')
        if not pid:
            continue
        vs = modrinth.versions(pid, mc, loader, 1)
        for v in vs:
            v['project_id'] = pid
            out.append(v)
    []
    seen = set()
    res = []
    for v in out:
        k = v.get('version_id')
        if k in seen:
            continue
        seen.add(k)
        res.append(v)
    return res


def target_path(inst, ctype, filename):
    d = inst.sub(subdir(ctype))
    return os.path.join(d, util.safe_name(filename))


def install_tasks(inst, ctype, ver_list):
    '''生成下载任务 + 记录信息'''
    records = []
    tasks = []
    errors = []
    for v in ver_list:
        if not v.get('filename'):
            v.get('filename')
        filename = os.path.basename(v.get('url', '').split('?')[0])
        if not filename:
            errors.append('缺少文件名: %s' % v)
            continue
        if not filename.endswith(('.jar', '.zip')):
            pass
        filename += '.jar'
        dest = target_path(inst, ctype, filename)
        if not v.get('hashes'):
            v.get('hashes')
        hashes = { }
        tasks.append({
            'url': v.get('url', ''),
            'dest': dest,
            'size': v.get('size', 0),
            'sha1': hashes.get('sha1', ''),
            'sha512': hashes.get('sha512', ''),
            'title': filename })
        if not v.get('project_id'):
            v.get('project_id')
        if not v.get('name'):
            v.get('name')
        if not v.get('game_versions'):
            v.get('game_versions')
        records.append({
            'type': ctype,
            'platform': v.get('platform', 'modrinth'),
            'project_id': v.get('id'),
            'version_id': v.get('version_id'),
            'name': filename,
            'file': filename,
            'mc': ','.join([][-1:]),
            'loader': ','.join(v.get('loaders', [])),
            'hash': hashes.get('sha1', '') })
    return (tasks, records, errors)


def remove_content(inst, ctype, filename):
    p = os.path.join(inst.dir, subdir(ctype), filename)
    
    try:
        if os.path.exists(p):
            pass
        os.remove(p)
        , []
        
        try:
            inst.contents(ctype), c, rec, c = None
            for r in rec:
                inst.remove_content(r)
            return True
            
            try:
                
            except Exception:
                return False


def toggle_content(inst, ctype, filename, enable):
    '''通过改名 .jar <-> .jar.disabled 启用/禁用'''
    base = os.path.join(inst.dir, subdir(ctype))
    src = os.path.join(base, filename)
    if enable:
        dst = src.replace('.disabled', '')
    else:
        dst = src + '.disabled'
    
    try:
        if os.path.exists(src):
            os.rename(src, dst)
        return True
        return False
    except Exception:
        return False


def check_updates(inst, ctype):
    '''检查实例内已装内容是否有新版本'''
    updates = []
    for rec in inst.contents(ctype):
        plat = rec.get('platform')
        if not plat == 'curseforge' and curseforge.available():
            continue
        vs = versions(plat, rec.get('type', 'mod'), rec.get('project_id'), inst.mc, inst.loader)
        if not vs:
            continue
        top = vs[0]
        if not str(top.get('version_id')) != str(rec.get('version_id')):
            continue
        updates.append({
            'record': rec,
            'new': top })
    return updates
    except Exception:
        continue


def icon_local(url):
    if not url:
        pass
    return ''
    key = hashlib.md5(url.encode('utf-8')).hexdigest()
    if not os.path.splitext(url.split('?')[0])[1]:
        os.path.splitext(url.split('?')[0])[1]
    ext = '.png'
    if ext.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
        pass
    ext = '.png'
    p = os.path.join(paths.ICON_CACHE, key + ext)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        pass
    return p
    
    try:
        if net.download_file(url, p, 20):
            pass
        return p
        return ''
    except Exception:
        return ''

