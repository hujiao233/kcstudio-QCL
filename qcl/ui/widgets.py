# Source Generated with Decompyle++
# File: widgets.pyc (Python 3.13)

'''通用 UI 组件'''
import os
from PySide6.QtCore import QBuffer, QByteArray, QFile, QIODevice, QObject, QRectF, QSize, Qt, QTimer, Signal
from PySide6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen, QPixmap, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, QPushButton, QSizePolicy, QVBoxLayout, QWidget, QScrollArea, QGraphicsOpacityEffect
from ..core import content as content_mod
from ..core import util
from ..core.qtdownload import DownloadItem, run_async
from . import theme
_ICON_CACHE = { }

def rounded_pixmap(pm, size, radius):
    out = QPixmap(size, size)
    out.fill(Qt.transparent)
    p = QPainter(out)
    p.setRenderHint(QPainter.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, size, size), radius, radius)
    p.setClipPath(path)
    scaled = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    x = (size - scaled.width()) // 2
    y = (size - scaled.height()) // 2
    p.drawPixmap(x, y, scaled)
    p.end()
    return out


class RemoteImage(QLabel):
    __doc__ = '异步加载网络图片'
    
    def __init__(self, size, radius, parent):
        super.__init__(parent)
        self.size_ = size
        self.radius = radius
        self._url = ''
        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignCenter)
        self._placeholder()

    
    def _placeholder(self):
        pm = QPixmap(self.size_, self.size_)
        pm.fill(Qt.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.Antialiasing)
        p.setBrush(QBrush(QColor(theme.CARD2)))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(QRectF(0, 0, self.size_, self.size_), self.radius, self.radius)
        p.setPen(QPen(QColor(theme.SUBTEXT)))
        f = QFont('Microsoft YaHei UI', max(7, self.size_ // 5))
        p.setFont(f)
        p.drawText(QRectF(0, 0, self.size_, self.size_), Qt.AlignCenter, 'MOD')
        p.end()
        self.setPixmap(pm)

    
    def load(self, url):
        if not url:
            url
        self._url = ''
        if not url:
            self._placeholder()
        return None
        if url in _ICON_CACHE:
            self._apply(_ICON_CACHE[url])
        return None
        run_async((lambda : content_mod.icon_local(url)), self._on_loaded)

    
    def _on_loaded(self, path):
        _ICON_CACHE[self._url] = path
        if path:
            self._apply(path)
        return None

    
    def _apply(self, path):
        pm = QPixmap(path)
        if not pm.isNull():
            self.setPixmap(rounded_pixmap(pm, self.size_, self.radius))
        return None

    return __class__


def vbox(*, margin, spacing, parent, *items):
    '''竖向布局。位置参数一律是要加入的子控件（或 int=间距、str=弹簧）。

parent 只接受**关键字参数**。原因：历史上很多调用写成 hbox(self.combo, refresh)，
位置参数是子控件，若把「第一个参数是 widget」自动当成宿主，这些调用会瞬间被破坏。
宿主的正确写法：`vbox(parent=w)` 或直接 `QVBoxLayout(w)`。
'''
    lay = QVBoxLayout(parent)
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    for i in items:
        if i is None:
            continue
        if isinstance(i, int):
            lay.addSpacing(i)
            continue
        if isinstance(i, QHBoxLayout) or isinstance(i, QVBoxLayout):
            lay.addLayout(i)
            continue
        lay.addWidget(i)
    return lay


def hbox(*, margin, spacing, parent, *items):
    lay = QHBoxLayout(parent)
    lay.setContentsMargins(margin, margin, margin, margin)
    lay.setSpacing(spacing)
    for i in items:
        if i is None:
            continue
        if isinstance(i, int):
            lay.addSpacing(i)
            continue
        if isinstance(i, (QHBoxLayout, QVBoxLayout)):
            lay.addLayout(i)
            continue
        if isinstance(i, str):
            lay.addStretch(1)
            continue
        lay.addWidget(i)
    return lay


def make_card(name):
    f = QFrame()
    f.setObjectName(name)
    return f


class Card(QFrame):
    clicked = Signal()
    
    def __init__(self, parent, name):
        super.__init__(parent)
        self.setObjectName(name)
        self.setCursor(Qt.PointingHandCursor)

    
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            pass
        self.clicked.emit()
        super.mouseReleaseEvent(e)

    return __class__


class SideBar(QWidget):
    changed = Signal(str)
    
    def __init__(self, items, parent):
        super.__init__(parent)
        self.setFixedWidth(196)
        self.setObjectName('panel')
        lay = QVBoxLayout(self)
        lay.setContentsMargins(12, 18, 12, 18)
        lay.setSpacing(6)
        self.buttons = { }
        title = QLabel('QCL')
        title.setStyleSheet('font-size: 22px; font-weight: 800; color: %s; letter-spacing:2px;' % theme.ACCENT)
        sub = QLabel('启动器')
        sub.setProperty('sub', True)
        sub.setStyleSheet('font-size: 11px;')
        lay.addWidget(title)
        lay.addWidget(sub)
        lay.addSpacing(14)
        for key, icon, text in items:
            b = QPushButton(f'''      ''')
            b.setObjectName('')
            b.setProperty('flat', True)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet('text-align: left; padding: 10px 12px; font-size: 13px;')
            b.clicked.connect((lambda _ = False, k = key: self._click(k)))
            self.buttons[key] = b
            lay.addWidget(b)
        lay.addStretch(1)
        self.active = ''

    
    def _click(self, key):
        self.set_active(key)
        self.changed.emit(key)

    
    def set_active(self, key):
        self.active = key
        for k, b in self.buttons.items():
            b.setProperty('flat', k != key)
            b.setStyleSheet('text-align: left; padding: 10px 12px; font-size: 13px;' + 'background: %s; color: #ffffff; border-radius: 8px;' % theme.ACCENT_DARK if k == key else '')
            b.update()

    return __class__


class DownloadRow(QFrame):
    removed = Signal(object)
    
    def __init__(self, item, parent):
        super.__init__(parent)
        self.item = item
        self.setObjectName('card2')
        lay = QVBoxLayout(self)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(4)
        top = QHBoxLayout()
        top.setSpacing(8)
        self.title = QLabel(item.title)
        self.title.setStyleSheet('font-weight: 600;')
        self.pct = QLabel('0%')
        self.pct.setProperty('sub', True)
        top.addWidget(self.title, 1)
        top.addWidget(self.pct)
        self.bar = QProgressBar()
        self.bar.setFixedHeight(8)
        self.bar.setTextVisible(False)
        self.info = QLabel('等待中')
        self.info.setProperty('sub', True)
        self.info.setStyleSheet('font-size: 11px;')
        lay.addLayout(top)
        lay.addWidget(self.bar)
        lay.addWidget(self.info)
        item.changed.connect(self.update_view)
        self.update_view(item)

    
    def update_view(self, item):
        if not item:
            item
        item = self.item
        p = int(item.percent)
        self.bar.setValue(p)
        self.pct.setText('%d%%' % p)
        if item.status == DownloadItem.RUNNING:
            if not item.total:
                item.total
            self.info.setText(f''' /    /s''')
        return None
        if item.status == DownloadItem.DONE:
            self.info.setText('已完成')
            self.pct.setText('完成')
        return None
        if item.status == DownloadItem.FAILED:
            if not item.error:
                item.error
            self.info.setText('失败：' + '未知错误')
        return None
        if item.status == DownloadItem.CANCELED:
            self.info.setText('已取消')
        return None
        self.info.setText('排队中')

    return __class__


class DownloadPanel(QWidget):
    __doc__ = '右下角下载面板'
    
    def __init__(self, dm, parent):
        super.__init__(parent)
        self.dm = dm
        self.rows = { }
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.inner = QWidget()
        self.inner_lay = QVBoxLayout(self.inner)
        self.inner_lay.setContentsMargins(4, 4, 4, 4)
        self.inner_lay.setSpacing(6)
        self.inner_lay.addStretch(1)
        self.scroll.setWidget(self.inner)
        lay.addWidget(self.scroll)
        self.setFixedHeight(190)
        dm.item_added.connect(self.add_row)
        dm.item_finished.connect(self.on_finished)

    
    def add_row(self, item):
        if item in self.rows:
            pass
        return None
        row = DownloadRow(item)
        self.rows[item] = row
        self.inner_lay.insertWidget(self.inner_lay.count() - 1, row)

    
    def on_finished(self, item, ok):
        row = self.rows.get(item)
        if not row:
            pass
        return None
        if ok:
            QTimer.singleShot(1500, (lambda : self._drop(item)))
        return None

    
    def _drop(self, item):
        row = self.rows.pop(item, None)
        if row:
            row.setParent(None)
            row.deleteLater()
        return None

    return __class__


class Toast(QLabel):
    
    def __init__(self, text, parent, kind):
        super.__init__(text, parent)
        color = {
            'ok': theme.ACCENT,
            'err': theme.DANGER,
            'warn': theme.WARN,
            'info': theme.INFO }.get(kind, theme.ACCENT)
        self.setStyleSheet('background: %s; color: #ffffff; padding: 8px 16px; border-radius: 8px; font-weight: 600;' % color)
        self.setAlignment(Qt.AlignCenter)
        self.adjustSize()
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._fade)

    
    def show_at(self, widget, y):
        self.setParent(widget)
        self.move((widget.width() - self.width()) // 2, y)
        self.show()
        self.raise_()
        self.timer.start(2600)

    
    def _fade(self):
        self.hide()
        self.deleteLater()

    return __class__

