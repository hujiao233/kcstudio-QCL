# Source Generated with Decompyle++
# File: versions.pyc (Python 3.13)

'''游戏版本：实时同步官网清单 + 加载器 + 创建实例'''
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout
from ..pages import Page
from .. import theme
from ..widgets import hbox, vbox, make_card
from ...core import instances as instances_mod, java as java_mod, launch, loaders, net, paths, settings, util, vanilla
from ...core.constants import required_java
from ...core.qtdownload import run_async
from ..actions import download_game
LOADER_ITEMS = [
    ('vanilla', '原版'),
    ('fabric', 'Fabric'),
    ('forge', 'Forge'),
    ('neoforge', 'NeoForge'),
    ('quilt', 'Quilt')]

class VersionsPage(Page):
    title = '游戏版本'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        self.all_versions = []
        self._lv_ok = None
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)
        head = hbox(8)
        t = QLabel('游戏版本')
        t.setStyleSheet('font-size: 18px; font-weight: 700;')
        self.latest_label = QLabel('')
        self.latest_label.setProperty('sub', True)
        self.filter = QComboBox()
        self.filter.addItems([
            '正式版',
            '快照 / 预览版',
            '全部版本'])
        self.filter.currentIndexChanged.connect(self._fill)
        self.search = QLineEdit()
        self.search.setPlaceholderText('搜索版本号')
        self.search.setFixedWidth(160)
        self.search.textChanged.connect(self._fill)
        self.refresh = QPushButton('刷新版本列表')
        self.refresh.clicked.connect(self._load)
        head.addWidget(t)
        head.addSpacing(6)
        head.addWidget(self.latest_label, 1)
        head.addWidget(self.filter)
        head.addWidget(self.search)
        head.addWidget(self.refresh)
        lay.addLayout(head)
        body = QHBoxLayout()
        body.setSpacing(14)
        lc = make_card()
        ll = vbox(10, 8)
        self.list = QListWidget()
        self.list.currentItemChanged.connect(self._on_select)
        self.list.itemDoubleClicked.connect((lambda _: self._create()))
        ll.addWidget(self.list, 1)
        lc.setLayout(ll)
        body.addWidget(lc, 2)
        rc = make_card()
        rc.setFixedWidth(340)
        rl = vbox(14, 10)
        self.sel = QLabel('未选择版本')
        self.sel.setStyleSheet('font-size: 16px; font-weight: 700;')
        self.sel_info = QLabel('')
        self.sel_info.setProperty('sub', True)
        self.sel_info.setWordWrap(True)
        rl.addWidget(self.sel)
        rl.addWidget(self.sel_info)
        self.name = QLineEdit()
        self.name.setPlaceholderText('实例名称（可留空）')
        rl.addWidget(QLabel('实例名称'))
        rl.addWidget(self.name)
        self.loader = QComboBox()
        for k, label in LOADER_ITEMS:
            self.loader.addItem(label, k)
        self.loader.currentIndexChanged.connect(self._load_loader_versions)
        rl.addWidget(QLabel('加载器'))
        rl.addWidget(self.loader)
        self.lver = QComboBox()
        self.lver.addItem('（自动选择最新）', '')
        rl.addWidget(QLabel('加载器版本'))
        rl.addWidget(self.lver)
        self.java_info = QLabel('')
        self.java_info.setProperty('sub', True)
        rl.addWidget(self.java_info)
        self.tip = QLabel('提示：每个实例拥有独立的 Mod / 光影 / 存档目录，互不干扰。')
        self.tip.setProperty('sub', True)
        self.tip.setWordWrap(True)
        rl.addWidget(self.tip)
        rl.addStretch(1)
        btn_create = QPushButton('创建实例并下载游戏文件')
        btn_create.setProperty('primary', True)
        btn_create.setFixedHeight(38)
        btn_create.clicked.connect(self._create)
        btn_only = QPushButton('仅创建实例（稍后下载）')
        btn_only.clicked.connect(self._create_only)
        rl.addWidget(btn_create)
        rl.addWidget(btn_only)
        rc.setLayout(rl)
        body.addWidget(rc, 0)
        lay.addLayout(body, 1)
        self._load()

    
    def _load(self):
        self.refresh.setEnabled(False)
        self.refresh.setText('获取中…')
        run_async((lambda : vanilla.manifest(True)), self._on_manifest, self._on_err)

    
    def _on_err(self, e):
        self.refresh.setEnabled(True)
        self.refresh.setText('刷新版本列表')
        self.ctx.toast('版本列表获取失败：%s' % e, 'err')

    
    def _on_manifest(self, data):
        self.refresh.setEnabled(True)
        self.refresh.setText('刷新版本列表')
        if not data:
            data
        self.all_versions = { }.get('versions', [])
        if not data:
            data
        lat = { }.get('latest', { })
        self.latest_label.setText('最新正式版 %s ｜ 最新快照 %s ｜ 共 %d 个版本' % (lat.get('release', '-'), lat.get('snapshot', '-'), len(self.all_versions)))
        self._fill()

    
    def _fill(self, *_):
        mode = self.filter.currentIndex()
        q = self.search.text().strip().lower()
        self.list.clear()
        for v in self.all_versions:
            if mode == 0 and v.get('type') != 'release':
                continue
            if mode == 1 and v.get('type') == 'release':
                continue
            if q and q not in v['id'].lower():
                continue
            it = QListWidgetItem(v['id'])
            if v.get('type') == 'release':
                pass
            elif v.get('type') == 'snapshot':
                pass
            
            tag = '预览版'
            it.setData(Qt.UserRole, v['id'])
            it.setText(f'''        ''')
            self.list.addItem(it)
        '正式版'
        if self.list.count():
            if not self.list.currentItem():
                self.list.setCurrentRow(0)
            return None
        return None

    
    def _on_select(self, cur, prev):
        if not cur:
            pass
        return None
        mc = cur.data(Qt.UserRole)
        self.mc = mc
        self.sel.setText(mc)
        self.sel_info.setText('')
        self.name.setText(f''' ''')
        need = required_java(mc)
        je = java_mod.find_java(need)
        self.java_info.setText('需要 Java %d：%s' % (need, '已检测到' if je else '未检测到，首次启动时会自动下载'))
        self._load_loader_versions()

    
    def _load_loader_versions(self, *_):
        mc = getattr(self, 'mc', '')
        kind = self.loader.currentData()
        self.lver.clear()
        self._lv_ok = None
        if mc or kind == 'vanilla':
            self.lver.addItem('（原版无需加载器）', '')
            self.lver.setEnabled(False)
            self.sel_info.setText('原版不含 Mod 支持，若需要 Mod 请选择 Fabric/Forge/NeoForge。')
        return None
        self.lver.setEnabled(True)
        self.lver.addItem('（自动选择最新）', '')
        self.lver.addItem('加载中…', '')
        run_async((lambda : self._fetch(kind, mc)), self._on_loader_versions)

    _fetch = (lambda kind, mc: if kind == 'fabric':
passloaders.fabric_versions(mc)if kind == 'quilt':
passloaders.quilt_versions(mc)if kind == 'forge':
passloaders.forge_versions(mc)loaders.neoforge_versions(mc))()
    
    def _on_loader_versions(self, data):
        if self.loader.currentData() == 'vanilla':
            pass
        return None
        self.lver.clear()
        self.lver.addItem('（自动选择最新）', '')
        self._lv_ok = bool(data)
        if not data:
            self.lver.addItem('未获取到，请检查网络/镜像', '')
            self.sel_info.setText('获取失败，可尝试在设置中切换镜像源为 BMCLAPI。')
        return None
        for d in data[:300]:
            v = { }.get('version') if isinstance(d, dict) else str(d)
            if not v:
                continue
            self.lver.addItem(v, v)
        kinds = {
            'fabric': 'Fabric',
            'forge': 'Forge',
            'neoforge': 'NeoForge',
            'quilt': 'Quilt' }
        self.sel_info.setText('已获取 %s 的 %d 个 %s 版本。' % (getattr(self, 'mc', ''), len(data), kinds.get(self.loader.currentData(), '')))

    
    def _create_only(self):
        inst = self._make()
        if inst:
            self.ctx.toast('已创建实例：%s' % inst.name, 'ok')
        return None

    
    def _create(self):
        inst = self._make()
        if inst:
            download_game(self.ctx, inst)
        return None

    
    def _make(self):
        mc = getattr(self, 'mc', '')
        if not mc:
            self.ctx.toast('请先选择一个游戏版本', 'warn')
        return None
        if not self.loader.currentData():
            self.loader.currentData()
        kind = 'vanilla'
        if not self.lver.currentData():
            self.lver.currentData()
        lv = ''
        if not kind != 'vanilla' and lv:
            state = getattr(self, '_lv_ok', None)
            if state is None:
                self.ctx.toast('加载器版本列表还在加载中，请稍候…', 'warn')
            return None
            if state is False:
                pass
        self.ctx.toast('加载器版本列表没拿到，将在首次启动时自动选择最新版；若仍失败，请在设置中把下载镜像切换为 BMCLAPI', 'warn')
        if not self.name.text().strip():
            self.name.text().strip()
        name = f''' '''
        inst = instances_mod.create_instance(name, mc, kind, lv, self.ctx.game_root)
        self.ctx.settings.set('last_instance', inst.id)
        self.ctx.emit('instances_changed', None)
        return inst

    
    def on_show(self):
        if not self.all_versions:
            self._load()
        return None

    return __class__

