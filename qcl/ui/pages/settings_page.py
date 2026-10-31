# Source Generated with Decompyle++
# File: settings_page.pyc (Python 3.13)

'''设置'''
import os
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QFileDialog, QFrame, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget
from ..pages import Page
from .. import theme
from ..widgets import hbox, vbox, make_card
from ...core import cleanup, instances as instances_mod, java as java_mod, net, paths, settings, updater
from ...core.constants import APP_VERSION, DEFAULT_API_PORT, DEFAULT_RELAY_PORT, MIRRORS
from ...core.qtdownload import run_async
from ..actions import check_launcher_update, open_folder
MIRROR_NAMES = [m.name for m in MIRRORS]

class SettingsPage(Page):
    title = '设置'
    
    def __init__(self, ctx, parent):
        super.__init__(ctx, parent)
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        inner = QWidget()
        lay = QVBoxLayout(inner)
        lay.setContentsMargins(24, 18, 24, 18)
        lay.setSpacing(12)
        self.all = lay
        lay.addWidget(self._card_paths())
        lay.addWidget(self._card_host())
        lay.addWidget(self._card_launch())
        lay.addWidget(self._card_download())
        lay.addWidget(self._card_ai())
        lay.addWidget(self._card_login())
        lay.addWidget(self._card_about())
        lay.addStretch(1)
        scroll.setWidget(inner)
        outer.addWidget(scroll)

    
    def _card(self, title, sub):
        c = make_card()
        lay = vbox(14, 10)
        t = QLabel(title)
        t.setStyleSheet('font-weight: 700; font-size: 15px;')
        lay.addWidget(t)
        if sub:
            s = QLabel(sub)
            s.setProperty('sub', True)
            s.setWordWrap(True)
        lay.addWidget(s)
        c.setLayout(lay)
        return (c, lay)

    
    def _card_paths(self):
        (c, lay) = self._card('游戏目录（.minecraft）', '实例、存档与 Mod 都存放在这里，可随时迁移')
        row = hbox(8)
        self.game_root = QLineEdit()
        self.game_root.setText(self.ctx.settings.game_root)
        b = QPushButton('浏览…')
        b.setFixedWidth(80)
        b.clicked.connect(self._browse)
        b2 = QPushButton('打开')
        b2.setFixedWidth(64)
        b2.clicked.connect((lambda : open_folder(self.game_root.text())))
        b3 = QPushButton('应用')
        b3.setFixedWidth(64)
        b3.setProperty('primary', True)
        b3.clicked.connect(self._apply_root)
        row.addWidget(self.game_root, 1)
        row.addWidget(b)
        row.addWidget(b2)
        row.addWidget(b3)
        lay.addLayout(row)
        row2 = hbox(8)
        b4 = QPushButton('恢复默认（桌面/.minecraft）')
        b4.clicked.connect(self._default_root)
        row2.addWidget(b4)
        row2.addStretch(1)
        lay.addLayout(row2)
        return c

    
    def _browse(self):
        d = QFileDialog.getExistingDirectory(self, '选择 .minecraft 所在目录', self.game_root.text())
        if d:
            self.game_root.setText(os.path.join(d, '.minecraft'))
            self._apply_root()
        return None

    
    def _default_root(self):
        self.game_root.setText(paths.default_game_root())
        self._apply_root()

    
    def _apply_root(self):
        p = self.game_root.text().strip()
        if not p:
            pass
        return None
        self.ctx.settings.set_game_root(p)
        for d in ('versions', 'libraries', 'assets', 'instances'):
            os.makedirs(os.path.join(p, d), True)
        self.ctx.emit('instances_changed', None)
        self.ctx.toast('游戏目录已更新：%s' % p, 'ok')
        return None
        except Exception:
            continue

    
    def _card_host(self):
        (c, lay) = self._card('主机与自动更新', '把发布者电脑的 HTTP 地址填到这里，客户端就能自动收到新版本提示')
        row = hbox(8)
        self.host = QLineEdit()
        self.host.setText(self.ctx.settings.host_url)
        self.host.setPlaceholderText('如 http://1.2.3.4:25800')
        row.addWidget(QLabel('主机地址'), 1)
        row.addWidget(self.host, 3)
        lay.addLayout(row)
        row2 = hbox(8)
        self.api_port = QSpinBox()
        self.api_port.setRange(1, 65535)
        self.api_port.setValue(int(self.ctx.settings.get('api_port', DEFAULT_API_PORT)))
        self.relay_port = QSpinBox()
        self.relay_port.setRange(1, 65535)
        self.relay_port.setValue(int(self.ctx.settings.get('relay_port', DEFAULT_RELAY_PORT)))
        row2.addWidget(QLabel('服务端口'))
        row2.addWidget(self.api_port)
        row2.addWidget(QLabel('联机中继端口'))
        row2.addWidget(self.relay_port)
        row2.addStretch(1)
        lay.addLayout(row2)
        self.is_host = QCheckBox('这台电脑就是主机（启动服务端，供他人更新与联机）')
        self.is_host.setChecked(bool(self.ctx.settings.get('is_host')))
        self.is_host.stateChanged.connect(self._toggle_host)
        lay.addWidget(self.is_host)
        row3 = hbox(8)
        b1 = QPushButton('保存并应用')
        b1.setProperty('primary', True)
        b1.clicked.connect(self._save_host)
        b2 = QPushButton('检查更新')
        b2.clicked.connect((lambda : check_launcher_update(self.ctx, self)))
        b3 = QPushButton('发布新版本…')
        b3.clicked.connect(self._publish)
        self.server_state = QLabel('')
        self.server_state.setProperty('sub', True)
        row3.addWidget(b1)
        row3.addWidget(b2)
        row3.addWidget(b3)
        row3.addWidget(self.server_state)
        row3.addStretch(1)
        lay.addLayout(row3)
        return c

    
    def _save_host(self):
        self.ctx.settings.set('host_url', self.host.text().strip().rstrip('/'))
        self.ctx.settings.set('api_port', self.api_port.value())
        self.ctx.settings.set('relay_port', self.relay_port.value())
        self.ctx.on_host_changed()
        self.ctx.toast('已保存主机设置', 'ok')

    
    def _toggle_host(self, state):
        on = bool(state)
        self.ctx.settings.set('is_host', on)
        if on:
            self._save_host()
            self.ctx.start_server()
            self.server_state.setText('服务端运行中')
        return None
        self.ctx.stop_server()
        self.server_state.setText('服务端已停止')

    
    def _publish(self):
        from ..dialogs import PublishDialog
        dlg = PublishDialog(self.ctx, self, APP_VERSION)
        dlg.exec()

    
    def _card_ai(self):
        (c, lay) = self._card('AI 助手', '优先使用本机已运行的 Ollama（不出网、免费、不上传游戏数据）；检测不到时，改成使用下方填写的云端接口。开启联网搜索后，AI 回答前会先检索最新资料。')
        row = hbox(8)
        row.addWidget(QLabel('使用来源'))
        self.ai_provider = QComboBox()
        for label, val in (('自动（本机 Ollama 优先）', 'auto'), ('只用本机 Ollama', 'ollama'), ('只用云端接口', 'openai'), ('关闭 AI 功能', 'off')):
            self.ai_provider.addItem(label, val)
        cur = self.ctx.settings.get('ai_provider', 'auto')
        i = self.ai_provider.findData(cur)
        self.ai_provider.setCurrentIndex(max(0, i))
        row.addWidget(self.ai_provider, 1)
        b = QPushButton('重新检测')
        b.setFixedWidth(90)
        b.clicked.connect(self._probe_ai)
        row.addWidget(b)
        lay.addLayout(row)
        self.ai_state = QLabel('')
        self.ai_state.setProperty('sub', True)
        self.ai_state.setWordWrap(True)
        lay.addWidget(self.ai_state)
        row0 = hbox(8)
        row0.addWidget(QLabel('Ollama 地址'))
        self.ai_ollama_url = QLineEdit(self.ctx.settings.get('ai_ollama_url', ''))
        row0.addWidget(self.ai_ollama_url, 1)
        row0.addWidget(QLabel('模型'))
        self.ai_ollama_model = QComboBox()
        self.ai_ollama_model.setEditable(True)
        self.ai_ollama_model.setMinimumWidth(180)
        saved = self.ctx.settings.get('ai_ollama_model', '')
        self.ai_ollama_model.addItem('（自动挑选）', '')
        if saved:
            self.ai_ollama_model.addItem(saved, saved)
        self.ai_ollama_model.setCurrentIndex(1)
        row0.addWidget(self.ai_ollama_model, 1)
        lay.addLayout(row0)
        lay.addWidget(QLabel('云端接口（OpenAI 格式，DeepSeek / 通义 / 豆包 / OpenAI 通用）'))
        row1 = hbox(8)
        self.ai_base = QLineEdit(self.ctx.settings.get('ai_openai_base', ''))
        self.ai_base.setPlaceholderText('https://api.deepseek.com')
        row1.addWidget(QLabel('地址'))
        row1.addWidget(self.ai_base, 2)
        self.ai_model = QLineEdit(self.ctx.settings.get('ai_openai_model', ''))
        self.ai_model.setPlaceholderText('deepseek-chat')
        row1.addWidget(QLabel('模型名'))
        row1.addWidget(self.ai_model, 1)
        lay.addLayout(row1)
        row2 = hbox(8)
        self.ai_key = QLineEdit(self.ctx.settings.get('ai_openai_key', ''))
        self.ai_key.setEchoMode(QLineEdit.Password)
        self.ai_key.setPlaceholderText('sk-…（仅保存在本机配置里）')
        row2.addWidget(QLabel('API Key'))
        row2.addWidget(self.ai_key, 1)
        lay.addLayout(row2)
        self.ai_search = QCheckBox('回答前先联网检索（推荐，能拿到最新版本-Mod 信息）')
        self.ai_search.setChecked(bool(self.ctx.settings.get('ai_web_search', True)))
        lay.addWidget(self.ai_search)
        row3 = hbox(8)
        bsave = QPushButton('保存 AI 设置')
        bsave.setProperty('primary', True)
        bsave.setFixedWidth(130)
        bsave.clicked.connect(self._save_ai)
        btest = QPushButton('测试连接')
        btest.setFixedWidth(100)
        btest.clicked.connect(self._test_ai)
        row3.addWidget(bsave)
        row3.addWidget(btest)
        row3.addStretch(1)
        lay.addLayout(row3)
        QTimer.singleShot(300, self._probe_ai)
        return c

    
    def _probe_ai(self):
        self.ai_state.setText('正在检测本机 AI…')
        
        def work():
            from ...core import ai as ai_mod
            if not self.ai_ollama_url.text().strip():
                self.ai_ollama_url.text().strip()
            return ai_mod.probe_ollama(None)

        
        def done(info):
            if not info.get('models'):
                info.get('models')
            models = []
            cur = self.ai_ollama_model.currentText()
            self.ai_ollama_model.blockSignals(True)
            self.ai_ollama_model.clear()
            self.ai_ollama_model.addItem('（自动挑选）', '')
            for m in models:
                self.ai_ollama_model.addItem(m, m)
            idx = self.ai_ollama_model.findText(cur)
            if idx > 0:
                pass
            self.ai_ollama_model.setCurrentIndex(idx)
            self.ai_ollama_model.blockSignals(False)
            if models:
                self.ai_state.setText('检测到本机 Ollama 正在运行，可用模型 %d 个：%s' % (len(models), '、'.join(models[:4])))
            return None
            if not info.get('error'):
                info.get('error')
            self.ai_state.setText('本机没有检测到正在运行的 Ollama（%s）。想用本机模型请先安装并启动 Ollama；不想装的话填下面的云端接口即可。' % '无法连接')

        run_async(work, done)

    
    def _save_ai(self):
        s = self.ctx.settings
        s.set('ai_provider', self.ai_provider.currentData())
        s.set('ai_ollama_url', self.ai_ollama_url.text().strip())
        if not self.ai_ollama_model.currentData():
            self.ai_ollama_model.currentData()
        s.set('ai_ollama_model', '')
        s.set('ai_openai_base', self.ai_base.text().strip())
        s.set('ai_openai_model', self.ai_model.text().strip())
        s.set('ai_openai_key', self.ai_key.text().strip())
        s.set('ai_web_search', self.ai_search.isChecked())
        self.ctx.toast('AI 设置已保存', 'ok')
        self._probe_ai()

    
    def _test_ai(self):
        self._save_ai()
        self.ai_state.setText('正在与 AI 对话测试…')
        
        def work():
            from ...core import ai as ai_mod
            p = ai_mod.resolve_provider()
            if p.get('kind') not in ('ollama', 'openai'):
                if not p.get('error'):
                    p.get('error')
            return '不可用：' + ''
            
            try:
                r = ai_mod.chat([
                    {
                        'role': 'user',
                        'content': '只回复两个字：你好' }], p, 32, 90)
                if not r:
                    r
                return f'''OK||'''
            except Exception:
                e = None
                del e
                return None
                None = 
                del e


        def done(res):
            if res.startswith('OK|'):
                (_x, label, reply) = res.split('|', 2)
                self.ai_state.setText(f'''连接正常：，回复：''')
                self.ctx.toast('AI 连接正常', 'ok')
            return None
            if res.startswith('ERR|'):
                self.ai_state.setText('连接失败：' + res[4:])
                self.ctx.toast('AI 连接失败', 'err')
            return None
            self.ai_state.setText(res)

        run_async(work, done)

    
    def _card_launch(self):
        (c, lay) = self._card('启动设置')
        row = hbox(10)
        self.mem = QSpinBox()
        self.mem.setRange(1024, 65536)
        self.mem.setSingleStep(512)
        self.mem.setValue(int(self.ctx.settings.get('max_memory', 4096)))
        self.minmem = QSpinBox()
        self.minmem.setRange(256, 16384)
        self.minmem.setValue(int(self.ctx.settings.get('min_memory', 512)))
        self.w = QSpinBox()
        self.w.setRange(320, 7680)
        self.w.setValue(int(self.ctx.settings.get('width', 1280)))
        self.h = QSpinBox()
        self.h.setRange(240, 4320)
        self.h.setValue(int(self.ctx.settings.get('height', 720)))
        row.addWidget(QLabel('最大内存 MB'))
        row.addWidget(self.mem)
        row.addWidget(QLabel('初始内存 MB'))
        row.addWidget(self.minmem)
        row.addWidget(QLabel('宽'))
        row.addWidget(self.w)
        row.addWidget(QLabel('高'))
        row.addWidget(self.h)
        row.addStretch(1)
        lay.addLayout(row)
        self.full = QCheckBox('全屏启动')
        self.full.setChecked(bool(self.ctx.settings.get('fullscreen')))
        self.auto_java = QCheckBox('缺少 Java 时自动下载（Adoptium）')
        self.auto_java.setChecked(bool(self.ctx.settings.get('auto_download_java')))
        lay.addWidget(self.full)
        lay.addWidget(self.auto_java)
        row2 = hbox(8)
        self.java = QComboBox()
        self.java.setEditable(True)
        self.java.addItem('')
        self.java.setCurrentText(self.ctx.settings.get('java_path', ''))
        row2.addWidget(QLabel('Java 路径'))
        row2.addWidget(self.java, 1)
        bs = QPushButton('扫描本机')
        bs.setFixedWidth(90)
        bs.clicked.connect(self._scan_java)
        row2.addWidget(bs)
        lay.addLayout(row2)
        row3 = hbox(8)
        self.after = QComboBox()
        self.after.addItem('隐藏启动器窗口', 'hide')
        self.after.addItem('保持显示', 'keep')
        self.after.addItem('直接退出启动器', 'quit')
        cur = self.ctx.settings.get('launcher_after_launch', 'hide')
        i = self.after.findData(cur)
        self.after.setCurrentIndex(max(0, i))
        row3.addWidget(QLabel('启动游戏后'))
        row3.addWidget(self.after)
        row3.addStretch(1)
        lay.addLayout(row3)
        self.jargs = QLineEdit()
        self.jargs.setText(self.ctx.settings.get('java_args', ''))
        lay.addWidget(QLabel('额外 Java 参数'))
        lay.addWidget(self.jargs)
        b = QPushButton('保存启动设置')
        b.setProperty('primary', True)
        b.setFixedWidth(140)
        b.clicked.connect(self._save_launch)
        lay.addWidget(b)
        return c

    
    def _scan_java(self):
        run_async((lambda : java_mod.find_all()), self._on_java)

    
    def _on_java(self, items):
        cur = self.java.currentText()
        self.java.clear()
        self.java.addItem('')
        for p, v in items:
            self.java.addItem(p, p)
        self.java.setCurrentText(cur)

    
    def _save_launch(self):
        s = self.ctx.settings
        s.set('max_memory', self.mem.value())
        s.set('min_memory', self.minmem.value())
        s.set('width', self.w.value())
        s.set('height', self.h.value())
        s.set('fullscreen', self.full.isChecked())
        s.set('auto_download_java', self.auto_java.isChecked())
        if not self.java.currentData():
            self.java.currentData()
        s.set('java_path', self.java.currentText())
        s.set('launcher_after_launch', self.after.currentData())
        s.set('java_args', self.jargs.text())
        self.ctx.toast('已保存启动设置', 'ok')

    
    def _card_download(self):
        (c, lay) = self._card('下载与镜像')
        row = hbox(8)
        self.mirror = QComboBox()
        self.mirror.addItems(MIRROR_NAMES)
        cur = self.ctx.settings.get('mirror', MIRROR_NAMES[0])
        i = self.mirror.findText(cur)
        self.mirror.setCurrentIndex(max(0, i))
        self.threads = QSpinBox()
        self.threads.setRange(1, 32)
        self.threads.setValue(int(self.ctx.settings.get('download_threads', 8)))
        row.addWidget(QLabel('镜像源'))
        row.addWidget(self.mirror)
        row.addWidget(QLabel('并发下载数'))
        row.addWidget(self.threads)
        row.addStretch(1)
        lay.addLayout(row)
        row2 = hbox(8)
        self.cf = QLineEdit()
        self.cf.setPlaceholderText('CurseForge API Key（可选）')
        self.cf.setText(self.ctx.settings.get('cf_api_key', ''))
        row2.addWidget(self.cf, 1)
        lay.addLayout(row2)
        row3 = hbox(8)
        self.lport = QSpinBox()
        self.lport.setRange(1024, 65535)
        self.lport.setValue(int(self.ctx.settings.get('local_proxy_port', 25565)))
        row3.addWidget(QLabel('联机本地端口'))
        row3.addWidget(self.lport)
        row3.addStretch(1)
        lay.addLayout(row3)
        b = QPushButton('保存')
        b.setProperty('primary', True)
        b.setFixedWidth(100)
        b.clicked.connect(self._save_dl)
        lay.addWidget(b)
        return c

    
    def _save_dl(self):
        s = self.ctx.settings
        s.set('mirror', self.mirror.currentText())
        s.set('download_threads', self.threads.value())
        s.set('cf_api_key', self.cf.text().strip())
        s.set('local_proxy_port', self.lport.value())
        net.mirrors.set_mirror(self.mirror.currentText())
        self.ctx.dm.max_concurrent = self.threads.value()
        self.ctx.toast('已保存下载设置', 'ok')

    
    def _card_login(self):
        (c, lay) = self._card('登录服务')
        self.ms = QLineEdit()
        self.ms.setPlaceholderText('微软登录 Client ID（Azure 应用注册）')
        self.ms.setText(self.ctx.settings.get('ms_client_id', ''))
        self.ygg = QLineEdit()
        self.ygg.setPlaceholderText('外置登录地址，如 https://littleskin.cn/api/yggdrasil')
        self.ygg.setText(self.ctx.settings.get('ygg_url', ''))
        lay.addWidget(QLabel('微软 Client ID'))
        lay.addWidget(self.ms)
        lay.addWidget(QLabel('外置登录地址'))
        lay.addWidget(self.ygg)
        b = QPushButton('保存')
        b.setProperty('primary', True)
        b.setFixedWidth(100)
        b.clicked.connect((lambda : (self.ctx.settings.set('ms_client_id', self.ms.text().strip()), self.ctx.settings.set('ygg_url', self.ygg.text().strip()), self.ctx.toast('已保存', 'ok'))))
        lay.addWidget(b)
        return c

    
    def _card_about(self):
        (c, lay) = self._card('关于 QCL', '版本 %s' % APP_VERSION)
        info = QLabel('remove 命令：在 cmd 中输入 remove QCL 即可卸载，会保留 .minecraft 存档目录。\n实例目录：每个版本/加载器组合都是独立实例，Mod 与存档互不干扰。')
        info.setProperty('sub', True)
        info.setWordWrap(True)
        lay.addWidget(info)
        row = hbox(8)
        b1 = QPushButton('复制 remove 命令')
        b1.clicked.connect((lambda : (QApplication.clipboard().setText('remove QCL'), self.ctx.toast('已复制，粘贴到 cmd 中运行', 'ok'))))
        b2 = QPushButton('卸载启动器')
        b2.setProperty('danger', True)
        b2.clicked.connect(self._uninstall)
        b3 = QPushButton('打开程序目录')
        b3.clicked.connect((lambda : open_folder(paths.APP_DIR)))
        row.addWidget(b1)
        row.addWidget(b2)
        row.addWidget(b3)
        row.addStretch(1)
        lay.addLayout(row)
        return c

    
    def _uninstall(self):
        r = QMessageBox.question(self, '卸载 QCL', '将删除 QCL 启动器的全部文件。\n\n存档目录（%s）会被完整保留。\n\n确定继续吗？' % self.ctx.settings.game_root)
        if r != QMessageBox.Yes:
            pass
        return None
        cleanup.uninstall(self.ctx.settings.game_root, (lambda m: self.ctx.append_log('[卸载] ' + m)))
        self.ctx.emit('quit_app', None)

    
    def on_show(self):
        self.game_root.setText(self.ctx.settings.game_root)
        self.host.setText(self.ctx.settings.host_url)



return None

