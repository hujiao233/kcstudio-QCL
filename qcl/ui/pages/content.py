# Source Generated with Decompyle++
# File: content.pyc (Python 3.13)

'''内容市场：Mod / 光影 / 资源包 / 数据包 / 插件'''
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QVBoxLayout
from ..pages import Page
from .. import theme
from ..widgets import RemoteImage, hbox, vbox, make_card
from ...core import content as content_mod, curseforge, instances as instances_mod
from ...core.qtdownload import run_async
from ..actions import install_content
TYPES = [
    ('mod', 'Mod 模组'),
    ('shader', '光影'),
    ('resourcepack', '资源包'),
    ('datapack', '数据包'),
    ('plugin', '插件')]

class ContentPage(Page):
    title = '内容中心'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        self.page = 0
        self.total = 0
        self.results = []
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)
        head = hbox(8)
        t = QLabel('内容中心')
        t.setStyleSheet('font-size: 18px; font-weight: 700;')
        self.inst_combo = QComboBox()
        self.inst_combo.setMinimumWidth(220)
        self.inst_combo.currentIndexChanged.connect((lambda _: self._search(True)))
        self.platform = QComboBox()
        self.platform.addItem('Modrinth', 'modrinth')
        self.platform.addItem('CurseForge', 'curseforge')
        self.platform.currentIndexChanged.connect((lambda _: self._search(True)))
        self.search = QLineEdit()
        self.search.setPlaceholderText('搜索名称，回车确定')
        self.search.returnPressed.connect((lambda : self._search(True)))
        self.search.setFixedWidth(230)
        btn = QPushButton('搜索')
        btn.clicked.connect((lambda : self._search(True)))
        btn.setFixedWidth(64)
        head.addWidget(t)
        head.addSpacing(10)
        head.addWidget(self.inst_combo)
        head.addWidget(self.platform)
        head.addWidget(self.search)
        head.addWidget(btn)
        head.addStretch(1)
        lay.addLayout(head)
        seg = hbox(6)
        self.type_btns = []
        for k, label in enumerate(TYPES):
            b = QPushButton(label)
            b.setFixedHeight(32)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect((lambda _ = False, i = i: self._set_type(i)))
            self.type_btns.append(b)
            seg.addWidget(b)
        enumerate(TYPES)
        seg.addStretch(1)
        lay.addLayout(seg)
        card = make_card()
        cl = vbox(10, 8)
        self.list = QListWidget()
        self.list.setSpacing(4)
        self.list.itemClicked.connect(self._open)
        cl.addWidget(self.list, 1)
        cl.addLayout(self._pager())
        card.setLayout(cl)
        lay.addWidget(card, 1)
        self._fill_instances()
        self._set_type(0)

    
    def _set_type(self, idx):
        self.type_index = idx
        for i, b in enumerate(self.type_btns):
            b.style().unpolish(b)
            b.style().polish(b)
        self._search(True)

    
    def _pager(self):
        lay = hbox(8)
        self.prev = QPushButton('上一页')
        self.prev.setFixedWidth(80)
        self.prev.clicked.connect((lambda : self._search(-1)))
        self.next = QPushButton('下一页')
        self.next.setFixedWidth(80)
        self.next.clicked.connect((lambda : self._search(1)))
        self.page_label = QLabel('第 1 页')
        self.page_label.setProperty('sub', True)
        lay.addWidget(self.prev)
        lay.addWidget(self.page_label)
        lay.addWidget(self.next)
        lay.addStretch(1)
        self.status = QLabel('')
        self.status.setProperty('sub', True)
        lay.addWidget(self.status)
        return lay

    
    def _fill_instances(self):
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

    inst = (lambda self: iid = self.inst_combo.currentData()if iid:
passinstances_mod.get_instance(iid, self.ctx.game_root))()
    ctype = (lambda self: TYPES[self.type_index][0])()
    
    def _search(self, reset, delta):
        if reset:
            self.page = 0
        self.page = max(0, self.page + delta)
        inst = self.inst
        if not inst:
            self.status.setText('请先在「游戏版本」页面创建一个实例')
        return None
        plat = self.platform.currentData()
        if not plat == 'curseforge' and curseforge.available():
            self.status.setText('CurseForge 需要 API Key（设置中填写），已自动改用 Modrinth')
            plat = 'modrinth'
        else:
            self.status.setText('搜索中…')
        q = self.search.text().strip()
        args = (plat, self.ctype, q, inst.mc, '' if inst.loader == 'vanilla' else inst.loader, self.page, 20)
        run_async((lambda : content_mod.search(*args)), self._on_results, self._on_err)

    
    def _on_err(self, e):
        self.status.setText('搜索失败：%s' % e)

    
    def _on_results(self, data):
        (items, total) = data if isinstance(data, tuple) else (data, 0)
        self.results = items
        self.total = total
        self.list.clear()
        if not items:
            pass
        self.list.addItem('没有找到相关内容，试试换个关键词或平台')
        for it in items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, it)
            row = self._row(it)
            item.setSizeHint(row.sizeHint())
            self.list.addItem(item)
            self.list.setItemWidget(item, row)
        self.page_label.setText('第 %d 页 / 共 %d 个结果' % (self.page + 1, total))
        self.status.setText('来源：%s' % 'Modrinth' if self.platform.currentData() == 'modrinth' else 'CurseForge')

    
    def _row(self, item):
        w = QFrame()
        w.setObjectName('card2')
        lay = QHBoxLayout(w)
        lay.setContentsMargins(10, 8, 10, 8)
        lay.setSpacing(12)
        img = RemoteImage(46, 10)
        img.load(item.get('icon', ''))
        lay.addWidget(img)
        col = vbox(2)
        title = QLabel(item.get('title', ''))
        title.setStyleSheet('font-weight: 700; font-size: 14px;')
        if not item.get('description'):
            item.get('description')
        desc = QLabel(''[:110])
        desc.setProperty('sub', True)
        desc.setWordWrap(True)
        col.addWidget(title)
        col.addWidget(desc)
        lay.addLayout(col, 1)
        meta = vbox(2)
        d = QLabel('%s 次下载' % _fmt(item.get('downloads', 0)))
        d.setProperty('sub', True)
        if not item.get('author'):
            item.get('author')
        a = QLabel('')
        a.setProperty('sub', True)
        meta.addWidget(d)
        meta.addWidget(a)
        lay.addLayout(meta)
        btn = QPushButton('安装')
        btn.setFixedWidth(80)
        btn.setProperty('primary', True)
        btn.clicked.connect((lambda _ = False, i = item: self._quick_install(i)))
        lay.addWidget(btn)
        return w

    
    def _open(self, item):
        data = item.data(Qt.UserRole)
        if not data:
            pass
        return None
        from ..dialogs import ProjectDialog
        inst = self.inst
        if not inst:
            pass
        return None
        plat = self.platform.currentData()
        if not plat == 'curseforge' and curseforge.available():
            pass
        plat = 'modrinth'
        dlg = ProjectDialog(self.ctx, inst, self.ctype, data, plat, self)
        dlg.exec()

    
    def _quick_install(self, item):
        inst = self.inst
        if not inst:
            pass
        return None
        plat = self.platform.currentData()
        if not plat == 'curseforge' and curseforge.available():
            pass
        plat = 'modrinth'
        
        def work():
            return content_mod.versions(plat, self.ctype, item.get('id'), inst.mc, inst.loader)[:1]

        
        def done(vs):
            if not vs:
                self.ctx.toast('没有兼容当前版本的可用文件', 'warn')
            return None
            for v in vs:
                v['platform'] = plat
                v['project_id'] = item.get('id')
            install_content(self.ctx, inst, self.ctype, list(vs))

        run_async(work, done, (lambda e: self.ctx.toast('获取版本失败：%s' % e, 'err')))

    
    def on_show(self):
        self._fill_instances()
        if not self.list.count():
            self._search(True)
        return None




def _fmt(n):
    
    try:
        n = int(n)
        if n >= 100000000:
            pass
        return '%.1f 亿' % n / 100000000
        if n >= 10000:
            pass
        return '%.1f 万' % n / 10000
        return str(n)
    except Exception:
        return '0'

