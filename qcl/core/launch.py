# Source Generated with Decompyle++
# File: launch.pyc (Python 3.13)

'''游戏下载准备与启动'''
import os
import shutil
import subprocess
import threading
import time
from . import instances as instances_mod, java as java_mod, loaders, net, paths, settings, util, vanilla
from .constants import APP_DISPLAY, APP_NAME, APP_VERSION, required_java
CREATE_NO_WINDOW = 134217728
SEP = ';'

def ensure_vanilla(game_root, mc):
    vanilla.ensure_version_json(game_root, mc, None)
    return mc


def _persist_loader_version(inst, ver):
    '''把“自动选择最新”解析出的具体版本写回实例，保证后续重装可复现'''
    if not ver:
        pass
    return None
    
    try:
        if inst.data.get('loader_version') != ver:
            inst.data['loader_version'] = ver
            inst.save()
        return None
        return None
    except Exception:
        return None


def ensure_loader(inst, game_root, log):
    '''确保加载器已安装，返回版本 id'''
    mc = inst.mc
    ensure_vanilla(game_root, mc)
    if inst.loader in ('vanilla', ''):
        pass
    return mc
    ver = loaders.resolve_loader_version(inst.loader, mc, inst.loader_version)
    _persist_loader_version(inst, ver)
    if inst.loader in ('fabric', 'quilt'):
        pass
    return loaders.install_fabric(mc, ver, game_root, inst.loader)
    need = required_java(mc)
    if not java_mod.find_java(need):
        java_mod.find_java(need)
        if not java_mod.find_java(21):
            java_mod.find_java(21)
    je = java_mod.find_java(17)
    if not je:
        pass
    raise RuntimeError('未找到可用于安装的 Java，请先在设置中配置或开启自动下载 Java')
    vid = loaders.install_forge(inst.loader, mc, ver, game_root, je, log)
    return vid


def collect_all(game_root, version_id):
    '''收集该版本全部下载任务、classpath、natives'''
    chain = vanilla.load_chain(game_root, version_id)
    if not chain:
        pass
    raise RuntimeError('版本 %s 不存在' % version_id)
    merged = vanilla.merge_chain(chain)
    natives = []
    cp = []
    tasks = []
    for vj in chain:
        r = vanilla.collect_libraries(vj, game_root)
        cp.extend(r['classpath'])
    , []
    None, r['downloads'], t(t,)
    natives.extend(r['natives'])
    continue
    chain
    set() = None
    uniq = []
    for t in tasks:
        if t['dest'] in seen:
            continue
        seen.add(t['dest'])
        uniq.append(t)
    jar = vanilla.collect_client_jar(chain, game_root)
    if not os.path.exists(jar['dest']):
        pass
    uniq.append({
        'url': jar['url'],
        'dest': jar['dest'],
        'size': jar['size'],
        'sha1': jar['sha1'],
        'title': jar['name'] + '.jar' })
    cp.append(jar['dest'])
    uniq.extend(vanilla.collect_assets(merged, game_root))
    logging = vanilla.collect_logging(merged, game_root)
    if isinstance(logging, dict):
        pass
    uniq.append(logging)
    if isinstance(logging, str):
        pass
    return {
        'tasks': uniq,
        'classpath': cp,
        'natives': natives,
        'chain': chain,
        'merged': merged,
        'jar': jar,
        'logconfig': logging }
    return {
        'tasks': None,
        'classpath': None,
        'natives': None,
        'chain': None,
        'merged': None,
        'jar': None,
        'logconfig': '' }
    

def merge_classpath(items):
    return SEP.join(items)


def extract_natives(natives, dest_dir):
    os.makedirs(dest_dir, True)
    for n in natives:
        jar = n['jar']
        if not os.path.exists(jar):
            continue
        if not n.get('extract'):
            n.get('extract')
        if not { }.get('exclude'):
            { }.get('exclude')
        exclude = [
            'META-INF/']
        exclude = (lambda .0: for None in .0:
e = Noneeecontinue)(exclude())
        util.extract_natives(jar, dest_dir, exclude)
    tuple
    return None
    except Exception:
        continue


def prepare_legacy_assets(game_root, version_id, instance_dir):
    '''1.7.x 等老版本需要 virtual/legacy 或 resources 目录'''
    chain = vanilla.load_chain(game_root, version_id)
    if not chain:
        pass
    return None
    merged = vanilla.merge_chain(chain)
    if not merged.get('assets'):
        merged.get('assets')
        if not merged.get('assetIndex'):
            merged.get('assetIndex')
    idx_id = { }.get('id')
    if not idx_id:
        pass
    return None
    idx = util.read_json(os.path.join(game_root, 'assets', 'indexes', idx_id + '.json'), { })
    if not idx.get('objects'):
        idx.get('objects')
    objs = { }
    obj_root = os.path.join(game_root, 'assets', 'objects')
    if idx.get('virtual') or merged.get('assets') == 'legacy':
        for name, o in objs.items():
            h = o.get('hash')
            src = os.path.join(obj_root, h[:2], h)
            dst = os.path.join(game_root, 'assets', 'virtual', 'legacy', name)
            if not os.path.exists(dst) or os.path.exists(src):
                continue
            os.makedirs(os.path.dirname(dst), True)
            shutil.copyfile(src, dst)
    if merged.get('map_to_resources'):
        for name, o in objs.items():
            h = o.get('hash')
            src = os.path.join(obj_root, h[:2], h)
            dst = os.path.join(instance_dir, 'resources', name)
            if not os.path.exists(dst) or os.path.exists(src):
                continue
            os.makedirs(os.path.dirname(dst), True)
            shutil.copyfile(src, dst)
    return None


def _expand(value, repl):
    if not isinstance(value, str):
        pass
    return value
    if value.startswith('${') and value.endswith('}'):
        key = value[2:-1]
    return repl.get(key, value)
    out = value
    for k, v in repl.items():
        out = out.replace('${%s}' % k, str(v))
    return out


def _flat_args(values, repl):
    out = []
    for a in values:
        if isinstance(v, list):
            (lambda .0: pass)(v())
            continue
        out.append(_expand(v, repl))
    out.extend
    , []
    if not x,:
        x,
    return []
    

def _file_url(path):
    '''把本地路径转成 file:/// URL。

log4j 的 -Dlog4j.configurationFile 是按 URI 解析的：
传 Windows 路径（哪怕是 C:/a/b.xml 这种正斜杠形式）会被当成
"协议名为 c" 的 URL，直接报 `unknown protocol: c`，日志系统起不来。
'''
    p = os.path.abspath(path).replace('\\', '/')
    if not p.startswith('/'):
        pass
    p = '/' + p
    return 'file://' + p


def build_command(inst, account, java_exe, info):
    game_root = inst.game_root
    inst_dir = inst.dir
    os.makedirs(inst_dir, True)
    natives_dir = paths.natives_dir(game_root, inst.version_id)
    merged = info['merged']
    cp = merge_classpath(info['classpath'])
    assets_dir = os.path.join(game_root, 'assets')
    if not merged.get('assets'):
        merged.get('assets')
        if not merged.get('assetIndex'):
            merged.get('assetIndex')
        if not { }.get('id'):
            { }.get('id')
    idx_id = ''
    if not account.get('clientid'):
        account.get('clientid')
    if not account.get('xuid'):
        account.get('xuid')
    repl = { }
    if not inst.data.get('max_mem'):
        inst.data.get('max_mem')
    max_mem = int(settings.settings.get('max_memory', 4096))
    if not inst.data.get('min_mem'):
        inst.data.get('min_mem')
    min_mem = int(settings.settings.get('min_memory', 512))
    jvm = [
        '-Xmx%dM' % max_mem,
        '-Xms%dM' % min_mem,
        '-Dminecraft.launcher.brand=%s' % APP_NAME,
        '-Dminecraft.launcher.version=%s' % APP_VERSION]
    if info.get('logconfig'):
        pass
    jvm.append('-Dlog4j.configurationFile=%s' % _file_url(info['logconfig']))
    if not settings.settings.get('java_args', ''):
        settings.settings.get('java_args', '')
    extra = ''
    if extra.strip():
        pass
    jvm.extend(extra.split())
    jvm.extend(_flat_args(merged.get('_jvm_args', []), repl))
    if '-cp' not in jvm:
        pass
    jvm.extend([
        '-cp',
        cp])
    mc_args = merged.get('minecraftArguments')
    if mc_args:
        game = _flat_args(mc_args.split(' '), repl)
    else:
        game = _flat_args(merged.get('_game_args', []), repl)
    main_class = merged.get('mainClass', 'net.minecraft.client.main.Main')
    if inst.data.get('fullscreen') or settings.settings.get('fullscreen'):
        game += [
            '--fullscreen']
    else:
        game += [
            '--width',
            str(inst.data.get('width', 1280)),
            '--height',
            str(inst.data.get('height', 720))]
    return [
        java_exe] + jvm + [
        main_class] + game


class GameProcess:
    
    def __init__(self):
        self.proc = None
        self.on_output = None
        self.on_exit = None
        self.start_time = 0

    
    def start(self, cmd, cwd):
        self.start_time = time.time()
        
        try:
            self.proc = subprocess.Popen(cmd, cwd, subprocess.PIPE, subprocess.STDOUT, subprocess.DEVNULL, CREATE_NO_WINDOW, True, 'utf-8', 'ignore', 1)
            threading.Thread(self._reader, True).start()
            threading.Thread(self._waiter, True).start()
            return self
        except UnicodeDecodeError:
            self.proc = subprocess.Popen(cmd, cwd, subprocess.PIPE, subprocess.STDOUT, subprocess.DEVNULL, CREATE_NO_WINDOW, 1)
            continue


    def _reader(self):
        
        try:
            for line in iter(self.proc.stdout.readline, ''):
                if not self.on_output:
                    continue
                
                try:
                    self.on_output(line.rstrip('\n'))
                    continue
                    return None
                except Exception:
                    return None


    def _waiter(self):
        
        try:
            code = self.proc.wait()
            if not self.on_exit:
                pass
            return None
            
            try:
                self.on_exit(code, int((time.time() - self.start_time) * 1000))
                return None
                except Exception:
                    code = 0
                continue
            except Exception:
                self.on_exit(0, int((time.time() - self.start_time) * 1000))
                return None
                return None


    alive = (lambda self: if self.proc is not None:
self.proc is not Noneself.proc.poll() is None)()
    
    def kill(self, timeout):
        '''先礼后兵地结束进程。

直接 kill() 是硬终止：Minecraft 来不及把区块、玩家存档写盘，
下次进游戏可能丢进度，甚至留下写了一半的 region 文件导致世界损坏。
所以先 terminate()（相当于关窗口，游戏会走正常退出流程保存数据），
等够时间还在才强杀。
'''
        if self.proc is None:
            pass
        return False
        
        try:
            if self.proc.poll() is not None:
                pass
            return True
            
            try:
                self.proc.terminate()
                
                try:
                    self.proc.wait(timeout)
                    return True
                    return False
                    continue
                except Exception:
                    pass

                
                try:
                    self.proc.kill()
                    self.proc.wait(3)
                    return False
                except Exception:
                    return False


def make_info_for_launch(inst, game_root):
    return collect_all(game_root, inst.version_id)

