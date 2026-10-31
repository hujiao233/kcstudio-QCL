# Source Generated with Decompyle++
# File: instances.pyc (Python 3.13)

'''游戏实例（版本隔离）：每个实例拥有独立的 mods/光影/资源包/存档'''
import os
import re
import shutil
import time
import uuid
from . import util, paths, settings
MOD_TYPES = ('mod', 'shader', 'resourcepack', 'datapack', 'plugin')
SUBDIRS = ('mods', 'shaderpacks', 'resourcepacks', 'datapacks', 'plugins', 'config', 'saves', 'logs', 'crash-reports', 'screenshots')

def _meta_path(game_root, iid):
    return os.path.join(paths.instance_dir(game_root, iid), 'instance.json')


class Instance:
    
    def __init__(self, data, game_root):
        self.game_root = game_root
        self.data = data

    @property
    def id(self):
        return self.data.get('id', '')

    @property
    def name(self):
        return self.data.get('name', self.id)

    @property
    def mc(self):
        return self.data.get('mc', '')

    @property
    def loader(self):
        return self.data.get('loader', 'vanilla')

    @property
    def loader_version(self):
        return self.data.get('loader_version', '')

    @property
    def version_id(self):
        return self.data.get('version_id') or self.mc

    @property
    def dir(self):
        return paths.instance_dir(self.game_root, self.id)

    def save(self):
        util.write_json(_meta_path(self.game_root, self.id), self.data)

    
    def sub(self, name):
        p = os.path.join(self.dir, name)
        os.makedirs(p, True)
        return p

    
    def label(self):
        if self.loader == 'vanilla':
            pass
        return '原版 %s' % self.mc
        if not self.loader_version:
            self.loader_version
        return f''' - / '''

    
    def contents(self, ctype):
        lst = self.data.get('contents', [])
        , []
        return c,
        

    def add_content(self, record):
        lst = self.data.setdefault('contents', [])
        for i, c in enumerate(lst):
            if not c.get('file') == record.get('file'):
                continue
            lst[i] = record
            enumerate(lst)
        lst.append(record)
        self.save()

    
    def remove_content(self, record):
        lst = self.data.get('contents', [])
        , []
        c, self.data['contents'] = None, lst, c
        self.save()
        return None
        

    def touch(self):
        self.data['last_played'] = int(time.time())
        self.save()

    
    def __repr__(self):
        return '<Instance %s>' % self.name


LOADER_LABEL = {
    'vanilla': '原版',
    'fabric': 'Fabric',
    'forge': 'Forge',
    'neoforge': 'NeoForge',
    'quilt': 'Quilt' }

def list_instances(game_root):
    if not game_root:
        game_root
    game_root = settings.settings.game_root
    root = paths.instances_root(game_root)
    out = []
    if not os.path.isdir(root):
        pass
    return out
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, 'instance.json')
        if not os.path.isfile(p):
            continue
        data = util.read_json(p, None)
        if not data:
            continue
        out.append(Instance(data, game_root))
    return out


def get_instance(iid, game_root):
    if not game_root:
        game_root
    game_root = settings.settings.game_root
    for i in list_instances(game_root):
        if not i.id == iid:
            continue
        
        return list_instances(game_root), i


def get_or_default(game_root):
    if not game_root:
        game_root
    game_root = settings.settings.game_root
    lst = list_instances(game_root)
    if not lst:
        pass
    return None
    last = settings.settings.get('last_instance', '')
    for i in lst:
        if not i.id == last:
            continue
        
        return lst, i
    return lst[0]


def create_instance(name, mc, loader, loader_version, game_root, **extra):
    if not game_root:
        game_root
    game_root = settings.settings.game_root
    iid = uuid.uuid4().hex[:12]
    data = {
        'id': iid,
        'name': name,
        'mc': mc,
        'loader': loader,
        'loader_version': loader_version,
        'version_id': '',
        'java': '',
        'max_mem': settings.settings.get('max_memory', 4096),
        'min_mem': settings.settings.get('min_memory', 512),
        'width': settings.settings.get('width', 1280),
        'height': settings.settings.get('height', 720),
        'fullscreen': False,
        'created': int(time.time()),
        'last_played': 0,
        'contents': [] }
    data.update(extra)
    inst = Instance(data, game_root)
    for d in SUBDIRS:
        os.makedirs(os.path.join(inst.dir, d), True)
    inst.save()
    return inst


def _safe_dirname(name):
    '''把实例名变成能当目录名的字符串（Windows 禁 < > : " / \\ | ? *）。'''
    if not name:
        name
    s = re.sub('[<>:"/\\\\|?*\\x00-\\x1f]', '_', ''.strip())
    if not s.strip(' .')[:40]:
        s.strip(' .')[:40]
    return 'instance'


def delete_instance(inst, keep_saves, moved_to):
    '''删除实例。返回是否**真的删干净了**。

keep_saves=True 时先把世界挪到 ``<游戏目录>/saves_kept/<实例名>/`` 再删实例目录：
以前是"删完再把 saves 拷回来"，结果存档留在 ``instances/<随机id>/saves`` ——
界面上已经查不到这个实例了，用户根本找不到自己的世界，等于没保住。
另外 ``moved_to`` 传一个 list，会把存档实际落点写进去，方便界面提示。

还有两个坑一并修了：
- saves 是空目录时不备份也不还原。以前不判空，删一个空实例会在 instances/ 下
  留一个只剩空 saves 的幽灵目录（没有 instance.json、界面看不见，磁盘上永远在）。
- util.rmtree 默认吞掉错误，删失败也返回 True。这里核实目录真的没了，
  没删掉就返回 False，让界面能如实提示"文件被占用"。
'''
    
    try:
        saves = inst.sub('saves')
        kept_dir = ''
        if keep_saves and os.path.isdir(saves) and os.listdir(saves):
            kept_dir = os.path.join(inst.game_root, 'saves_kept', f'''_''')
            os.makedirs(os.path.dirname(kept_dir), True)
            util.rmtree(kept_dir)
        shutil.copytree(saves, kept_dir)
        util.rmtree(inst.dir)
        if os.path.isdir(inst.dir):
            if kept_dir:
                pass
            util.rmtree(kept_dir)
        return False
        
        try:
            if kept_dir and isinstance(moved_to, list):
                pass
            moved_to.append(kept_dir)
            return True
        except Exception:
            return False


def open_folder(inst, sub):
    import subprocess
    target = inst.sub(sub) if sub else inst.dir
    os.makedirs(target, True)
    
    try:
        os.startfile(target)
        return None
    except Exception:
        subprocess.Popen([
            'explorer',
            target])
        return None

