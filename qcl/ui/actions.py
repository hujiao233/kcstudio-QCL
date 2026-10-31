# Source Generated with Decompyle++
# File: actions.pyc (Python 3.13)

'''共享业务流程：安装内容 / 启动游戏 / 检查更新'''
import os
import subprocess
import time
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QMessageBox, QPushButton, QVBoxLayout
from ..core import auth, content as content_mod, instances as instances_mod, java as java_mod, launch, paths, updater, util, vanilla
from ..core.constants import APP_VERSION, CONTENT_TYPE_LABELS, required_java
from ..core.qtdownload import DownloadItem, run_async
from . import theme

class _GameBridge(QObject):
    __doc__ = '把游戏进程的输出/退出转回主线程。\n\n游戏的 stdout 是在独立线程里读的（launch.GameProcess._reader），\n如果直接把回调当槽用，等于在后台线程里操作 QPlainTextEdit 这类控件。\nQt 明确规定控件只能在 GUI 线程碰，违反后的症状是随机访问违规或界面错乱，\n而且没有任何 Python 报错 —— 极难定位。\n这里统一走 QueuedConnection，把调用排回主线程。\n'
    line = Signal(str)
    exited = Signal(object, object)

_BRIDGES = set()

def install_content(ctx, inst, ctype, vers, with_deps):
    '''把内容（及其依赖）下载并安装到实例'''
    if not inst:
        ctx.toast('请先选择一个游戏实例', 'err')
    return []
    allv = []
    if with_deps:
        for v in list(vers):
            deps = content_mod.resolve_dependencies(v.get('platform', 'modrinth'), ctype, v, inst.mc, inst.loader)
            for d in deps:
                d.setdefault('platform', v.get('platform', 'modrinth'))
            list(vers)
            allv.extend(deps)
    allv.extend(vers)
    for v in allv:
        v.setdefault('platform', 'modrinth')
    (tasks, records, errors) = content_mod.install_tasks(inst, ctype, allv)
    if errors:
        pass
    ctx.toast('部分内容无法解析：' + errors[0], 'err')
    if not tasks:
        pass
    return []
    for r in records:
        inst.add_content(r)
    group = 'ct-%d' % int(time.time() * 1000)
    ctx.dm.add_many(tasks, group)
    ctx.emit('content_changed', inst)
    ctx.dm.wait_group(group, (lambda ok: _content_done(ctx, inst, ctype, group, records)))
    return tasks
    except Exception:
        continue


def _content_done(ctx, inst, ctype, group, records):
    , []
    ctx.dm.items, i, failed, i = None
    if failed:
        for f in failed:
            pass
        , []
        records, r, rec, r = failed
        for r in rec:
            inst.remove_content(r)
        continue
        if not failed[0].error:
            failed[0].error
        ctx.toast('%s 安装失败 %d 个：%s' % (CONTENT_TYPE_LABELS.get(ctype, ctype), len(failed), '未知'), 'err')
    else:
        ctx.toast('%s 安装完成（%d 个文件）' % (CONTENT_TYPE_LABELS.get(ctype, ctype), len(records)), 'ok')
    ctx.emit('content_changed', inst)
    return None
    
    
def _ensure_runtime(ctx, inst, prog, log):
    '''工作线程：确保版本与 Java 就绪，返回 (version_id, java_path)'''
    need = required_java(inst.mc)
    vid = launch.ensure_loader(inst, inst.game_root, log)
    if not inst.data.get('java'):
        inst.data.get('java')
    exe = ''
    if not exe and java_mod.java_version(exe) >= need:
        pass
    exe = ''
    if not exe:
        pass
    exe = java_mod.find_java(need)
    if exe and ctx.settings.get('auto_download_java', True):
        if log:
            pass
        log('未检测到 Java %d，正在自动下载…' % need)
        exe = java_mod.download_java(need, prog)
        if log:
            pass
    log('Java 就绪：%s' % exe)
    return (vid, exe)


def launch_instance(ctx, inst, on_status, on_log, on_exit):
    '''完整启动流程'''
    if not inst:
        ctx.toast('请先创建并选择一个游戏实例', 'err')
    return None
    if not ctx.settings.get('account'):
        ctx.toast('请先登录游戏账号（首页右上角）', 'warn')
    return None
    
    def log(msg):
        if on_log:
            on_log(msg)
        return None

    
    def status(msg, busy):
        if on_status:
            on_status(msg, busy)
        return None

    
    def step1():
        return _ensure_runtime(ctx, inst, (lambda d, t: ctx.set_prog('java', d, t)), (lambda m: ctx.append_log(m)))

    
    def step2(res):
        (vid, java_exe) = res
        if not vid:
            ctx.toast('版本准备失败', 'err')
        return None
        if not java_exe:
            ctx.toast('未找到可用的 Java，请在设置中指定或开启自动下载', 'err')
        return None
        if inst.data.get('version_id') != vid:
            inst.data['version_id'] = vid
        inst.save()
        status('正在检查游戏文件…')
        
        try:
            info = launch.collect_all(inst.game_root, vid)
            
            , [], tasks = info['tasks'], t
            t = None
            group = 'mc-%d' % int(time.time() * 1000)
            if tasks:
                for t in tasks:
                    t.setdefault('title', os.path.basename(t['dest']))
                ctx.dm.add_many(tasks, group)
                ctx.dm.wait_group(group, (lambda ok: step3(ok, info, java_exe, vid)))
            return None
            step3(True, info, java_exe, vid)
            return None
        except Exception:
            e = None
            ctx.toast('版本解析失败：%s' % e, 'err')
            e = None
            del e
            return None
            e = None
            del e
            

    def step3(ok, info, java_exe, vid):
        if not ok:
            ctx.toast('游戏文件下载失败，请检查网络或镜像设置', 'err')
            status('下载失败')
        return None
        status('正在准备原生库…')
        nd = paths.natives_dir(inst.game_root, vid)
        launch.extract_natives(info['natives'], nd)
        
        try:
            launch.prepare_legacy_assets(inst.game_root, vid, inst.dir)
            acc = auth.refresh_if_needed(ctx.settings.get('account'))
            ctx.settings.set('account', acc)
            
            try:
                cmd = launch.build_command(inst, acc, java_exe, info)
                status('正在启动游戏…')
                gp = launch.GameProcess()
                bridge = _GameBridge()
                _BRIDGES.add(bridge)
                bridge.exited.connect((lambda : _BRIDGES.discard(bridge)), Qt.QueuedConnection)
                if log:
                    bridge.line.connect(log, Qt.QueuedConnection)
                    gp.on_output = bridge.line.emit
                if on_exit:
                    pass
                bridge.exited.connect(on_exit, Qt.QueuedConnection)
                gp.on_exit = bridge.exited.emit
                gp.start(cmd, inst.dir)
                ctx.emit('game_started', (inst, gp))
                if log:
                    pass
                log('='.join([
                    ''] * 1) + ' 启动命令：' + ' '.join(cmd[:3]) + ' …')
                inst.touch()
                ctx.emit('instances_changed', None)
                status('游戏运行中', False)
                return None
                except Exception:
                    continue
                    except Exception:
                        e = None
                        ctx.toast('启动参数生成失败：%s' % e, 'err')
                        e = None
                        del e
                        return None
                        e = None
                        del e


    status('正在准备版本…')
    run_async(step1, step2, (lambda e: (ctx.toast('准备失败：%s' % e, 'err'), status('准备失败', False))))


def download_game(ctx, inst, on_done):
    '''仅下载游戏文件（不启动）'''
    
    def step1():
        return _ensure_runtime(ctx, inst, (lambda d, t: ctx.set_prog('java', d, t)), (lambda m: ctx.append_log(m)))

    
    def step2(res):
        (vid, java_exe) = res
        if not vid:
            ctx.toast('版本准备失败', 'err')
        return None
        inst.data['version_id'] = vid
        inst.save()
        ctx.append_log('开始下载 %s 的游戏文件…' % vid)
        
        try:
            info = launch.collect_all(inst.game_root, vid)
            
            , [], tasks = info['tasks'], t
            t = None
            group = 'game-%d' % int(time.time() * 1000)
            if not tasks:
                _game_ready(ctx, inst, info, vid, on_done)
            return None
            for t in tasks:
                t.setdefault('title', os.path.basename(t['dest']))
            ctx.dm.add_many(tasks, group)
            ctx.dm.wait_group(group, (lambda ok: _game_ready(ctx, inst, info, vid, on_done)))
            return None
        except Exception:
            e = None
            ctx.toast('版本解析失败：%s' % e, 'err')
            e = None
            del e
            return None
            e = None
            del e
            

    run_async(step1, step2, (lambda e: ctx.toast('准备失败：%s' % e, 'err')))


def _game_ready(ctx, inst, info, vid, on_done):
    from ..core import paths
    try:
        launch.extract_natives(info['natives'], paths.natives_dir(inst.game_root, vid))
        launch.prepare_legacy_assets(inst.game_root, vid, inst.dir)
        ctx.append_log('%s 的下载与准备已完成' % vid)
        ctx.toast('游戏文件已就绪：%s' % inst.name, 'ok')
        if on_done:
            on_done()
        return None
        return None
    except Exception:
        continue


def open_folder(path):
    
    try:
        os.startfile(path)
        return None
    except Exception:
        subprocess.Popen([
            'explorer',
            path])
        return None
        return None


def check_launcher_update(ctx, parent, silent):
    from ..core import updater as up
    def on_manifest(m):
        if not m:
            if not silent:
                pass
            ctx.toast('当前已是最新版本（%s）' % up.effective_version(), 'ok')
        return None
        dlg = UpdateDialog(ctx, m, parent)
        dlg.exec()

    
    def on_err(e):
        if not silent:
            ctx.toast('无法连接主机：%s' % e, 'warn')
        return None

    run_async((lambda : up.check()), on_manifest, on_err)


class UpdateDialog(QDialog):
    
    def __init__(self, ctx, manifest, parent):
        from ..core import updater as up
        super.__init__(parent)
        self.ctx = ctx
        self.manifest = manifest
        self.setWindowTitle('发现新版本')
        self.resize(420, 260)
        lay = QVBoxLayout(self)
        lay.setSpacing(8)
        t = QLabel(f'''新版本 （当前 ）''')
        t.setStyleSheet('font-size: 16px; font-weight: 700;')
        lay.addWidget(t)
        if not manifest.get('notes'):
            manifest.get('notes')
        notes = QLabel('（暂无更新说明）')
        notes.setWordWrap(True)
        notes.setProperty('sub', True)
        lay.addWidget(notes)
        self.status = QLabel('点击“立即更新”后会自动下载并在关闭后完成替换')
        self.status.setProperty('sub', True)
        lay.addWidget(self.status)
        self.bar = None
        QProgressBar = QProgressBar
        import PySide6.QtWidgets
        self.bar = QProgressBar()
        self.bar.setTextVisible(True)
        self.bar.setValue(0)
        lay.addWidget(self.bar)
        lay.addStretch(1)
        box = QHBoxLayout()
        later = QPushButton('稍后')
        later.clicked.connect(self.reject)
        self.go = QPushButton('立即更新')
        self.go.setProperty('primary', True)
        self.go.clicked.connect(self._do)
        box.addStretch(1)
        box.addWidget(later)
        box.addWidget(self.go)
        lay.addLayout(box)

    
    def _do(self):
        from ..core import updater as up
        self.go.setEnabled(False)
        self.status.setText('正在下载更新包…')
        
        def work():
            return up.do_update(self.manifest, (lambda d, t: self.ctx.set_prog('update', d, t)))

        
        def done(ok):
            if ok:
                self.status.setText('更新完成，即将重启启动器…')
                self.accept()
                self.ctx.emit('restart_after_update', None)
            return None
            self.status.setText('更新失败，请稍后重试或手动下载')
            self.go.setEnabled(True)

        run_async(work, done, (lambda e: (self.status.setText('更新失败：%s' % e), self.go.setEnabled(True))))

    return __class__

