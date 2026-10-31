# Source Generated with Decompyle++
# File: assistant.pyc (Python 3.13)

'''AI 助手：一句话生成实例 + Minecraft 问答'''
import html
import re as _re
from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QAbstractItemView, QCheckBox, QComboBox, QFrame, QLabel, QLineEdit, QMenu, QPushButton, QScrollArea, QSpinBox, QTextBrowser, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget
from ..pages import Page
from .. import theme
from ..widgets import make_card, hbox, vbox
from ...core import ai, instances as instances_mod, planner, settings as st
from ...core.constants import LOADER_LABELS
from ...core.qtdownload import run_async
from ..actions import download_game, install_content
EXAMPLES = [
    '低配电脑，想让 Minecraft 跑得流畅一点',
    '想玩大型科技自动化，机械动力那种',
    '魔法 + 冒险，有新 Boss 可以打',
    '原版向，加点小地图和背包整理就行',
    '专门用来建房子，需要投影和批量建造']
ASK_EXAMPLES = [
    '1.21 更新了什么内容？',
    'Fabric 和 Forge 有什么区别，我该选哪个？',
    '为什么我的整合包一直闪退？',
    '光影要怎么装？']

class _Sig(QObject):
    status = Signal(str)
    plan = Signal(object)
    ask_done = Signal(object)
    ask_delta = Signal(str)
    failed = Signal(str)


class AssistantPage(Page):
    title = 'AI 助手'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        self.plan_data = None
        self._pending_plan = None
        self._stop = False
        self.sig = _Sig()
        self.sig.status.connect(self._status)
        self.sig.plan.connect(self._show_plan)
        self.sig.ask_done.connect(self._ask_done)
        self.sig.ask_delta.connect(self._ask_delta)
        self.sig.failed.connect(self._failed)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        head = QFrame()
        hl = hbox(0, 8)
        self.btn_plan = QPushButton('✧ 一句话生成实例')
        self.btn_ask = QPushButton('◎ 问一句')
        for b in (self.btn_plan, self.btn_ask):
            b.setCheckable(True)
            b.setFixedHeight(32)
        self.btn_plan.setChecked(True)
        self.btn_plan.clicked.connect((lambda : self._mode('plan')))
        self.btn_ask.clicked.connect((lambda : self._mode('ask')))
        hl.addWidget(self.btn_plan)
        hl.addWidget(self.btn_ask)
        self.backend = QLabel('')
        self.backend.setProperty('sub', True)
        hl.addWidget(self.backend, 1)
        self.btn_cfg = QPushButton('AI 设置')
        self.btn_cfg.setFixedWidth(88)
        self.btn_cfg.clicked.connect(self._goto_settings)
        hl.addWidget(self.btn_cfg)
        head.setLayout(hl)
        outer.addWidget(head)
        self.stack_plan = self._build_plan_ui()
        self.stack_ask = self._build_ask_ui()
        outer.addWidget(self.stack_plan, 1)
        outer.addWidget(self.stack_ask, 1)
        self.stack_ask.hide()
        self._refresh_backend()

    
    def _mode(self, m):
        self.btn_plan.setChecked(m == 'plan')
        self.btn_ask.setChecked(m == 'ask')
        self.stack_plan.setVisible(m == 'plan')
        self.stack_ask.setVisible(m == 'ask')

    
    def _goto_settings(self):
        win = self.ctx.main_window
        if win:
            win.show_page('settings')
        return None

    
    def _refresh_backend(self):
        
        def work():
            return ai.describe()

        
        def done(label):
            self.backend.setText('后端：' + label)
            self.backend.setStyleSheet('color: %s;' % theme.ACCENT if '不支持' not in label and '未' not in label and '关闭' not in label else theme.DANGER)

        run_async(work, done)

    
    def on_show(self):
        self._refresh_backend()

    
    def _build_plan_ui(self):
        w = QWidget()
        lay = vbox(0, 10, w)
        c = make_card()
        cl = vbox(14, 8)
        t = QLabel('想玩什么？用一句话描述就够了')
        t.setStyleSheet('font-weight: 700; font-size: 15px;')
        cl.addWidget(t)
        s = QLabel('QCL 会把你想要的玩法翻译成一套真实的 Mod 清单并校验版本兼容性，确认后自动创建实例、下载加载器与 Mod。')
        s.setProperty('sub', True)
        s.setWordWrap(True)
        cl.addWidget(s)
        row = hbox(8)
        self.input = QLineEdit()
        self.input.setPlaceholderText('例如：低配电脑，想玩带传送带的科技模组')
        self.input.setFixedHeight(34)
        self.input.returnPressed.connect(self._generate)
        self.btn_gen = QPushButton('生成方案')
        self.btn_gen.setProperty('primary', True)
        self.btn_gen.setFixedWidth(100)
        self.btn_gen.setFixedHeight(34)
        self.btn_gen.clicked.connect(self._generate)
        row.addWidget(self.input, 1)
        row.addWidget(self.btn_gen)
        cl.addLayout(row)
        chips = hbox(6)
        chips.addWidget(QLabel('试试：'))
        for ex in EXAMPLES[:3]:
            b = QPushButton(ex if len(ex) <= 18 else ex[:18] + '…')
            b.setToolTip(ex)
            b.setProperty('chip', True)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect((lambda _ = False, e = ex: self.input.setText(e)))
            chips.addWidget(b)
        chips.addStretch(1)
        cl.addLayout(chips)
        c.setLayout(cl)
        lay.addWidget(c)
        self.result = QScrollArea()
        self.result.setWidgetResizable(True)
        self.result.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.result_inner = QWidget()
        self.result_lay = vbox(0, 10, self.result_inner)
        self.result_lay.addStretch(1)
        self.result.setWidget(self.result_inner)
        lay.addWidget(self.result, 1)
        self.status = QLabel('')
        self.status.setProperty('sub', True)
        lay.addWidget(self.status)
        return w

    
    def _generate(self):
        text = self.input.text().strip()
        if not text:
            self.ctx.toast('先描述一下你想玩什么', 'warn')
        return None
        prov = ai.resolve_provider()
        if prov.get('kind') not in ('ollama', 'openai'):
            pass
        self._status('未检测到 AI 后端，使用内置方案库生成（离线可用）')
        self.btn_gen.setEnabled(False)
        self.btn_gen.setText('生成中…')
        s = st.settings
        
        def work():
            return planner.build_plan(text, prov.get('kind') in ('ollama', 'openai'), bool(s.get('ai_web_search', True)), prov, (lambda m: self.sig.status.emit(m)))

        run_async(work, (lambda p: self.sig.plan.emit(p)), (lambda e: self.sig.failed.emit(str(e))))

    
    def _status(self, msg):
        self.status.setText(msg)

    
    def _failed(self, msg):
        self.btn_gen.setEnabled(True)
        self.btn_gen.setText('生成方案')
        self.status.setText('失败：' + msg)
        self.ctx.toast('方案生成失败：' + msg, 'err')

    
    def showEvent(self, e):
        super.showEvent(e)
        if getattr(self, '_pending_plan', None):
            plan = 
            self._show_plan(plan)
        return None

    
    def _show_plan(self, plan):
        self.btn_gen.setEnabled(True)
        self.btn_gen.setText('生成方案')
        self.status.setText('')
        if not self.is_current_page():
            self._pending_plan = plan
        return None
        self._clear(self.result_lay)
        self.plan_data = plan
        head = make_card()
        hl = vbox(14, 8)
        r1 = hbox(8)
        r1.addWidget(QLabel('实例名称'))
        if not plan.get('name'):
            plan.get('name')
        self.name_edit = QLineEdit('AI 整合包')
        self.name_edit.setFixedWidth(240)
        r1.addWidget(self.name_edit)
        r1.addStretch(1)
        src = plan.get('source')
        if not src:
            src
        tag = QLabel({
            'local': '内置方案库',
            'local+ai': 'AI 增强' }.get(src, ''))
        tag.setProperty('sub', True)
        r1.addWidget(tag)
        hl.addLayout(r1)
        r2 = hbox(10)
        r2.addWidget(QLabel('游戏版本'))
        self.mc_combo = QComboBox()
        if not plan.get('mc'):
            plan.get('mc')
        self.mc_combo.addItems([
            '1.21.1'] + _alt_mcs(plan.get('mc')))
        self.mc_combo.setFixedWidth(120)
        r2.addWidget(self.mc_combo)
        r2.addWidget(QLabel('加载器'))
        self.ld_combo = QComboBox()
        for k, label in LOADER_LABELS.items():
            if k == 'vanilla' and plan.get('loader') != 'vanilla':
                continue
            self.ld_combo.addItem(label, k)
        if not plan.get('loader'):
            plan.get('loader')
        idx = self.ld_combo.findData('fabric')
        self.ld_combo.setCurrentIndex(max(0, idx))
        self.ld_combo.setFixedWidth(110)
        r2.addWidget(self.ld_combo)
        r2.addWidget(QLabel('内存 MB'))
        self.mem_spin = QSpinBox()
        self.mem_spin.setRange(1024, max(2048, self.ctx.settings.total_memory_mb - 2048))
        self.mem_spin.setSingleStep(512)
        if not plan.get('memory_mb'):
            plan.get('memory_mb')
        self.mem_spin.setValue(int(4096))
        self.mem_spin.setFixedWidth(100)
        r2.addWidget(self.mem_spin)
        r2.addStretch(1)
        hl.addLayout(r2)
        if not plan.get('summary'):
            plan.get('summary')
        summary = QLabel('')
        summary.setWordWrap(True)
        summary.setProperty('sub', True)
        hl.addWidget(summary)
        head.setLayout(hl)
        self.result_lay.insertWidget(0, head)
        if not plan.get('mods'):
            plan.get('mods')
        mods = []
        if mods:
            pass
        self.result_lay.insertWidget(1, self._mod_card(mods))
        if not plan.get('dropped'):
            plan.get('dropped')
        dropped = []
        if dropped:
            pass
        self.result_lay.insertWidget(2, self._dropped_card(dropped))
        foot = make_card()
        fl = vbox(14, 8)
        self.cb_game = QCheckBox('同时下载游戏本体（推荐）')
        self.cb_game.setChecked(True)
        fl.addWidget(self.cb_game)
        actions = hbox(8)
        self.btn_create = QPushButton('一键创建实例并安装')
        self.btn_create.setProperty('primary', True)
        self.btn_create.setFixedHeight(36)
        self.btn_create.clicked.connect(self._create)
        self.btn_exist = QPushButton('装到已有实例…')
        self.btn_exist.setFixedHeight(36)
        self.btn_exist.clicked.connect(self._install_existing)
        actions.addWidget(self.btn_create)
        actions.addWidget(self.btn_exist)
        actions.addStretch(1)
        fl.addLayout(actions)
        foot.setLayout(fl)
        self.result_lay.insertWidget(3, foot)
        self.ctx.toast('已生成方案：可用 Mod %s' % plan.get('availability', ''), 'ok')

    
    def _mod_card(self, mods):
        c = make_card()
        cl = vbox(14, 8)
        top = hbox(8)
        t = QLabel('推荐 Mod（已校验版本兼容性）')
        t.setStyleSheet('font-weight: 700;')
        top.addWidget(t)
        top.addStretch(1)
        bulb = QPushButton('全选')
        bulb.clicked.connect((lambda : self._check_all(True)))
        bn = QPushButton('全不选')
        bn.clicked.connect((lambda : self._check_all(False)))
        top.addWidget(bulb)
        top.addWidget(bn)
        cl.addLayout(top)
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels([
            '',
            '名称',
            '说明',
            '下载量'])
        self.tree.setRootIsDecorated(False)
        self.tree.setAlternatingRowColors(True)
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tree.setColumnWidth(0, 26)
        self.tree.setColumnWidth(1, 220)
        self.tree.setColumnWidth(2, 300)
        for m in mods:
            if not m.get('title'):
                m.get('title')
            if not m.get('why'):
                m.get('why')
            it = QTreeWidgetItem([
                '',
                '',
                '',
                _dl(m.get('downloads'))])
            it.setFlags(it.flags() | Qt.ItemIsUserCheckable)
            it.setCheckState(0, Qt.Checked)
            it.setData(0, Qt.UserRole, m)
            if not m.get('description'):
                m.get('description')
            it.setToolTip(1, '')
            self.tree.addTopLevelItem(it)
        self.tree.resizeColumnToContents(3)
        self.tree.setMinimumHeight(min(320, 26 * len(mods) + 40))
        cl.addWidget(self.tree)
        c.setLayout(cl)
        return c

    
    def _dropped_card(self, dropped):
        c = make_card()
        cl = vbox(14, 6)
        t = QLabel('以下 %d 个在本方案版本下找不到适配版本（未勾选）' % len(dropped))
        t.setStyleSheet('font-weight: 600;')
        t.setWordWrap(True)
        cl.addWidget(t)
        for d in dropped[:12]:
            if not d.get('title'):
                d.get('title')
            if not d.get('reason'):
                d.get('reason')
            line = QLabel(f'''·  —— 不可用''')
            line.setProperty('sub', True)
            line.setStyleSheet('font-size: 11px;')
            line.setWordWrap(True)
            cl.addWidget(line)
        c.setLayout(cl)
        return c

    
    def _check_all(self, on):
        if not hasattr(self, 'tree'):
            pass
        return None
        for i in range(self.tree.topLevelItemCount()):
            it = self.tree.topLevelItem(i)
            it.setCheckState(0, Qt.Checked if on else Qt.Unchecked)

    
    def _selected_mods(self):
        if not hasattr(self, 'tree'):
            pass
        return []
        out = []
        for i in range(self.tree.topLevelItemCount()):
            it = self.tree.topLevelItem(i)
            if not it.checkState(0) == Qt.Checked:
                continue
            m = it.data(0, Qt.UserRole)
            v = m.get('version')
            if not v:
                continue
            out.append(dict(v))
        return out

    
    def _target_spec(self):
        mc = self.mc_combo.currentText() if hasattr(self, 'mc_combo') else '1.21.1'
        loader = self.ld_combo.currentData() if hasattr(self, 'ld_combo') else 'fabric'
        mem = self.mem_spin.value() if hasattr(self, 'mem_spin') else 4096
        name = self.name_edit.text().strip() if hasattr(self, 'name_edit') else 'AI 整合包'
        if not name:
            name
        return ('AI 整合包', mc, loader, mem)

    
    def _create(self):
        (name, mc, loader, mem) = self._target_spec()
        mods = self._selected_mods()
        
        try:
            inst = instances_mod.create_instance(name, mc, loader, '', self.ctx.game_root, mem)
            self.ctx.settings.set('last_instance', inst.id)
            self.ctx.emit('instances_changed', None)
            self.ctx.toast('已创建实例：%s，开始安装 Mod' % name, 'ok')
            if mods:
                pass
            install_content(self.ctx, inst, 'mod', mods)
            if self.cb_game.isChecked():
                download_game(self.ctx, inst)
            return None
            return None
        except Exception:
            e = None
            self.ctx.toast('创建实例失败：%s' % e, 'err')
            e = None
            del e
            return None
            e = None
            del e


    def _install_existing(self):
        mods = self._selected_mods()
        if not mods:
            self.ctx.toast('请先勾选要安装的 Mod', 'warn')
        return None
        lst = instances_mod.list_instances(self.ctx.game_root)
        if not lst:
            self.ctx.toast('还没有实例，先用上面的「一键创建实例」吧', 'warn')
        return None
        m = QMenu(self)
        for inst in lst:
            act = m.addAction(f'''（）''')
            act.triggered.connect((lambda _ = False, i = inst: install_content(self.ctx, i, 'mod', mods)))
        m.exec(self.btn_exist.mapToGlobal(self.btn_exist.rect().bottomLeft()))

    
    def _clear(self, lay):
        self.plan_data = None
        for attr in ('name_edit', 'mc_combo', 'ld_combo', 'mem_spin', 'cb_game', 'btn_create', 'btn_exist'):
            if not hasattr(self, attr):
                continue
            setattr(self, attr, None)
        if lay.count():
            item = lay.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
                w.deleteLater()
            elif item.layout() is not None:
                pass
            self._clear(item.layout())
            if lay.count():
                continue
        lay.addStretch(1)

    
    def _build_ask_ui(self):
        w = QWidget()
        lay = vbox(0, 10, w)
        self.chat = QTextBrowser()
        self.chat.setOpenExternalLinks(True)
        self.chat.setStyleSheet('font-size: 13px; line-height: 150%;')
        self.chat.setHtml(_welcome())
        lay.addWidget(self.chat, 1)
        chips = hbox(6)
        chips.addWidget(QLabel('试试：'))
        for ex in ASK_EXAMPLES[:3]:
            b = QPushButton(ex if len(ex) <= 16 else ex[:16] + '…')
            b.setToolTip(ex)
            b.setProperty('chip', True)
            b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect((lambda _ = False, e = ex: self.ask_input.setText(e)))
            chips.addWidget(b)
        chips.addStretch(1)
        lay.addLayout(chips)
        row = hbox(8)
        self.ask_input = QLineEdit()
        self.ask_input.setPlaceholderText('问点什么？例如：1.21 更新了什么')
        self.ask_input.setFixedHeight(34)
        self.ask_input.returnPressed.connect(self._ask)
        self.btn_send = QPushButton('发送')
        self.btn_send.setProperty('primary', True)
        self.btn_send.setFixedWidth(80)
        self.btn_send.setFixedHeight(34)
        self.btn_send.clicked.connect(self._ask)
        self.btn_stop = QPushButton('停止')
        self.btn_stop.setFixedWidth(70)
        self.btn_stop.setFixedHeight(34)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect((lambda : setattr(self, '_stop', True)))
        row.addWidget(self.ask_input, 1)
        row.addWidget(self.btn_send)
        row.addWidget(self.btn_stop)
        lay.addLayout(row)
        self.ask_status = QLabel('')
        self.ask_status.setProperty('sub', True)
        lay.addWidget(self.ask_status)
        return w

    
    def _ask(self):
        text = self.ask_input.text().strip()
        if not text:
            pass
        return None
        self.ask_input.clear()
        self._stop = False
        self.btn_send.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self._append('我', text)
        self._stream_target = []
        self._append_stream_open()
        prov = ai.resolve_provider()
        search_on = bool(st.settings.get('ai_web_search', True))
        
        def work():
            return planner.explain_mc_update(text, prov, search_on, (lambda m: self.sig.status.emit(m)), (lambda s: self.sig.ask_delta.emit(s)), (lambda : self._stop))

        run_async(work, (lambda r: self.sig.ask_done.emit(r)), (lambda e: self.sig.ask_done.emit({
'ok': False,
'error': str(e),
'answer': '',
'sources': [] })))

    
    def _append_stream_open(self):
        self.chat.append('<div style="color:%s;font-weight:700;margin-top:10px;">AI</div>' % theme.ACCENT)
        cur = self.chat.textCursor()
        cur.movePosition(QTextCursor.End)
        self._stream_pos = cur.position()
        self._streamed_len = 0

    
    def _ask_delta(self, s):
        self.chat.insertPlainText(s)

    
    def _replace_stream(self, html_text):
        '''用排版好的版本替换掉刚才那段纯文本流式内容。'''
        doc = self.chat.document()
        end = doc.characterCount() - 1
        start = getattr(self, '_stream_pos', None)
        if start is not None or end <= start:
            self.chat.insertHtml(html_text)
        return None
        cur = QTextCursor(doc)
        cur.setPosition(start)
        cur.setPosition(end, QTextCursor.KeepAnchor)
        cur.removeSelectedText()
        self.chat.setTextCursor(cur)
        self.chat.insertHtml(html_text)

    
    def _ask_done(self, res):
        self.btn_send.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.ask_status.setText('')
        if not res.get('ok'):
            if not res.get('error'):
                res.get('error')
            err = '未知错误'
            self.chat.insertHtml(f'''<div style="color:;">生成失败：</div>''')
            self.ctx.toast('AI 回答失败：' + err, 'err')
        return None
        if not res.get('answer'):
            res.get('answer')
        ans = ''.strip()
        if ans:
            self._replace_stream(_md_ish(ans))
        elif not getattr(self, '_streamed_len', 0):
            pass
        self.chat.insertHtml(_md_ish('（AI 没有给出回答）'))
        if not res.get('sources'):
            res.get('sources')
        srcs = []
        if srcs:
            links = (lambda .0: pass)(enumerate(srcs[:6])())
        self.chat.insertHtml(f'''<div style="margin-top:8px;color:;font-size:11px;">参考来源：</div>''')
        self.chat.verticalScrollBar().setValue(self.chat.verticalScrollBar().maximum())

    
    def _append(self, who, text):
        color = theme.ACCENT if who == 'AI' else theme.TEXT
        self.chat.append(f'''<div style="font-weight:700;margin-top:10px;color:;"></div><div></div>''')




def _alt_mcs(mc):
    base = [
        '1.21.1',
        '1.20.1',
        '1.21.4',
        '1.20.4',
        '1.19.2']
    , []
    return v,[:4]
    

def _dl(n):
    
    try:
        n = int(n)
        if n >= 100000000:
            pass
        return '%.1f 亿' % n / 1e+08
        if n >= 10000:
            pass
        return '%.1f 万' % n / 10000
        return str(n)
    except Exception:
        return '-'


def _md_ish(text):
    '''极简 Markdown 渲染：**粗体**、`代码`、换行'''
    if not text:
        text
    esc = html.escape('')
    esc = esc.replace('\n', '<br/>')
    esc = _re.sub('\\*\\*(.+?)\\*\\*', '<b>\\1</b>', esc)
    esc = _re.sub('`(.+?)`', '<code style="background:%s;padding:1px 4px;border-radius:3px;">\\1</code>' % theme.CARD2, esc)
    esc = _re.sub('^• ', '· ', esc)
    return '<div style="line-height:155%%;">%s</div>' % esc


def _welcome():
    return '<div style="font-size:15px;font-weight:700;margin-bottom:6px;">QCL AI 助手</div><div style="color:%s;line-height:160%%;">可以问版本更新内容、Mod 用法、报错排查，也可以切到上面「一句话生成实例」让我直接帮你配好一套能玩的整合包。<br/><br/>回答时会先联网检索，再结合本机模型整理成答案；网络不通或未配置 AI 时，实例生成仍可用内置方案库离线工作。</div>' % theme.SUBTEXT

