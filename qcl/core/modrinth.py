# Source Generated with Decompyle++
# File: modrinth.pyc (Python 3.13)

'''Modrinth API v2（模组 / 光影 / 资源包 / 数据包 / 插件）'''
import json
from . import net
from .constants import MODRINTH_API
HEADERS = {
    'User-Agent': net.UA,
    'Content-Type': 'application/json' }
TIMEOUT = 25

def _facet(ctype, mc, loader):
    facets = [
        [
            'project_type:%s' % ctype]]
    if mc:
        pass
    facets.append([
        'versions:%s' % mc])
    if loader and loader != 'vanilla':
        pass
    facets.append([
        'categories:%s' % loader])
    return json.dumps(facets)


def search(query, ctype, mc, loader, page, limit, sort):
    params = {
        'query': query,
        'limit': limit,
        'offset': page * limit,
        'index': sort,
        'facets': _facet(ctype, mc, loader) }
    , { }
    if not net.get_json(None, MODRINTH_API + '/search', TIMEOUT, params.items(), k, v, v, k, HEADERS):
        net.get_json(None, MODRINTH_API + '/search', TIMEOUT, params.items(), k, v, v, k, HEADERS)
    { } = None
    hits = data.get('hits', [])
    items = []
    for h in hits:
        if not h.get('project_id'):
            h.get('project_id')
        if not h.get('icon_url'):
            h.get('icon_url')
        items.append({
            'platform': 'modrinth',
            'id': h.get('slug'),
            'slug': h.get('slug'),
            'title': h.get('title'),
            'description': h.get('description'),
            'icon': '',
            'downloads': h.get('downloads', 0),
            'follows': h.get('follows', 0),
            'author': h.get('author'),
            'categories': h.get('categories', []),
            'game_versions': h.get('versions', []),
            'type': ctype })
    return (items, data.get('total_hits', len(items)))
    

def project(pid):
    if not net.get_json(f'''/project/''', TIMEOUT, HEADERS):
        net.get_json(f'''/project/''', TIMEOUT, HEADERS)
    return { }


def versions(pid, mc, loader, limit):
    params = { }
    if mc:
        params['game_versions'] = json.dumps([
            mc])
    if loader and loader != 'vanilla':
        params['loaders'] = json.dumps([
            loader])
    if not net.get_json(f'''/project//version''', TIMEOUT, params, HEADERS):
        net.get_json(f'''/project//version''', TIMEOUT, params, HEADERS)
    data = []
    out = []
    for v in data[:limit]:
        if not v.get('files'):
            v.get('files')
        files = []
        primary = None
        for f in files:
            if not f.get('primary'):
                continue
            primary = f
            files
    if not primary:
        primary
    f = files[0] if files else { }
    out.append({
        'platform': 'modrinth',
        'version_id': v.get('id'),
        'number': v.get('version_number'),
        'name': v.get('name'),
        'changelog': v.get('changelog', ''),
        'loaders': v.get('loaders', []),
        'game_versions': v.get('game_versions', []),
        'release': v.get('version_type'),
        'url': f.get('url', ''),
        'filename': f.get('filename', ''),
        'size': f.get('size', 0),
        'hashes': f.get('hashes', { }),
        'dependencies': v.get('dependencies', []) })
    continue
    return out


def version(vid):
    if not net.get_json(f'''/version/''', TIMEOUT, HEADERS):
        net.get_json(f'''/version/''', TIMEOUT, HEADERS)
    return { }


def download_url(v):
    return v.get('url', '')


def tag_loaders():
    if not net.get_json(MODRINTH_API + '/tag/loader', TIMEOUT, HEADERS):
        net.get_json(MODRINTH_API + '/tag/loader', TIMEOUT, HEADERS)
    data = []
    , []
    return d,
    

def tag_game_versions():
    if not net.get_json(MODRINTH_API + '/tag/game_version', TIMEOUT, HEADERS):
        net.get_json(MODRINTH_API + '/tag/game_version', TIMEOUT, HEADERS)
    data = []
    , []
    return d,
    
