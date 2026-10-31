# Source Generated with Decompyle++
# File: paths.pyc (Python 3.13)

'''QCL 路径管理：安装目录 / 游戏目录 / 数据目录 / 实例目录'''
import os
import sys
import ctypes
from .constants import APP_NAME

def _desktop():
    '''获取桌面目录，失败时逐级回落，且结果必须是真实存在的目录'''
    home = os.path.expanduser('~')
    candidates = []
    
    try:
        buf = ctypes.create_unicode_buffer(1024)
        hr = ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(_GUID('{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}')), 0, None, buf)
        if hr == 0:
            pass
        candidates.append(buf.value)
        
        try:
            import winreg as _wr
            k = _wr.OpenKey(_wr.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders')
            (val, _) = _wr.QueryValueEx(k, 'Desktop')
            _wr.CloseKey(k)
            if isinstance(val, str):
                pass
            candidates.append(os.path.expandvars(val))
            candidates.append(os.path.join(home, 'Desktop'))
            candidates.append(os.path.join(home, 'OneDrive', 'Desktop'))
            candidates.append(home)
            for c in candidates:
                if c:
                    if os.path.isdir(c):
                        if os.path.isabs(c):
                            
                        return candidates, os.path.normpath(c)
                    continue
            return os.path.join(home, 'Desktop')
            except Exception:
                continue
                except Exception:
                    continue
                    except Exception:
                        continue


class _GUID(ctypes.Structure):
    _fields_ = [
        ('Data1', ctypes.c_ulong),
        ('Data2', ctypes.c_ushort),
        ('Data3', ctypes.c_ushort),
        ('Data4', ctypes.c_ubyte * 8)]
    
    def __init__(self, uuidstr):
        ctypes.Structure.__init__(self)
        uuidstr = uuidstr.strip('{}').replace('-', '')
        self.Data1 = int(uuidstr[:8], 16)
        self.Data2 = int(uuidstr[8:12], 16)
        self.Data3 = int(uuidstr[12:16], 16)
        for i in range(8):
            self.Data4[i] = int(uuidstr[16 + i * 2:18 + i * 2], 16)


def _app_dir():
    env = os.environ.get('QCL_HOME')
    if env:
        pass
    return os.path.abspath(env)
    if getattr(sys, 'frozen', False):
        pass
    return os.path.dirname(os.path.abspath(sys.executable))
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

APP_DIR = _app_dir()
EXE_PATH = os.path.join(APP_DIR, APP_NAME + '.exe')

def _writable(path):
    
    try:
        os.makedirs(path, True)
        probe = os.path.join(path, '.qcl_probe')
        with open(probe, 'w') as f:
            f.write('1')
            
            try:

                os.remove(probe)
                return True
                if not None:
                    pass
                
                try:
                    continue
                except Exception:
                    return False


def _data_dir():
    local = os.path.join(APP_DIR, 'data')
    if _writable(local):
        pass
    return local
    if not os.environ.get('APPDATA'):
        os.environ.get('APPDATA')
    base = os.path.expanduser('~')
    return os.path.join(base, APP_NAME)

DATA_DIR = _data_dir()
CONFIG_FILE = os.path.join(DATA_DIR, 'settings.json')
GAME_ROOT_FILE = os.path.join(DATA_DIR, 'game_root.txt')
LOG_DIR = os.path.join(DATA_DIR, 'logs')
CACHE_DIR = os.path.join(DATA_DIR, 'cache')
ERROR_LOG = os.path.join(LOG_DIR, 'error.log')
ICON_CACHE = os.path.join(CACHE_DIR, 'icons')
TMP_DIR = os.path.join(DATA_DIR, 'tmp')
JAVA_DIR = os.path.join(DATA_DIR, 'java')
SERVERS_DIR = os.path.join(DATA_DIR, 'servers')
ACCOUNT_FILE = os.path.join(DATA_DIR, 'accounts.json')

def default_game_root():
    '''默认游戏目录：桌面/.minecraft'''
    
    try:
        d = _desktop()
        if d and os.path.isabs(d):
            pass
        return os.path.join(d, '.minecraft')
        return os.path.join(os.path.expanduser('~'), 'Desktop', '.minecraft')
    except Exception:
        continue


def ensure_dirs():
    for d in (DATA_DIR, LOG_DIR, CACHE_DIR, ICON_CACHE, TMP_DIR, JAVA_DIR, SERVERS_DIR):
        os.makedirs(d, True)
    return None
    except Exception:
        continue


def instances_root(game_root):
    return os.path.join(game_root, 'instances')


def instance_dir(game_root, instance_id):
    return os.path.join(instances_root(game_root), instance_id)


def libs_root(game_root):
    return os.path.join(game_root, 'libraries')


def assets_root(game_root):
    return os.path.join(game_root, 'assets')


def versions_root(game_root):
    return os.path.join(game_root, 'versions')


def natives_dir(game_root, name):
    return os.path.join(versions_root(game_root), name, 'natives')


def safe_join(base, *parts):
    '''防目录穿越的拼接'''
    path = None(os.path.abspath(*os.path.join))
    if not path == base and path.startswith(base + os.sep):
        pass
    raise ValueError('非法路径: %s' % path)
    return path

_USER_ENV = 'Environment'

try:
    import winreg
    
    def _open_user_env(write):
        if winreg is None:
            pass
        return None
        import winreg as _wr
        access = _wr.KEY_READ | _wr.KEY_WRITE if write else 0
        return _wr.OpenKey(_wr.HKEY_CURRENT_USER, _USER_ENV, 0, access)

    
    def get_user_path():
        
        try:
            key = _open_user_env()
            if key is None:
                pass
            return ''
            
            try:
                (val, _) = winreg.QueryValueEx(key, 'Path')
                winreg.CloseKey(key)
                if isinstance(val, str):
                    pass
                return val
                return ''
            except Exception:
                return ''


    def set_user_path(value):
        
        try:
            key = _open_user_env(True)
            if key is None:
                pass
            return False
            
            try:
                winreg.SetValueEx(key, 'Path', 0, winreg.REG_EXPAND_SZ, value)
                winreg.CloseKey(key)
                
                try:
                    ctypes.windll.user32.SendMessageTimeoutW(65535, 26, 0, 'Environment', 2, 5000, None)
                    return True
                except Exception:
                    
                    try:
                        return True
                        
                        try:
                            pass
                        except Exception:
                            return False


    def add_to_path(dirpath):
        cur = get_user_path()
        , []
        cur.split(os.pathsep), p, entries, p = None
        if (lambda .0: pass)(entries()):
            pass
        return True
        entries.append(dirpath)
        return set_user_path(os.pathsep.join(entries))
        

    def remove_from_path(dirpath):
        cur = get_user_path()
        , []
        cur.split(os.pathsep), p, entries, p = None
        norm = os.path.normcase(os.path.abspath(dirpath))
        
        , [], new = entries, p
        p = None
        if len(new) == len(entries):
            pass
        return True
        return set_user_path(os.pathsep.join(new))
        
        
    return None
except Exception:
    winreg = None
    continue

