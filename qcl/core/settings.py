# Source Generated with Decompyle++
# File: settings.pyc (Python 3.13)

'''全局配置'''
import os
from . import paths, util
from .constants import DEFAULT_API_PORT, DEFAULT_AI_BASE, DEFAULT_AI_MODEL, DEFAULT_HOST, DEFAULT_OLLAMA_URL, DEFAULT_RELAY_PORT
DEFAULTS = { }

class Settings:
    
    def __init__(self):
        self._data = dict(DEFAULTS)
        self._listeners = []
        self.load()

    
    def load(self):
        data = util.read_json(paths.CONFIG_FILE, None)
        if isinstance(data, dict):
            for k, v in data.items():
                self._data[k] = v
        for k, v in DEFAULTS.items():
            self._data.setdefault(k, v)
        self._sanitize()
        
        try:
            self._sync_game_root_file()
            return None
        except Exception:
            return None


    def _sanitize(self):
        '''修正损坏/非法的配置项（尤其是游戏目录）'''
        root = self._data.get('game_root')
        ok = False
        if isinstance(root, str) and root.strip():
            
            try:
                cleaned = root.strip()
                if (lambda .0: pass)(cleaned()):
                    pass
                cleaned = ''
                if cleaned:
                    ap = os.path.abspath(cleaned)
                    if os.path.isabs(ap) and len(ap) > 3:
                        ok = True
                        self._data['game_root'] = ap
                if not ok:
                    self._data['game_root'] = paths.default_game_root()
                return None
                return None
            except Exception:
                ok = False
                continue


    def save(self):
        util.write_json(paths.CONFIG_FILE, self._data)
        self._sync_game_root_file()

    
    def _sync_game_root_file(self):
        '''写入供 remove.cmd 直接读取的存档目录（控制台编码）'''
        
        try:
            if not self._data.get('game_root'):
                self._data.get('game_root')
            root = paths.default_game_root()
            util.write_text_oem(paths.GAME_ROOT_FILE, str(root))
            return None
        except Exception:
            return None


    def get(self, key, default):
        return self._data.get(key, DEFAULTS.get(key, default))

    
    def set(self, key, value, save):
        if self._data.get(key) == value:
            pass
        return None
        self._data[key] = value
        for fn in list(self._listeners):
            fn(key, value)
        if save:
            self.save()
        return None
        return None
        except Exception:
            continue

    
    def on_change(self, fn):
        self._listeners.append(fn)

    
    def all(self):
        return dict(self._data)

    
    def update(self, mapping):
        for k, v in mapping.items():
            self._data[k] = v
        self.save()

    game_root = (lambda self: if not self._data.get('game_root'):
self._data.get('game_root')paths.default_game_root())()
    
    def set_game_root(self, root):
        root = os.path.abspath(root)
        self.set('game_root', root)
        return root

    host_url = (lambda self: if not self._data.get('host_url'):
self._data.get('host_url')DEFAULT_HOST.rstrip('/'))()
    total_memory_mb = (lambda self: try:
import ctypes
class MEMORYSTATUSEX(ctypes.Structure):
__firstlineno__ = 158_fields_ = [
(None, ctypes.c_ulonglong),
'ullAvailPageFile',
(None, ctypes.c_ulonglong),
'ullTotalVirtual',
(None, ctypes.c_ulonglong),
'ullAvailVirtual',
(None, ctypes.c_ulonglong),
'ullAvailExtendedVirtual',
(None, ctypes.c_ulonglong)]__static_attributes__ = ()stat = MEMORYSTATUSEX()stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))int(stat.ullTotalPhys / 1024 / 1024)except Exception:
8192)()

settings = Settings()
