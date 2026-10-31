# Source Generated with Decompyle++
# File: instances.pyc (Python 3.13)

'''实例管理：版本隔离、内容管理、内存与 Java 设置'''
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QComboBox, QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QListWidget, QListWidgetItem, QPushButton, QSpinBox, QVBoxLayout
from ..pages import Page
from .. import theme
from ..widgets import hbox, vbox, make_card
from ...core import content as content_mod, instances as instances_mod, java as java_mod
from ...core.constants import CONTENT_TYPE_LABELS, required_java
from ...core.qtdownload import run_async
from ..actions import open_folder, install_content
TYPES = [
    'mod',
    'shader',
    'resourcepack',
    'datapack',
    'plugin']

class InstancesPage(Page):
    title = '实例管理'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 20, 24, 16)
        lay.setSpacing(12)
        head = hbox(8)
        t = QLabel('实例管理')
        t.setStyleSheet('font-size: 18px; font-weight: 700;')
        tip = QLabel('每个实例都有独立的 Mod / 光影 / 资源包 / 存档目录，互不干扰')
        tip.setProperty('sub', True)
        head.addWidget(t)
        head.addSpacing(8)
        head.addWidget(tip)
        head.addStretch(1)
        btn_new = QPushButton('新建实例')
        btn_new.clicked.connect(self._new)
        head.addWidget(btn_new)
        lay.addLayout(head)
        body = QHBoxLayout()
        body.setSpacing(14)
        lc = make_card()
        lc.setFixedWidth(280)
        ll = vbox(10, 8)
        self.list = QListWidget()
        self.list.currentItemChanged.connect(self._select)
        ll.addWidget(self.list, 1)
        lc.setLayout(ll)
        body.addWidget(lc, 0)
        rc = make_card()
        rl = vbox(14, 10)
        self.name = QLabel('未选择实例')
        self.name.setStyleSheet('font-size: 17px; font-weight: 700;')
        self.info = QLabel('')
        self.info.setProperty('sub', True)
        self.info.setWordWrap(True)
        rl.addWidget(self.name)
        rl.addWidget(self.info)
        form = QHBoxLayout()
        form.setSpacing(10)
        col1 = vbox(6)
        col1.addWidget(QLabel('最大内存 (MB)'))
        self.mem = QSpinBox()
        self.mem.setRange(512, 65536)
        self.mem.setSingleStep(512)
        col1.addWidget(self.mem)
        col1.addWidget(QLabel('初始内存 (MB)'))
        self.minmem = QSpinBox()
        self.minmem.setRange(256, 16384)
        self.minmem.setSingleStep(256)
        col1.addWidget(self.minmem)
        col2 = vbox(6)
        col2.addWidget(QLabel('窗口宽度'))
        self.w = QSpinBox()
        self.w.setRange(320, 7680)
        col2.addWidget(self.w)
        col2.addWidget(QLabel('窗口高度'))
        self.h = QSpinBox()
        self.h.setRange(240, 4320)
        col2.addWidget(self.h)
        form.addLayout(col1)
        form.addLayout(col2)
        rl.addLayout(form)
        self.full = QCheckBox('全屏启动')
        rl.addWidget(self.full)
        jrow = hbox(8)
        self.java = QComboBox()
        self.java.setEditable(True)
        self.java.setMinimumWidth(220)
        jrow.addWidget(self.java, 1)
        jscan = QPushButton('扫描')
        jscan.setFixedWidth(70)
        jscan.clicked.connect(self._scan_java)
        jrow.addWidget(jscan)
        rl.addWidget(QLabel('Java（留空则自动选择）'))
        rl.addLayout(jrow)
        brow = hbox(8)
        save = QPushButton('保存设置')
        save.setProperty('primary', True)
        save.clicked.connect(self._save)
        folder = QPushButton('打开实例目录')
        folder.clicked.connect((lambda : if self.inst:
self.instopen_folder(self.inst.dir)))
        self.del_btn = QPushButton('删除实例')
        self.del_btn.setProperty('danger', True)
        self.del_btn.clicked.connect(self._delete)
        upd = QPushButton('检查内容更新')
        upd.clicked.connect(self._check_updates)
        brow.addWidget(save)
        brow.addWidget(folder)
        brow.addWidget(upd)
        brow.addWidget(self.del_btn)
        brow.addStretch(1)
        rl.addLayout(brow)
        self.tabs = QComboBox()
        for k in TYPES:
            self.tabs.addItem(CONTENT_TYPE_LABELS[k], k)
        self.tabs.currentIndexChanged.connect(self._fill_contents)
        rl.addWidget(QLabel('已安装内容'))
        rl.addWidget(self.tabs)
        self.files = QListWidget()
        self.files.setSpacing(3)
        rl.addWidget(self.files, 1)
        rc.setLayout(rl)
        body.addWidget(rc, 1)
        lay.addLayout(body, 1)
        self.inst = None
        self.refresh()
        self._scan_java()

    
    def bind_events(self):
        self.listen('instances_changed', self.refresh)
        self.listen('content_changed', (lambda i: self._fill_contents()))

    
    def refresh(self, *_):
        self.instances = instances_mod.list_instances(self.ctx.game_root)
        self.list.clear()
        for i in self.instances:
            it = QListWidgetItem(f'''\n''')
            it.setData(Qt.UserRole, i.id)
            self.list.addItem(it)
        if self.instances:
            if not self.list.currentItem():
                self.list.setCurrentRow(0)
            return None
        return None

    
    def _select(self, cur, prev):
        if not cur:
            pass
        return None
        iid = cur.data(Qt.UserRole)
        self.inst = instances_mod.get_instance(iid, self.ctx.game_root)
        if not self.inst:
            pass
        return None
        i = self.inst
        self.name.setText(i.name)
        self.info.setText(f'''版本： ｜ 目录：''')
        self.mem.setValue(i.data.get('max_mem', 4096))
        self.minmem.setValue(i.data.get('min_mem', 512))
        self.w.setValue(i.data.get('width', 1280))
        self.h.setValue(i.data.get('height', 720))
        self.full.setChecked(bool(i.data.get('fullscreen', False)))
        self.java.setCurrentText(i.data.get('java', ''))
        self._fill_contents()

    
    def _fill_contents(self, *_):
        self.files.clear()
        if not self.inst:
            pass
        return None
        ctype = self.tabs.currentData()
        d = os.path.join(self.inst.dir, content_mod.subdir(ctype))
        if not os.path.isdir(d):
            pass
        return None
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith(('.jar', '.zip', '.disabled')):
                continue
            it = QListWidgetItem()
            row = self._row(ctype, f, os.path.getsize(os.path.join(d, f)))
            it.setSizeHint(row.sizeHint())
            self.files.addItem(it)
            self.files.setItemWidget(it, row)
        if not self.files.count():
            it = QListWidgetItem('（还没有安装任何内容，去「内容中心」下载吧）')
            self.files.addItem(it)
        return None

    
    def _row(self, ctype, filename, size):
        w = QFrame()
        w.setObjectName('card2')
        lay = QHBoxLayout(w)
        lay.setContentsMargins(10, 6, 10, 6)
        lay.setSpacing(8)
        disabled = filename.endswith('.disabled')
        lab = QLabel('⏸ ' if disabled else '' + filename)
        if disabled:
            pass
        lab.setProperty('sub', True)
        from ...core import util
        sz = QLabel(util.human_size(size))
        sz.setProperty('sub', True)
        lay.addWidget(lab, 1)
        lay.addWidget(sz)
        bt = QPushButton('启用' if disabled else '禁用')
        bt.setFixedWidth(60)
        bt.clicked.connect((lambda : self._toggle(ctype, filename)))
        bd = QPushButton('删除')
        bd.setFixedWidth(60)
        bd.setProperty('danger', True)
        bd.clicked.connect((lambda : self._remove(ctype, filename)))
        lay.addWidget(bt)
        lay.addWidget(bd)
        return w

    
    def _scan_java(self):
        run_async((lambda : java_mod.find_all()), self._on_java)

    
    def _on_java(self, items):
        cur = self.java.currentText()
        self.java.clear()
        self.java.addItem('')
        for p, v in items:
            self.java.addItem('%s（Java %d）' % (p, v), p)
        if not cur:
            cur
        self.java.setCurrentText('')

    
    def _save(self):
        if not self.inst:
            pass
        return None
        i = self.inst
        i.data['max_mem'] = self.mem.value()
        i.data['min_mem'] = self.minmem.value()
        i.data['width'] = self.w.value()
        i.data['height'] = self.h.value()
        i.data['fullscreen'] = self.full.isChecked()
        if not self.java.currentData():
            self.java.currentData()
        i.data['java'] = self.java.currentText()
        i.save()
        self.ctx.toast('已保存实例设置', 'ok')

    
    def _toggle(self, ctype, filename):
        content_mod.toggle_content(self.inst, ctype, filename, filename.endswith('.disabled'))
        self._fill_contents()

    
    def _remove(self, ctype, filename):
        content_mod.remove_content(self.inst, ctype, filename)
        self._fill_contents()
        self.ctx.toast('已删除 %s' % filename, 'ok')

    
    def _new(self):
        from ..dialogs import NewInstanceDialog
        dlg = NewInstanceDialog(self.ctx, self)
        if dlg.exec():
            if dlg.result_:
                r = dlg.result_
                inst = instances_mod.create_instance(r['name'], r['mc'], r['loader'], r['loader_version'], self.ctx.game_root)
                self.ctx.settings.set('last_instance', inst.id)
                self.ctx.emit('instances_changed', None)
                self.ctx.toast('已创建实例 %s' % inst.name, 'ok')
            return None
        return None

    
    def _delete(self):
        if not self.inst:
            pass
        return None
        QMessageBox = QMessageBox
        import PySide6.QtWidgets
        r = QMessageBox.question(self, '删除实例', '确定删除「%s」吗？\n（存档会保留，其他内容将被移除）' % self.inst.name, QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            kept = []
            ok = instances_mod.delete_instance(self.inst, True, kept)
            self.ctx.emit('instances_changed', None)
            if not ok:
                self.ctx.toast('实例没能完全删除：文件可能正被游戏或其他程序占用，关掉后重试一次', 'err')
            return None
            if kept:
                self.ctx.toast('已删除实例，存档保留在 %s' % kept[0], 'ok')
            return None
            self.ctx.toast('已删除实例', 'ok')
        return None

    
    def _check_updates(self):
        if not self.inst:
            pass
        return None
        self.ctx.toast('正在检查更新…', 'info')
        run_async((lambda : content_mod.check_updates(self.inst)), self._on_updates, (lambda e: self.ctx.toast('检查失败：%s' % e, 'err')))

    
    def _on_updates(self, updates):
        if not updates:
            self.ctx.toast('全部内容都是最新版本', 'ok')
        return None
        dlg = QDialog(self)
        dlg.setWindowTitle('内容更新')
        dlg.resize(520, 380)
        lay = QVBoxLayout(dlg)
        lay.addWidget(QLabel('发现 %d 个内容有新版本：' % len(updates)))
        lst = QListWidget()
        for u in updates:
            rec = u['record']
            new = u['new']
            if not new.get('number'):
                new.get('number')
            it = QListWidgetItem(f'''： → ''')
            it.setData(Qt.UserRole, u)
            it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
            it.setCheckState(Qt.Checked)
            lst.addItem(it)
        lay.addWidget(lst, 1)
        box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        box.button(QDialogButtonBox.Ok).setText('更新选中')
        box.accepted.connect(dlg.accept)
        box.rejected.connect(dlg.reject)
        lay.addWidget(box)
        if dlg.exec():
            vers = []
            for i in range(lst.count()):
                it = lst.item(i)
                if not it.checkState() == Qt.Checked:
                    continue
                u = it.data(Qt.UserRole)
                v = dict(u['new'])
                v['platform'] = u['record'].get('platform')
                v['project_id'] = u['record'].get('project_id')
                vers.append(v)
            if vers:
                install_content(self.ctx, self.inst, 'mod', vers, False)
            return None
        return None

    
    def on_show(self):
        self.refresh()



