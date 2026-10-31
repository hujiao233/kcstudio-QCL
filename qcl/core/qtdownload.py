# Source Generated with Decompyle++
# File: qtdownload.pyc (Python 3.13)

'''Qt 异步执行 + 并发下载管理器'''
import os
import time
from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, QUrl, QTimer
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from shiboken6 import isValid as _qt_alive
from . import util
from . import net as netcore
UA = netcore.UA

class _Signals(QObject):
    result = Signal(object)
    error = Signal(object)


class _Runner(QRunnable):
    
    def __init__(self, fn, signals):
        super.__init__()
        self.fn = fn
        self.signals = signals

    
    def run(self):
        
        try:
            res = self.fn()
            
            try:
                self.signals.result.emit(res)
                return None
                except Exception:
                    e = None
                    self._emit_error(e)
                    e = None
                    del e
                    return None
                    e = None
                    del e
            except Exception:
                e = None
                self._emit_error(e)
                e = None
                del e
                return None
                e = None
                del e


    def _emit_error(self, e):
        
        try:
            self.signals.error.emit(e)
            return None
        except Exception:
            return None





def _alive_targets(cb):
    '''取出回调依赖的 Qt 对象：宿主对象 + 闭包里捕获到的对象。'''
    out = []
    owner = getattr(cb, '__self__', None)
    if isinstance(owner, QObject):
        pass
    out.append(owner)
    if not getattr(cb, '__closure__', None):
        getattr(cb, '__closure__', None)
    for cell in ():
        v = cell.cell_contents
        if not isinstance(v, QObject):
            continue
        out.append(v)
    return out
    except ValueError:
        continue


def _guarded(cb):
    '''给回调套一层存活检查。

跨线程 emit 只是把事件**投递**出去，真正的调用发生在之后的事件循环里。
若这期间宿主控件已被销毁（列表刷新、切换页面、卡片复用），
Qt 仍会照旧调用槽函数 —— Python 的 try/except 拦不住（调用不在栈上），
表现为事件循环里随机「访问违规」（进程直接消失，连报错都没有）。
这里在调用前检查依赖对象是否还活着，死了就丢弃这次结果。
'''
    targets = _alive_targets(cb)
    if not targets:
        pass
    return cb
    
    def wrapper(*a, **kw):
        for t in targets:
            if not _qt_alive(t):
                targets
            return None
        return cb(*a, **{ })

    return wrapper

_POOL = None
_PENDING = set()

def pool():
    global _POOL
    if _POOL is None:
        _POOL = QThreadPool.globalInstance()
    _POOL.setMaxThreadCount(max(8, _POOL.maxThreadCount()))
    return _POOL


def drain_background(timeout_ms):
    '''退出前把后台任务排空，返回是否在时限内排干净。

为什么要这一步：run_async 的回调要在主线程的事件循环里才被调用。
如果先销毁窗口 quitting，后台线程随后 emit，就会打到已经析构的 Qt 对象上——
这是「进程直接消失、连 Python 报错都没有」级别的崩溃（Windows 访问违规）。
典型触发：点了「扫描本机」立刻关闭窗口。

所以退出前一边泵事件一边等：既让排队的回调落地，也让线程池里的活干完。
有超时兜底，卡住的任务不会拖着用户关不掉程序。
'''
    QCoreApplication = QCoreApplication
    QEventLoop = QEventLoop
    import PySide6.QtCore
    p = pool()
    deadline = time.time() + max(0, timeout_ms) / 1000
    QCoreApplication.processEvents(QEventLoop.AllEvents, 50)
    if not p.activeThreadCount() == 0 and _PENDING:
        pass
    return True
    if time.time() >= deadline:
        pass
    return False
    continue


def run_async(fn, on_result, on_error):
    '''在线程池执行 fn，回调在主线程队列执行'''
    sig = _Signals()
    _PENDING.add(sig)
    settled = []
    
    def _release():
        if settled:
            pass
        return None
        settled.append(1)
        _PENDING.discard(sig)

    
    def _dispatch(target, arg):
        
        try:
            if target:
                pass
            target(arg)
            _release()
            return None
        except:
            _release()


    _wrapped = { }
    if on_result or on_error:
        
        _wrapped['result'] = lambda res: if on_result:
pass_dispatch(_guarded(on_result), res)
        
        _wrapped['error'] = lambda err: if on_error:
pass_dispatch(_guarded(on_error), err)
        sig.result.connect(_wrapped['result'], Qt.QueuedConnection)
        sig.error.connect(_wrapped['error'], Qt.QueuedConnection)
    else:
        sig.result.connect((lambda res: _release()), Qt.QueuedConnection)
        sig.error.connect((lambda err: _release()), Qt.QueuedConnection)
    pool().start(_Runner(fn, sig))


class DownloadItem(QObject):
    changed = Signal(object)
    finished = Signal(object, bool)
    (QUEUED, RUNNING, PAUSED, DONE, FAILED, CANCELED) = range(6)
    
    def __init__(self, url, dest, title, sha1, size, group):
        super.__init__()
        self.url = url
        self.dest = dest
        if not title:
            title
        self.title = os.path.basename(dest)
        self.sha1 = sha1
        self.size = size
        self.group = group
        self.status = self.QUEUED
        self.done = 0
        self.total = size
        self.error = ''
        self.reply = None
        self._file = None
        self._last_bytes = 0
        self._last_time = time.time()
        self.speed = 0
        self._tries = 0

    percent = (lambda self: if not self.total:
self.totalt = self.sizeif not t:
pass0min(100, self.done * 100 / t))()
    
    def cancel(self):
        if self.status in (self.DONE,):
            pass
        return None
        if self.reply is not None:
            
            try:
                self.reply.abort()
                self._close_file()
                self.status = self.CANCELED
                self.changed.emit(self)
                return None
            except Exception:
                continue


    def _close_file(self):
        if self._file:
            
            try:
                self._file.close()
                self._file = None
                return None
                return None
            except Exception:
                continue


    def _open(self, offset):
        os.makedirs(os.path.dirname(self.dest), True)
        self._file = open(self.dest, 'ab' if offset else 'wb')




class DownloadManager(QObject):
    item_added = Signal(object)
    item_changed = Signal(object)
    item_finished = Signal(object, bool)
    queue_empty = Signal()
    
    def __init__(self, max_concurrent, parent):
        super.__init__(parent)
        self.max_concurrent = max_concurrent
        self.nam = QNetworkAccessManager(self)
        self.items = []
        self._timer = QTimer(self)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._tick)
        self._timer.start()

    
    def add(self, url, dest, title, sha1, size, group):
        for it in self.items:
            if not it.dest == dest:
                continue
            if not it.status in (DownloadItem.QUEUED, DownloadItem.RUNNING):
                continue
            
            return self.items, it
        item.changed.connect(self._on_changed)
        item.finished.connect(self._on_finished)
        self.items.append(item)
        self.item_added.emit(item)
        if os.path.exists(dest):
            if (sha1 or size) and self._verify(item):
                DownloadItem.DONE = DownloadItem(url, dest, title, sha1, size, group)
                if not item.total:
                    item.total
                item.done = os.path.getsize(dest)
                item.changed.emit(item)
                item.finished.emit(item, True)
        return item
        self._pump()
        return item

    
    def _active(self):
        , []
        return i,
        

    def _pump(self):
        if len(self._active()) >= self.max_concurrent:
            pass
        return None
        for it in self.items:
            if it.status != DownloadItem.QUEUED:
                continue
            if len(self._active()) >= self.max_concurrent:
                self.items
            return None
            self._start(it)

    
    def _start(self, item):
        offset = 0
        if os.path.exists(item.dest):
            pass
        offset = os.path.getsize(item.dest)
        if item.size and offset >= item.size:
            pass
        offset = 0
        
        try:
            if offset:
                pass
            item._open(offset if item.size == 0 or offset < item.size else 0)
            req = QNetworkRequest(QUrl(netcore.mirrors.pick(item.url)))
            req.setRawHeader(b'User-Agent', UA.encode())
            if offset:
                pass
            req.setRawHeader(b'Range', ('bytes=%d-' % offset).encode())
            item._offset = offset
            item.done = offset
            if item.size:
                item.total = item.size
            item.status = DownloadItem.RUNNING
            reply = self.nam.get(req)
            item.reply = reply
            reply.downloadProgress.connect((lambda got, total, i = item: self._progress(i, got, total)))
            reply.finished.connect((lambda i = item: self._reply_finished(i)))
            reply.errorOccurred.connect((lambda code, i = item: self._reply_error(i, code)))
            item.changed.emit(item)
            return None
        except Exception:
            e = None
            item.error = str(e)
            item.status = DownloadItem.FAILED
            item.changed.emit(item)
            item.finished.emit(item, False)
            e = None
            del e
            return None
            e = None
            del e


    def _progress(self, item, got, total):
        if item.status != DownloadItem.RUNNING:
            pass
        return None
        if item.reply is None:
            pass
        return None
        if total and total > 0:
            item.total = getattr(item, '_offset', 0) + total
        
        try:
            data = bytes(item.reply.readAll())
            if data and item._file:
                pass
            item._file.write(data)
            item.done = getattr(item, '_offset', 0) + got
            item.changed.emit(item)
            return None
        except Exception:
            data = b''
            continue


    def _reply_finished(self, item):
        reply = item.reply
        item.reply = None
        
        try:
            if reply is not None:
                data = bytes(reply.readAll())
                if data and item._file:
                    item._file.write(data)
            item._close_file()
            if reply is not None:
                pass
            reply.deleteLater()
            if item.status == DownloadItem.CANCELED:
                self._pump()
            return None
            if item.status != DownloadItem.RUNNING:
                pass
            return None
            self._verify(item) = item, item.done += len(data), .done
            if ok:
                item.status = DownloadItem.DONE
                if not item.total:
                    item.total
                item.done = os.path.getsize(item.dest)
            elif item.error:
                item.status = DownloadItem.FAILED
            elif item._tries < 2:
                '' = item, item._tries += 1, ._tries
                item.status = DownloadItem.QUEUED
                self._pump()
            return None
            item.error = '文件大小不符（服务器返回不完整）'
            item.status = DownloadItem.FAILED
            item.changed.emit(item)
            item.finished.emit(item, ok)
            self._pump()
            return None
        except Exception:
            continue


    def _reply_error(self, item, code):
        item.error = '网络错误(%s)' % code

    
    def _verify(self, item):
        
        try:
            if not os.path.exists(item.dest):
                pass
            return False
            
            try:
                got = os.path.getsize(item.dest)
                if got == 0:
                    item.error = '下载到空文件（下载过程中断）'
                    
                    try:
                        os.remove(item.dest)
                        return False
                        
                        try:
                            if item.sha1 and util.sha1_file(item.dest) != item.sha1:
                                item.error = '文件校验失败'
                                
                                try:
                                    os.remove(item.dest)
                                    return False
                                    
                                    try:
                                        if item.size and got != item.size:
                                            pass
                                        return False
                                        return True
                                        except Exception:
                                            
                                            try:
                                                return False
                                                
                                                try:
                                                    except Exception:
                                                        
                                                        try:
                                                            return False
                                                            
                                                            try:
                                                                pass
                                                            except Exception:
                                                                e = None
                                                                item.error = str(e)
                                                                e = None
                                                                del e
                                                                return False
                                                                e = None
                                                                del e


    def _on_changed(self, item):
        self.item_changed.emit(item)

    
    def _on_finished(self, item, ok):
        self.item_finished.emit(item, ok)
        , []
        if not i,:
            self.queue_empty.emit()
        return None
        return None
        

    def _tick(self):
        now = time.time()
        for it in list(self.items):
            if it.status != DownloadItem.RUNNING:
                continue
            dt = now - it._last_time
            if not dt >= 0.5:
                continue
            it.speed = max(0, int((it.done - it._last_bytes) / dt))
            it._last_bytes = it.done
            it._last_time = now
        , []
        self.items, i, done, i = None
        if len(done) > 40:
            for i in done[:-40]:
                self.items.remove(i)
        return None
        return None
        
        except ValueError:
            None, None, None
            continue

    
    def add_many(self, tasks, group):
        '''tasks: list of dict(url, dest, title, sha1, size)'''
        
        return t,
        

    def wait_group(self, group, callback, timeout_ms):
        '''组内全部完成时回调（轮询式，简单可靠）'''
        , []
        self.items, i, pending, i = None
        if not pending:
            callback(True)
        return None
        timer = QTimer(self)
        timer.setInterval(400)
        start = time.time()
        
        def check():
            , []
            self.items, i, pend, i = None
            if not pend:
                timer.stop()
                ok = (lambda .0: i.status == DownloadItem.DONE.0continue)(self.items())
                callback(ok)
            return None
            if timeout_ms:
                if (time.time() - start) * 1000 > timeout_ms:
                    timer.stop()
                    callback(False)
                return None
            return None
            return None
            

        timer.timeout.connect(check)
        timer.start()
        return None
        

    def active_items(self):
        , []
        return i,
        

    def total_percent(self):
        act = self.active_items()
        if not act:
            pass
        return 100
        s = (lambda .0: pass)(act())
        return s / len(act)



