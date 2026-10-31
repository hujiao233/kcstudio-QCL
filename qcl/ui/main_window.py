# Source Generated with Decompyle++
# File: main_window.pyc (Python 3.13)

'''主窗口'''
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QMainWindow, QPushButton, QStackedWidget, QSystemTrayIcon, QMenu, QVBoxLayout, QWidget
from . import theme
from .widgets import SideBar, DownloadPanel, hbox, vbox
from .pages.home import HomePage
from .pages.versions import VersionsPage
from .pages.content import ContentPage
from .pages.instances import InstancesPage
from .pages.multiplayer import MultiplayerPage
from .pages.community import CommunityPage
from .pages.assistant import AssistantPage
from .pages.settings_page import SettingsPage
from ..core.constants import APP_DISPLAY, APP_NAME, APP_VERSION
NAV = [
    ('home', '▤', '首页'),
    ('versions', '▣', '游戏版本'),
    ('content', '◈', '内容中心'),
    ('instances', '▦', '实例管理'),
    ('assistant', '✦', 'AI 助手'),
    ('multiplayer', '⇄', '联机'),
    ('community', '☰', '社区'),
    ('settings', '⚙', '设置')]

def make_app_icon():
    pm = QPixmap(64, 64)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing)
    p.setBrush(QColor(theme.ACCENT))
    p.setPen(Qt.NoPen)
    p.drawRoundedRect(0, 0, 64, 64, 14, 14)
    p.setPen(QColor('#ffffff'))
    f = QFont('Microsoft YaHei UI', 26, QFont.Bold)
    p.setFont(f)
    p.drawText(0, 0, 64, 64, Qt.AlignCenter, 'Q')
    p.end()
    return QIcon(pm)


class MainWindow(QMainWindow):
    
    def __init__(self, ctx):
        super.__init__()
        self.ctx = ctx
        ctx.main_window = self
        self.setWindowTitle(f'''  ''')
        self.setWindowIcon(make_app_icon())
        self.resize(1180, 760)
        self.setMinimumSize(1020, 640)
        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)
        self.sidebar = SideBar(NAV)
        self.sidebar.changed.connect(self.show_page)
        root.addWidget(self.sidebar)
        right = QWidget()
        rl = QVBoxLayout(right)
        rl.setContentsMargins(18, 14, 18, 12)
        rl.setSpacing(10)
        top = QHBoxLayout()
        top.setSpacing(10)
        self.title = QLabel('首页')
        self.title.setStyleSheet('font-size: 20px; font-weight: 800;')
        self.status_label = QLabel('')
        self.status_label.setProperty('sub', True)
        self.btn_dl = QPushButton('下载管理  (0)')
        self.btn_dl.setFixedWidth(140)
        self.btn_dl.clicked.connect(self.toggle_downloads)
        self.btn_update = QPushButton('有新版本')
        self.btn_update.setProperty('primary', True)
        self.btn_update.hide()
        self.btn_update.clicked.connect(self._update)
        top.addWidget(self.title)
        top.addSpacing(10)
        top.addWidget(self.status_label, 1)
        top.addWidget(self.btn_update)
        top.addWidget(self.btn_dl)
        rl.addLayout(top)
        self.stack = QStackedWidget()
        self.pages = {
            'home': HomePage(ctx, self),
            'versions': VersionsPage(ctx, self),
            'content': ContentPage(ctx, self),
            'instances': InstancesPage(ctx, self),
            'assistant': AssistantPage(ctx, self),
            'multiplayer': MultiplayerPage(ctx, self),
            'community': CommunityPage(ctx, self),
            'settings': SettingsPage(ctx, self) }
        for key, _i, _t in NAV:
            self.stack.addWidget(self.pages[key])
        rl.addWidget(self.stack, 1)
        self.dl_panel = DownloadPanel(ctx.dm)
        self.dl_panel.hide()
        rl.addWidget(self.dl_panel)
        root.addWidget(right, 1)
        self.tray = QSystemTrayIcon(make_app_icon(), self)
        self.tray.setToolTip(APP_DISPLAY)
        menu = QMenu()
        act_show = menu.addAction('显示主窗口')
        act_show.triggered.connect(self.show_normal)
        act_quit = menu.addAction('退出')
        act_quit.triggered.connect((lambda : self.ctx.emit('quit_app', None)))
        self.tray.setContextMenu(menu)
        self.tray.activated.connect((lambda r: if r == QSystemTrayIcon.Trigger:
passself.show_normal()))
        self.tray.show()
        ctx.on('update_available', self._on_update)
        ctx.on('tray_show', (lambda d: self.tray.showMessage(APP_DISPLAY, '游戏运行中，启动器已最小化到托盘', QSystemTrayIcon.Information, 3000)))
        ctx.on('quit_app', (lambda d: self._quit()))
        ctx.on('restart_after_update', (lambda d: self._quit()))
        self.show_page('home')
        self.sidebar.set_active('home')
        self.timer = QTimer(self)
        self.timer.setInterval(600)
        self.timer.timeout.connect(self._tick)
        self.timer.start()
        QTimer.singleShot(2500, self._startup_check)

    
    def show_page(self, key):
        page = self.pages.get(key)
        if not page:
            pass
        return None
        self.stack.setCurrentWidget(page)
        self.title.setText(page.title)
        if self.sidebar.active != key:
            pass
        self.sidebar.set_active(key)
        page.on_show()

    
    def toggle_downloads(self):
        self.dl_panel.setVisible(not self.dl_panel.isVisible())

    
    def _tick(self):
        act = self.ctx.dm.active_items()
        self.btn_dl.setText('下载管理  (%d)' % len(act))
        if act:
            self.status_label.setText('正在下载 %d 个文件（%.0f%%）' % (len(act), self.ctx.dm.total_percent()))
        else:
            self.status_label.setText('')
        prog = self.ctx.get_prog('java')
        if prog:
            pass
        self.status_label.setText(f'''正在下载 Java： / ''')
        prog = self.ctx.get_prog('update')
        if prog:
            self.status_label.setText(f'''正在下载更新包： / ''')
        return None

    
    def _startup_check(self):
        from .actions import check_launcher_update
        check_launcher_update(self.ctx, self, True)

    
    def _on_update(self, m):
        if not m:
            pass
        return None
        self.btn_update.setText('更新到 %s' % m.get('version'))
        self.btn_update.show()
        self._update_manifest = m

    
    def _update(self):
        from .actions import UpdateDialog
        dlg = UpdateDialog(self.ctx, getattr(self, '_update_manifest', { }), self)
        dlg.exec()

    
    def show_normal(self):
        self.show()
        self.raise_()
        self.activateWindow()

    
    def _quit(self):
        self.ctx.emit('app_exit', None)
        self.ctx.cleanup()
        QApplication = QApplication
        import PySide6.QtWidgets
        QApplication.quit()

    
    def closeEvent(self, e):
        if getattr(self, '_force', False):
            e.accept()
            self._quit()
        return None
        e.accept()
        self._quit()




def _h(n):
    from ..core import util
    return util.human_size(n)

