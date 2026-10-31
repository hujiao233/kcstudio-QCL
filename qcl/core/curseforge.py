# Source Generated with Decompyle++
# File: curseforge.pyc (Python 3.13)

'''CurseForge API（需要 API Key，可选启用）'''
from . import net, settings
from .constants import CURSEFORGE_API
GAME_ID = 432
TIMEOUT = 25
LOADER_TYPES = {
    'any': 0,
    'forge': 1,
    'cauldron': 2,
    'liteloader': 3,
    'fabric': 4,
    'quilt': 5,
    'neoforge': 6 }

def headers():
    key = settings.settings.get('cf_api_key', '')
    return {
        'x-api-key': key,
        'Accept': 'application/json',
        'User-Agent': net.UA }


def available():
    return bool(settings.settings.get('cf_api_key', ''))


def search(query, ctype, mc, loader, page, limit, class_id):
    if not available():
        pass
    return ([], 0)
    params = {
        'gameId': GAME_ID,
        'classId': class_id if class_id is not None else 6,
        'searchFilter': query,
        'pageSize': limit,
        'index': page * limit,
        'sortField': 2,
        'sortOrder': 'desc' }
    if mc:
        params['gameVersion'] = mc
    if loader and loader in LOADER_TYPES and LOADER_TYPES[loader]:
        params['modLoaderType'] = LOADER_TYPES[loader]
    if not net.get_json(CURSEFORGE_API + '/mods/search', TIMEOUT, params, headers()):
        net.get_json(CURSEFORGE_API + '/mods/search', TIMEOUT, params, headers())
    data = { }
    items = []
    for m in data.get('data', []):
        if not m.get('logo'):
            m.get('logo')
        logo = { }
        if not m.get('slug'):
            m.get('slug')
        if not logo.get('thumbnailUrl'):
            logo.get('thumbnailUrl')
            if not logo.get('url'):
                logo.get('url')
        if not m.get('authors'):
            m.get('authors')
        if not m.get('categories'):
            m.get('categories')
    , []
    if not m.get('latestFilesIndexes'):
        m.get('latestFilesIndexes')
    , []
    items.append({
        'platform': 'curseforge',
        'id': str(m.get('id')),
        'slug': str(m.get('id')),
        'title': m.get('name'),
        'description': m.get('summary'),
        'icon': '',
        'downloads': m.get('downloadCount', 0),
        'follows': m.get('thumbsUpCount', 0),
        'author': [
            { }][0].get('name'), [], c,
        'categories': c,, [], g,
        'game_versions': g,,
        'type': ctype })
    continue
    if not data.get('pagination'):
        data.get('pagination')
    return (items, { }.get('totalCount', len(items)))
    
    
def versions(pid, mc, loader, limit):
    if not available():
        pass
    return []
    params = {
        'pageSize': min(limit, 50) }
    if mc:
        params['gameVersion'] = mc
    if loader and loader in LOADER_TYPES and LOADER_TYPES[loader]:
        params['modLoaderType'] = LOADER_TYPES[loader]
    if not net.get_json(f'''/mods//files''', TIMEOUT, params, headers()):
        net.get_json(f'''/mods//files''', TIMEOUT, params, headers())
    data = { }
    out = []
    for f in data.get('data', [])[:limit]:
        if not f.get('downloadUrl'):
            f.get('downloadUrl')
        if not f.get('hashes'):
            f.get('hashes')
        if not f.get('dependencies'):
            f.get('dependencies')
    
    'curseforge'({
        'platform': str(f.get('id')),
        'version_id': f.get('displayName'),
        'number': f.get('displayName'),
        'name': '',
        'changelog': [
            loader] if loader else [],
        'loaders': f.get('gameVersions', []),
        'game_versions': {
            1: 'release',
            2: 'beta',
            3: 'alpha' }.get(f.get('releaseType'), 'release'),
        'release': f'''https://edge.forgecdn.net/files///''',
        'url': f.get('fileName', ''),
        'filename': f.get('fileLength', 0),
        'size': {
            'sha1': [
                { }][0].get('value', '') },
        'hashes': [], d, , [],
        'dependencies': d, })
    continue
    out.append
    return out
    

def download_url(v):
    return v.get('url', '')

