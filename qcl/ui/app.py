# Source Generated with Decompyle++
# File: app.pyc (Python 3.13)

'''应用上下文与启动'''
import os
import shutil
import sys
import threading
import time
import traceback
from collections import deque
from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtWidgets import QApplication
from . import theme
from .widgets import Toast
from .main_window import MainWindow
from ..core import account, cleanup, net, paths, relay, settings, server as server_mod, util, updater, util
from ..core.qtdownload import DownloadManager
_CTX_REF = {
    'ctx': None }
_NOISE_EVENTS = (QEvent.MouseMove, QEvent.HoverMove, QEvent.Paint, QEvent.Timer, QEvent.UpdateRequest, QEvent.Enter, QEvent.Leave)

def _short(exc):
    '''一句话描述异常。

有些异常（尤其是 PySide 里由 C++ 转换失败抛出的 OverflowError）**没有消息**，
直接拼出来就是「OverflowError: 」，用户完全看不懂。
这种情况补一句人话，并给出写日志的位置。
'''
    
    try:
        msg = str(exc).strip()
        name = type(exc).__name__
        if not msg:
            if name == 'OverflowError':
                pass
            return '%s：某处数值超出 Qt 能接受的范围（详见 logs\\error.log）' % name
        return None % name
        return f''': '''
    except Exception:
        msg = ''
        continue


def report_exception(exc, where):
    head = f''''''
    ctx = _CTX_REF.get('ctx')
    if ctx is not None:
        
        try:
            ctx.append_log('[异常] ' + head)
            ctx.toast('操作失败：' + _short(exc), 'err')
            
            try:
                os.makedirs(paths.LOG_DIR, True)
                with open(paths.ERROR_LOG, 'a', 'utf-8', 'replace') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S ') + head + '\n')
                    f.write(''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)) + '\n')
                    
                    try:

                        return None
                        continue
                        if not None:
                            pass
                        
                        try:
                            return None
                            
                            try:
                                pass
                            except Exception:
                                return None


def _excepthook(t, v, tb):
    if issubclass(t, KeyboardInterrupt):
        sys.__excepthook__(t, v, tb)
    return None
    report_exception(v, '未捕获')


class QCLApplication(QApplication):
    __doc__ = '捕获界面回调中的异常，杜绝「点了没反应」'
    
    def notify(self, receiver, event):
        
        try:
            return super.notify(receiver, event)
        except BaseException:
            e = None
            if event.type() not in _NOISE_EVENTS:
                pass
            report_exception(e, '界面')
            e = None
            del e
            return False
            e = None
            del e


    return __class__


class _UiBus(QObject):
    __doc__ = '把「从后台线程发起的界面动作」排队送回主线程。\n\n背景：启动流程（准备版本 / 下载 / 装加载器）跑在线程池里，\n过程中会调用 ctx.append_log / ctx.toast。如果这些方法直接改控件，\n就是在后台线程操作 Qt 控件 —— Qt 只允许 GUI 线程碰，\n违反后的症状是进程直接消失（访问违规），连 Python 报错都没有。\n典型触发：NeoForge 安装器失败后要提示用户，结果提示还没弹出来就崩了。\n'
    log = Signal(str)
    toast = Signal(str, str)


class Ctx:
    __doc__ = '全局上下文：事件总线 + 下载器 + 主机 API + 联机对象'
    
    def __init__(self):
        self.settings = settings.settings
        self.events = util.Emitter()
        self.logs = deque(800)
        self._prog = { }
        self.main_window = None
        self.server = None
        self.room_host = None
        self.guest = None
        self.lan = None
        self.dm = DownloadManager(int(self.settings.get('download_threads', 8)))
        self.api = account.Api(self.settings.host_url)
        self._ui_tid = threading.get_ident()
        self._bus = _UiBus()
        self._bus.log.connect(self._emit_log, Qt.QueuedConnection)
        self._bus.toast.connect(self._show_toast, Qt.QueuedConnection)

    
    def emit(self, name, data):
        self.events.emit(name, data)

    
    def on(self, name, fn):
        return self.events.on(name, fn)

    
    def off(self, name, fn):
        '''取消订阅。页面切走时反注册，避免旧页面的槽一直被事件总线调着。'''
        
        try:
            self.events.off(name, fn)
            return None
        except Exception:
            return None


    def _on_main(self):
        return threading.get_ident() == self._ui_tid

    game_root = (lambda self: self.settings.game_root)()
    
    def append_log(self, line):
        line = str(line)
        self.logs.append(line)
        if self._on_main():
            self._emit_log(line)
        return None
        self._bus.log.emit(line)

    
    def _emit_log(self, line):
        self.emit('log', line)

    
    def toast(self, msg, kind):
        self.append_log('[提示] %s' % msg)
        if self._on_main():
            self._show_toast(msg, kind)
        return None
        self._bus.toast.emit(msg, kind)

    
    def _show_toast(self, msg, kind):
        if self.main_window:
            
            try:
                Toast(msg, self.main_window, kind).show_at(self.main_window, 76)
                return None
                return None
            except Exception:
                return None


    def set_prog(self, key, done, total):
        self._prog[key] = (done, total)

    
    def get_prog(self, key):
        return self._prog.get(key)

    
    def on_host_changed(self):
        self.api.set_base(self.settings.host_url)

    
    def start_server(self):
        if self.server:
            pass
        return self.server
        
        try:
            self.server = server_mod.QCLServer(int(self.settings.get('api_port', 25800)), int(self.settings.get('relay_port', 25801)), paths.DATA_DIR, updater.update_dir(), (lambda m: self.append_log('[服务端] ' + m)))
            self.server.start()
            self.append_log('[服务端] 已启动：%s' % self.settings.host_url)
            return self.server
        except Exception:
            e = None
            self.append_log('[服务端] 启动失败：%s' % e)
            self.server = None
            e = None
            del e
            return self.server
            e = None
            del e


    def stop_server(self):
        if self.server:
            
            try:
                self.server.stop()
                self.server = None
                return None
                return None
            except Exception:
                continue


    def cleanup(self):
        
        try:
            if self.room_host:
                pass
            self.room_host.close()
            
            try:
                if self.lan:
                    pass
                self.lan.stop.set()
                self.stop_server()
                
                try:
                    self.settings.save()
                    return None
                    continue
                    continue
                except Exception:
                    return None


def ensure_remove_cmd():
    '''确保 remove.cmd 位于程序目录，且编码与控制台一致'''
    target = os.path.join(paths.APP_DIR, 'remove.cmd')
    src = None
    for cand in (os.path.join(paths.APP_DIR, 'tools', 'remove.cmd'), os.path.join(getattr(sys, '_MEIPASS', ''), 'tools', 'remove.cmd')):
        if not cand:
            continue
        if not os.path.isfile(cand):
            continue
        src = cand
        (os.path.join(paths.APP_DIR, 'tools', 'remove.cmd'), os.path.join(getattr(sys, '_MEIPASS', ''), 'tools', 'remove.cmd'))
    if not src:
        pass
    return target
    
    try:
        text = util.normalize_crlf(util.read_text_any(src))
        if not text.strip():
            pass
        return target
        
        try:
            enc = util.oem_encoding()
            data = text.encode(enc, 'replace')
            cur = None
            if os.path.isfile(target):
                with open(target, 'rb') as f:
                    cur = f.read()
                    
                    try:

                        if cur != data:
                            with open(target, 'wb') as f:
                                f.write(data)
                                
                                try:

                                    return target
                                    return target
                                    if not None:
                                        pass
                                    
                                    try:
                                        continue
                                        if not None:
                                            pass
                                        
                                        try:
                                            return target
                                            
                                            try:
                                                pass
                                            except Exception:
                                                if not os.path.isfile(target):
                                                    pass
                                                shutil.copyfile(src, target)
                                                return target
                                                return None


def run_gui():
    sys.excepthook = _excepthook
    app = QCLApplication(sys.argv)
    app.setApplicationName('QCL')
    app.setQuitOnLastWindowClosed(False)
    theme.apply(app)
    paths.ensure_dirs()
    ctx = Ctx()
    _CTX_REF['ctx'] = ctx
    net.mirrors.set_mirror(ctx.settings.get('mirror', '官方源'))
    ensure_remove_cmd()
    if ctx.settings.get('first_run', True):
        ensure_remove_cmd()
        cleanup.register_command()
        cleanup.create_shortcut()
        cleanup.write_uninstall_entry()
        ctx.settings.set('first_run', False)
    else:
        
        try:
            cleanup.ensure_integration()
            ctx.lan = relay.LANScanner((lambda info: ctx.emit('lan_found', info)), (lambda m: ctx.append_log('[局域网] ' + m)))
            ctx.lan.start()
            if ctx.settings.get('is_host', False):
                pass
            ctx.start_server()
            win = MainWindow(ctx)
            ctx.on('app_exit', (lambda d: ctx.cleanup()))
            win.show()
            ctx.append_log('QCL 启动器已启动，程序目录：%s' % paths.APP_DIR)
            ctx.append_log('游戏目录：%s' % ctx.game_root)
            
            def _shutdown():
                
                try:
                    from ..core.qtdownload import drain_background
                    drain_background(2000)
                    
                    try:
                        ctx.cleanup()
                        return None
                        continue
                    except Exception:
                        return None


            app.aboutToQuit.connect(_shutdown)
            code = app.exec()
            
            try:
                win.hide()
                app.processEvents()
                win.deleteLater()
                app.processEvents()
                ctx.cleanup()
                return code
                except Exception:
                    continue
                    continue

