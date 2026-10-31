# Source Generated with Decompyle++
# File: dialogs.pyc (Python 3.13)

'''各种对话框'''
import os
import webbrowser
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPlainTextEdit, QProgressBar, QPushButton, QTabWidget, QTextEdit, QVBoxLayout, QWidget
from ..core import account as account_mod, auth, content as content_mod, instances, loaders, settings, util, vanilla
from ..core.qtdownload import DownloadItem, run_async
from . import theme
from .widgets import RemoteImage, hbox, vbox
MC_ALL = []

def mc_versions(force):
    '''原版正式版列表（缓存）'''
    global MC_ALL, MC_ALL
    if not MC_ALL and force:
        pass
    return MC_ALL
    
    try:
        , []
        
        try:
            v, MC_ALL = None, vanilla.releases(force), v
            return MC_ALL
            
            try:
                
            except Exception:
                if not MC_ALL:
                    MC_ALL
                [] = None
                return MC_ALL


class NewInstanceDialog(QDialog):
    
    def __init__(self, ctx, parent, mc, loader):
        super.__init__(parent)
        self.ctx = ctx
        self.result_ = None
        self.setWindowTitle('新建游戏实例')
        self.resize(460, 320)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        self.name = QLineEdit()
        self.name.setPlaceholderText('实例名称，如：1.20.1 生存')
        self.combo = QComboBox()
        self.combo.setEditable(False)
        if not mc_versions():
            mc_versions()
        self.combo.addItems([
            '1.20.4'])
        if mc:
            i = self.combo.findText(mc)
            if i >= 0:
                pass
        self.combo.setCurrentIndex(i)
        refresh = QPushButton('刷新版本列表')
        refresh.setFixedWidth(110)
        refresh.clicked.connect(self._refresh)
        self.loader = QComboBox()
        for k, label in (('vanilla', '原版'), ('fabric', 'Fabric'), ('forge', 'Forge'), ('neoforge', 'NeoForge'), ('quilt', 'Quilt')):
            self.loader.addItem(label, k)
        idx = self.loader.findData(loader)
        if idx >= 0:
            pass
        self.loader.setCurrentIndex(idx)
        self.lver = QComboBox()
        self.lver.addItem('（加载器版本）', '')
        self.lver.setEnabled(False)
        lay.addWidget(QLabel('实例名称'))
        lay.addWidget(self.name)
        lay.addWidget(QLabel('游戏版本'))
        lay.addLayout(hbox(self.combo, refresh))
        lay.addWidget(QLabel('加载器'))
        lay.addWidget(self.loader)
        lay.addWidget(QLabel('加载器版本（留空自动选择最新）'))
        lay.addWidget(self.lver)
        lay.addStretch(1)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Ok).setText('创建')
        box.button(QDialogButtonBox.Cancel).setText('取消')
        box.accepted.connect(self._ok)
        box.rejected.connect(self.reject)
        lay.addWidget(box)
        self.loader.currentIndexChanged.connect(self._load_versions)
        self.combo.currentTextChanged.connect(self._load_versions)
        self._load_versions()

    
    def _refresh(self):
        run_async((lambda : mc_versions(True)), self._on_refresh)

    
    def _on_refresh(self, vs):
        if not vs:
            pass
        return None
        cur = self.combo.currentText()
        self.combo.clear()
        self.combo.addItems(vs)
        if cur in vs:
            self.combo.setCurrentText(cur)
        return None

    
    def _load_versions(self, *_):
        mc = self.combo.currentText()
        kind = self.loader.currentData()
        if not mc:
            pass
        return None
        if kind in ('vanilla', ''):
            self.lver.clear()
            self.lver.addItem('（原版无需加载器）', '')
            self.lver.setEnabled(False)
        return None
        self.lver.setEnabled(True)
        self.lver.clear()
        self.lver.addItem('加载中…', '')
        run_async((lambda : self._fetch(kind, mc)), self._on_versions)

    _fetch = (lambda kind, mc: if kind == 'fabric':
passloaders.fabric_versions(mc)if kind == 'quilt':
passloaders.quilt_versions(mc)if kind == 'forge':
passloaders.forge_versions(mc)loaders.neoforge_versions(mc))()
    
    def _on_versions(self, data):
        self.lver.clear()
        self.lver.addItem('（自动选择最新）', '')
        if not data:
            self.lver.addItem('未获取到版本，请检查网络', '')
        return None
        for d in data[:200]:
            if not v:
                continue
            self.lver.addItem(v, v)

    
    def _ok(self):
        if not self.name.text().strip():
            self.name.text().strip()
        name = f''' '''
        if not self.loader.currentData():
            self.loader.currentData()
        if not self.lver.currentData():
            self.lver.currentData()
        self.result_ = {
            'name': name,
            'mc': self.combo.currentText(),
            'loader': 'vanilla',
            'loader_version': '' }
        self.accept()




class AccountDialog(QDialog):
    
    def __init__(self, ctx, parent):
        super.__init__(parent)
        self.ctx = ctx
        self.account = None
        self.setWindowTitle('登录 Minecraft 账号')
        self.resize(460, 430)
        self.tabs = QTabWidget(self)
        self.tabs.addTab(self._offline_tab(), '离线登录')
        self.tabs.addTab(self._ms_tab(), '微软账号')
        self.tabs.addTab(self._ygg_tab(), '外置登录')
        lay = QVBoxLayout(self)
        lay.addWidget(self.tabs)
        cur = ctx.settings.get('account')
        if cur and cur.get('type') == 'offline':
            self.off_name.setText(cur.get('name', ''))
            self.tabs.setCurrentIndex(0)
        return None
        if cur:
            if cur.get('type') == 'yggdrasil':
                self.tabs.setCurrentIndex(2)
            return None
        return None

    
    def _offline_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(10)
        tip = QLabel('离线登录无需正版账号，可直接进入单机与局域网游戏。')
        tip.setProperty('sub', True)
        tip.setWordWrap(True)
        self.off_name = QLineEdit()
        self.off_name.setPlaceholderText('游戏内显示的名称')
        if not self.ctx.settings.get('last_offline_name', ''):
            self.ctx.settings.get('last_offline_name', '')
        self.off_name.setText('Player')
        box = QDialogButtonBox(QDialogButtonBox.Ok)
        box.button(QDialogButtonBox.Ok).setText('使用此名称登录')
        box.accepted.connect(self._do_offline)
        lay.addWidget(QLabel('玩家名称'))
        lay.addWidget(self.off_name)
        lay.addWidget(tip)
        lay.addStretch(1)
        lay.addWidget(box)
        return w

    
    def _do_offline(self):
        if not self.off_name.text():
            self.off_name.text()
        n = 'Player'.strip()
        if not n:
            pass
        return None
        self.ctx.settings.set('last_offline_name', n)
        self.account = auth.offline(n)
        self.accept()

    
    def _ms_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(8)
        self.ms_cid = QLineEdit()
        self.ms_cid.setPlaceholderText('Azure 应用 Client ID')
        self.ms_cid.setText(self.ctx.settings.get('ms_client_id', ''))
        self.ms_code = QLabel('')
        self.ms_code.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.ms_code.setStyleSheet('font-size: 26px; font-weight: 800; color: %s; letter-spacing: 4px;' % theme.ACCENT)
        self.ms_code.setAlignment(Qt.AlignCenter)
        self.ms_url = QLabel('')
        self.ms_url.setProperty('sub', True)
        self.ms_url.setWordWrap(True)
        self.ms_status = QLabel('')
        self.ms_status.setProperty('sub', True)
        self.ms_status.setWordWrap(True)
        open_btn = QPushButton('在浏览器中打开并粘贴代码')
        open_btn.clicked.connect(self._open_browser)
        start_btn = QPushButton('开始登录')
        start_btn.setProperty('primary', True)
        start_btn.clicked.connect(self._start_ms)
        save_cid = QPushButton('保存 Client ID')
        save_cid.clicked.connect((lambda : self.ctx.settings.set('ms_client_id', self.ms_cid.text().strip())))
        lay.addWidget(QLabel('Client ID（需在 Azure 注册应用，类型选“公共客户端”）'))
        lay.addLayout(hbox(self.ms_cid, save_cid))
        lay.addLayout(hbox(open_btn, start_btn))
        lay.addSpacing(6)
        lay.addWidget(self.ms_code)
        lay.addWidget(self.ms_url)
        lay.addWidget(self.ms_status)
        hint = QLabel('没有 Client ID？访问 portal.azure.com → 应用注册 → 新注册 → “任何组织目录中的账户和个人 Microsoft 账户” → 重定向 URI 填 http://localhost → 复制应用程序(客户端) ID 填到上面。')
        hint.setProperty('sub', True)
        hint.setWordWrap(True)
        lay.addWidget(hint)
        lay.addStretch(1)
        self._ms_timer = QTimer(self)
        self._ms_timer.setInterval(5000)
        self._ms_timer.timeout.connect(self._poll)
        self._device = None
        return w

    
    def _open_browser(self):
        if self._device:
            webbrowser.open(self._device['verification_uri'])
        return None

    
    def _start_ms(self):
        cid = self.ms_cid.text().strip()
        if not cid:
            self.ms_status.setText('请先填写 Client ID')
        return None
        self.ctx.settings.set('ms_client_id', cid)
        self.ms_status.setText('正在获取登录代码…')
        run_async((lambda : auth.ms_device_code(cid)), self._on_code, self._on_err)

    
    def _on_err(self, e):
        self.ms_status.setText('失败：%s' % e)

    
    def _on_code(self, d):
        self._device = d
        self.ms_code.setText(d.get('user_code', ''))
        self.ms_url.setText(d.get('verification_uri', ''))
        self.ms_status.setText('请在浏览器中粘贴该代码并确认登录，此窗口会自动完成登录。')
        webbrowser.open(d.get('verification_uri', ''))
        self._ms_timer.start()
        QTimer.singleShot(500, self._poll)

    
    def _poll(self):
        if not self._device:
            pass
        return None
        cid = self.ms_cid.text().strip()
        dc = self._device['device_code']
        run_async((lambda : auth.ms_poll(cid, dc)), self._on_poll)

    
    def _on_poll(self, res):
        if res.get('pending'):
            pass
        return None
        if res.get('error'):
            self.ms_status.setText('登录失败：%s' % res['error'])
            self._ms_timer.stop()
        return None
        
        try:
            acc = auth.ms_login(res['access_token'])
            acc['refresh_token'] = res.get('refresh_token', '')
            self.account = acc
            self._ms_timer.stop()
            self.accept()
            return None
        except Exception:
            e = None
            self.ms_status.setText('Minecraft 认证失败：%s' % e)
            self._ms_timer.stop()
            e = None
            del e
            return None
            e = None
            del e


    def _ygg_tab(self):
        w = QWidget()
        lay = QVBoxLayout(w)
        lay.setSpacing(8)
        self.ygg_url = QLineEdit()
        self.ygg_url.setPlaceholderText('如 https://littleskin.cn/api/yggdrasil')
        self.ygg_url.setText(self.ctx.settings.get('ygg_url', ''))
        self.ygg_user = QLineEdit()
        self.ygg_user.setPlaceholderText('邮箱或用户名')
        self.ygg_pwd = QLineEdit()
        self.ygg_pwd.setEchoMode(QLineEdit.Password)
        self.ygg_pwd.setPlaceholderText('密码')
        self.ygg_status = QLabel('')
        self.ygg_status.setProperty('sub', True)
        btn = QPushButton('登录')
        btn.setProperty('primary', True)
        btn.clicked.connect(self._do_ygg)
        lay.addWidget(QLabel('外置登录地址'))
        lay.addWidget(self.ygg_url)
        lay.addWidget(QLabel('账号'))
        lay.addWidget(self.ygg_user)
        lay.addWidget(QLabel('密码'))
        lay.addWidget(self.ygg_pwd)
        lay.addWidget(btn)
        lay.addWidget(self.ygg_status)
        lay.addStretch(1)
        return w

    
    def _do_ygg(self):
        url = self.ygg_url.text().strip()
        u = self.ygg_user.text().strip()
        p = self.ygg_pwd.text()
        if not url and u or p:
            self.ygg_status.setText('请填写完整')
        return None
        self.ctx.settings.set('ygg_url', url)
        self.ygg_status.setText('登录中…')
        run_async((lambda : auth.ygg_login(url, u, p)), self._on_ygg, self._on_ygg_err)

    
    def _on_ygg_err(self, e):
        self.ygg_status.setText('失败：%s' % e)

    
    def _on_ygg(self, acc):
        self.account = acc
        self.accept()




class ProjectDialog(QDialog):
    
    def __init__(self, ctx, inst, ctype, project, platform, parent):
        super.__init__(parent)
        self.ctx = ctx
        self.inst = inst
        self.ctype = ctype
        self.project = project
        self.platform = platform
        self.versions = []
        self.setWindowTitle(project.get('title', '详情'))
        self.resize(720, 520)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)
        head = QHBoxLayout()
        img = RemoteImage(64, 12)
        img.load(project.get('icon', ''))
        head.addWidget(img)
        info = QVBoxLayout()
        t = QLabel(project.get('title', ''))
        t.setStyleSheet('font-size: 17px; font-weight: 700;')
        if not project.get('description', ''):
            project.get('description', '')
        d = QLabel('')
        d.setProperty('sub', True)
        d.setWordWrap(True)
        d.setMaximumHeight(48)
        info.addWidget(t)
        info.addWidget(d)
        head.addLayout(info, 1)
        lay.addLayout(head)
        self.list = QListWidget()
        self.list.itemSelectionChanged.connect(self._sel)
        lay.addWidget(self.list, 1)
        self.dep = QLabel('')
        self.dep.setProperty('sub', True)
        lay.addWidget(self.dep)
        box = QHBoxLayout()
        self.inst_btn = QPushButton('安装')
        self.inst_btn.setProperty('primary', True)
        self.inst_btn.setEnabled(False)
        self.inst_btn.clicked.connect(self._install)
        cancel = QPushButton('关闭')
        cancel.clicked.connect(self.reject)
        box.addStretch(1)
        box.addWidget(cancel)
        box.addWidget(self.inst_btn)
        lay.addLayout(box)
        run_async((lambda : content_mod.versions(platform, ctype, project.get('id'), inst.mc, inst.loader)), self._on_versions)

    
    def _on_versions(self, vs):
        if not vs:
            vs
        self.versions = []
        if not self.versions:
            self.list.addItem('没有找到与当前版本兼容的内容')
        return None
        for v in self.versions:
            if not v.get('name'):
                v.get('name')
            if not ' / '.join(v.get('loaders', [])):
                ' / '.join(v.get('loaders', []))
            if not ' / '.join(v.get('game_versions', [])[:3]):
                ' / '.join(v.get('game_versions', [])[:3])
            it = QListWidgetItem(f'''   -   -   ''')
            it.setData(Qt.UserRole, v)
            self.list.addItem(it)
        if self.list.count():
            self.list.setCurrentRow(0)
        return None

    
    def _sel(self):
        items = self.list.selectedItems()
        if not items:
            self.inst_btn.setEnabled(False)
        return None
        v = items[0].data(Qt.UserRole)
        if v:
            v
        self.inst_btn.setEnabled(bool(v.get('url')))
        if v and ctype_has_deps(v):
            , []
            '包含 %d 个必需依赖，安装时将自动一并下载'(len % None, v.get('dependencies', []), d(d,))
        return None
        self.dep.setText('')
        return None
        

    def _install(self):
        items = self.list.selectedItems()
        if not items:
            pass
        return None
        v = dict(items[0].data(Qt.UserRole))
        v['platform'] = self.platform
        v['project_id'] = self.project.get('id')
        from .actions import install_content
        install_content(self.ctx, self.inst, self.ctype, [
            v])
        self.accept()




def ctype_has_deps(v):
    if not v.get('dependencies'):
        v.get('dependencies')
    return (lambda .0: pass)([]())


class PublishDialog(QDialog):
    
    def __init__(self, ctx, parent, current):
        super.__init__(parent)
        self.ctx = ctx
        self.setWindowTitle('发布新版本到主机')
        self.resize(420, 300)
        lay = QVBoxLayout(self)
        lay.setSpacing(8)
        self.ver = QLineEdit()
        self.ver.setPlaceholderText('例如 1.0.1')
        self.ver.setText(current)
        self.notes = QPlainTextEdit()
        self.notes.setPlaceholderText('更新说明（会展示给客户端）')
        self.req = QComboBox()
        self.req.addItem('可选更新', False)
        self.req.addItem('强制更新', True)
        self.status = QLabel('')
        self.status.setProperty('sub', True)
        lay.addWidget(QLabel('版本号（需大于当前版本）'))
        lay.addWidget(self.ver)
        lay.addWidget(QLabel('更新说明'))
        lay.addWidget(self.notes, 1)
        lay.addWidget(QLabel('更新方式'))
        lay.addWidget(self.req)
        lay.addWidget(self.status)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Ok).setText('打包并发布')
        box.button(QDialogButtonBox.Cancel).setText('取消')
        box.accepted.connect(self._ok)
        box.rejected.connect(self.reject)
        lay.addWidget(box)

    
    def _ok(self):
        ver = self.ver.text().strip()
        if not ver:
            self.status.setText('请填写版本号')
        return None
        from ..core import updater
        from ..core.constants import APP_VERSION
        if not updater.newer(ver, APP_VERSION):
            self.status.setText('版本号需大于当前版本 %s' % APP_VERSION)
        return None
        self.status.setText('正在打包，请稍候…')
        self.setEnabled(False)
        run_async((lambda : updater.publish(ver, self.notes.toPlainText().strip(), self.req.currentData())), self._done, self._err)

    
    def _err(self, e):
        self.setEnabled(True)
        self.status.setText('发布失败：%s' % e)

    
    def _done(self, m):
        self.setEnabled(True)
        self.ctx.toast('已发布版本 %s，客户端将自动收到更新提示' % m.get('version'), 'ok')
        self.accept()




class ServerDialog(QDialog):
    
    def __init__(self, parent, data):
        super.__init__(parent)
        self.setWindowTitle('服务器')
        self.resize(380, 220)
        lay = QVBoxLayout(self)
        self.name = QLineEdit()
        self.name.setPlaceholderText('名称')
        self.addr = QLineEdit()
        self.addr.setPlaceholderText('地址，如 mc.example.com 或 127.0.0.1:25565')
        if data:
            self.name.setText(data.get('name', ''))
        self.addr.setText(data.get('addr', ''))
        lay.addWidget(QLabel('名称'))
        lay.addWidget(self.name)
        lay.addWidget(QLabel('地址'))
        lay.addWidget(self.addr)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Ok).setText('保存')
        box.button(QDialogButtonBox.Cancel).setText('取消')
        box.accepted.connect(self.accept)
        box.rejected.connect(self.reject)
        lay.addWidget(box)

    
    def data(self):
        if not self.name.text().strip():
            self.name.text().strip()
        return {
            'name': '服务器',
            'addr': self.addr.text().strip() }




class TextDialog(QDialog):
    
    def __init__(self, title, text, parent):
        super.__init__(parent)
        self.setWindowTitle(title)
        self.resize(640, 420)
        lay = QVBoxLayout(self)
        e = QPlainTextEdit()
        e.setReadOnly(True)
        e.setPlainText(text)
        lay.addWidget(e, 1)
        b = QPushButton('关闭')
        b.clicked.connect(self.accept)
        lay.addWidget(b)



