# Source Generated with Decompyle++
# File: home.pyc (Python 3.13)

'''首页：账号、启动、控制台'''
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QPlainTextEdit, QPushButton, QVBoxLayout
from ..pages import Page
from .. import theme
from ..widgets import hbox, vbox, make_card
from ...core import auth, instances as instances_mod, util
from ...core.constants import APP_VERSION
from ...core.qtdownload import run_async
from ..actions import launch_instance, check_launcher_update, open_folder

class HomePage(Page):
    title = '首页'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(14)
        self.banner = QFrame()
        self.banner.setObjectName('card')
        self.banner.setStyleSheet('QFrame#card{border-color:%s;}' % theme.ACCENT)
        b = hbox(10, 10)
        self.banner_text = QLabel('发现新版本')
        self.banner_btn = QPushButton('立即更新')
        self.banner_btn.setProperty('primary', True)
        self.banner_btn.clicked.connect(self._update_now)
        b.addWidget(self.banner_text, 1)
        b.addWidget(self.banner_btn)
        self.banner.setLayout(b)
        self.banner.hide()
        lay.addWidget(self.banner)
        top = QHBoxLayout()
        top.setSpacing(14)
        top.addWidget(self._account_card(), 1)
        top.addWidget(self._launch_card(), 2)
        lay.addLayout(top, 0)
        c = make_card()
        cl = vbox(12, 8)
        self.console = QPlainTextEdit()
        head = hbox(8)
        t = QLabel('运行日志')
        t.setStyleSheet('font-weight: 700;')
        clear = QPushButton('清空')
        clear.setFixedWidth(64)
        clear.clicked.connect(self.console.clear)
        head.addWidget(t, 1)
        head.addWidget(clear)
        self.console.setReadOnly(True)
        self.console.setMaximumBlockCount(2000)
        self.console.setStyleSheet(f'''font-family: Consolas, monospace; font-size: 12px; background: ;border: 1px solid ; border-radius: 8px; padding: 6px;''')
        cl.addLayout(head)
        cl.addWidget(self.console, 1)
        c.setLayout(cl)
        lay.addWidget(c, 1)
        for line in list(ctx.logs)[-200:]:
            self.console.appendPlainText(line)
        self._refresh()
        self._refresh_account()

    
    def bind_events(self):
        self.listen('log', self._on_log)
        self.listen('instances_changed', self._refresh)
        self.listen('update_available', self._on_update)
        self.listen('game_started', self._on_game)
        self.listen('game_exited', self._on_game)

    
    def _account_card(self):
        c = make_card()
        c.setFixedHeight(168)
        lay = vbox(14, 10)
        title = QLabel('游戏账号')
        title.setStyleSheet('font-weight: 700; font-size: 15px;')
        self.acc_avatar = QLabel('?')
        self.acc_avatar.setFixedSize(56, 56)
        self.acc_avatar.setAlignment(Qt.AlignCenter)
        self.acc_avatar.setStyleSheet('background:%s; color:#ffffff; border-radius:28px; font-size:24px; font-weight:800;' % theme.ACCENT)
        self.acc_name = QLabel('未登录')
        self.acc_name.setStyleSheet('font-size: 16px; font-weight: 700;')
        self.acc_type = QLabel('登录后才能启动游戏')
        self.acc_type.setProperty('sub', True)
        row = hbox(12)
        col = vbox(2)
        col.addWidget(self.acc_name)
        col.addWidget(self.acc_type)
        row.addWidget(self.acc_avatar)
        row.addLayout(col, 1)
        self.login_btn = QPushButton('登录 / 切换账号')
        self.login_btn.setProperty('primary', True)
        self.login_btn.clicked.connect(self._login)
        lay.addWidget(title)
        lay.addLayout(row)
        lay.addStretch(1)
        lay.addWidget(self.login_btn)
        c.setLayout(lay)
        return c

    
    def _launch_card(self):
        c = make_card()
        c.setFixedHeight(168)
        lay = vbox(14, 10)
        row = hbox(10)
        self.inst_combo = QComboBox()
        self.inst_combo.setMinimumWidth(260)
        self.inst_combo.currentIndexChanged.connect(self._on_pick)
        self.launch_btn = QPushButton('启 动 游 戏')
        self.launch_btn.setProperty('primary', True)
        self.launch_btn.setFixedHeight(46)
        self.launch_btn.setStyleSheet('font-size: 16px; font-weight: 800;')
        self.launch_btn.clicked.connect(self._launch)
        row.addWidget(self.inst_combo, 1)
        row.addWidget(self.launch_btn)
        self.inst_info = QLabel('还没有实例，请先到「游戏版本」页面创建一个')
        self.inst_info.setProperty('sub', True)
        self.status = QLabel('')
        self.status.setProperty('sub', True)
        btns = hbox(8)
        self.folder_btn = QPushButton('打开实例目录')
        self.folder_btn.clicked.connect(self._open_dir)
        self.mods_btn = QPushButton('打开 Mod 目录')
        self.mods_btn.clicked.connect(self._open_mods)
        self.kill_btn = QPushButton('结束游戏')
        self.kill_btn.setProperty('danger', True)
        self.kill_btn.clicked.connect(self._kill)
        self.kill_btn.hide()
        btns.addWidget(self.folder_btn)
        btns.addWidget(self.mods_btn)
        btns.addWidget(self.kill_btn)
        btns.addStretch(1)
        lay.addLayout(row)
        lay.addWidget(self.inst_info)
        lay.addWidget(self.status)
        lay.addStretch(1)
        lay.addLayout(btns)
        c.setLayout(lay)
        return c

    
    def _refresh(self, *_):
        self.instances = instances_mod.list_instances(self.ctx.game_root)
        self.inst_combo.blockSignals(True)
        self.inst_combo.clear()
        for i in self.instances:
            self.inst_combo.addItem(f'''  ·  ''', i.id)
        cur = self.ctx.settings.get('last_instance', '')
        idx = self.inst_combo.findData(cur)
        if idx < 0 and self.instances:
            pass
        idx = 0
        self.inst_combo.setCurrentIndex(max(0, idx))
        self.inst_combo.blockSignals(False)
        self._on_pick()

    
    def _on_pick(self, *_):
        iid = self.inst_combo.currentData()
        inst = instances_mod.get_instance(iid, self.ctx.game_root) if iid else None
        self.inst = inst
        if inst:
            self.ctx.settings.set('last_instance', iid, False)
            n = len(inst.contents())
            self.inst_info.setText('%s ｜ 内存 %d MB ｜ 已装内容 %d 个' % (inst.label(), inst.data.get('max_mem', 4096), n))
        return None
        self.inst_info.setText('还没有实例，请先到「游戏版本」页面创建一个')

    
    def _refresh_account(self):
        acc = self.ctx.settings.get('account')
        if not acc:
            self.acc_name.setText('未登录')
            self.acc_type.setText('支持离线 / 微软 / 外置登录')
            self.acc_avatar.setText('?')
            self.acc_avatar.setStyleSheet(f'''background:; color:; border-radius:28px; font-size:24px; font-weight:800;''')
        return None
        name = acc.get('name', '?')
        self.acc_name.setText(name)
        self.acc_type.setText(auth.display(acc))
        if not name[:1]:
            name[:1]
        self.acc_avatar.setText('?'.upper())
        self.acc_avatar.setStyleSheet('background:%s; color:#ffffff; border-radius:28px; font-size:24px; font-weight:800;' % theme.ACCENT)

    
    def _login(self):
        from ..dialogs import AccountDialog
        dlg = AccountDialog(self.ctx, self)
        if dlg.exec():
            if dlg.account:
                self.ctx.settings.set('account', dlg.account)
                self._refresh_account()
                self.ctx.toast('已登录：%s' % dlg.account.get('name'), 'ok')
            return None
        return None

    
    def _launch(self):
        inst = getattr(self, 'inst', None)
        if not inst:
            self.ctx.toast('请先创建实例', 'err')
        return None
        self.launch_btn.setEnabled(False)
        self.launch_btn.setText('准备中…')
        launch_instance(self.ctx, inst, self._status, (lambda m: self.ctx.append_log(m)), self._exited)

    
    def _status(self, msg, busy):
        self.status.setText(msg)
        self.launch_btn.setText(msg if busy else '启 动 游 戏')
        if not busy:
            self.launch_btn.setEnabled(True)
        return None

    
    def _on_game(self, data):
        (inst, gp) = data
        self.kill_btn.show()
        self._proc = gp
        self.status.setText('游戏运行中：%s' % inst.name)
        self.launch_btn.setEnabled(False)
        self.launch_btn.setText('运行中')
        mode = self.ctx.settings.get('launcher_after_launch', 'hide')
        if mode == 'hide' and self.ctx.main_window:
            self.ctx.main_window.hide()
            self.ctx.emit('tray_show', None)
        return None
        if mode == 'quit':
            self.ctx.emit('quit_app', None)
        return None

    
    def _exited(self, code, ms):
        self.ctx.append_log('游戏已退出（代码 %s，运行 %d 秒）' % (code, ms // 1000))
        self.status.setText('上次游戏运行了 %d 分钟' % ms // 60000)
        self.launch_btn.setEnabled(True)
        self.launch_btn.setText('启 动 游 戏')
        self.kill_btn.hide()
        self._proc = None
        if self.ctx.main_window:
            if self.ctx.main_window.isHidden():
                self.ctx.main_window.show()
                self.ctx.main_window.raise_()
            return None
        return None

    
    def _kill(self):
        p = getattr(self, '_proc', None)
        if not p:
            pass
        return None
        self.ctx.toast('正在结束游戏（会先让游戏保存存档）…', 'info')
        
        def work():
            return p.kill()

        run_async(work, (lambda ok: if ok:
passself.ctx.toast('已结束游戏进程', 'warn')None('游戏未能正常退出，已强制结束', 'warn')))

    
    def _open_dir(self):
        if getattr(self, 'inst', None):
            open_folder(self.inst.dir)
        return None

    
    def _open_mods(self):
        if getattr(self, 'inst', None):
            open_folder(os.path.join(self.inst.dir, 'mods'))
        return None

    
    def _on_log(self, line):
        self.console.appendPlainText(line)

    
    def _on_update(self, m):
        if not m:
            pass
        return None
        if not m.get('notes'):
            m.get('notes')
        self.banner_text.setText(f'''发现新版本 ：''')
        self.banner.show()
        self._update_manifest = m

    
    def _update_now(self):
        from ..actions import UpdateDialog
        dlg = UpdateDialog(self.ctx, getattr(self, '_update_manifest', { }), self)
        dlg.exec()

    
    def on_show(self):
        self._refresh()
        self._refresh_account()

    return __class__

